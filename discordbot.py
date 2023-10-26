import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='/', intents=intents)

# 사용자 정보와 잔액을 저장할 파일
DATA_FILE = "user_data.txt"

# 봇이 시작할 때 파일에서 데이터를 로드
user_balances = {}

def load_user_data():
    try:
        with open(DATA_FILE, "r") as file:
            lines = file.readlines()
            for line in lines:
                user_id, balance = line.strip().split(":")
                user_id = int(user_id)
                balance = int(balance)
                user = bot.get_user(user_id)
                user_balances[user] = balance
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다. 데이터를 초기화합니다.")

# 봇이 실행될 때 초기 설정
@bot.event
async def on_ready():
    print(f'봇이 {bot.user.name}로 로그인했습니다.')
    load_user_data()

# 동전 뒤집기 명령어
@bot.command(name='동전뒤집기')
async def coin_flip(ctx, amount: int):
    user = ctx.author

    if user not in user_balances:
        user_balances[user] = 100  # 사용자 잔액 초기화 (예시로 100으로 설정)

    if amount <= 0:
        await ctx.send('금액은 0보다 커야 합니다.')
    elif amount > user_balances[user]:
        await ctx.send('잔액이 부족합니다.')
    else:
        outcome = random.choice(['성공', '실패'])
        if outcome == '성공':
            user_balances[user] += amount
            await ctx.send(f'성공! {amount}을 얻었습니다. 현재 잔액: {user_balances[user]}')
        else:
            user_balances[user] -= amount
            await ctx.send(f'실패! {amount}을 잃었습니다. 현재 잔액: {user_balances[user]}')


# 관리자 잔액 추가 명령어
@bot.command(name='잔액추가')
async def add_balance(ctx, user_tag: str, amount: int):
    if ctx.author.guild_permissions.administrator:
        # 사용자 태그를 사용자 객체로 변환
        user = discord.utils.get(ctx.guild.members, mention=user_tag)

        if user:
            if user in user_balances:
                user_balances[user] += amount
                await ctx.send(f'{user.mention}의 잔액이 {amount} 추가되었습니다. 현재 잔액: {user_balances[user]}')
            else:
                await ctx.send(f'{user.mention}은(는) 봇을 사용한적이 없습니다.')
            
            # 결과가 나면 파일에 데이터를 저장
            save_user_data()
        else:
            await ctx.send('사용자를 찾을 수 없습니다.')
    else:
        await ctx.send('관리자만 이 명령어를 사용할 수 있습니다.')

# 데이터를 파일에 저장
def save_user_data():
    with open(DATA_FILE, "w") as file:
        for user, balance in user_balances.items():
            file.write(f"{user.id}:{balance}\n")

# 봇을 실행
bot.run('MTE2NTI0MzcwMzUwNjUyMjIzMg.GfcjwJ.fMlGoZwPd-s3B56UChBz7HCbj4EP1_SxXqoCIg')
