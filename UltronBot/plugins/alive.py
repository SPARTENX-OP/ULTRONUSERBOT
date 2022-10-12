import datetime
import random
import time

from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

from UltronBot.sql.gvar_sql import gvarstat
from . import *

#-------------------------------------------------------------------------------

ALIVE_TEMP = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━┓
┣<b><i>🔥🔥ԱӀէɾօղβօէ įʂ ටղƑìɾҽ🔥🔥</b></i>
┣<i><b>--ԱӀէɾօղ Աʂҽɾ--</i></b> : 『 <a href='tg://user?id={}'>{}</a> 』
┗━━━━━━━━━━━━━━━━━━━━━━━━━┛
╔════✣✤༻⋇༺✤✣════╗
┣─ <b>♦️ ͲҽӀҽէհօղ ┣</b> <i>{}</i>
┣─ <b>♦️ ԱӀէɾօղβօէ ┣</b> <i>{}</i>
┣─ <b>♦️ ʂմժօ ┣</b> <i>{}</i>
┣─ <b>♦️βօէ Աքէìʍҽ ┣</b> <i>{}</i>
┣─ <b>♦️βօէ φìղց ┣</b> <i>{}</i>
╚════✣✤༻⋇༺✤✣════╝
╔══════════✣✤༻⋇༺✤✣════════╗
┣<b><i>. <a href='https://t.me/LegendHacker_IIN'>[🅻🅴🅶🅴🅽🅳🅷🅰🅲🅺🅴🆁]</a> .</i></b>
┣<b><i>. <a href='https://t.me/LegendHacker_IIN'>[🆃🅷🅰🅽🅾🆂🅱🅾🆈]</a> .</i></b>
╚══════════✣✤༻⋇༺✤✣════════╝
┏━━━━━(φօաҽɾƑմӀӀ=ԱӀէɾօղβօէ)━━━━━┓
┣─<b><i>💥💥💥 <a href='https://t.me/UltronBot_XD'>[♦️ටղƑìɾҽ-ԱӀէɾօղβօէ♦️]</a> 💥💥💥</i></b>
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""

msg = """{}\n
<b><i>🏅 𝙱𝚘𝚝 𝚂𝚝𝚊𝚝𝚞𝚜 🏅</b></i>
<b>Telethon ≈</b>  <i>{}</i>
<b>Ultronẞø† ≈</b>  <i>{}</i>
<b>Uptime ≈</b>  <i>{}</i>
<b>Abuse ≈</b>  <i>{}</i>
<b>Sudo ≈</b>  <i>{}</i>
"""
#-------------------------------------------------------------------------------

@hell_cmd(pattern="alive$")
async def up(event):
    cid = await client_id(event)
    ForGo10God, HELL_USER, hell_mention = cid[0], cid[1], cid[2]
    start = datetime.datetime.now()
    hell = await eor(event, "`ԱӀէɾօղβօէ įʂ ටղƑìɾҽ....`")
    uptime = await get_time((time.time() - StartTime))
    a = gvarstat("ALIVE_PIC")
    pic_list = []
    if a:
        b = a.split(" ")
        if len(b) >= 1:
            for c in b:
                pic_list.append(c)
        PIC = random.choice(pic_list)
    else:
        PIC = "https://telegra.ph/file/eaad0c60c09f04bdb2024.jpg"
    end = datetime.datetime.now()
    ling = (end - start).microseconds / 1000
    omk = ALIVE_TEMP.format(ForGo10God, HELL_USER, tel_ver, hell_ver, is_sudo, uptime, ling)
    await event.client.send_file(event.chat_id, file=PIC, caption=omk, parse_mode="HTML")
    await hell.delete()



@hell_cmd(pattern="ultron$")
async def hell_a(event):
    cid = await client_id(event)
    ForGo10God, HELL_USER, hell_mention = cid[0], cid[1], cid[2]
    uptime = await get_time((time.time() - StartTime))
    am = gvarstat("ALIVE_MSG") or "<b>🔥🔥ԱӀէɾօղβօէ įʂ ටղƑìɾҽ🔥🔥</b>"
    try:
        hell = await event.client.inline_query(Config.BOT_USERNAME, "alive")
        await hell[0].click(event.chat_id)
        if event.sender_id == ForGo10God:
            await event.delete()
    except (noin, dedbot):
        await eor(event, msg.format(am, tel_ver, hell_ver, uptime, abuse_m, is_sudo), parse_mode="HTML")


CmdHelp("alive").add_command(
  "alive", None, "Shows the Default Alive Message"
).add_command(
  "ultron", None, "Shows Inline Alive Menu with more details."
).add_warning(
  "✅ Harmless Module"
).add()
