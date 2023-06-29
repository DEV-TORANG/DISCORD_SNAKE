from keep_alive import keep_alive
from pymongo import MongoClient
from discord.ext import commands
from asyncio import sleep as s
import datetime as dt
import os
import discord

#################################################################
# 몽고 DB 연결
mongo_URI = os.environ['M_URI']
client = MongoClient(mongo_URI)
db = client['DISCORD']  # DISCORD 컬렉션 접속
col = db['List_ID']
col_m = db['Month_List']

# 몽고 DB 연결 확인
print(" == MongoDB Connected == ")

#################################################################
# 디스코드 연결
discord_bot_token = os.environ['TOKEN']
intents = discord.Intents.default()
intents.message_content = True
bot_activity = discord.Game(name=':: DB가 싫어요 ::')
bot = commands.Bot(activity=bot_activity, command_prefix="$", intents=intents)


#################################################################
#디스코드 봇 이벤트
@bot.event
async def on_ready():
  print('Bot: {}'.format(bot.user))


#################################################################
#디스코드 봇 커맨드
# 인사
@bot.command()
async def ping(ctx):
  await ctx.send("pong")


@bot.command()
async def 월초기화(ctx):
  await ctx.send("```:: 수동 월 초기화작업을 시작합니다 ::```")

  if ctx.author.id == 698525539102883890 or ctx.author.id == 234923479722491904 or ctx.author.id == 416565422045790219:
    print("초기화 시작")
    embed = discord.Embed(title=":: RANKING ::",
                          description="현재까지의 이번 한 달간의 정산표 입니다.")
    data = col_m.find({}, {"_id": False}).sort("timer", -1)
    for d in data:
      # discord id
      # O_id = d["id"]
      # discord name
      O_name = d["name"]
      # timer
      O_timer = d["timer"]
      # cnt
      O_cnt = d["cnt"]

      # 시간 표기 변경 파트
      O_hour = O_timer // 10000
      O_min = (O_timer - (O_hour * 10000)) // 100
      O_sec = O_timer % 100

      if O_sec >= 60:
        O_sec -= 60
        O_min += 1

      if O_min >= 60:
        O_min -= 60
        O_hour += 1

      embed.add_field(name="이름   ", value=O_name, inline=True)
      embed.add_field(name="총 공부한 시간   ",
                      value=str(O_hour) + " 시간 " + str(O_min) + " 분 " +
                      str(O_sec) + " 초",
                      inline=True)
      embed.add_field(name="추가 횟수   ", value=O_cnt, inline=True)
    await ctx.send(embed=embed)

    await ctx.send("``` 보로스 :: 저번달의 데이터를 초기화 할게요. ```")
    col_m.delete_many({})


@bot.command()
async def 초기화(ctx):
  await ctx.send("```:: 수동 초기화작업을 시작합니다 ::```")

  if ctx.author.id == 698525539102883890 or ctx.author.id == 234923479722491904 or ctx.author.id == 416565422045790219:
    print("초기화 시작")
    embed = discord.Embed(title=":: RANKING ::",
                          description="현재까지의 이번 한 주간의 정산표 입니다.")
    data = col.find({}, {"_id": False}).sort("timer", -1)
    for d in data:
      # discord id
      # O_id = d["id"]
      # discord name
      O_name = d["name"]
      # timer
      O_timer = d["timer"]
      # cnt
      O_cnt = d["cnt"]

      # 시간 표기 변경 파트
      O_hour = O_timer // 10000
      O_min = (O_timer - (O_hour * 10000)) // 100
      O_sec = O_timer % 100

      if O_sec >= 60:
        O_sec -= 60
        O_min += 1

      if O_min >= 60:
        O_min -= 60
        O_hour += 1

      embed.add_field(name="이름   ", value=O_name, inline=True)
      embed.add_field(name="총 공부한 시간   ",
                      value=str(O_hour) + " 시간 " + str(O_min) + " 분 " +
                      str(O_sec) + " 초",
                      inline=True)
      embed.add_field(name="추가 횟수   ", value=O_cnt, inline=True)
    await ctx.send(embed=embed)

    await ctx.send("```보로스 :: 저번주의 데이터를 초기화 할게요.```")
    col.delete_many({})


@bot.command()
async def 헬프(ctx):
  embed = discord.Embed(title=" :: 명령어 모음 :: ",
                        description="모든 명령어는 $를 앞에 붙히셔야 가능합니다.")
  embed.add_field(
    name="$추가 [시간]",
    value="'$추가 5000' 형식으로 사용가능합니다.\n시간은 1시간 23분 45초라면 $추가 12345로 하시면됩니다.\n",
    inline=False)
  embed.add_field(
    name="$빼기 [시간]",
    value="'$빼기 5000' 형식으로 사용가능합니다.\n사용법은 $추가와 동일합니다. 실수로 추가된 시간을 지울때 사용하세요.\n",
    inline=False)
  embed.add_field(
    name="$조회, $월조회",
    value="'$조회' '$월조회' 로 사용가능합니다.\n현재까지 이번 주에 공부하여 추가한 모든 시간을 확인하실수 있습니다.\n",
    inline=False)
  embed.add_field(
    name="$랭킹, $월랭킹",
    value="'$랭킹' '$월랭킹' 으로 사용가능합니다.\n현재까지 이번 주의 추가 시간을 기준으로 랭킹을 볼 수 있습니다.\n",
    inline=False)
  embed.add_field(
    name="$초기화, $월초기화",
    value="'$초기화' '$월초기화' 로 사용가능합니다.\n현재까지 모든 시간을 초기화 합니다. 관리자 전용 명령어 입니다.\n",
    inline=False)
  await ctx.send(embed=embed)


@bot.command()
async def 리(ctx):
  print("remind!")
  check_week = 0
  print("지금부터 요일이 바뀔때마다 알람을 드리겠습니다.")
  while (True):
    await s(60)
    x = dt.datetime.now()
    now_time = x.strftime("%H:%M")
    now_weekday = x.weekday()

    # or now_time == '15:01' or now_time == '15:02' or now_time == '15:03' or now_time == '15:04'
    if now_time == '15:00':
      check_week = 1
    else:
      check_week = 0

    if check_week == 1:
      if now_weekday == 0:
        await ctx.send("```" + "::: 2  일 차 :::\n::: 화 요 일 :::" + "```")
      elif now_weekday == 1:
        await ctx.send("```" + "::: 3  일 차 :::\n::: 수 요 일 :::" + "```")
      elif now_weekday == 2:
        await ctx.send("```" + "::: 4  일 차 :::\n::: 목 요 일 :::" + "```")
      elif now_weekday == 3:
        await ctx.send("```" + "::: 5  일 차 :::\n::: 금 요 일 :::" + "```")
      elif now_weekday == 4:
        await ctx.send("```" + "::: 6  일 차 :::\n::: 토 요 일 :::" + "```")
      elif now_weekday == 5:
        await ctx.send("```" + "::: 7  일 차 :::\n::: 일 요 일 :::" + "```")
      elif now_weekday == 6:
        embed = discord.Embed(title=":: RANKING ::",
                              description="현재까지의 이번 한 주간의 정산표 입니다.")
        data = col.find({}, {"_id": False}).sort("timer", -1)
        for d in data:
          # discord id
          # O_id = d["id"]
          # discord name
          O_name = d["name"]
          # timer
          O_timer = d["timer"]
          # cnt
          O_cnt = d["cnt"]

          # 시간 표기 변경 파트
          O_hour = O_timer // 10000
          O_min = (O_timer - (O_hour * 10000)) // 100
          O_sec = O_timer % 100

          if O_sec >= 60:
            O_sec -= 60
            O_min += 1

          if O_min >= 60:
            O_min -= 60
            O_hour += 1

          embed.add_field(name="이름   ", value=O_name, inline=True)
          embed.add_field(name="총 공부한 시간   ",
                          value=str(O_hour) + " 시간 " + str(O_min) + " 분 " +
                          str(O_sec) + " 초",
                          inline=True)
          embed.add_field(name="추가 횟수   ", value=O_cnt, inline=True)
        await ctx.send(embed=embed)

        await ctx.send("```보로스 :: 이번주의 데이터를 초기화 할게요.```")
        col.delete_many({})
        await ctx.send("```" + "::: 새로운 한주가 시작되었습니다. :::" + "```")
        await ctx.send("```" + "::: 1  일 차 :::\n::: 월 요 일 :::" + "```")
      check_week = 0
    else:
      print("아직 아님")


# DB 저장을 위한 회원가입
@bot.command()
async def 추가(ctx, P_time):

  daycnt = 1

  print("up!")
  P_time = int(P_time)

  # 시간 표기 변경 파트
  P_hour = P_time // 10000
  P_min = (P_time - (P_hour * 10000)) // 100
  P_sec = P_time % 100

  if P_sec >= 120:
    P_sec -= 120
    P_min += 2
  elif P_sec >= 60:
    P_sec -= 60
    P_min += 1

  if P_min >= 120:
    P_min -= 120
    P_hour += 2
  elif P_min >= 60:
    P_min -= 60
    P_hour += 1

  print("1111")
  result = col.find({"id": ctx.author.id}, {"_id": False, "id": True})
  print("1112")
  for r in result:
    print("1113")
    result = r
  print("1114")
  result_m = col_m.find({"id": ctx.author.id}, {"_id": False, "id": True})
  for rm in result_m:
    result_m = rm
  # 첫 등록이 아닌 경우
  if result != 0 and result == {
      'id': ctx.author.id
  } and result_m == {
      'id': ctx.author.id
  }:
    print("1114")
    data = col.find({"id": ctx.author.id}, {"_id": False})
    data_m = col_m.find({"id": ctx.author.id}, {"_id": False})
    for d in data:
      # discord id
      # O_id = d["id"]
      # discord name
      # O_name = d["name"]
      # timer
      O_timer = d["timer"]

      O_hour = O_timer // 10000
      O_min = (O_timer - (O_hour * 10000)) // 100
      O_sec = O_timer % 100

      if O_sec >= 120:
        O_sec -= 120
        O_min += 2
      elif O_sec >= 60:
        O_sec -= 60
        O_min += 1

      if O_min >= 120:
        O_min -= 120
        O_hour += 2
      elif O_min >= 60:
        O_min -= 60
        O_hour += 1

      O_timer = O_hour * 10000 + O_min * 100 + O_sec

      F_timer = int(O_timer) + int(P_time)
      # cnt
      O_cnt = d["cnt"]
      F_cnt = int(O_cnt) + 1

    col.delete_one({'id': ctx.author.id})

    F_data = {
      'id': ctx.author.id,
      'name': ctx.author.name,
      'timer': F_timer,
      'cnt': F_cnt
    }
    dpInsert = db.List_ID.insert_one(F_data)

    ###########################################################
    # 월 추가 관련
    for dm in data_m:
      # discord id
      # O_id_m = dm["id"]
      # discord name
      # O_name_m = dm["name"]
      # timer
      O_timer_m = dm["timer"]

      O_hour_m = O_timer_m // 10000
      O_min_m = (O_timer_m - (O_hour_m * 10000)) // 100
      O_sec_m = O_timer_m % 100

      if O_sec_m >= 120:
        O_sec_m -= 120
        O_min_m += 2
      elif O_sec_m >= 60:
        O_sec_m -= 60
        O_min_m += 1

      if O_min_m >= 120:
        O_min_m -= 120
        O_hour_m += 2
      elif O_min_m >= 60:
        O_min_m -= 60
        O_hour_m += 1

      O_timer_m = O_hour_m * 10000 + O_min_m * 100 + O_sec_m

      F_timer_m = int(O_timer_m) + int(P_time)
      # cnt
      O_cnt_m = dm["cnt"]
      F_cnt_m = int(O_cnt_m) + 1

    col_m.delete_one({'id': ctx.author.id})

    F_data_m = {
      'id': ctx.author.id,
      'name': ctx.author.name,
      'timer': F_timer_m,
      'cnt': F_cnt_m
    }
    dpInsert = db.Month_List.insert_one(F_data_m)

    await ctx.send("```" + ctx.author.name + " 님의 타이머에\n" + str(P_hour) +
                   " 시간 " + str(P_min) + " 분 " + str(P_sec) +
                   " 초가 추가 되었습니다!```")

    #############################################

  # 월은 있지만, 주가 없는 경우
  elif result != 0 and result_m == {'id': ctx.author.id}:
    await ctx.send("```이번 주의 " + ctx.author.name +
                   " 님의 정보가 없습니다.\n따라서, 새로 등록합니다.\n환영합니다, " + ctx.author.name +
                   " 님\n이번 주도 즐거운 작품활동 되시길 바랍니다.```")

    data_m = col_m.find({"id": ctx.author.id}, {"_id": False})

    data = {
      'id': ctx.author.id,
      'name': ctx.author.name,
      'timer': int(P_time),
      'cnt': int(daycnt)
    }
    dpInsert = db.List_ID.insert_one(data)

    ###########################################################
    # 월 추가 관련
    for dm in data_m:
      # discord id
      # O_id_m = dm["id"]
      # discord name
      # O_name_m = dm["name"]
      # timer
      O_timer_m = dm["timer"]

      O_hour_m = O_timer_m // 10000
      O_min_m = (O_timer_m - (O_hour_m * 10000)) // 100
      O_sec_m = O_timer_m % 100

      if O_sec_m >= 120:
        O_sec_m -= 120
        O_min_m += 2
      elif O_sec_m >= 60:
        O_sec_m -= 60
        O_min_m += 1

      if O_min_m >= 120:
        O_min_m -= 120
        O_hour_m += 2
      elif O_min_m >= 60:
        O_min_m -= 60
        O_hour_m += 1

      O_timer_m = O_hour_m * 10000 + O_min_m * 100 + O_sec_m

      F_timer_m = int(O_timer_m) + int(P_time)
      # cnt
      O_cnt_m = dm["cnt"]
      F_cnt_m = int(O_cnt_m) + 1

    col_m.delete_one({'id': ctx.author.id})

    F_data_m = {
      'id': ctx.author.id,
      'name': ctx.author.name,
      'timer': F_timer_m,
      'cnt': F_cnt_m
    }
    dpInsert = db.Month_List.insert_one(F_data_m)

    await ctx.send("```" + ctx.author.name + " 님의 타이머에\n" + str(P_hour) +
                   " 시간 " + str(P_min) + " 분 " + str(P_sec) +
                   " 초가 추가 되었습니다!```")

  # 첫 등록인 경우
  elif result != 0:
    await ctx.send("```이번 주 및 이번 달의 " + ctx.author.name +
                   " 님의 정보가 없습니다.\n따라서, 새로 등록합니다.\n환영합니다, " + ctx.author.name +
                   " 님\n이번 주도 즐거운 작품활동 되시길 바랍니다.```")

    data = {
      'id': ctx.author.id,
      'name': ctx.author.name,
      'timer': int(P_time),
      'cnt': int(daycnt)
    }
    dpInsert = db.List_ID.insert_one(data)
    dpInsert = db.Month_List.insert_one(data)

    await ctx.send("```" + ctx.author.name + " 님의 타이머에\n" + str(P_hour) +
                   " 시간 " + str(P_min) + " 분 " + str(P_sec) +
                   " 초가 추가 되었습니다!```")
  # 에러 처리
  else:
    await ctx.send("```에러가 발생했습니다.\n관리자에게 문의해주세요.```")


# DB 저장 실수를 대비한 삭제
@bot.command()
async def 빼기(ctx, P_time):

  result = 0

  P_time = abs(int(P_time))

  # 시간 표기 변경 파트
  P_hour = P_time // 10000
  P_min = (P_time - (P_hour * 10000)) // 100
  P_sec = P_time % 100

  if P_sec >= 60:
    P_sec -= 60
    P_min += 1

  if P_min >= 60:
    P_min -= 60
    P_hour += 1

  result = col.find({"id": ctx.author.id}, {"_id": False, "id": True})
  for r in result:
    result = r

  result_m = col_m.find({"id": ctx.author.id}, {"_id": False, "id": True})
  for rm in result_m:
    result_m = rm

  # 첫 등록이 아닌 경우
  if result != 0 and result == {'id': ctx.author.id}:
    data = col.find({"id": ctx.author.id}, {"_id": False})
    data_m = col_m.find({"id": ctx.author.id}, {"_id": False})
    for d in data:
      # discord id
      #O_id = d["id"]
      # discord name
      #O_name = d["name"]
      # timer
      O_timer = d["timer"]

      O_hour = O_timer // 10000
      O_min = (O_timer - (O_hour * 10000)) // 100
      O_sec = O_timer % 100

      O_timer = O_hour * 10000 + O_min * 100 + O_sec

      if O_timer < P_time:
        await ctx.send("```ERROR! 너무 많은 시간을 입력했습니다!```")
      else:
        if O_sec < P_sec:
          O_min -= 1
          O_sec += 60

        if O_min < P_min:
          O_hour -= 1
          O_min += 60

        F_sec = O_sec - P_sec
        F_min = O_min - P_min
        F_hour = O_hour - P_hour

        F_timer = F_hour * 10000 + F_min * 100 + F_sec
        # cnt
        O_cnt = d["cnt"]
        F_cnt = int(O_cnt) - 1

    col.delete_one({'id': ctx.author.id})

    F_data = {
      'id': ctx.author.id,
      'name': ctx.author.name,
      'timer': F_timer,
      'cnt': F_cnt
    }
    dpInsert = db.List_ID.insert_one(F_data)

    #######################################################################

    for dm in data_m:
      # discord id
      #O_id = dm["id"]
      # discord name
      #O_name = dm["name"]
      # timer
      O_timer_m = dm["timer"]

      O_hour_m = O_timer_m // 10000
      O_min_m = (O_timer_m - (O_hour * 10000)) // 100
      O_sec_m = O_timer_m % 100

      O_timer_m = O_hour_m * 10000 + O_min_m * 100 + O_sec_m

      if O_timer_m < P_time:
        await ctx.send("```ERROR! 너무 많은 시간을 입력했습니다!```")
      else:
        if O_sec_m < P_sec:
          O_min_m -= 1
          O_sec_m += 60

        if O_min_m < P_min:
          O_hour_m -= 1
          O_min_m += 60

        F_sec = O_sec_m - P_sec
        F_min = O_min_m - P_min
        F_hour = O_hour_m - P_hour

        F_timer_m = F_hour * 10000 + F_min * 100 + F_sec
        # cnt
        O_cnt_m = dm["cnt"]
        F_cnt_m = int(O_cnt_m) - 1

    col_m.delete_one({'id': ctx.author.id})

    F_data_m = {
      'id': ctx.author.id,
      'name': ctx.author.name,
      'timer': F_timer_m,
      'cnt': F_cnt_m
    }
    dpInsert = db.Month_List.insert_one(F_data_m)

    await ctx.send("```" + ctx.author.name + " 님의 타이머에\n" + str(abs(P_hour)) +
                   " 시간 " + str(abs(P_min)) + " 분 " + str(abs(P_sec)) +
                   " 초가 삭제 되었습니다!```")

  # 첫 등록의 경우
  elif result != 0:
    await ctx.send(
      "```이번주의 " + ctx.author.name +
      " 님의 정보가 없습니다.\n따라서, 요청을 실행할수 없습니다.\n문제가 발생했다면 관리자에게 문의해주세요.```")

  # 에러 처리
  else:
    await ctx.send("```에러가 발생했습니다.\n관리자에게 문의해주세요.```")


# DB 조회하기
@bot.command()
async def 조회(ctx):

  result = col.find({"id": ctx.author.id}, {"_id": False, "id": True})
  for r in result:
    result = r
  # 첫 등록이 아닌 경우
  if result != 0 and result == {'id': ctx.author.id}:
    data = col.find({"id": ctx.author.id}, {"_id": False})
    for d in data:
      # discord id
      #O_id = d["id"]
      # discord name
      #O_name = d["name"]
      # timer
      O_timer = d["timer"]
      # cnt
      O_cnt = d["cnt"]

    # 시간 표기 변경 파트
    O_hour = O_timer // 10000
    O_min = (O_timer - (O_hour * 10000)) // 100
    O_sec = O_timer % 100

    if O_sec >= 60:
      O_sec -= 60
      O_min += 1

    if O_min >= 60:
      O_min -= 60
      O_hour += 1

    embed = discord.Embed(title=ctx.author.name,
                          description="현재까지의 이번 한 주간의 정산표 입니다.")
    embed.add_field(name="이번 주 총 공부한 시간",
                    value=str(O_hour) + " 시간 " + str(O_min) + " 분 " +
                    str(O_sec) + " 초",
                    inline=False)
    embed.add_field(name="추가 횟수", value=O_cnt, inline=False)
    await ctx.send(embed=embed)
  else:
    await ctx.send("```이번 주의 등록 정보를 찾을 수 없습니다!```")


@bot.command()
async def 월조회(ctx):

  result_m = col_m.find({"id": ctx.author.id}, {"_id": False, "id": True})
  for rm in result_m:
    result_m = rm

  # 첫 등록이 아닌 경우
  if result_m != 0 and result_m == {'id': ctx.author.id}:
    data = col_m.find({"id": ctx.author.id}, {"_id": False})
    for d in data:
      # discord id
      #O_id = d["id"]
      # discord name
      #O_name = d["name"]
      # timer
      O_timer = d["timer"]
      # cnt
      O_cnt = d["cnt"]

    # 시간 표기 변경 파트
    O_hour = O_timer // 10000
    O_min = (O_timer - (O_hour * 10000)) // 100
    O_sec = O_timer % 100

    if O_sec >= 60:
      O_sec -= 60
      O_min += 1

    if O_min >= 60:
      O_min -= 60
      O_hour += 1

    embed = discord.Embed(title=ctx.author.name,
                          description="현재까지의 이번 한 달간의 정산표 입니다.")
    embed.add_field(name="이번 주 총 공부한 시간",
                    value=str(O_hour) + " 시간 " + str(O_min) + " 분 " +
                    str(O_sec) + " 초",
                    inline=False)
    embed.add_field(name="추가 횟수", value=O_cnt, inline=False)
    await ctx.send(embed=embed)
  else:
    await ctx.send("```이번 달의 등록 정보를 찾을 수 없습니다!```")


# 랭킹 시스템
@bot.command()
async def 랭킹(ctx):

  embed = discord.Embed(title=":: RANKING ::",
                        description="현재까지의 이번 한 주간의 정산표 입니다.")

  data = col.find({}, {"_id": False}).sort("timer", -1)
  for d in data:
    # discord id
    #O_id = d["id"]
    # discord name
    O_name = d["name"]
    # timer
    O_timer = d["timer"]
    # cnt
    O_cnt = d["cnt"]

    # 시간 표기 변경 파트
    O_hour = O_timer // 10000
    O_min = (O_timer - (O_hour * 10000)) // 100
    O_sec = O_timer % 100

    if O_sec >= 60:
      O_sec -= 60
      O_min += 1

    if O_min >= 60:
      O_min -= 60
      O_hour += 1

    embed.add_field(name="이름   ", value=O_name, inline=True)
    embed.add_field(name="총 공부한 시간   ",
                    value=str(O_hour) + " 시간 " + str(O_min) + " 분 " +
                    str(O_sec) + " 초",
                    inline=True)
    embed.add_field(name="추가 횟수   ", value=O_cnt, inline=True)
  await ctx.send(embed=embed)


# 랭킹 시스템
@bot.command()
async def 월랭킹(ctx):

  embed = discord.Embed(title=":: RANKING ::",
                        description="현재까지의 이번 한 달간의 정산표 입니다.")

  data = col_m.find({}, {"_id": False}).sort("timer", -1)
  for d in data:
    # discord id
    #O_id = d["id"]
    # discord name
    O_name = d["name"]
    # timer
    O_timer = d["timer"]
    # cnt
    O_cnt = d["cnt"]

    # 시간 표기 변경 파트
    O_hour = O_timer // 10000
    O_min = (O_timer - (O_hour * 10000)) // 100
    O_sec = O_timer % 100

    if O_sec >= 60:
      O_sec -= 60
      O_min += 1

    if O_min >= 60:
      O_min -= 60
      O_hour += 1

    embed.add_field(name="이름   ", value=O_name, inline=True)
    embed.add_field(name="총 공부한 시간   ",
                    value=str(O_hour) + " 시간 " + str(O_min) + " 분 " +
                    str(O_sec) + " 초",
                    inline=True)
    embed.add_field(name="추가 횟수   ", value=O_cnt, inline=True)
  await ctx.send(embed=embed)


keep_alive()

try:
  bot.run(discord_bot_token)
except discord.errors.HTTPException:
  print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
  os.system('kill 1')
  os.system("python restarter.py")
