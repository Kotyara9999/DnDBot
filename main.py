# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
from discord.ui import Button, View
import random
from dnd_su_monster import Monser_Card

TOKEN = ""

description = '''An example bot to showcase the discord.ext.commands extension
module.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)
chan = None
moved = {}
ids = {}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return
    lis = [str(random.randint(1, limit)) for r in range(rolls)]
    result = ', '.join(lis) + str(sum(lis))
    await ctx.send(result)


@bot.command()
async def maw(ctx, *list_mem: discord.Member):
    cat = discord.utils.get(ctx.guild.categories, name="Голосовые каналы")
    if not ctx.author in moved.keys():
        chan: discord.VoiceChannel = await ctx.guild.create_voice_channel(
            str(ctx.author) + " и " + " ".join(map(str, list_mem)) + "(temp)", category=cat)
        await chan.set_permissions(ctx.author, connect=True, view_channel=True)
        moved[ctx.author] = ctx.author.voice.channel
        await ctx.author.move_to(chan)
        for i in range(len(list_mem)):
            moved[list_mem[i]] = list_mem[i].voice.channel
            await chan.set_permissions(list_mem[i], connect=True, view_channel=True)
            await list_mem[i].move_to(chan)
        await chan.set_permissions(ctx.guild.default_role, connect=False, view_channel=False)
    else:
        await ctx.send("Вы и так отдельно сидите")


@bot.command()
async def mbw(ctx):
    try:
        aut = moved[ctx.author]
    except BaseException:
        ctx.send("Author dosent moved")
        raise KeyError("Author dosent moved")
    chan = ctx.author.voice.channel
    mems = ctx.author.voice.channel.members
    for i in range(len(mems)):
        try:
            await mems[i].move_to(moved[mems[i]])
            moved.pop(mems[i])
        except:
            pass
    await chan.delete()


@bot.command()
async def get_monster(ctx: discord.ext.commands.Context, name):
    card = Monser_Card(name)
    mons_data: str = card.get_monster()
    if len(mons_data) > 2000:
        while '\n\n' in mons_data:
            try:
                await ctx.send(mons_data[:mons_data.find("\n\n")])
            except BaseException:
                a = mons_data[:mons_data.find("\n\n")]
                n = len(a) // 2000 + 1
                for i in range(n):
                    await ctx.send(a[(i * 2000):min((i + 1) * 2000, len(a))])

            mons_data = mons_data[mons_data.find("\n\n") + 2:]


@bot.command()
async def dnd_start(ctx: discord.ext.commands.Context):
    if not discord.utils.get(ctx.guild.categories, name="DnD"):
        cat = await ctx.guild.create_category("DnD")
    else:
        cat = discord.utils.get(ctx.guild.categories, name="DnD")
    chan: discord.VoiceChannel = await ctx.guild.create_voice_channel("DnD(temp)", category=cat)
    ids["DnD"] = chan.id
    fight_but = Button(label="Битва")
    bigin_but = Button(label="Начинаем")
    emb = discord.Embed()
    emb.add_field(name="check", value=1)
    butman = View()

    async def beginCallback(interaction: discord.Interaction):
        await interaction.response.send_message("Игра начинается", embed=emb)

        async def createdmchan(interaction: discord.Interaction):
            gmrole = await interaction.guild.create_role(name="Dungeon Master")
            plrole = await interaction.guild.create_role(name="Players")
            ids["Dungeon Master"] = gmrole.id
            ids["Players"] = plrole.id
            dmchan = await interaction.guild.create_text_channel(name="botlog", category=cat)
            ids["botlog"] = dmchan.id
            await dmchan.set_permissions(interaction.guild.default_role, view_channel=False)
            await dmchan.set_permissions(gmrole, view_channel=True)

        await createdmchan(interaction)

        async def fightCallback(interaction: discord.Interaction):
            await interaction.response.send_message("Да начнётся битва", embed=emb)

        fight_but.callback = fightCallback
        butman.remove_item(bigin_but)
        butman.add_item(fight_but)
        await ctx.send("test", view=butman)

    bigin_but.callback = beginCallback
    butman.add_item(bigin_but)
    await ctx.send("", view=butman)


@bot.command()
async def dnd_stop(ctx: discord.ext.commands.Context):
    if discord.utils.get(ctx.guild.channels, name="DnD"):
        await discord.utils.get(ctx.guild.channels, name="DnD(temp)").delete()
        await discord.utils.get(ctx.guild.channels, name="botlog").delete()
        await discord.utils.get(ctx.guild.roles, name="Dungeon Master").delete()
        await discord.utils.get(ctx.guild.roles, name="Players").delete()


bot.run(TOKEN)
