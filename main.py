from src import (
  bot, bridge, env, webhooks
)

env.apply()
bridge.restart()
webhooks.init()
bot.init()
