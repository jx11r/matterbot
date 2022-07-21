from flask import Flask, request, jsonify
import os, requests, re

app = Flask(__name__)
webhook = os.environ.get('WEBHOOK_LOGS')

@app.route('/logs', methods = ['POST'])
async def logs():
  sanitize(request.data.decode('utf-8'))
  return jsonify({'status': 'ok'})

def sanitize(text: str) -> None:
  regex, error = '^.*\s\d{4}.*?\s-\s?', ''

  if re.search('Traceback', text, flags = re.M):
    for i in text.split('\n'):
      error += f"{re.sub(regex, '', i)}\n"
    send(error.strip())
  else:
    for i in text.split('\n'):
      send(re.sub(regex, '', i).strip())

def send(text: str) -> None:
  payload = {
    'username': 'Heroku',
    'embeds': [{
      'color': 0x79589f,
      'description': text,
    }]
  }

  requests.post(webhook, json = payload)

if __name__ == '__main__':
  app.run(debug = False)
