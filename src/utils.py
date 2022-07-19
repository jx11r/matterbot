from datetime import datetime
from zoneinfo import ZoneInfo
import requests

from src import env

def logger(content) -> None:
  payload = {
    'username': 'Heroku',
    'embeds': [{
      'color': 0x79589f,
      'description': content,
      # 'footer': { 'text': time() },
    }]
  }

  requests.post(env.webhook['logs'], json = payload)

def time() -> str:
  now = datetime.now(tz = ZoneInfo('US/Central'))
  return now.strftime('%I:%M:%S %p')
