import discord
import Maker
import Model
import os
from dotenv import load_dotenv
from discord.ext import commands

#Prefix to write out commands
client = commands.Bot(command_prefix = '!')
#client.remove_command('help')

#Load .env variables
load_dotenv()
TOKEN = os.getenv('GACHOW_TOKEN')

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
	randomMaker = discord.Embed(
		colour = discord.Colour(13938487)
	)
	randomMaker.add_field(name = 'Maker:', value = f'{maker.Name}', inline = False)
	randomMaker.add_field(name = 'Wikipedia:', value = f"https://en.wikipedia.org{maker.WikiLink}", inline = False)
	await ctx.send(embed = randomMaker)

@client.command()
async def randomcar(ctx):
	car = Model.randomCar()
	randomCar = discord.Embed(
		title = car.Maker,
		description = car.Name + '\n' + car.Date + '\n' + car.Description,
		colour = discord.Colour(524543)
	)
	#randomCar.set_image(url = f'https://www.automobile-catalog.com{car.Image}')
	await ctx.send(embed = randomCar)

#Sends user a link to fill out google form
@client.command()
async def addmodel(ctx):
	add = discord.Embed(
		colour = discord.Colour(5630772),
		title = "Google form to add missing car"
	)
	add.add_field(name = "Link:", value = "https://forms.gle/zb4Y3ELamyqVjyoz8", inline = False)
	await ctx.send(embed = add)

#Personal Token
client.run(TOKEN)
