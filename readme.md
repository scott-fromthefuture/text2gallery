```
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
#                                                                       #
#########################################################################

```
You will need to register a bot, and get your application ID, 
and set the perms on https://discord.com/developers/applications/
```py
CLIENT_ID = ''
PERMS = 395137117248
```
  
A person with credentials on the target and source servers must open the following invite link in a browser to invite the  script to the server, and ensure it has the proper permissions in both channels. 
```py
'https://discord.com/api/oauth2/authorize?client_id=' + CLIENT_ID + '&permissions=' + PERMS + '&scope=bot%20applications.commands
``` 

Then get the source and destination channel ID's for the script, following this incredible guide on how to right-click:


<a href="https://www.youtube.com/watch?v=ySZWoD5UpgA">
  <img style="width: 300px;" src="https://img.youtube.com/vi/ySZWoD5UpgA/maxresdefault.jpg" />
</a>


Configure config.py and send it
