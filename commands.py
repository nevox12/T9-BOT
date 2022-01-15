from logging import exception
from time import sleep

from discord import Game, Embed, Role, Colour, Member
from discord.utils import get
from discord.ext.commands import Cog, command, has_permissions, MissingPermissions

from numexpr import evaluate
from discord.ext import commands
import requests
import datetime
perfix = "T9$"
bypass_id = [752847699535069184]
class Commands(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "✅"]
        self.roles = None
        self.channel_id = 919552512879644684

    def check_if_roles_are_built(self):
        if self.roles is None:
            roles = self.bot.guilds[0].roles
            self.roles = [
                get(roles, name="Back-End"),
                get(roles, name="Front-End"),
                get(roles, name="C++"),
                get(roles, name="Java"),
                get(roles, name="C"),
                get(roles, name="js"),
                get(roles, name="Python"),
                get(roles, name="Flutter"),
                get(roles, name="Helper")
            ]

    @Cog.listener()
    async def on_ready(self):
        print("Logged in as {} (ID: {})!".format(self.bot.user.name, self.bot.user.id))
        await self.bot.change_presence(activity=Game(name=perfix +"help"))

    def convert(self,seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d hour(s), %02d minute(s) and %02d second(s)" % (hour, minutes, seconds)

    @command(name="gen-mine",brief='Generate Minecraft account.',
                 description='Use this command to generate Minecraft account and send to your DM.')
    @commands.cooldown(1, 60 * 60 * 12, commands.BucketType.user)
    async def gen_mine(self,ctx):
        id = ctx.author.id
        member = self.bot.get_user(id)
        try:
            channel = await member.create_dm()

            url = requests.get("https://gen.teamic.me/api/generate.php?type=Minecraft")
            data_get = url.text

            account = data_get.split(":")
            email = account[0]
            password = account[1]

            embed = Embed(
                title='Generated Account',
                description=f'Email: {email}\nPassword: {password}',
                timestamp=datetime.datetime.utcnow(),
                colour=Colour.blue()
            )

            send = Embed(
                title='Done',
                description='I have send you an account in DM.',
                timestamp=datetime.datetime.utcnow(),
                colour=Colour.blue()
            )

            await channel.send(embed=embed)
            await ctx.send(embed=send)

            if ctx.author.id in bypass_id:
                self.gen_mine.reset_cooldown(ctx)

        except:
            embed = Embed(
                title='Error',
                description='uhh! Enable DM so I can send you!',
                timestamp=datetime.datetime.utcnow(),
                colour=Colour.red()
            )
            await ctx.send(embed=embed)
            self.gen_mine.reset_cooldown(ctx)

    @gen_mine.error
    async def gen_mine_error(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            time_left = int(error.retry_after)
            embed = Embed(
                title=f":warning: Error!",
                description=f"You need to wait for {self.convert(time_left)} to continue use this command!",
                color=Colour.red()
            )
            await ctx.send(embed=embed)

    @command(name='say')
    async def say(self, ctx, *args):
        args = " ".join(args)
        await ctx.send(args)

    @command(name="help")
    async def help(self, ctx):
        embed = Embed(title="Help",description=""":regional_indicator_t: :nine:     :regional_indicator_b: :regional_indicator_o: :regional_indicator_t:
:regional_indicator_i: :regional_indicator_s:     :regional_indicator_t: :regional_indicator_h: :regional_indicator_e:     :regional_indicator_b: :regional_indicator_e: :regional_indicator_s: :regional_indicator_t:""")
        embed.add_field(name='{}ping'.format(perfix), value="Show ping:signal_strength::globe_with_meridians:", inline=True)
        embed.add_field(name='{}say'.format(perfix),value="say any message", inline=True)
        embed.add_field(name='{}calc'.format(perfix),value="Calculator", inline=True)
        # embed.set_author(name=ctx.message.author, url=ctx.message.show_avatar)
        await ctx.reply(embed=embed,mention_author=False)

    @command(name='calc')
    async def calculator(self, ctx, *args):
        try:
            arg = evaluate("".join(args))
            embed_calc = Embed(title=f"{args} = ",
                               description="{}".format(arg),
                               color=Colour.dark_grey())
            embed_calc.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed_calc, mention_author=False)

        except KeyError:
            await ctx.reply("Error: Invalid", mention_author=False)

        except TypeError:
            await ctx.reply("Error: Invalid", mention_author=False)

        except SyntaxError:
            await ctx.reply("Error: Invalid", mention_author=False)

        except Exception as E:
            await ctx.reply("Error: Invalid", mention_author=False)
            exception(E)

    @command(name='clear')
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, arg: int = None):
        if arg is None:
            await ctx.channel.purge(limit=10000000000000)
        else:
            arg = int(arg)
            await ctx.channel.purge(limit=arg)
        sleep(0.2)
        await ctx.send("Done!", delete_after=2)

    @command(name="role")
    @has_permissions(manage_roles=True)
    async def role(self, ctx, user: Member, role: Role):
        if role in user.roles:
            await user.remove_roles(role)
            await ctx.reply(f"Removed {role} from {user.mention}", mention_author=False)
        else:
            await user.add_roles(role)
            await ctx.reply(f"Added {role} to {user.mention}", mention_author=False)

    @role.error
    async def role_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.reply(text, mention_author=False)

    @command(name="m_role")
    @has_permissions(manage_roles=True)
    async def give_role_to_role_members(self, ctx, *args):
        server = ctx.guild
        try:
            role_1 = get(server.roles, id=int(''.join(args[0])[3:-1]))
            role_2 = get(server.roles, id=int(''.join(args[1])[3:-1]))
        except ValueError:
            await ctx.reply("one of the roles doesn't exist", mention_author=False)
            return None

        if None in {role_1, role_2}:
            await ctx.reply("one of the roles doesn't exist", mention_author=False)
            return None

        for member in role_1.members:
            await member.add_roles(role_2)
        await ctx.reply("Done!", mention_author=False)

    @command(name="avatar")
    async def avatar(self, ctx, member: Member = None):
        avatar_url = ctx.author.avatar_url if member is None else member.avatar_url

        embed_avatar = Embed(title="Avatar Url", url=avatar_url, color=Colour.dark_grey())
        embed_avatar.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed_avatar.set_image(url=avatar_url)

        await ctx.reply(embed=embed_avatar, mention_author=False)

    @command(name="remove_all")
    @has_permissions(manage_roles=True)
    async def remove_all_roles_from_member_with_all_roles(self, ctx):
        self.check_if_roles_are_built()
        for member in ctx.guild.members:
            print(f"looking throw {member.name}'s account")
            if set(self.roles).issubset(set(member.roles)):
                print("Found!")
                for role in member.roles:
                    if role in self.roles:
                        print(f"Deleted {role}")
                        await member.remove_roles(role)

    @command(name='generate_auto_role_message', help='Generates auto roles message')
    @has_permissions(manage_roles=True)
    async def generate_verification(self, ctx):
        embed = Embed(title="Click reaction",
                      description="1️⃣ to take Back-End role\n 2️⃣ to take Front-End role\n 3️⃣ to take C++ "
                                  "role\n 4️⃣ to take Java role\n 5️⃣ to take C role\n 6️⃣ to take js role\n 7️⃣ "
                                  "to take Python role\n 8️⃣ to take Flutter role\n 9️⃣ to take Helper role\n✅ "
                                  "Delete all roles\n")
        message = await ctx.send(embed=embed)

        for emoji in self.emojis:
            await message.add_reaction(emoji)

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id != self.channel_id:
            return None
        elif payload.member.bot:
            return None

        self.check_if_roles_are_built()
        emoji = payload.emoji

        if emoji.name == "1️⃣":
            await payload.member.add_roles(self.roles[0], reason="clicked on emoji", atomic=True)

        elif emoji.name == "2️⃣":
            await payload.member.add_roles(self.roles[1], reason="clicked on emoji", atomic=True)

        elif emoji.name == "3️⃣":
            await payload.member.add_roles(self.roles[2], reason="clicked on emoji", atomic=True)

        elif emoji.name == "4️⃣":
            await payload.member.add_roles(self.roles[3], reason="clicked on emoji", atomic=True)

        elif emoji.name == "5️⃣":
            await payload.member.add_roles(self.roles[4], reason="clicked on emoji", atomic=True)

        elif emoji.name == "6️⃣":
            await payload.member.add_roles(self.roles[5], reason="clicked on emoji", atomic=True)

        elif emoji.name == "7️⃣":
            await payload.member.add_roles(self.roles[6], reason="clicked on emoji", atomic=True)

        elif emoji.name == "8️⃣":
            await payload.member.add_roles(self.roles[7], reason="clicked on emoji", atomic=True)

        elif emoji.name == "9️⃣":
            await payload.member.add_roles(self.roles[8], reason="clicked on emoji", atomic=True)

        elif emoji.name == "✅":
            for role in self.roles:
                if role in payload.member.roles:
                    await payload.member.remove_roles(role, reason="clicked on emoji", atomic=True)

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.channel_id != self.channel_id:
            return None

        self.check_if_roles_are_built()
        emoji = payload.emoji
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if emoji.name == "1️⃣":
            await member.remove_roles(self.roles[0], reason="clicked on emoji", atomic=True)

        elif emoji.name == "2️⃣":
            await member.remove_roles(self.roles[1], reason="clicked on emoji", atomic=True)

        elif emoji.name == "3️⃣":
            await member.remove_roles(self.roles[2], reason="clicked on emoji", atomic=True)

        elif emoji.name == "4️⃣":
            await member.remove_roles(self.roles[3], reason="clicked on emoji", atomic=True)

        elif emoji.name == "5️⃣":
            await member.remove_roles(self.roles[4], reason="clicked on emoji", atomic=True)

        elif emoji.name == "6️⃣":
            await member.remove_roles(self.roles[5], reason="clicked on emoji", atomic=True)

        elif emoji.name == "7️⃣":
            await member.remove_roles(self.roles[6], reason="clicked on emoji", atomic=True)

        elif emoji.name == "8️⃣":
            await member.remove_roles(self.roles[7], reason="clicked on emoji", atomic=True)

        elif emoji.name == "9️⃣":
            await member.remove_roles(self.roles[8], reason="clicked on emoji", atomic=True)
    
    @command(name='ping', help='Shows Ping(ms)')
    async def ping(self, ctx):
        ping = f'{round (self.bot.latency * 1000)} ms :signal_strength::globe_with_meridians: '
        embed = Embed(title="Pong!",
                      description=ping)
        await ctx.reply(embed=embed,mention_author=False)
