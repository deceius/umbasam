import discord
import constants.tokens as tokens
import modules.mageraid as mage
import modules.avaraid as ava
import modules.util as util
from discord_components import ComponentsBot


bot = ComponentsBot("!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.command()
async def mageraid(ctx, user: discord.User = None):
    if user == None:
        user = ctx.message.author
    await mage.start(ctx, bot, user)

@bot.command()
async def avaraid(ctx, *, arg):
    await ava.start(ctx, bot, arg)

@bot.command()
async def desc(ctx, *, arg):
   await util.set_description(ctx, arg)

@bot.command()
async def tank(ctx, *, arg):
    await ava.set_role_qty(ctx, "TANK",  arg)


@bot.command()
async def dps(ctx, *, arg):
    await ava.set_role_qty(ctx, "DPS",  arg)
        
@bot.command()
async def heal(ctx, *, arg):
    await ava.set_role_qty(ctx, "HEAL",  arg)

@bot.command()
async def supp(ctx, *, arg):
    await ava.set_role_qty(ctx, "SUPP", arg)

@bot.command()
async def cta_attendance(ctx, *, arg):
    await ava.set_role_qty(ctx, "SUPP", arg)

bot.run(tokens.BOT_TOKEN)