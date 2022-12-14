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
USER_BOT_WARN_ZERO = "πΌππ π¦ππ ππ ππ π¦π£ π½ππ π ππππ ππ ππͺ πππ€π₯ππ£'π€ πππβπββπ!! \n\n**π« πΉππ ππππ πππ βππ‘π π£π₯ππ.**"

alive_txt = """{}\n
<b><i>π π±ππ ππππππ π</b></i>
<b>Telethon β</b>  <i>{}</i>
<b>UltronαΊΓΈβ  β</b>  <i>{}</i>
<b>Uptime β</b>  <i>{}</i>
<b>Abuse β</b>  <i>{}</i>
<b>Sudo β</b>  <i>{}</i>
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
               f"π₯πΉπππ {hell_emoji}", data=f"page({(max_pages - 1) if page == 0 else (page - 1)})"
            ),
            custom.Button.inline(
               f"β’ β β’", data="close"
            ),
            custom.Button.inline(
               f"{hell_emoji} Υ²?½ΓΥ§π₯", data=f"page({0 if page == (max_pages - 1) else page + 1})"
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
                
                help_msg = f"π₯π₯ **{hell_mention}**\n\nπ₯π₯Τ±ΣΥ§ΙΎΦΥ²-ΟΣΥ΄ΦΓ¬Υ²Κ : `{len(CMD_HELP)}` \nπ₯π₯Τ±ΣΥ§ΙΎΦΥ²-β»ΚΥͺΚ: `{len(apn)}`\nπ₯π₯Τ±ΣΥ§ΙΎΦΥ²-ΟΔΦ?½Κ: 1/{veriler[0]}"
                
                #help_msg = f"ββββπ«β¨π«βββ\n"
                #help_msg = f"β**{hell_mention}**\n"
                #help_msg = f"ββββπ«β¨π«βββ\n"
                #help_msg = f"ββββββββ£β€ΰΌ»βΰΌΊβ€β£βββββββ\n"
                #help_msg = f"β£π₯Τ±ΣΥ§ΙΎΦΥ²-ΟΣΥ΄ΦΓ¬Υ²Κ: `{len(CMD_HELP)}` \n"
                #help_msg = f"β£π₯Τ±ΣΥ§ΙΎΦΥ²-β»ΚΥͺΚ: `{len(apn)}`\n"
                #help_msg = f"β£π₯Τ±ΣΥ§ΙΎΦΥ²-ΟΔΦ?½Κ : 1/{veriler[0]}`\n"
                #help_msg = f"ββββββββ£β€ΰΌ»βΰΌΊβ€β£βββββββ\n"""
                
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
            alv_msg = gvarstat("ALIVE_MSG") or "Β»Β»Β» <b>Τ±ΣΥ§ΙΎΦΥ²Ξ²ΦΥ§ Δ―Κ ΰΆ§Υ²ΖΓ¬ΙΎ?½</b> Β«Β«Β«"
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
            CSTM_PMP = gvarstat("CUSTOM_PMPERMIT") or "**ππ π¦ βππ§π ππ£ππ€π‘ππ€π€ππ ππ  ππͺ πππ€π₯ππ£'π€ πππ₯π£π π βπ.!\nππππ€ ππ€ πππππππ πΈππ βππππ£πππ πΈπ€ βπ£πππ.**"
            HELL_FIRST = "**π₯ Τ±ΣΥ§ΙΎΦΥ²Ξ²ΦΥ§ βπ£ππ§ππ₯π πππ₯π£π π βπͺπππ£ ππππ¦π£ππ₯πͺ βπ£π π₯π ππ π π₯**\n\ΡΡΙ­Ι­ΰΉ!! πππππ ππ ππ  {}'π€ πππ₯π£π π βπ. ππππ€ ππ€ ππ ππ¦π₯π πππ₯ππ πππ€π€πππ.\n\n{}".format(hell_mention, CSTM_PMP)
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
                        [custom.Button.inline("π Request Approval", data="req")],
                        [custom.Button.inline("π« Block", data="heheboi")],
                        [custom.Button.inline("β Curious", data="pmclick")],
                    ],
                    link_preview=False,
                )
            elif PIC:
                result = builder.document(
                    file=PIC,
                    text=HELL_FIRST,
                    title="πππ₯π£π ππΉπ π₯ βπ βππ£πππ₯.",
                    buttons=[
                        [custom.Button.inline("π πππ₯π£π π βππ’π¦ππ€π₯ πΈπ‘π‘π£π π§ππ", data="req")],
                        [custom.Button.inline("π« πΉππ ππ", data="heheboi")],
                        [custom.Button.inline("β βπ¦π£ππ π¦π€.", data="pmclick")],
                    ],
                    link_preview=False,
                )
            else:
                result = builder.article(
                    text=HELL_FIRST,
                    title="πππ₯π£π ππΉπ π₯ βπ βππ£πππ₯.",
                    buttons=[
                        [custom.Button.inline("π πππ₯π£π π βππ’π¦ππ€π₯ πΈπ‘π‘π£π π§ππ", data="req")],
                        [custom.Button.inline("π« πΉππ ππ", data="heheboi")],
                        [custom.Button.inline("β βπ¦π£ππ π¦π€.", data="pmclick")],
                    ],
                    link_preview=False,
                )
                
        elif event.query.user_id in auth and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"**β‘ κ?½Φ?½Υ²ΥͺΔΙΎΥΎ ΘΊΖ Τ±ΣΥ§ΙΎΦΥ²Ξ²ΦΥ§β‘**",
                buttons=[
                    [Button.url("π₯ Τ±ΣΥ§ΙΎΦΥ² ΙΎ?½ΦΦΚ π₯", "https://github.com/LEGENDXTHANOS/ULTRONBOT")],
                    [Button.url("π₯Τ±ΣΥ§ΙΎΦΥ²Ξ²ΦΥ§ α ?½Υ§Υ‘ΦΙΎ?π₯", "https://t.me/UltronBot_OP")],
                ],
            )

        elif query.startswith("http"):
            part = query.split(" ")
            result = builder.article(
                "File uploaded",
                text=f"**File uploaded successfully to {part[2]} site.\n\nUpload Time : {part[1][:3]} second\n[βββ β]({part[0]})",
                buttons=[[custom.Button.url("URL", part[0])]],
                link_preview=True,
            )

        else:
            result = builder.article(
                "@UltronBot_XD",
                text="""**βππͺ! ππππ€ ππ€ [Τ±ΣΥ§ΙΎΦΥ²Ξ²ΦΥ§](https://t.me/UltronBot_XD) \nππ π¦ πππ πππ π¨ ππ π£π πππ π¦π₯ ππ ππ£π π π₯ππ πππππ€ πππ§ππ ππππ π¨ π**""",
                buttons=[
                    [
                        custom.Button.url("π₯ Τ±ΣΥ§ΙΎΦΥ² β»Υ°ΔΥ²Υ²?½Σ π₯", "https://t.me/UltronBot_OP"),
                        custom.Button.url("β‘ Τ±ΣΥ§ΙΎΦΥ² ΖΙΎΦΥ΄Φ β‘", "https://t.me/UltronBot_XD"),
                    ],
                    [
                        custom.Button.url("β¨ Τ±ΣΥ§ΙΎΦΥ² ΙΎ?½ΦΦΚ β¨", "https://github.com/LEGENDXTHANOS/ULTRONBOT"),
                        custom.Button.url("π° Τ±ΣΥ§ΙΎΦΥ² ΙΎ?½ΦΣΚ π°", "https://replit.com/@LEGEND-LX/PYTHONBOT-4"),
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
            reply_pop_up_alert = "π° ππππ€ ππ€ πππ₯π£π ππΉπ π₯ βπ ππππ¦π£ππ₯πͺ π₯π  ππππ‘ ππ¨ππͺ π¦ππ¨πππ₯ππ π£ππ₯ππ£ππ€ ππ£π π π€π‘ππππππ βπ !!"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"req")))
    async def on_pm_click(event):
        auth = await clients_list()
        if event.query.user_id in auth:
            reply_pop_up_alert = "ππππ€ ππ€ ππ π£ π π₯πππ£ π¦π€ππ£π€!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit("β **βππ’π¦ππ€π₯ βππππ€π₯ππ£π** \n\nππͺ πππ€π₯ππ£ π¨πππ ππ π¨ ππππππ π₯π  ππ π π ππ π£ πͺπ π¦π£ π£ππ’π¦ππ€π₯ π π£ ππ π₯.\nπ ππππ π₯πππ π¨πππ₯ π‘ππ₯ππππ₯ππͺ πππ ππ π'π₯ π€π‘ππ!!")
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            await tbot.send_message(LOG_GP, f"#ULTRON_REQUEST \n\nβοΈ ππ π¦ ππ π₯ π πππβπβ π£ππ’π¦ππ€π₯ ππ£π π [{first_name}](tg://user?id={event.query.user_id}) !")


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"heheboi")))
    async def on_pm_click(event):
        auth = await clients_list()
        if event.query.user_id in auth:
            reply_pop_up_alert = "ππππ€ ππ€ ππ π£ π π₯πππ£ π¦π€ππ£π€!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(f"πΈπ ππ π¦ πππ€π. **Ξ²κΰΆ§β»? Ζα  !!**")
            await H1(functions.contacts.BlockRequest(event.query.user_id))
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            await tbot.send_message(LOG_GP, f"#BETA_CHOD_GYA_TUTO_BLOCK \n\n**Ξ²κΰΆ§β»? Ζα ** [{first_name}](tg://user?id={event.query.user_id}) \nβπππ€π π:- πππ₯π£π π βπ ππππ πΉππ ππ")


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
                         f"π₯π₯ **{hell_mention}**\n\nπ₯π₯ Τ±ΣΥ§ΙΎΦΥ²-ΟΣΥ΄ΦΓ¬Υ²Κπ : `{len(CMD_HELP)}` \nπ₯π₯Τ±ΣΥ§ΙΎΦΥ²-β»ΚΥͺ : `{len(apn)}`\nπ₯π₯Τ±ΣΥ§ΙΎΦΥ²-ΟΔΦ?½Κ: 1/{veriler[0]}",
                
                           #f"ββββπ«β¨π«βββ\n"
                           #f"β**{hell_mention}**\n"
                           #f"ββββπ«β¨π«βββ\n"
                           #f"ββββββββ£β€ΰΌ»βΰΌΊβ€β£βββββββ\n"
                           #f"β£π₯Τ±ΣΥ§ΙΎΦΥ²-ΟΣΥ΄ΦΓ¬Υ²Κ: `{len(CMD_HELP)}` \n"
                           #f"β£π₯Τ±ΣΥ§ΙΎΦΥ²-β»ΚΥͺΚ: `{len(apn)}`\n"
                           #f"β£π₯Τ±ΣΥ§ΙΎΦΥ²-ΟΔΦ?½Κ : 1/{veriler[0]}`\n"
                           #f"ββββββββ£β€ΰΌ»βΰΌΊβ€β£βββββββ\n","""
                           
                buttons=simp[1],
                link_preview=False,
            )
        else:
            reply_pop_up_alert = "ππ π¦ ππ£π ππ π₯ ππ¦π₯ππ π£ππ«ππ π₯π  π¦π€π ππ! \nΒ© Τ±ΣΥ§ΙΎΦΥ²Ξ²ΦΥ§ β’"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        if event.query.user_id in auth:
            veriler = custom.Button.inline(f"{hell_emoji} Re-Open Menu {hell_emoji}", data="reopen")
            await event.edit(f"**π₯π₯πππ₯π£π ππΉπ π₯ ππππ¦ βπ£π π§ππππ£ ππ€ βπ π¨ βππ π€πππ₯π₯**\n\n**πππ₯π£π ππΉπ π₯ ππ:**  {hell_mention}\n\n        [Β©οΈΤ±ΣΥ§ΙΎΦΥ²Ξ²ΦΥ§β’οΈ]({chnl_link})", buttons=veriler, link_preview=False)   
                                #f"ββββπ«β¨π«βββ\n"
                                #f"β**βοΈ πππ₯π£π ππΉπ π₯ ππππ¦ βπ£π π§ππππ£ ππ€ βπ π¨ βππ π€ππ βοΈ**\n"
                                #f"β**πππ₯π£π ππΉπ π₯ ππ :**  {hell_mention}\n"  
                                #f"ββββπ«β¨π«βββ\n"
                                #[Β©οΈ Τ±ΣΥ§ΙΎΦΥ²Ξ²ΦΥ§ β’οΈ]({chnl_link})", buttons=veriler, link_preview=False)"
        else:
            reply_pop_up_alert = "ππ π¦ ππ£π ππ π₯ ππ¦π₯ππ π£ππ«ππ π₯π  π¦π€π ππ! \nΒ© Τ±ΣΥ§ΙΎΦΥ²Ξ²ΦΥ§ β’"
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
                           f"π₯π₯ **{hell_mention}**\n\nπ₯π₯ Τ±ΣΥ§ΙΎΦΥ²-ΟΣΥ΄ΦΓ¬Υ²Κπ : `{len(CMD_HELP)}` \nπ₯π₯Τ±ΣΥ§ΙΎΦΥ²-β»ΚΥͺ : `{len(apn)}`\nπ₯π₯Τ±ΣΥ§ΙΎΦΥ²-ΟΔΦ?½Κ: 1/{veriler[0]}",
                           #f"ββββπ«β¨π«βββ\n"
                           #f"β**{hell_mention}**\n"
                           #f"ββββπ«β¨π«βββ\n"
                           #f"ββββββββ£β€ΰΌ»βΰΌΊβ€β£βββββββ\n"
                           #f"β£π₯Τ±ΣΥ§ΙΎΦΥ²-ΟΣΥ΄ΦΓ¬Υ²Κ: `{len(CMD_HELP)}` \n"
                           #f"β£π₯Τ±ΣΥ§ΙΎΦΥ²-β»ΚΥͺΚ: `{len(apn)}`\n"
                           #f"β£π₯Τ±ΣΥ§ΙΎΦΥ²-ΟΔΦ?½Κ : 1/{veriler[0]}`\n"
                           #f"ββββββββ£β€ΰΌ»βΰΌΊβ€β£βββββββ\n","""
                buttons=veriler[1],
                link_preview=False,
            )
        else:
            return await event.answer("ππ π¦ ππ£π ππ π₯ ππ¦π₯ππ π£ππ«ππ π₯π  π¦π€π ππ! \nΒ© Τ±ΣΥ§ΙΎΦΥ²Ξ²ΦΥ§ β’", cache_time=0, alert=True)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"Information\[(\d*)\]\((.*)\)")))
    async def Information(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        page = int(event.data_match.group(1).decode("UTF-8"))
        commands = event.data_match.group(2).decode("UTF-8")
        try:
            buttons = [
                custom.Button.inline("β‘ " + cmd[0] + " β‘", data=f"commands[{commands}[{page}]]({cmd[0]})")
                for cmd in CMD_HELP_BOT[commands]["commands"].items()
            ]
        except KeyError:
            return await event.answer("No Description is written for this plugin", cache_time=0, alert=True)

        buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        buttons.append([custom.Button.inline(f"{hell_emoji} Main Menu {hell_emoji}", data=f"page({page})")])
        if event.query.user_id in auth:
            await event.edit(
                f"**π File :**  `{commands}`\n**π’ Number of commands :**  `{len(CMD_HELP_BOT[commands]['commands'])}`",
                buttons=buttons,
                link_preview=False,
            )
        else:
            return await event.answer("ππ π¦ ππ£π ππ π₯ ππ¦π₯ππ π£ππ«ππ π₯π  π¦π€π ππ! \nΒ© Τ±ΣΥ§ΙΎΦΥ²Ξ²ΦΥ§ β’", cache_time=0, alert=True)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"commands\[(.*)\[(\d*)\]\]\((.*)\)")))
    async def commands(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        cmd = event.data_match.group(1).decode("UTF-8")
        page = int(event.data_match.group(2).decode("UTF-8"))
        commands = event.data_match.group(3).decode("UTF-8")
        result = f"**π File :**  `{cmd}`\n"
        if CMD_HELP_BOT[cmd]["info"]["info"] == "":
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**β οΈ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
        else:
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**β οΈ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
            result += f"**βΉοΈ Info :**  {CMD_HELP_BOT[cmd]['info']['info']}\n"
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
            result += f"**π  Commands :**  `{HANDLER[:1]}{command['command']}`\n"
        else:
            result += f"**π  Commands :**  `{HANDLER[:1]}{command['command']} {command['params']}`\n"
        if command["example"] is None:
            result += f"**π¬ Explanation :**  `{command['usage']}`\n\n"
        else:
            result += f"**π¬ Explanation :**  `{command['usage']}`\n"
            result += f"**β¨οΈ For Example :**  `{HANDLER[:1]}{command['example']}`\n\n"
        if event.query.user_id in auth:
            await event.edit(
                result,
                buttons=[custom.Button.inline(f"{hell_emoji} Return {hell_emoji}", data=f"Information[{page}]({cmd})")],
                link_preview=False,
            )
        else:
            return await event.answer("ππ π¦ ππ£π ππ π₯ ππ¦π₯ππ π£ππ«ππ π₯π  π¦π€π ππ! \nΒ© Τ±ΣΥ§ΙΎΦΥ²Ξ²ΦΥ§ β’", cache_time=0, alert=True)


# UltronBot
