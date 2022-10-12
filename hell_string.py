import os
os.system("pip install telethon")
os.system("pip install pyrogram")
from pyrogram import Client
from telethon.sessions import StringSession
from telethon.sync import TelegramClient


print("•••   UltronBot  SESSION  GENERATOR   •••")
print("\nHello!! Welcome to UltronBot Session Generator\n")
okvai = input("Enter 69 to continue: ")
if okvai == "69":
    print("Choose the string session type: \n1. UltronBot \n2. Music Bot")
    library = input("\nYour Choice: ")
    if library == "1":
        print("\nTelethon Session For UltronBot")
        APP_ID = int(input("\nEnter APP ID here: "))
        API_HASH = input("\nEnter API HASH here: ")
        with TelegramClient(StringSession(), APP_ID, API_HASH) as UltronBot:
            print("\nYour UltronBot Session Is sent in your Telegram Saved Messages.")
            UltronBot.send_message("me", f"#UltronBot #UltronBot_SESSION \n\n`{UltronBot.session.save()}`")
    elif library == "2":
        print("Pyrogram Session for Music Bot")
        APP_ID = int(input("\nEnter APP ID here: "))
        API_HASH = input("\nEnter API HASH here: ")
        with Client(':memory:', api_id=APP_ID, api_hash=API_HASH) as UltronBot:
            print("\nYour UltronBot Session Is sent in your Telegram Saved Messages.")
            UltronBot.send_message("me", f"#UltronBot_MUSIC #UltronBot_SESSION\n\n`{UltronBot.export_session_string()}`")
    else:
        print("Please Enter 1 or 2 only.")
else:
    print("Bhag jaa bhosdike")
