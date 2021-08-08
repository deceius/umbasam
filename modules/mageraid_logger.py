import discord
import constants.tokens as tokens
import modules.quotes as quotes
import csv
import ast


async def add_mage_raid(client, data):
    log_channel = client.get_channel(tokens.CHANNEL_MAGE_RAID_LOGS_ID)
    msg = await log_channel.send(content = "#{0}".format(data))
    return msg.id

async def update_mage_raid(client, msg_id, data):
    log_channel = client.get_channel(tokens.CHANNEL_MAGE_RAID_LOGS_ID)
    msg = await log_channel.fetch_message(msg_id)
    await msg.edit(content = "#{0}".format(data))
    return

async def fetch_mage_raid(ctx, limit = 100):
    data = []
    async for msg in ctx.message.channel.history(limit = limit):
        if msg.content.startswith('#'):
            data.append(ast.literal_eval(msg.content[1:]))
    # write to file
    with open("result.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(data)
        
    # send file to Discord in message
    with open("result.csv", "rb") as file:
        await ctx.send("Attached is the dump file. {0}".format(quotes.generate_quote()[0]), file=discord.File(file, "result.csv"))
    return