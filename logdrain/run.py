from flask import Flask, request, jsonify
import os, requests, re

app = Flask(__name__)
webhook = os.environ.get('WEBHOOK_LOGS')

@app.route('/logs', methods = ['POST'])
async def logs():
  sanitize(request.data.decode('utf-8'))
  return jsonify({'status': 'ok'})

def sanitize(text: str) -> None:
  for i in text.split('\n'):
    send(re.sub('^.*\s\d{4}.+\w.*-\s', '', i.strip()))

def send(text: str) -> str:
  payload = {
    'username': 'Heroku',
    'embeds': [{
      'color': 0x79589f,
      'description': text,
    }]
  }

  with requests.post(webhook, json = payload) as response:
    return response.status_code

port = int(os.environ.get('PORT', 5000))
app.run(debug = False, host = '0.0.0.0', port = port)
