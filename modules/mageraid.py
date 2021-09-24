from discord_components import ButtonStyle, Button
import discord
import constants.strings as strings 


async def start(ctx, bot, user):

    embedVar = discord.Embed(title= "Mage Raid", description="Reply with `!desc <your_description_here>` to set a description.", color=0xf0f0f0)
    embedVar.add_field(name=strings.PARTY_MEMBERS, value="--", inline=False)
    embedVar.add_field(name=strings.SIPHONED_ENERGY_COUNT, value="0", inline=False)
    embedVar.set_footer(text = "Created by {0}".format(user.display_name))
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
                    Button(style=ButtonStyle.blue, label="+5"),
                    btn_add_5
                ),
                bot.components_manager.add_callback(
                    Button(style=ButtonStyle.red, label="Join"),
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

    
async def btn_add_5(interaction):
    await siphoned_update(interaction, 5)

async def btn_join(interaction):
    success = await add_member(interaction.message, interaction.user)
    if (success):
         await interaction.respond(type = 6)
    else:
         await interaction.send(content = "You are already in this mage party.")

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
        embed_dict = msg.embeds[0].to_dict()
        for field in embed_dict["fields"]:
            if field["name"] == strings.SIPHONED_ENERGY_COUNT:
                field["value"] = int(field["value"].strip()) + for_add
        embed = discord.Embed.from_dict(embed_dict)
        await msg.edit(embed = embed)
        await interaction.respond(type = 6)
    else:
        await interaction.send(content = "You are not the party leader of this mage raid.")


async def add_member(msg, member):
    if msg.mentions[0].id == member.id:
        return False
    embed_dict = msg.embeds[0].to_dict()
    for field in embed_dict["fields"]:
        if field["name"] == strings.PARTY_MEMBERS:
            if (member.display_name in field["value"]):
                return False
            if (field["value"] == "--"):
                field["value"] = member.display_name
            else:
                field["value"] = field["value"] + "\n" + member.display_name
    embed = discord.Embed.from_dict(embed_dict)
    await msg.edit(embed = embed)
    return True