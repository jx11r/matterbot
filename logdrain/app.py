from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)
webhook = os.environ.get('WEBHOOK_LOGS')

@app.route('/logs', methods = ['POST'])
async def logs():
  log = request.data.decode('utf-8')
  return jsonify({'status': send(log)})

def send(content) -> str:
  payload = {
    'username': 'Heroku',
    'embeds': [{
      'color': 0x79589f,
      'description': content,
    }]
  }

  with requests.post(webhook, json = payload) as response:
    return str(response.status_code)

port = int(os.environ.get('PORT', 5000))
app.run(debug = False, host = '0.0.0.0', port = port)
