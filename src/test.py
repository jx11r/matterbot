from src.webhooks import Issue, Reddit, Release
from src import env

issues = Issue(
  name = 'test',
  api = 'https://api.github.com/repos/qtile/qtile/issues?per_page=1',
  webhook = env.webhook['test'],
)

reddit = Reddit(
  name = 'test',
  api = 'https://www.reddit.com/r/qtile/new.json?limit=1',
  webhook = env.webhook['test'],
)

releases = Release(
  name = 'test',
  api = 'https://api.github.com/repos/qtile/qtile/releases/latest',
  webhook = env.webhook['test'],
)
