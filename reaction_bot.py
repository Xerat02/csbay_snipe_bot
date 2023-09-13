import discord
from discord.ext import commands

TOKEN = 'MTE0MTQ5NDA4ODUyOTYyOTMxOQ.GosWpf.Sa_MakeEn8jY5eTgnqG8OCBhEI-o5FDcXsLDoQ'

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def get_reactions(ctx, channel_id: int, message_id: int):
    channel = bot.get_channel(channel_id)
    if not channel:
        await ctx.send("Channel with this ID was not found!")
        return

    try:
        message = await channel.fetch_message(message_id)
    except discord.NotFound:
        await ctx.send("Message with this ID was not found in the given channel!")
        return

    # Find the group with the most reactions
    max_reaction = None
    max_users = []

    for reaction in message.reactions:
        users = [user async for user in reaction.users()]
        if len(users) > len(max_users):
            max_reaction = reaction
            max_users = users

    if not max_users:
        await ctx.send("No reactions were found on the message.")
        return

    user_list = "\n".join([f"{i+1}. <@{user.id}>" for i, user in enumerate(max_users)])
    response = f"Group with the most reactions ({len(max_users)} reactions):\n{user_list}"

    # Send response in chunks if it's longer than 2000 characters
    while response:
        # If there's more response left than fits in a chunk, we find the last full user mention in the chunk to send.
        if len(response) > 2000:
            last_index = response.rfind("\n", 0, 2000)
            chunk = response[:last_index]
            await ctx.send(chunk)
            response = response[last_index + 1:]
        else:
            await ctx.send(response)
            response = ""


bot.run(TOKEN)