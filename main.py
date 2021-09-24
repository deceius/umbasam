import discord
import constants.tokens as tokens
import constants.commands as commands
import modules.mageraid as mageraid
import modules.avaraid as avaraid
import modules.gank as ganking
import modules.zvz as zerg
import modules.util as util
import modules.lfg as lfg
import modules.quotes as quotes
from discord_components import ComponentsBot


bot = ComponentsBot("!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.command()
async def mage(ctx, user: discord.User = None):
    if user == None:
        user = ctx.message.author
    await mageraid.start(ctx, bot, user)

@bot.command()
async def ava(ctx, *, arg):
    await avaraid.start(ctx, bot, arg)
    
@bot.command()
async def comp(ctx):
    await zerg.start(ctx, bot)

@bot.command()
async def fight(ctx):
    await ganking.start(ctx, bot)

@bot.command()
async def desc(ctx, *, arg):
   await util.set_description(ctx, arg)

@bot.command()
async def tank(ctx, *, arg):
    await lfg.set_role_qty(ctx, "TANK",  arg)


@bot.command()
async def mdps(ctx, *, arg):
    await lfg.set_role_qty(ctx, "MDPS",  arg)

    
@bot.command()
async def rdps(ctx, *, arg):
    await lfg.set_role_qty(ctx, "RDPS",  arg)


@bot.command()
async def dps(ctx, *, arg):
    await lfg.set_role_qty(ctx, "DPS",  arg)
        
@bot.command()
async def heal(ctx, *, arg):
    await lfg.set_role_qty(ctx, "HEAL",  arg)

@bot.command()
async def supp(ctx, *, arg):
    await lfg.set_role_qty(ctx, "SUPP", arg)


@bot.command()
async def oath(ctx, arg):
    result = quotes.generate_oath(arg.lower())
    if result.startswith("#"):
        file = open(result[1:], "rb")
        await ctx.channel.send(file = discord.File(file))
    else:
        await ctx.channel.send(content = result)


@bot.command()
async def poglog(ctx):
    file = open("files/poglog.mp4", "rb")
    await ctx.channel.send(file = discord.File(file))

@bot.command()
async def judwigcares(ctx):
    await ctx.channel.send(content = "https://media.discordapp.net/attachments/873398167587131452/887017963146866708/unknown.png")


@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return
    if commands.UMBASAM in message.content:
        await message.channel.send(content = quotes.generate_quote()[0])
        return
    if commands.JUDWIG in message.content:
        await message.channel.send(content = quotes.generate_judwig_quote()[0])
        return
    # single liner commands go here
    await bot.process_commands(message)

bot.run(tokens.BOT_TOKEN)