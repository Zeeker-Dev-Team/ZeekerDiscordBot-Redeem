import os
import discord
import uuid
from discord.ext import commands
from replit import db

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

# 设置允许新增代码的身份组名称
AUTHORIZED_ROLE = '/ STAFF ACCESS'


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


# 新增代码命令，仅限有指定身份组的成员使用
@client.command()
@commands.has_role(AUTHORIZED_ROLE)
async def newCode(ctx, code: str, value: str):
    new_key = f'key::{code}'
    if new_key == 'key::RANDOM':
        new_key = "key::" + str(uuid.uuid4())
    if new_key in db:
        await ctx.send('This code already exists!')
    else:
        db[new_key] = value
        await ctx.author.send(f'New code {new_key.split("::")[1]} has been created!')
    await ctx.message.delete()


# 兑换代码命令，结果发送到私聊
@client.command()
async def redeem(ctx, code: str):
    await ctx.send('Trying to redeem this code...')
    code_key = f'key::{code}'
    if code_key in db:
        await ctx.send('Code is valid! Please check your DM to get result!')
        await ctx.author.send(f'Reedem result for {code}: {db[code_key]}')
        del db[code_key]
    else:
        await ctx.author.send('Code is invalid or already redeemed!')


try:
    token = os.getenv("TOKEN")
    if not token:
        raise Exception("Please add your token to the Secrets pane.")
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print("Too many requests to the Discord servers.")
        print(
            "Check https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests for help."
        )
    else:
        raise e
