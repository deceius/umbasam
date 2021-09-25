from discord_components import ButtonStyle, Button
import discord
import constants.strings as strings 


async def start(ctx, bot, user):

    embedVar = discord.Embed(title= "Mage Raid", description="Reply with `!desc <your_description_here>` to set a description.", color=0xf0f0f0)
    embedVar.add_field(name=strings.PARTY_MEMBERS, value="--", inline=False)
    embedVar.add_field(name=strings.SIPHONED_ENERGY_COUNT, value="0", inline=False)
    embedVar.set_footer(text = "Reply with !energy <value> to update siphoned energy with specific value.\nNegative values will decrease the counted value.")
    embedVar.set_thumbnail(url="https://render.albiononline.com/v1/item/UNIQUE_GVGTOKEN_GENERIC.png")

    await ctx.send( 
        content = strings.MAGE_RAID_START.format(user),
        embed = embedVar, 
        components = [
            [
                bot.components_manager.add_callback(
                    Button(style=ButtonStyle.blue, label="+1"),
                    btn_add_1
                ),
                bot.components_manager.add_callback(
                    Button(style=ButtonStyle.blue, label="-1"),
                    btn_sub_1
                ),
                bot.components_manager.add_callback(
                    Button(style=ButtonStyle.red, label="Join / Leave Party"),
                    btn_join
                ),
                bot.components_manager.add_callback(
                    Button(style=ButtonStyle.green, label="Set Finished"),
                    btn_finish
                )
            ]
        ])
    await ctx.message.delete()



async def btn_add_1(interaction):
    await siphoned_update(interaction, 1)

    
async def btn_sub_1(interaction):
    await siphoned_update(interaction, -1)

async def btn_join(interaction):
    success = await add_member(interaction.message, interaction.user)
    if (success):
         await interaction.respond(type = 6)
    else:
         await interaction.send(content = "You are the party leader of this mage raid.")

async def btn_finish(interaction):
    msg = interaction.message
    if msg.mentions[0].id == interaction.user.id:
        embed_dict = interaction.message.embeds[0].to_dict()
        embed_dict["color"] = strings.COLOR_SUCCESS
        embed = discord.Embed.from_dict(embed_dict)
        await interaction.message.edit(embed = embed, components = [])
        await interaction.respond(type = 6)
    else:
        await interaction.send(content = "You are not the party leader of this mage raid.")


async def siphoned_update(interaction, for_add):
    msg = interaction.message
    if msg.mentions[0].id == interaction.user.id:
        await process_siphoned(msg, for_add)
        await interaction.respond(type = 6)
    else:
        await interaction.send(content = "You are not the party leader of this mage raid.")

async def process_siphoned(msg, for_add):
    embed_dict = msg.embeds[0].to_dict()
    if embed_dict["color"] == strings.COLOR_SUCCESS:
        return False
    for field in embed_dict["fields"]:
        if field["name"] == strings.SIPHONED_ENERGY_COUNT:
            field["value"] = str(int(field["value"].strip()) + for_add)
            if int(field["value"].strip()) < 0:
                field["value"] = 0
    embed = discord.Embed.from_dict(embed_dict)
    await msg.edit(embed = embed)
    return True

async def add_member(msg, member):
    if msg.mentions[0].id == member.id:
        return False
    embed_dict = msg.embeds[0].to_dict()
    if embed_dict["color"] == strings.COLOR_SUCCESS:
        return False
    for field in embed_dict["fields"]:
        if field["name"] == strings.PARTY_MEMBERS:
            if (member.mention in field["value"]):
                field["value"] = field["value"].replace(member.mention + "\n", "")
                field["value"] = field["value"].replace(member.mention, "")
                if (len(field["value"]) == 0):
                    field["value"] = "--"
            else:
                if (field["value"] == "--"):
                    field["value"] = member.mention
                else:
                    field["value"] = field["value"] + "\n" + member.mention
    embed = discord.Embed.from_dict(embed_dict)
    await msg.edit(embed = embed)
    return True