
import discord
import os
import constants.strings as strings
import constants.tokens as tokens
import constants.commands as commands
import modules.mageraid_logger as logger

def is_correct_mr_channel(channel):
    if channel.id in tokens.CHANNEL_MAGE_RAID_SESSION_IDS:
        return True
    return False

async def start(client, ctx):
    message = ctx.message
    if not is_correct_mr_channel(ctx.message.channel):
        await message.channel.send(strings.INCORRECT_MR_CHANNEL.format(message.author))
        return
    
    if not message.attachments:
        await message.channel.send(strings.ERROR_MR_PROOF.format(message.author))
        return

    embedVar = generate_embed_message(client, message, message.attachments[0].url)

    data = [message.author.display_name, '--', '0', strings.STATUS_STARTED, message.created_at.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]]
    msg_id = await logger.add_mage_raid(client, data)
    embedVar.set_author(name="{0}".format(msg_id))
    msg = await message.channel.send(embed = embedVar, content = strings.MAGE_RAID_START.format(message.author))
    await msg.add_reaction(commands.REACT_SUCCESS)
    await msg.add_reaction(commands.REACT_FAILED)
    await message.delete()

def generate_embed_message(client, message, image = None):
    embedVar = discord.Embed(title= strings.TITLE, description="", color=0x0000ff)
    embedVar.add_field(name=strings.PARTY_LEADER, value=message.author.display_name, inline=False)
    embedVar.add_field(name=strings.OFFICER_CONFIRMATION, value="--", inline=False)
    embedVar.add_field(name=strings.SIPHONED_ENERGY_COUNT, value="0", inline=False)
    embedVar.add_field(name=strings.STATUS, value=strings.STATUS_STARTED, inline=False)
    embedVar.add_field(name=strings.DATETIME, value=message.created_at, inline=False)
    embedVar.add_field(name="** **", value=strings.PROMPT, inline=False)
    embedVar.set_thumbnail(url=image)
    return embedVar

async def generate_outcome(client, embed_dict, status, color, officer = None):
    pt_lead = ""
    date_time = ""
    count = ""
    officer_name = ""
    for field in embed_dict["fields"]:
        if field["name"] == strings.PARTY_LEADER:
            pt_lead = field["value"]
        if field["name"] == strings.STATUS:
            field["value"] = status
            embed_dict["color"] = color
        if field["name"] == strings.SIPHONED_ENERGY_COUNT:
            count = field["value"]
        if field["name"] == strings.DATETIME:
            date_time = field["value"]
        if field["name"] == strings.OFFICER_CONFIRMATION:
            if not officer == None:
                field["value"] = officer.display_name
            officer_name = field["value"]
        if field["name"] == "** **":
            field["value"] = strings.PROMPT_DELETE
    embed = discord.Embed.from_dict(embed_dict)
    data = [pt_lead, officer_name, count, status, date_time]
    await logger.update_mage_raid(client, embed.author.name, data)
    return embed

def validate_reaction(embed_dict, reaction, user):
    if embed_dict["color"] != strings.COLOR_STARTED:
        return False
    return True

def has_officer_role(user):
    for role in user.roles:
        if role.name == strings.SEASON_RAID_OFFICER or role.name == strings.SHOTCALLER or role.name == strings.ROUND_TABLE:
            return True
    return False

async def validate_message_status(message):
    msg = await message.channel.fetch_message(message.reference.message_id)
    embed = msg.embeds[0]
    embed_dict = embed.to_dict()
    if embed_dict["color"] != strings.COLOR_STARTED:
        return False
    return True

async def reply_siphoned(message):
    is_valid = False
    try: 
        is_valid = await is_mage_raid_valid(message)
    except:
        is_valid = False

    if message.reference is not None and message.content.startswith(commands.MAGE_SIPHONED) and is_valid:
         is_valid = True
    else:
        await message.channel.send(strings.ERROR_SIPHONED.format(message.author))
        await message.delete()
    return is_valid

async def reply_outcome(message):
    is_valid = False
    try: 
        is_valid = await is_mage_raid_valid(message)
    except:
        is_valid = False

    if message.reference is not None and message.content.startswith(commands.MAGE_OUTCOME) and is_valid:
         is_valid = True
    else:
        await message.channel.send(strings.ERROR_MR_PROOF.format(message.author))
        await message.delete()

    return is_valid

async def is_mage_raid_valid(message):
    is_valid_reply = await is_mage_raid_valid_reply(message) 
    is_valid_status = await validate_message_status(message)
    return is_valid_reply and is_valid_status

async def is_mage_raid_valid_reply(message):
    msg = await message.channel.fetch_message(message.reference.message_id)
    # Check if the mentioned party lead is the one who replied
    if msg.mentions[0].id == message.author.id:
        return True
    return False

async def is_mage_raid_party_leader(reaction, user):
    message = reaction.message
    msg = await message.channel.fetch_message(message.id)
    # Check if the mentioned party lead is the one who reacted
    if msg.mentions[0].id == user.id:
        return True
    return False

async def process_siphoned(client, message, siphoned_count):
    msg = await message.channel.fetch_message(message.reference.message_id)
    status = ""
    officer = ""
    pt_lead = ""
    date_time = ""
    embed_dict = msg.embeds[0].to_dict()
    for field in embed_dict["fields"]:
        if field["name"] == strings.PARTY_LEADER:
            pt_lead = field["value"]
        if field["name"] == strings.SIPHONED_ENERGY_COUNT:
            field["value"] = siphoned_count
        if field["name"] == strings.STATUS:
            status = field["value"]
        if field["name"] == strings.OFFICER_CONFIRMATION:
            officer = field["value"]
        if field["name"] == strings.DATETIME:
            date_time = field["value"]
    embed = discord.Embed.from_dict(embed_dict)
    data = [pt_lead, officer, siphoned_count, status, date_time]
    await logger.update_mage_raid(client, embed.author.name, data)
    await msg.edit(embed = embed)
    await message.delete()

async def process_outcome(client, message):
    msg = await message.channel.fetch_message(message.reference.message_id)
    embed = msg.embeds[0]
    embed.set_image(url = message.attachments[0].url)
    embed.set_footer(text = "Outcome Season Points screenshot is attached at: {0}".format(message.created_at))
    await msg.edit(embed = embed)
    await message.delete()


async def fetch_mage_raid(ctx, limit):
    await logger.fetch_mage_raid(ctx, limit)
    return