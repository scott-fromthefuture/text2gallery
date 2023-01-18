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
# START WITH THE -README.MD- and -config.py-                            #
#                                                                       #
#########################################################################

import discord
import os
import config

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

client =discord.ext.commands.Bot(command_prefix=">", intents=discord.Intents.all())

# connect client
@client.event
async def on_ready():

    # get the source and destination channels by ID
    source_channel = client.get_channel(config.SOURCE_CHANNEL_ID)
    destination_channel = client.get_channel(config.DESTINATION_CHANNEL_ID)

    # iterate through messages in source channel
    async for message in source_channel.history():

        # check if the message has an attachment
        if message.attachments:
            for attachment in message.attachments:
                included = str(attachment).lower().endswith(target_exts)
                
                # check if the attachment is a file type we want to move
                if included:

                    # download the file
                    await attachment.save(attachment.filename)

                    # open the file
                    with open(attachment.filename, "rb") as f:
                        file = discord.File(f)

                        # send message with file attached in destination channel
                        # include original poster's username
                        await destination_channel.create_thread(
                            name="Originaly posted by " + str(message.author),
                            content="Originaly posted by @" + str(message.author), 
                            file=file)

                        # remove tmp file stored locally
                        os.remove(attachment.filename) 
                    
# run script                    
if __name__=="__main__":        
    client.run(config.BOT_TOKEN)
