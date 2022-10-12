import asyncio
import html
import os
import re
import random
import sys

from math import ceil
from re import compile

from telethon import Button, custom, events, functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.events import InlineQuery, callbackquery
from telethon.sync import custom
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

from UltronBot.sql.gvar_sql import gvarstat
from . import *

hell_row = Config.BUTTONS_IN_HELP
hell_emoji = Config.EMOJI_IN_HELP
PM_WARNS = {}
PREV_REPLY_MESSAGE = {}

mybot = Config.BOT_USERNAME
if mybot.startswith("@"):
    botname = mybot
else:
    botname = f"@{mybot}"
LOG_GP = Config.LOGGER_ID
USER_BOT_WARN_ZERO = "𝔼𝕟𝕠𝕦𝕘𝕙 𝕆𝕗 𝕐𝕠𝕦𝕣 𝔽𝕝𝕠𝕠𝕕𝕚𝕟𝕘 𝕀𝕟 𝕄𝕪 𝕄𝕒𝕤𝕥𝕖𝕣'𝕤 𝕌𝕃𝕋ℝ𝕆ℕℙ𝕄!! \n\n**🚫 𝔹𝕝𝕠𝕔𝕜𝕖𝕕 𝕒𝕟𝕕 ℝ𝕖𝕡𝕠𝕣𝕥𝕖𝕕.**"

alive_txt = """{}\n
<b><i>🏅 𝙱𝚘𝚝 𝚂𝚝𝚊𝚝𝚞𝚜 🏅</b></i>
<b>Telethon ≈</b>  <i>{}</i>
<b>Ultronẞø† ≈</b>  <i>{}</i>
<b>Uptime ≈</b>  <i>{}</i>
<b>Abuse ≈</b>  <i>{}</i>
<b>Sudo ≈</b>  <i>{}</i>
"""

def button(page, modules):
    Row = hell_row
    Column = 3

    modules = sorted([modul for modul in modules if not modul.startswith("_")])
    pairs = list(map(list, zip(modules[::2], modules[1::2])))
    if len(modules) % 2 == 1:
        pairs.append([modules[-1]])
    max_pages = ceil(len(pairs) / Row)
    pairs = [pairs[i : i + Row] for i in range(0, len(pairs), Row)]
    buttons = []
    for pairs in pairs[page]:
        buttons.append(
            [
                custom.Button.inline(f"{hell_emoji} " + pair + f" {hell_emoji}", data=f"Information[{page}]({pair})")
                for pair in pairs
            ]
        )

    buttons.append(
        [
            custom.Button.inline(
               f"💥𝔹𝕒𝕔𝕜 {hell_emoji}", data=f"page({(max_pages - 1) if page == 0 else (page - 1)})"
            ),
            custom.Button.inline(
               f"• ❌ •", data="close"
            ),
            custom.Button.inline(
               f"{hell_emoji} ղҽ×է💥", data=f"page({0 if page == (max_pages - 1) else page + 1})"
            ),
        ]
    )
    return [max_pages, buttons]


    modules = CMD_HELP
if Config.BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(InlineQuery)
    async def inline_handler(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        builder = event.builder
        result = None
        query = event.text
        auth = await clients_list()
        if event.query.user_id in auth and query == "UltronBot_help":
            rev_text = query[::-1]
            veriler = button(0, sorted(CMD_HELP))
            apn = []
            for x in CMD_LIST.values():
                for y in x:
                    apn.append(y)
            a = gvarstat("HELP_PIC")
            if a:
                help_pic = a.split(" ")[0]
            else:
                help_pic = "https://telegra.ph/file/193fd25d076d8fa882c58.jpg"
                
                help_msg = f"💥💥 **{hell_mention}**\n\n💥💥ԱӀէɾօղ-φӀմցìղʂ : `{len(CMD_HELP)}` \n💥💥ԱӀէɾօղ-↻ʍժʂ: `{len(apn)}`\n💥💥ԱӀէɾօղ-φąցҽʂ: 1/{veriler[0]}"
                
                #help_msg = f"╔═══💫✨💫═══\n"
                #help_msg = f"┃**{hell_mention}**\n"
                #help_msg = f"╚═══💫✨💫═══\n"
                #help_msg = f"╔══════✣✤༻⋇༺✤✣══════╗\n"
                #help_msg = f"┣💥ԱӀէɾօղ-φӀմցìղʂ: `{len(CMD_HELP)}` \n"
                #help_msg = f"┣💥ԱӀէɾօղ-↻ʍժʂ: `{len(apn)}`\n"
                #help_msg = f"┣💥ԱӀէɾօղ-φąցҽʂ : 1/{veriler[0]}`\n"
                #help_msg = f"╚══════✣✤༻⋇༺✤✣══════╝\n"""
                
            if help_pic == "DISABLE":
                result = builder.article(
                    f"Hey! Only use {hl}help please",
                    text=help_msg,
                    buttons=veriler[1],
                    link_preview=False,
                )
            elif help_pic.endswith((".jpg", ".png")):
                result = builder.photo(
                    help_pic,
                    text=help_msg,
                    buttons=veriler[1],
                    link_preview=False,
                )
            elif help_pic:
                result = builder.document(
                    help_pic,
                    text=help_msg,
                    title="UltronBot Alive",
                    buttons=veriler[1],
                    link_preview=False,
                )
        elif event.query.user_id in auth and query == "alive":
            uptime = await get_time((time.time() - StartTime))
            alv_msg = gvarstat("ALIVE_MSG") or "»»» <b>ԱӀէɾօղβօէ įʂ ටղƑìɾҽ</b> «««"
            he_ll = alive_txt.format(alv_msg, tel_ver, hell_ver, uptime, abuse_m, is_sudo)
            alv_btn = [
                [Button.url(f"{HELL_USER}", f"tg://openmessage?user_id={ForGo10God}")],
                [Button.url("My Channel", f"https://t.me/{my_channel}"), 
                Button.url("My Group", f"https://t.me/{my_group}")],
            ]
            a = gvarstat("ALIVE_PIC")
            pic_list = []
            if a:
                b = a.split(" ")
                if len(b) >= 1:
                    for c in b:
                        pic_list.append(c)
                PIC = random.choice(pic_list)
            else:
                PIC = "https://telegra.ph/file/193fd25d076d8fa882c58.jpg4"
            if PIC and PIC.endswith((".jpg", ".png")):
                result = builder.photo(
                    PIC,
                    text=he_ll,
                    buttons=alv_btn,
                    link_preview=False,
                    parse_mode="HTML",
                )
            elif PIC:
                result = builder.document(
                    PIC,
                    text=he_ll,
                    title="UltronBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                    parse_mode="HTML",
                )
            else:
                result = builder.article(
                    text=he_ll,
                    title="UltronBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                    parse_mode="HTML",
                )

        elif event.query.user_id in auth and query == "pm_warn":
            CSTM_PMP = gvarstat("CUSTOM_PMPERMIT") or "**𝕐𝕠𝕦 ℍ𝕒𝕧𝕖 𝕋𝕣𝕖𝕤𝕡𝕒𝕤𝕤𝕖𝕕 𝕋𝕠 𝕄𝕪 𝕄𝕒𝕤𝕥𝕖𝕣'𝕤 𝕌𝕝𝕥𝕣𝕠𝕟 ℙ𝕄.!\n𝕋𝕙𝕚𝕤 𝕀𝕤 𝕀𝕝𝕝𝕖𝕘𝕒𝕝 𝔸𝕟𝕕 ℝ𝕖𝕘𝕒𝕣𝕕𝕖𝕕 𝔸𝕤 ℂ𝕣𝕚𝕞𝕖.**"
            HELL_FIRST = "**🔥 ԱӀէɾօղβօէ ℙ𝕣𝕚𝕧𝕒𝕥𝕖 𝕌𝕝𝕥𝕣𝕠𝕟 ℂ𝕪𝕓𝕖𝕣 𝕊𝕖𝕔𝕦𝕣𝕚𝕥𝕪 ℙ𝕣𝕠𝕥𝕠𝕔𝕠𝕝 🔥**\n\ђєɭɭ๏!! 𝕎𝕖𝕝𝕔𝕠𝕞𝕖 𝕋𝕠 {}'𝕤 𝕌𝕝𝕥𝕣𝕠𝕟 ℙ𝕄. 𝕋𝕙𝕚𝕤 𝕚𝕤 𝕒𝕟 𝕒𝕦𝕥𝕠𝕞𝕒𝕥𝕖𝕕 𝕞𝕖𝕤𝕤𝕒𝕘𝕖.\n\n{}".format(hell_mention, CSTM_PMP)
            a = gvarstat("PMPERMIT_PIC")
            pic_list = []
            if a:
                b = a.split(" ")
                if len(b) >= 1:
                    for c in b:
                        pic_list.append(c)
                PIC = random.choice(pic_list)
            else:
                PIC = "https://telegra.ph/file/193fd25d076d8fa882c58.jpg"
            if PIC and PIC.endswith((".jpg", ".png")):
                result = builder.photo(
                    file=PIC,
                    text=HELL_FIRST,
                    buttons=[
                        [custom.Button.inline("📝 Request Approval", data="req")],
                        [custom.Button.inline("🚫 Block", data="heheboi")],
                        [custom.Button.inline("❓ Curious", data="pmclick")],
                    ],
                    link_preview=False,
                )
            elif PIC:
                result = builder.document(
                    file=PIC,
                    text=HELL_FIRST,
                    title="𝕌𝕝𝕥𝕣𝕠𝕟𝔹𝕠𝕥 ℙ𝕄 ℙ𝕖𝕣𝕞𝕚𝕥.",
                    buttons=[
                        [custom.Button.inline("📝 𝕌𝕝𝕥𝕣𝕠𝕟 ℝ𝕖𝕢𝕦𝕖𝕤𝕥 𝔸𝕡𝕡𝕣𝕠𝕧𝕒𝕝", data="req")],
                        [custom.Button.inline("🚫 𝔹𝕝𝕠𝕔𝕜", data="heheboi")],
                        [custom.Button.inline("❓ ℂ𝕦𝕣𝕚𝕠𝕦𝕤.", data="pmclick")],
                    ],
                    link_preview=False,
                )
            else:
                result = builder.article(
                    text=HELL_FIRST,
                    title="𝕌𝕝𝕥𝕣𝕠𝕟𝔹𝕠𝕥 ℙ𝕄 ℙ𝕖𝕣𝕞𝕚𝕥.",
                    buttons=[
                        [custom.Button.inline("📝 𝕌𝕝𝕥𝕣𝕠𝕟 ℝ𝕖𝕢𝕦𝕖𝕤𝕥 𝔸𝕡𝕡𝕣𝕠𝕧𝕒𝕝", data="req")],
                        [custom.Button.inline("🚫 𝔹𝕝𝕠𝕔𝕜", data="heheboi")],
                        [custom.Button.inline("❓ ℂ𝕦𝕣𝕚𝕠𝕦𝕤.", data="pmclick")],
                    ],
                    link_preview=False,
                )
                
        elif event.query.user_id in auth and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"**⚡ Ꝉҽցҽղժąɾվ ȺƑ ԱӀէɾօղβօէ⚡**",
                buttons=[
                    [Button.url("💥 ԱӀէɾօղ ɾҽքօʂ 💥", "https://github.com/LEGENDXTHANOS/ULTRONBOT")],
                    [Button.url("💥ԱӀէɾօղβօէ ហҽէաօɾҟ💥", "https://t.me/UltronBot_OP")],
                ],
            )

        elif query.startswith("http"):
            part = query.split(" ")
            result = builder.article(
                "File uploaded",
                text=f"**File uploaded successfully to {part[2]} site.\n\nUpload Time : {part[1][:3]} second\n[‏‏‎ ‎]({part[0]})",
                buttons=[[custom.Button.url("URL", part[0])]],
                link_preview=True,
            )

        else:
            result = builder.article(
                "@UltronBot_XD",
                text="""**ℍ𝕖𝕪! 𝕋𝕙𝕚𝕤 𝕀𝕤 [ԱӀէɾօղβօէ](https://t.me/UltronBot_XD) \n𝕐𝕠𝕦 𝕔𝕒𝕟 𝕜𝕟𝕠𝕨 𝕞𝕠𝕣𝕖 𝕒𝕓𝕠𝕦𝕥 𝕞𝕖 𝕗𝕣𝕠𝕞 𝕥𝕙𝕖 𝕝𝕚𝕟𝕜𝕤 𝕘𝕚𝕧𝕖𝕟 𝕓𝕖𝕝𝕠𝕨 👇**""",
                buttons=[
                    [
                        custom.Button.url("🔥 ԱӀէɾօղ ↻հąղղҽӀ 🔥", "https://t.me/UltronBot_OP"),
                        custom.Button.url("⚡ ԱӀէɾօղ Ɠɾօմք ⚡", "https://t.me/UltronBot_XD"),
                    ],
                    [
                        custom.Button.url("✨ ԱӀէɾօղ ɾҽքօʂ ✨", "https://github.com/LEGENDXTHANOS/ULTRONBOT"),
                        custom.Button.url("🔰 ԱӀէɾօղ ɾҽքӀʂ 🔰", "https://replit.com/@LEGEND-LX/PYTHONBOT-4"),
                    ],
                ],
                link_preview=False,
            )
        await event.answer([result] if result else None)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"pmclick")))
    async def on_pm_click(event):
        auth = await clients_list()
        if event.query.user_id in auth:
            reply_pop_up_alert = "This is for Other Users..."
        else:
            reply_pop_up_alert = "🔰 𝕋𝕙𝕚𝕤 𝕚𝕤 𝕌𝕝𝕥𝕣𝕠𝕟𝔹𝕠𝕥 ℙ𝕄 𝕊𝕖𝕔𝕦𝕣𝕚𝕥𝕪 𝕥𝕠 𝕜𝕖𝕖𝕡 𝕒𝕨𝕒𝕪 𝕦𝕟𝕨𝕒𝕟𝕥𝕖𝕕 𝕣𝕖𝕥𝕒𝕣𝕕𝕤 𝕗𝕣𝕠𝕞 𝕤𝕡𝕒𝕞𝕞𝕚𝕟𝕘 ℙ𝕄 !!"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"req")))
    async def on_pm_click(event):
        auth = await clients_list()
        if event.query.user_id in auth:
            reply_pop_up_alert = "𝕋𝕙𝕚𝕤 𝕚𝕤 𝕗𝕠𝕣 𝕠𝕥𝕙𝕖𝕣 𝕦𝕤𝕖𝕣𝕤!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit("✅ **ℝ𝕖𝕢𝕦𝕖𝕤𝕥 ℝ𝕖𝕘𝕚𝕤𝕥𝕖𝕣𝕖** \n\n𝕄𝕪 𝕞𝕒𝕤𝕥𝕖𝕣 𝕨𝕚𝕝𝕝 𝕟𝕠𝕨 𝕕𝕖𝕔𝕚𝕕𝕖 𝕥𝕠 𝕝𝕠𝕠𝕜 𝕗𝕠𝕣 𝕪𝕠𝕦𝕣 𝕣𝕖𝕢𝕦𝕖𝕤𝕥 𝕠𝕣 𝕟𝕠𝕥.\n😐 𝕋𝕚𝕝𝕝 𝕥𝕙𝕖𝕟 𝕨𝕒𝕚𝕥 𝕡𝕒𝕥𝕚𝕖𝕟𝕥𝕝𝕪 𝕒𝕟𝕕 𝕕𝕠𝕟'𝕥 𝕤𝕡𝕒𝕞!!")
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            await tbot.send_message(LOG_GP, f"#ULTRON_REQUEST \n\n⚜️ 𝕐𝕠𝕦 𝕘𝕠𝕥 𝕒 𝕌𝕃𝕋ℝ𝕆ℕ 𝕣𝕖𝕢𝕦𝕖𝕤𝕥 𝕗𝕣𝕠𝕞 [{first_name}](tg://user?id={event.query.user_id}) !")


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"heheboi")))
    async def on_pm_click(event):
        auth = await clients_list()
        if event.query.user_id in auth:
            reply_pop_up_alert = "𝕋𝕙𝕚𝕤 𝕚𝕤 𝕗𝕠𝕣 𝕠𝕥𝕙𝕖𝕣 𝕦𝕤𝕖𝕣𝕤!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(f"𝔸𝕊 𝕐𝕠𝕦 𝕎𝕚𝕤𝕙. **βꝈට↻ҠƐᎠ !!**")
            await H1(functions.contacts.BlockRequest(event.query.user_id))
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            await tbot.send_message(LOG_GP, f"#BETA_CHOD_GYA_TUTO_BLOCK \n\n**βꝈට↻ҠƐᎠ** [{first_name}](tg://user?id={event.query.user_id}) \nℝ𝕖𝕒𝕤𝕠𝕟:- 𝕌𝕝𝕥𝕣𝕠𝕟 ℙ𝕄 𝕊𝕖𝕝𝕗 𝔹𝕝𝕠𝕔𝕜")


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"reopen")))
    async def reopn(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        if event.query.user_id in auth:
            current_page_number=0
            simp = button(current_page_number, CMD_HELP)
            veriler = button(0, sorted(CMD_HELP))
            apn = []
            for x in CMD_LIST.values():
                for y in x:
                    apn.append(y)
            await event.edit(
                         f"💥💥 **{hell_mention}**\n\n💥💥 ԱӀէɾօղ-φӀմցìղʂ𝖗 : `{len(CMD_HELP)}` \n💥💥ԱӀէɾօղ-↻ʍժ : `{len(apn)}`\n💥💥ԱӀէɾօղ-φąցҽʂ: 1/{veriler[0]}",
                
                           #f"╔═══💫✨💫═══\n"
                           #f"┃**{hell_mention}**\n"
                           #f"╚═══💫✨💫═══\n"
                           #f"╔══════✣✤༻⋇༺✤✣══════╗\n"
                           #f"┣💥ԱӀէɾօղ-φӀմցìղʂ: `{len(CMD_HELP)}` \n"
                           #f"┣💥ԱӀէɾօղ-↻ʍժʂ: `{len(apn)}`\n"
                           #f"┣💥ԱӀէɾօղ-φąցҽʂ : 1/{veriler[0]}`\n"
                           #f"╚══════✣✤༻⋇༺✤✣══════╝\n","""
                           
                buttons=simp[1],
                link_preview=False,
            )
        else:
            reply_pop_up_alert = "𝕐𝕠𝕦 𝕒𝕣𝕖 𝕟𝕠𝕥 𝕒𝕦𝕥𝕙𝕠𝕣𝕚𝕫𝕖𝕕 𝕥𝕠 𝕦𝕤𝕖 𝕞𝕖! \n© ԱӀէɾօղβօէ ™"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        if event.query.user_id in auth:
            veriler = custom.Button.inline(f"{hell_emoji} Re-Open Menu {hell_emoji}", data="reopen")
            await event.edit(f"**💥💥𝕌𝕝𝕥𝕣𝕠𝕟𝔹𝕠𝕥 𝕄𝕖𝕟𝕦 ℙ𝕣𝕠𝕧𝕚𝕕𝕖𝕣 𝕀𝕤 ℕ𝕠𝕨 ℂ𝕝𝕠𝕤𝕖𝕕💥💥**\n\n**𝕌𝕝𝕥𝕣𝕠𝕟𝔹𝕠𝕥 𝕆𝕗:**  {hell_mention}\n\n        [©️ԱӀէɾօղβօէ™️]({chnl_link})", buttons=veriler, link_preview=False)   
                                #f"╔═══💫✨💫═══\n"
                                #f"┃**⚜️ 𝕌𝕝𝕥𝕣𝕠𝕟𝔹𝕠𝕥 𝕄𝕖𝕟𝕦 ℙ𝕣𝕠𝕧𝕚𝕕𝕖𝕣 𝕀𝕤 ℕ𝕠𝕨 ℂ𝕝𝕠𝕤𝕖𝕕 ⚜️**\n"
                                #f"┃**𝕌𝕝𝕥𝕣𝕠𝕟𝔹𝕠𝕥 𝕆𝕗 :**  {hell_mention}\n"  
                                #f"╚═══💫✨💫═══\n"
                                #[©️ ԱӀէɾօղβօէ ™️]({chnl_link})", buttons=veriler, link_preview=False)"
        else:
            reply_pop_up_alert = "𝕐𝕠𝕦 𝕒𝕣𝕖 𝕟𝕠𝕥 𝕒𝕦𝕥𝕙𝕠𝕣𝕚𝕫𝕖𝕕 𝕥𝕠 𝕦𝕤𝕖 𝕞𝕖! \n© ԱӀէɾօղβօէ ™"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
   

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"page\((.+?)\)")))
    async def page(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        page = int(event.data_match.group(1).decode("UTF-8"))
        veriler = button(page, CMD_HELP)
        apn = []
        for x in CMD_LIST.values():
            for y in x:
                apn.append(y)
        if event.query.user_id in auth:
            await event.edit(
                           f"💥💥 **{hell_mention}**\n\n💥💥 ԱӀէɾօղ-φӀմցìղʂ𝖗 : `{len(CMD_HELP)}` \n💥💥ԱӀէɾօղ-↻ʍժ : `{len(apn)}`\n💥💥ԱӀէɾօղ-φąցҽʂ: 1/{veriler[0]}",
                           #f"╔═══💫✨💫═══\n"
                           #f"┃**{hell_mention}**\n"
                           #f"╚═══💫✨💫═══\n"
                           #f"╔══════✣✤༻⋇༺✤✣══════╗\n"
                           #f"┣💥ԱӀէɾօղ-φӀմցìղʂ: `{len(CMD_HELP)}` \n"
                           #f"┣💥ԱӀէɾօղ-↻ʍժʂ: `{len(apn)}`\n"
                           #f"┣💥ԱӀէɾօղ-φąցҽʂ : 1/{veriler[0]}`\n"
                           #f"╚══════✣✤༻⋇༺✤✣══════╝\n","""
                buttons=veriler[1],
                link_preview=False,
            )
        else:
            return await event.answer("𝕐𝕠𝕦 𝕒𝕣𝕖 𝕟𝕠𝕥 𝕒𝕦𝕥𝕙𝕠𝕣𝕚𝕫𝕖𝕕 𝕥𝕠 𝕦𝕤𝕖 𝕞𝕖! \n© ԱӀէɾօղβօէ ™", cache_time=0, alert=True)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"Information\[(\d*)\]\((.*)\)")))
    async def Information(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        page = int(event.data_match.group(1).decode("UTF-8"))
        commands = event.data_match.group(2).decode("UTF-8")
        try:
            buttons = [
                custom.Button.inline("⚡ " + cmd[0] + " ⚡", data=f"commands[{commands}[{page}]]({cmd[0]})")
                for cmd in CMD_HELP_BOT[commands]["commands"].items()
            ]
        except KeyError:
            return await event.answer("No Description is written for this plugin", cache_time=0, alert=True)

        buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        buttons.append([custom.Button.inline(f"{hell_emoji} Main Menu {hell_emoji}", data=f"page({page})")])
        if event.query.user_id in auth:
            await event.edit(
                f"**📗 File :**  `{commands}`\n**🔢 Number of commands :**  `{len(CMD_HELP_BOT[commands]['commands'])}`",
                buttons=buttons,
                link_preview=False,
            )
        else:
            return await event.answer("𝕐𝕠𝕦 𝕒𝕣𝕖 𝕟𝕠𝕥 𝕒𝕦𝕥𝕙𝕠𝕣𝕚𝕫𝕖𝕕 𝕥𝕠 𝕦𝕤𝕖 𝕞𝕖! \n© ԱӀէɾօղβօէ ™", cache_time=0, alert=True)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"commands\[(.*)\[(\d*)\]\]\((.*)\)")))
    async def commands(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        cmd = event.data_match.group(1).decode("UTF-8")
        page = int(event.data_match.group(2).decode("UTF-8"))
        commands = event.data_match.group(3).decode("UTF-8")
        result = f"**📗 File :**  `{cmd}`\n"
        if CMD_HELP_BOT[cmd]["info"]["info"] == "":
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⚠️ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
        else:
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⚠️ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
            result += f"**ℹ️ Info :**  {CMD_HELP_BOT[cmd]['info']['info']}\n"
        sextraa = CMD_HELP_BOT[cmd]["extra"]
        if sextraa:
            a = sorted(sextraa.keys())
            for b in a:
                c = b
                d = sextraa[c]["content"]
                result += f"**{c} :**  `{d}`\n"
        result += "\n"
        command = CMD_HELP_BOT[cmd]["commands"][commands]
        if command["params"] is None:
            result += f"**🛠 Commands :**  `{HANDLER[:1]}{command['command']}`\n"
        else:
            result += f"**🛠 Commands :**  `{HANDLER[:1]}{command['command']} {command['params']}`\n"
        if command["example"] is None:
            result += f"**💬 Explanation :**  `{command['usage']}`\n\n"
        else:
            result += f"**💬 Explanation :**  `{command['usage']}`\n"
            result += f"**⌨️ For Example :**  `{HANDLER[:1]}{command['example']}`\n\n"
        if event.query.user_id in auth:
            await event.edit(
                result,
                buttons=[custom.Button.inline(f"{hell_emoji} Return {hell_emoji}", data=f"Information[{page}]({cmd})")],
                link_preview=False,
            )
        else:
            return await event.answer("𝕐𝕠𝕦 𝕒𝕣𝕖 𝕟𝕠𝕥 𝕒𝕦𝕥𝕙𝕠𝕣𝕚𝕫𝕖𝕕 𝕥𝕠 𝕦𝕤𝕖 𝕞𝕖! \n© ԱӀէɾօղβօէ ™", cache_time=0, alert=True)


# UltronBot
