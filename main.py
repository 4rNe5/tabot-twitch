import json
from twitchio.ext import commands
from collections import defaultdict

# timeout count struct gen
timeouts = defaultdict(int)

# import Twitch Bot Setting  -> define Class
with open("./config.json", "r", encoding="utf-8") as E:
  config = json.loads(E.read())

token = config['token']
cid = config['cid']


class TwitchBot(commands.Bot):

  def __init__(self):
    super().__init__(
      token=token,  # Twitch OAuth Token - Secret
      client_id=cid,  # Twitch Client ID - Secret
      nick='악질봇',  # Bot's Twitch Nick
      prefix='!',  # Bot Command Start emoji
      initial_channels=['heart0331']  # Streamer's Name for Bot's Tracking
    )

  # MEssage Event Method -> when msg comes
  async def event_message(self, message):
    # If message author is None, skip handling.
    if message.author is None:
        return

    # Run Func when receive message
    await self.handle_commands(message)

  async def check_permissions(self, ctx):
    broadcaster = ctx.author.is_broadcaster or ctx.author.is_mod  # Check if either Streamer or Moderator.

    if broadcaster:
      return True
    else:
      await ctx.send("명령어 사용 권한이 없습니다.")
      return False

  # define timeout ranking command -> !timeoutrank
  @commands.command(name='timeoutrank')
  async def timeout_stats(self, ctx):
    if not await self.check_permissions(ctx):  # Checking Permission
      return

    timeout_ranking = sorted(timeouts.items(), key=lambda x: x[1], reverse=True)[:10]

    response = "타임아웃 랭킹 : "
    for idx, (user, count) in enumerate(timeout_ranking):
      response += f"\n{idx + 1}. {user}: {count}회"

    await ctx.send(response)

  # define timeout tracking event method
  async def event_clearchat(self, data):
    user = data.target_user
    timeouts[user] += 1
    channel = self.get_channel('heart0331')  # Replace with the name of the streamer's channel you want to track timeouts
    await channel.send(f"{user}게이야...넌 나가라")



# Bot Run
if __name__ == "__main__":
  bot = TwitchBot()
  bot.run()
