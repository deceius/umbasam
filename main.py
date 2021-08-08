# Work with Python 3.6
import discord
import os
import constants.strings as strings
import constants.commands as commands
import constants.tokens as tokens
from discord.ext import commands as bot_commands
import modules.mageraid as mageraid
import modules.quotes as quotes
import modules.guide as guide


intents = discord.Intents().all()

bot = bot_commands.Bot(command_prefix = "!", intents = intents, help_command = None)

async def reply_siphoned(message):
    return await mageraid.reply_siphoned(message)


async def reply_outcome(message):
    if not message.attachments:
        return False
    return await mageraid.reply_outcome(message)

def validate_reaction(embed_dict, reaction, user):
    if not mageraid.validate_reaction(embed_dict, reaction, user):
        return False
    return True

@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return

    if commands.UMBASAM in message.content:
        await message.channel.send(content = quotes.generate_quote()[0])
        return
        
    # single liner commands go here
    await bot.process_commands(message)
    


@bot.command(name="oath")
async def cmd_oath(ctx, arg):
    await ctx.channel.send(content = quotes.generate_oath(arg.lower()))

@bot.command(name="umbasam")
async def cmd_umbasam(ctx):
    await ctx.channel.send(content = quotes.generate_quote()[0])

@bot.command(name="mageraid")
async def cmd_mageraid(ctx):
    await mageraid.start(bot, ctx)

@bot.command(name="siphoned")
async def cmd_siphoned(ctx, arg):
    message = ctx.message
    siphoned_count = arg
    if await reply_siphoned(message):
        await mageraid.process_siphoned(bot, message, siphoned_count)

@bot.command(name="compile")
async def cmd_compile(ctx, arg):
    if not ctx.message.channel.id == tokens.CHANNEL_MAGE_RAID_LOGS_ID:
        return
    await mageraid.fetch_mage_raid(ctx, int(arg))


@bot.command(name="outcome")
async def cmd_outcome(ctx):
    message = ctx.message
    if await reply_outcome(message):
        await mageraid.process_outcome(bot, message)

@bot.command(name = "umbaguide")
async def cmd_umbaguide(ctx, arg):
    if arg == "pvp":
        await guide.pvp(ctx)
    elif arg == "cdg":
        await guide.cdg(ctx)

@bot.command('cta')
async def cmd_cta(ctx):
    if mageraid.has_officer_role(ctx.message.author):
        await ctx.channel.send(content = "{0} ".format(ctx.guild.default_role)+ quotes.generate_cta()[0])
    else:
        await ctx.channel.send(content = "YOU CAN'T @ everyone. YOU HAVE NO POWAH HERE. ANYWAY, "+ quotes.generate_cta()[0])

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == user:
        return
    if reaction.emoji == commands.REACT_DELETE:
        if mageraid.has_officer_role(user):
            await reaction.message.delete()
        return
    embed = reaction.message.embeds[0]
    embed_dict = embed.to_dict()
    if not validate_reaction(embed_dict, reaction, user):
        return
    if reaction.emoji == commands.REACT_FAILED:
        is_party_lead = await mageraid.is_mage_raid_party_leader(reaction, user)
        if is_party_lead:
            failed_embed = await mageraid.generate_outcome(bot, embed_dict, strings.STATUS_FAILED, strings.COLOR_FAILED)
            await reaction.message.edit(embed = failed_embed)
            await reaction.message.add_reaction(commands.REACT_DELETE)
        return
    elif reaction.emoji == commands.REACT_SUCCESS:
        if mageraid.has_officer_role(user):
            success_embed = await  mageraid.generate_outcome(bot, embed_dict, strings.STATUS_SUCCESS, strings.COLOR_SUCCESS, user)
            await reaction.message.edit(embed = success_embed)
            await reaction.message.add_reaction(commands.REACT_DELETE)
        return
            

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

bot.run(tokens.BOT_TOKEN)