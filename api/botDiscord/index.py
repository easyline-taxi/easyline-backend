from discord.ext import commands
from cogwatch import Watcher
import threading
from pathlib import Path
import os 

"""
['__abstractmethods__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', 
'__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', 
'__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__', '__str__', 
'__subclasshook__', '__weakref__', '_abc_impl', '_get_channel', '_state', 'args', 'author', 'bot', 'channel', 'cog', 
'command', 'command_failed', 'fetch_message', 'guild', 'history', 'invoke', 'invoked_parents', 'invoked_subcommand', 
'invoked_with', 'kwargs', 'me', 'message', 'pins', 'prefix', 'reinvoke', 'reply', 'send', 'send_help', 'subcommand_passed',
 'trigger_typing', 'typing', 'valid', 'view', 'voice_client']
"""

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print("Os portões de HellHeim estão se Abrindo!!")
    
    watcher = Watcher(client, path='api/botDiscord/commands', preload=True)
    await watcher.start()
try:
    x = threading.Thread(target=client.run, args=("ODE4NDc2MjIxMjgwODEzMDg2.YEYnYQ.IRGH9F0DU4iIWOT7r9DdwZhzJnk",))
    x.start()
except Exception as ex:
    print(ex)
    



