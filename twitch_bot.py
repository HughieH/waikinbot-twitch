import os
import twitchio
from twitchio.ext import commands
from twitchio.ext import routines
import SessionStats_class
import Player_class
import datetime

class waikinBot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token = os.getenv("TWITCH_TOKEN"), prefix='!', initial_channels=['Waikin_'])
        
        self.eventMessage: str 
        self.overallSession: dict
        self.session: SessionStats_class.SessionStatsTracker
        self.initialPlayer: Player_class.Player # initializing as an instance variable as I want routine to continuosly update it for reference when finding latest battle
        

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    # announce that bot has arrived
    async def event_channel_joined(self, channel: twitchio.Channel):
        await channel.send("/me HAS ARRIVED!")

    # collects all message content
    async def event_message(self, message):
        if message.echo:
            return
        print(message.content)
        self.eventMessage = message.content
        await self.handle_commands(message)
        
    """
    @commands.command(name="bestgame")
    async def bestGame(self, ctx: commands.Context):
        try:
            await ctx.send(self.session.bestGameOnCurrentDate())
        except AttributeError:
            await ctx.send("Session has not started yet!")
    """

    @commands.command(name="hello")
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')

    @routines.routine(seconds = 10.0)
    async def routine(self, ctx: commands.Context):

        player_now = Player_class.Player(self.session.server, self.session.user_name)
        player_now.fetchStats()
        tank_id = self.session.diffInBattles(self.initialPlayer, player_now)
            
        if tank_id:                 
            print(f"NEW battles found at {datetime.datetime.now()}")
            print(f"Tank ID with new battle is {tank_id}")
            inital_tank = self.initialPlayer.individualTank(tank_id)
            tank_now = player_now.individualTank(tank_id)
            self.session.battleStats(tank_id, inital_tank, tank_now)
            
            print(self.session.lastBattle)
            await ctx.send(self.session.lastBattle)
            print(self.session.compareQBMsg)
            await ctx.send(self.session.compareQBMsg)
            print(self.session.overallTwitchCompareScore())
            await ctx.send(self.session.overallTwitchCompareScore())

        else:
            print(f"No new battles found at {datetime.datetime.now()}\n")
            # await ctx.send("New game not found COPIUM")            

        self.initialPlayer = player_now # update latest player to initial for comparison in the next routine cycle

    @commands.command(name="stop")
    async def stopSession(self, ctx: commands.Context):
        
        self.routine.stop()
        await ctx.send("Session has been ended!")
        await ctx.send(self.session.overallTwitchCompareScore())
        print("Session has been ended!")
        
    
    @commands.command(name="start")
    async def startSession(self, ctx: commands.Context):
        
        print(f"Session stats initialized at {datetime.datetime.now()}\n")
        await ctx.send(f"Session stats initialized at {datetime.datetime.now()}\n")
        
        self.session = SessionStats_class.SessionStatsTracker("na", "waikin_reppinKL")
        self.initialPlayer = Player_class.Player(self.session.server, self.session.user_name)
        self.initialPlayer.fetchStats()
        
        self.routine.start(ctx)

bot = waikinBot()
bot.run()

