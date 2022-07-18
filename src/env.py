import os, subprocess
from src.bridge import CONFIG

def apply() -> None:
  envsubst = './.apt/usr/bin/envsubst'
  subprocess.Popen(
    [f'{envsubst} < bridge/config.toml > {CONFIG}'],
    shell = True,
  ).wait()

token = {
  'discord': os.environ.get('DISCORD_TOKEN'),
  'github': os.environ.get('GITHUB_TOKEN'),
  'telegram': os.environ.get('TELEGRAM_TOKEN'),
}

webhook = {
  'issues': os.environ.get('WEBHOOK_ISSUES'),
  'reddit': os.environ.get('WEBHOOK_REDDIT'),
  'releases': os.environ.get('WEBHOOK_RELEASES'),
  'tests': os.environ.get('WEBHOOK_TESTS'),
}
