import requests, traceback

GITHUB = ''

class _Base:
  def __init__(self, name: str, api: str, webhook: str) -> None:
    self.name = name
    self._api = api
    self._webhook = webhook
    self._dir = f'file/{self.name}'

  def _get(self) -> dict:
    headers = {
      'User-Agent': 'jx11r',
      'Authorization': f'token {GITHUB}',
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
