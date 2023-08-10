import asyncio
import json
from twitchio.ext import commands
from collections import defaultdict

# 저장할 타임아웃 카운트 구조체를 생성
timeouts = defaultdict(int)

# Twitch 봇 설정을 가져와서 클래스를 정의.

with open("./config.json", "r", encoding="utf-8") as E:
  config = json.loads(E.read())

irc = config['irc']
cid = config['cid']

class TwitchBot(commands.Bot):

    def __init__(self):
        super().__init__(
            irc_token=irc,              # Twitch OAuth 토큰으로 교체하세요
            client_id=cid,                # Twitch 클라이언트 ID로 교체하세요
            nick='BOT_USERNAME',                         # 봇의 Twitch 사용자 이름으로 교체하세요
            prefix='!',                                  # 원하는 챗 명령어 접두사로 교체 (예: !timeoutstats)
            initial_channels=['TWITCH_STREAMER_CHANNEL'] # 스트리머 채널 이름으로 교체하세요
        )

    # 메시지 이벤트 메서드 정의
    async def event_message(self, message):
        # 메시지를 받으면 처리 함수를 실행합.
        await self.handle_commands(message)

    # 타임아웃 랭킹 명령어 정의
    @commands.command(name='timeoutstats')
    async def timeout_stats(self, ctx):
        timeout_ranking = sorted(timeouts.items(), key=lambda x: x[1], reverse=True)[:10]

        response = "타임아웃 랭킹:"
        for idx, (user, count) in enumerate(timeout_ranking):
            response += f"\n{idx+1}. {user}: {count}회"

        await ctx.send(response)

    # 타임아웃 추적 이벤트 메서드를 정의
    async def event_clearchat(self, params):
        user = params['target_user']
        timeouts[user] += 1

# 봇 실행
if __name__ == "__main__":
    bot = TwitchBot()
    bot.run()
