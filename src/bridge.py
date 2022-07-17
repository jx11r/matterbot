import os, subprocess

CONFIG = 'file/env.toml'

def status() -> bool | str:
  process = subprocess.Popen(
    ['pgrep', 'matterbridge'],
    stdout = subprocess.PIPE,
    text = True,
  )
  output = process.communicate()[0].strip()
  return output if output != '' else False

def version() -> str:
  process = subprocess.Popen(
    ["./matterbridge -version | awk '{print $2}'"],
    stdout = subprocess.PIPE,
    shell = True,
    text = True,
  )
  return f'Matterbridge v{process.communicate()[0].strip()}'

def start() -> str:
  if status():
    return 'Error: matterbridge is already running.'
  else:
    os.system(f'./matterbridge -conf {CONFIG} &')
    return 'Matterbridge has been started.'

def stop() -> str:
  if status():
    subprocess.run(['kill', status()])
    return 'Matterbridge stopped.'
  else:
    return 'Error: mattebridge is not running.'

def restart() -> str:
  if status():
    stop()
    start()
  else:
    start()
  return 'Matterbridge has been restarted.'
