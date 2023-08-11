import asyncio
import json
from twitchio.ext import commands
from collections import defaultdict

# timeout count struct gen
timeouts = defaultdict(int)

# import Twitch Bot Setting  -> define Class

with open("./config.json", "r", encoding="utf-8") as E:
  config = json.loads(E.read())

irc = config['irc']
cid = config['cid']

class TwitchBot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=irc, # Twitch OAuth Token - Secret
            client_id=cid, # Twitch Client ID - Secret
            nick='악질봇', # Bot's Twitch Nick
            prefix='!', #Bot Command Start emoji
            initial_channels=['마야100'] # Streamer's Name for Bot's Tracking
        )

    # MEssage Event Method
    async def event_message(self, message):
        # Run Func when receive message
        await self.handle_commands(message)

    # define timeout ranking command -> !timeoutrank
    @commands.command(name='timeoutrank')
    async def timeout_stats(self, ctx):
        timeout_ranking = sorted(timeouts.items(), key=lambda x: x[1], reverse=True)[:10]

        response = "타임아웃 랭킹 : "
        for idx, (user, count) in enumerate(timeout_ranking):
            response += f"\n{idx+1}. {user}: {count}회"

        await ctx.send(response)

    # define timeout tracking event method
    async def event_clearchat(self, params):
      user = params['target_user']
      timeouts[user] += 1
      channel = self.get_channel('마야100')  # 봇이 타임아웃을 추적할 스트리머 채널 이름으로 교체하세요.
      await channel.send(f"{user}님이 {timeouts[user]}번째로 나갔습니다...")


# Bot Run
if __name__ == "__main__":
    bot = TwitchBot()
    bot.run()
