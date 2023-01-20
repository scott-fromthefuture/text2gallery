#!/usr/bin/env python3

#########################################################################
#                                                                       #
# text2gallery.py                                                       #
#                                                                       #
# This is a simple bot script to transfer the image and movie files     #
# from all posts in a discord text channel, and repost the file in      #
# a forum gallery.                                                      #
#                                                                       #
# DO NOT USE - an incomplete script made for a speciic purpouse         #
# for a specific case. Adapt to your needs, but do not use blindly      #
# as is. Is missing certain useful features and can be expanded on.     #
#                                                                       #
# START WITH THE README.MD                                              #
#                                                                       #
#########################################################################

import discord
from discord.ext import commands
import os
import time
import datetime
import random
import string
import re

# configuration
BOT_TOKEN = ""
SOURCE_CHANNEL_ID = 0         # text channel
DESTINATION_CHANNEL_ID = 0   # forum gallery

seconds_per_message = 1  # for rate limt
save_attachments = True  # all images will be saved in archive/ locally  

# Attachments to move
target_exts = (
    'gif',
    'gifv',
    'jpeg',
    'jpg',
    'png',
    'webp',
    'webm',
    'mp4')

# connect discord bot
client = commands.Bot(command_prefix=">", intents=discord.Intents.all())


# create directories if they dont exist
def createStructure():
    if not os.path.exists("transfer"):
        os.makedirs("transfer")
    if not os.path.exists("archive") and save_attachments:
        os.makedirs("archive")


# check if message has any attachemnst we want
def checkAttachment(message):
    attachments = []
    if message.attachments:
        for attachment in message.attachments:

            # if it has an attachment, check if extension is included
            included = str(attachment).lower().endswith(target_exts)
            if included:
                attachments.append(attachment)

    # if attachements, return them       
    if len(attachments) > 0:
        return attachments
    else:
        return False


# iterate through messages and remove ones without attachment
def filterMessages(messages):
    messages_tokeep = []

    for message in messages:
        # check if the message has an attachment
        attachments = checkAttachment(message)

        # if no attachments, next messages
        if not attachments:
            print("attachment false | no target attachment")
            continue   

        # otherwise, has attachemnt so keep message
        print("attachment true  | keeping message")
        messages_tokeep.append(message)

    return messages_tokeep


def cleanup(file):
    # if we want to save images, move them
    if save_attachments:
        dest_path = "archive/"
        destination = dest_path + str(os.path.basename(file))
        os.rename(file, destination)
    else:
        # not saving, so remove
        os.remove(file) 


# connect client
@client.event
async def on_ready():
    starttime = time.time()

    # get all message history from teh source channel
    print("\nscanning message history in source channel...")
    source_channel = client.get_channel(SOURCE_CHANNEL_ID)
    raw_messages = [message async for message in source_channel.history(
        limit=None, oldest_first=True)]
    rawmessage_count = len(raw_messages)

    # iterate through messages and remove ones without attachments
    print(f"removing messages with no desirable attachment...")
    messages = filterMessages(raw_messages)

    # we now have a list of only the messages we want to get attachemnts from
    message_count = len(messages)
    print(f"\n  total messages: {rawmessage_count}")
    print(f"messages skipped: {rawmessage_count - message_count}")
    print(f"   messages kept: {message_count}\n")

    # begin pricessing messages
    createStructure()
    destination_channel = client.get_channel(DESTINATION_CHANNEL_ID)
    skipping = transferring = failed = total = 0

    for message in messages:
        total += 1

        # check if the message has an attachment
        attachments = checkAttachment(message)

        # if no attachments, next messages
        if not attachments:
            skipping += 1
            reason = "skipping, no target attachments"
            continue

        # otherwise that means we have attachments
        for attachment in attachments:

            try:              
                # rename file and download
                raw_username = message.author.display_name
                s=string.ascii_letters + string.digits
                randomid = ''.join(random.sample(s,6))
                file_username = "".join([c for c in str(raw_username) if re.match(r'\w', c)])
                tmpfile_path = "transfer/"
                tmpfile_filename = str(file_username) + str(f"_{randomid}_") + str(attachment.filename)
                tmpfile = tmpfile_path + tmpfile_filename

                await attachment.save(tmpfile)

                # open the file
                with open(tmpfile, "rb") as f:
                    file = discord.File(f)

                    # include original poster's username
                    mention = message.author.mention
                    
                    # send message with file attached in destination channel
                    await destination_channel.create_thread(
                        auto_archive_duration=60,
                        name="Posted by: " + str(raw_username),
                        content="Originaly posted by " + str(mention) + " on " + 
                        str(message.created_at.strftime('%a %d-%m-%Y')), file=file)

                    # handle local file
                    cleanup(tmpfile)

                    # update stats
                    reason = "✓  " + str(attachment.filename)                 
                    transferring += 1

            # if transfer fails, continue with next
            except Exception as error:
                reason = "x  " + str(error)
                failed += 1

        # print stats, and sleep before next to prevent rate limit
        remaining = message_count - total
        elapsed_time = str(datetime.timedelta(seconds=time.time() - starttime))
        print(f"{elapsed_time}  | success {transferring} skipped {skipping} failed {failed} |  msgs {total} (r: {remaining}) {reason}")
        time.sleep(seconds_per_message)


# run script                    
if __name__=="__main__":        
    client.run(BOT_TOKEN)