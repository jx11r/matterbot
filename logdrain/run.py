from flask import Flask, request, jsonify
import os, requests, re

app = Flask(__name__)
webhook = os.environ.get('WEBHOOK_LOGS')

@app.route('/logs', methods = ['POST'])
async def logs():
  sanitize(request.data.decode('utf-8'))
  return jsonify({'status': 'ok'})

def sanitize(text: str) -> None:
  regex, msg = '^.*\s\d{4}.*?\s-\s?', ''
  for i in text.split('\n'):
    msg += f"{re.sub(regex, '', i)}\n"
  send(msg.strip())

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
