import discord
import Maker
from discord.ext import commands

#Prefix to write out commands
client = commands.Bot(command_prefix = '!')

#Checks if bot is online
@client.event
async def on_ready():
	print('Bot is ready!')

#Prints out when a member has joined
@client.event
async def on_member_join(member):
	print(f'{member} has joined!')

#Prints out when a member has left
@client.event
async def on_member_removed(member):
	print(f'{member} has left :(')

#Replies with a list of every car
@client.command()
async def maker(ctx):
	makerList = Maker.allManufacturers()
	#await ctx.send(listToSend)

#Replies with a random brand
@client.command()
async def randommaker(ctx):
	maker = Maker.randomManufacturer()
	await ctx.send(maker.Name)
	await ctx.send(f'https://en.wikipedia.org{maker.WikiLink}')

#Personal Token
client.run('MzA0NzY3MzgwNTUzNDY1ODU2.WPlKvQ.lhqDUlkexhQlv2w8ldi8R9PV3Tg')
