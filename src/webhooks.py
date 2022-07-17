import requests, traceback, time, random
from threading import Thread
from bs4 import BeautifulSoup
from packaging import version

from src import env

class _Base:
  def __init__(self, name: str, api: str, webhook: str) -> None:
    self.name = name
    self._api = api
    self._webhook = webhook
    self._dir = f'file/{self.name}'

  def _get(self) -> dict:
    headers = {
      'User-Agent': 'jx11r',
      'Authorization': f"token {env.token['github']}",
      'Accept': 'application/vnd.github.v3+json',
    }

    with requests.get(self._api, headers = headers) as response:
      return response.json()

  def _write(self, content: str) -> None:
    with open(self._dir, 'w') as file:
      file.write(content)
      file.close()

  @property
  def local(self) -> str:
    with open(self._dir, 'r') as file:
      content = file.read()
      file.close()

    return content

  def send(self) -> bool:
    payload = self.payload
    try:
      with requests.post(self._webhook, json = payload) as response:
        print(f'[{self.name}:status] {response.status_code}')
        print(f'[{self.name}:payload] {payload}')
      return True

    except Exception:
      print(f'[{self.name}:error] data not send.')
      print(f'[{self.name}:payload] {payload}')
      print(traceback.format_exc())
      return False

  @property
  def payload(self) -> dict:
    try:
      return self._payload()
    except Exception:
      print(f'[{self.name}:error] unable to get payload.')
      print(traceback.format_exc())
      return {}

  def _payload(self) -> dict:
    raise NotImplementedError

  @property
  def remote(self) -> str | int:
    raise NotImplementedError

  def validate(self) -> bool:
    raise NotImplementedError

  def run(self) -> None:
    try:
      if self.validate():
        print(f'[{self.name}:{self.remote}] new data received, sending...')
        if self.send():
          self._write(str(self.remote))

    except FileNotFoundError:
      self._write(str(self.remote))

    except Exception:
      print(f"[{self.name}:error] data couldn't be obtained.")
      print(traceback.format_exc())


class Issue(_Base):
  def __init__(self, name: str, api: str, webhook: str) -> None:
    super().__init__(name, api, webhook)

  @property
  def remote(self) -> str | int:
    return self._get()[0]['number']

  def validate(self) -> bool:
    if self.remote > int(self.local):
      return True

  def _payload(self) -> dict:
    data = self._get()[0]
    color = 0xeb6420
    title = f"Issue opened: #{data['number']}"

    if 'pull_request' in data:
      color = 0x7289da
      title = f"Pull request opened: #{data['number']}"

    return {
      'username': 'GitHub',
      'embeds': [{
        'color': color,
        'title': title,
        'url': data['html_url'],
        'author': {
          'name': data['user']['login'],
          'icon_url': data['user']['avatar_url'],
          'url': data['user']['html_url'],
        },
        'image': { 'url': self.image(data['html_url']) },
      }]
    }

  def image(self, url: str) -> str:
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    url = soup.find('meta', property = 'og:image')

    return url['content']


class Reddit(_Base):
  def __init__(self, name: str, api: str, webhook: str) -> None:
    super().__init__(name, api, webhook)

  @property
  def remote(self) -> str | int:
    return self._get()['data']['children'][0]['data']['id']

  def validate(self) -> bool:
    if self.remote != self.local:
      return True

  def _payload(self) -> dict:
    data = self._get()['data']['children'][0]['data']
    link, thumbnail = 'https://reddit.com', ''
    footer = 'Flair Name: Unspecified'

    if data['link_flair_text'] is not None:
      footer = f"Flair Name: {data['link_flair_text'].capitalize()}"

    if 'https' in data['thumbnail']:
      thumbnail = data['thumbnail']

    return {
      'username': data['subreddit_name_prefixed'],
      'embeds': [{
        'color': 0xff4400,
        'title': data['title'],
        'url': f"{link}{data['permalink']}",
        'author': {
          'name': data['author'],
          'icon_url': self.icon(),
          'url': f"{link}/user/{data['author']}",
        },
        'thumbnail': { 'url': thumbnail },
        'footer': { 'text': footer },
      }]
    }

  def icon(self) -> str:
    number = random.randint(0, 7)
    return f'https://www.redditstatic.com/avatars/defaults/v2/avatar_default_{number}.png'


class Release(_Base):
  def __init__(self, name: str, api: str, webhook: str) -> None:
    super().__init__(name, api, webhook)

  @property
  def remote(self) -> str | int:
    return self._get()['tag_name']

  def validate(self) -> bool:
    if version.parse(self.remote) > version.parse(self.local):
      return True

  def _payload(self) -> dict:
    data = self._get()

    return {
      'username': 'GitHub',
      'embeds': [{
        'color': 0x202225,
        'title': data['tag_name'],
        'url': data['html_url'],
        'author': {
          'name': data['author']['login'],
          'icon_url': data['author']['avatar_url'],
          'url': data['author']['html_url'],
        },
        'description': data['body'],
      }]
    }


issues = Issue(
  name = 'issues',
  api = 'https://api.github.com/repos/qtile/qtile/issues?per_page=1',
  webhook = env.webhook['github'],
)

reddit = Reddit(
  name = 'reddit',
  api = 'https://www.reddit.com/r/qtile/new.json?limit=1',
  webhook = env.webhook['reddit'],
)

releases = Release(
  name = 'releases',
  api = 'https://api.github.com/repos/qtile/qtile/releases/latest',
  webhook = env.webhook['announcements'],
)

def loop() -> None:
  while True:
    issues.run()
    reddit.run()
    releases.run()
    time.sleep(60)

def start() -> None:
  thread = Thread(target = loop)
  thread.daemon = True
  thread.start()
