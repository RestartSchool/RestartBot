# RestartBot v1
# Made by Restart, 2024

# Imports - bot
import discord
from discord import app_commands, Color, ButtonStyle
from discord.ui import View, Select
import sys
import os
import asyncio
import re
import time
from datetime import datetime
from datetime import timedelta
#import psutil
import cpuinfo

# Imports - Wikipedia
import wikipedia
from bs4 import GuessedAtParserWarning

# Imports - Cat / Dog
import requests

# Imports - Insult, Compliment
import random

# Current Running Path
path = os.getcwd()

# Set path type
if f"{os.name}" == "nt":
    pathtype = "\\"
    print(f"[INIT] OS name is {os.name}, path type {pathtype}")
else:
    pathtype = "/"
    print(f"[INIT] OS name is {os.name}, path type {pathtype}")

# Open Token Files
discord_token_file = open(f"{path}{pathtype}tokens{pathtype}discord_token.txt", "r")
spotify_id_file = open(f"{path}{pathtype}tokens{pathtype}spotify_id.txt", "r")
spotify_secret_file = open(f"{path}{pathtype}tokens{pathtype}spotify_secret.txt", "r")

# Read Token Files, assign vars
discord_token = discord_token_file.read()
spotify_id = spotify_id_file.read()
spotify_secret = spotify_secret_file.read()

# Close Token Files as they are no longer needed
discord_token_file.close()
spotify_id_file.close()
spotify_secret_file.close()

# Imports, Setup - Spotify Search command
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import quote
auth_manager = SpotifyClientCredentials(client_id = spotify_id, client_secret = spotify_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Cat / Dog Embed Titles
cat_titles = ["Aww!", "Cute cat!", "Adorable!", "Meow!", "Purrfect!", "Cat!", ":3"]
dog_titles = ["Aww!", "Cute dog!", "Adorable!", "Woof!", "Woof woof!", "Dog!", "Bark!"]

# Restart's User ID
restart_id = 563372552643149825

# Client class
class aclient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if self.synced == False:
            await tree.sync()
            self.synced = True
            print("[INIT] Commands synced.")
        print(f"[INIT] We have logged into Discord as {self.user}!")

# Define client and command tree
client = aclient()
tree = app_commands.CommandTree(client)

# Spotify Embed Autosender
@client.event
async def on_message(message):
    # Ignore bots
    if message.author.bot != True:
        # Check if there is a Spotify link in the message
        if "https://open.spotify.com/" in message.content:
            messageTargetURLs = []
            i = 0

            # Extract only URLs, put them in messageAllURLs list
            urlRegex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
            messageAllURLs = re.findall(urlRegex, message.content)

            # Add Spotify URLs to messageTargetURLs, while ignoring irrelevant URLs
            for url in messageAllURLs:
                if "https://open.spotify.com/" in url:
                    messageTargetURLs.append(url)

            # Work through all URLs
            for url in messageTargetURLs:
                i += 1
                artist_string = ""
                # Catch any uncaught errors
                try:
                    # Identify URL type
                    if "track" in url:
                        # Track URL
                        # Query information from Spotify
                        result = sp.track(url)

                        # If song is explicit...
                        if result['explicit'] == True:
                            # We add an explicit tag and generate the Discord Embed with title
                            embed = discord.Embed(title = f"{result['name']} (Explicit) (Song)")
                        # Else...
                        else:
                            # We just generate the Discord Embed with title
                            embed = discord.Embed(title = f"{result['name']} (Song)")

                        # Add all artists for song to comma separated string
                        # Example: artist1, artist2, artist3
                        for artist in result['artists']:
                            if artist_string == "":
                                artist_string = artist['name']
                            else:
                                artist_string = f"{artist_string}, {artist['name']}"
                        
                        # Populate embed with information
                        embed.add_field(name = "Artists", value = artist_string, inline = True)
                        embed.add_field(name = "Album", value = result['album']["name"], inline = True)
                        embed.set_thumbnail(url = result["album"]["images"][0]["url"])
                        embed.set_footer(text = f"Message by {message.author.name} - Link {i}/{len(messageTargetURLs)}", icon_url = message.author.avatar.url)

                        # Define view
                        view = View()
                                    
                        # Work out song length in sec:min
                        seconds, result['duration_ms'] = divmod(result['duration_ms'], 1000)
                        minutes, seconds = divmod(seconds, 60)

                        # Add Dismiss Embed Button
                        async def deleteCallback(interaction: discord.Interaction):
                            await interaction.response.defer()
                            
                            # If attempt is from message creator...
                            if interaction.user.id == message.author.id:
                                # We delete the message
                                await msg.delete()
                            # Else...
                            else:
                                # Display permission error that deletes after 3 seconds
                                embed = discord.Embed(title = f"Error", description = f"{interaction.user.mention}, you are not the message OP.", color = Color.red())
                                await message.channel.send(embed = embed, delete_after=3)
                        
                        # Add Dismiss button, define callback as deleteCallback
                        delete_button = discord.ui.Button(label=f'Dismiss Embed', style=discord.ButtonStyle.red)
                        delete_button.callback = deleteCallback
                        view.add_item(delete_button)
                        
                        # Add Open in Spotify button
                        spotify_button = discord.ui.Button(label=f'Play on Spotify ({int(minutes):02d}:{int(seconds):02d})', style=discord.ButtonStyle.url, url=result["external_urls"]["spotify"])
                        view.add_item(spotify_button)
                        
                        # Add Search on YT Music button
                        ytm_button = discord.ui.Button(label='Search on YT Music', style=discord.ButtonStyle.url, url=f'https://music.youtube.com/search?q={(quote(result["name"])).replace("%2B", "+")}+{(quote(artist_string)).replace("%2B", "+")}')
                        view.add_item(ytm_button)

                        # Add Search on Google button
                        google_button = discord.ui.Button(label='Search on Google', style=discord.ButtonStyle.url, url=f'https://www.google.com/search?q={(quote(result["name"])).replace("%2B", "+")}+{(quote(artist_string)).replace("%2B", "+")}')
                        view.add_item(google_button)
                        
                        # Send new embed
                        msg = await message.reply(embed = embed, view = view, mention_author = False)
                    elif "artist" in url:
                        # Artist URL
                        # Fetch artist info
                        result_info = sp.artist(url)

                        # Fetch artist top songs
                        result_top_tracks = sp.artist_top_tracks(url)

                        # Create embed, populate it with information
                        embed = discord.Embed(title = f"{result_info['name']} (Artist)")
                        embed.add_field(name = "Followers", value = f"{result_info['followers']['total']:,}")
                        embed.set_thumbnail(url = result_info["images"][0]["url"])
                        embed.set_footer(text = f"Message by {message.author.name} - Link {i}/{len(messageTargetURLs)}", icon_url = message.author.avatar.url)
                        
                        topsong_string = ""
                        for i in range(0,5):
                            # Add all artists for song to comma separated string
                            # Example: artist1, artist2, artist3
                            artist_string = ""
                            for artist in result_top_tracks['tracks'][i]['artists']:
                                if artist_string == "":
                                    artist_string = artist['name'] 
                                else:
                                    artist_string = f"{artist_string}, {artist['name']}"
                                    
                            # Add each song to a new line in topsong_string
                            # If string is empty...
                            if topsong_string == "":
                                # Set topsong_string to song
                                topsong_string = f"**{i + 1}: {result_top_tracks['tracks'][i]['name']}** - {artist_string}"
                            else:
                                # Add current song to topsong_string, separated with new line
                                topsong_string = f"{topsong_string}\n**{i + 1}: {result_top_tracks['tracks'][i]['name']}** - {artist_string}"
                        
                        # Add top songs to embed
                        embed.add_field(name = "Top Songs", value = topsong_string, inline = False)

                        # Define view
                        view = View()
                        
                        # Dismiss Button callback
                        async def deleteCallback(interaction: discord.Interaction):
                            await interaction.response.defer()
                            
                            # If attempt is from message creator...
                            if interaction.user.id == message.author.id:
                                # We delete the message
                                await msg.delete()
                            # Else...
                            else:
                                # Display permission error that deletes after 3 seconds
                                embed = discord.Embed(title = f"Error", description = f"{interaction.user.mention}, you are not the message OP.", color = Color.red())
                                await message.channel.send(embed = embed, delete_after=3)
                        
                        # Add Dismiss button, define callback as deleteCallback
                        delete_button = discord.ui.Button(label=f'Dismiss Embed', style=discord.ButtonStyle.red)
                        delete_button.callback = deleteCallback
                        view.add_item(delete_button)
                        
                        # Add Open in Spotify button
                        spotify_button = discord.ui.Button(label=f'Show on Spotify', style=discord.ButtonStyle.url, url=result_info["external_urls"]["spotify"])
                        view.add_item(spotify_button)

                        # Add Search on YT Music button
                        ytm_button = discord.ui.Button(label='Search on YT Music', style=discord.ButtonStyle.url, url=f'https://music.youtube.com/search?q={(quote(result_info["name"])).replace("%2B", "+")}+{(quote(artist_string)).replace("%2B", "+")}')
                        view.add_item(ytm_button)

                        # Add Search on Google button
                        google_button = discord.ui.Button(label='Search on Google', style=discord.ButtonStyle.url, url=f'https://www.google.com/search?q={(quote(result_info["name"])).replace("%2B", "+")}+{(quote(artist_string)).replace("%2B", "+")}')
                        view.add_item(google_button)

                        msg = await message.reply(embed = embed, view = view, mention_author = False)
                    elif "album" in url:
                        # Album URL
                        # Fetch artist info
                        result_info = sp.album(url)

                        songlist_string = ""
                        # Work through all songs in album
                        for i in range(len(result_info['tracks']['items'])):
                            # Add all artists for song to comma separated string
                            # Example: artist1, artist2, artist3
                            artist_string = ""
                            for artist in result_top_tracks['tracks'][i]['artists']:
                                if artist_string == "":
                                    artist_string = artist['name'] 
                                else:
                                    artist_string = f"{artist_string}, {artist['name']}"
                                    
                            # Add song listing to song list
                            if songlist_string == "":
                                songlist_string = f"**{i + 1}: {result_info['tracks']['items'][i]['name']}** - {artist_string}"
                            else:
                                songlist_string = f"{songlist_string}\n**{i + 1}: {result_info['tracks']['items'][i]['name']}** - {artist_string}"

                        # Add all artists for album to comma separated string
                        # Example: artist1, artist2, artist3
                        artist_string = ""
                        for artist in result_info['artists']:
                            if artist_string == "":
                                artist_string = artist['name'] 
                            else:
                                artist_string = artist_string + ", " + artist['name']
                        
                        # Create embed, populate it with information
                        embed = discord.Embed(title = f"{result_info['name']} - {artist_string} (Album)", description = songlist_string)
                        embed.set_thumbnail(url = result_info["images"][0]["url"])
                        embed.set_footer(text = f"Message by {message.author.name} - Link {i}/{len(messageTargetURLs)}", icon_url = message.author.avatar.url)

                        view = View()

                        # Add Dismiss Embed Button
                        async def deleteCallback(interaction: discord.Interaction):
                            await interaction.response.defer()
                            
                            # If attempt is from message creator...
                            if interaction.user.id == message.author.id:
                                # We delete the message
                                await msg.delete()
                            # Else...
                            else:
                                # Display permission error that deletes after 3 seconds
                                embed = discord.Embed(title = f"Error", description = f"{interaction.user.mention}, you are not the message OP.", color = Color.red())
                                await message.channel.send(embed = embed, delete_after=3)
                        
                        # Add Dismiss button, define callback as deleteCallback
                        delete_button = discord.ui.Button(label=f'Dismiss Embed', style=discord.ButtonStyle.red)
                        delete_button.callback = deleteCallback
                        view.add_item(delete_button)
                        
                        # Add Open in Spotify button
                        spotify_button = discord.ui.Button(label=f'Show on Spotify', style=discord.ButtonStyle.url, url=result_info["external_urls"]["spotify"])
                        view.add_item(spotify_button)

                        # Add Search on YT Music button
                        ytm_button = discord.ui.Button(label='Search on YT Music', style=discord.ButtonStyle.url, url=f'https://music.youtube.com/search?q={(quote(result_info["name"])).replace("%2B", "+")}+{(quote(artist_string)).replace("%2B", "+")}')
                        view.add_item(ytm_button)

                        # Add Search on Google button
                        google_button = discord.ui.Button(label='Search on Google', style=discord.ButtonStyle.url, url=f'https://www.google.com/search?q={(quote(result_info["name"])).replace("%2B", "+")}+{(quote(artist_string)).replace("%2B", "+")}')
                        view.add_item(google_button)

                        msg = await message.reply(embed = embed, view = view, mention_author = False)
                    elif "playlist" in url:
                        # Search playlist on Spotify
                        result_info = sp.playlist(url, market="GB")
                        
                        # Variables
                        i = 0
                        pages = []
                        pageStr = ""

                        # Work through all tracks in playlist, adding them to a page
                        for playlist_item in result_info['tracks']['items']:
                            i += 1
                            artist_string = ""

                            # Check if item is a track, podcast, unavailable in current reigon or unknown
                            if playlist_item['track'] == None:
                                # Item type is unavailable in the GB reigon
                                # If there's nothing in the current page, make a new one
                                if pageStr == "":
                                    pageStr = f"**{i}:** *(Media Unavailable)*"
                                # Else, add string to existing page
                                else:
                                    pageStr = f"{pageStr}\n**{i}:** *(Media Unavailable)*"
                            elif playlist_item['track']['type'] == "track":
                                # Item is a track
                                # Work through all artists of item
                                for artist in playlist_item['track']['artists']:
                                    # If there is no artists already in the artist string
                                    if artist_string == "":
                                        # We set the artist string to the artist we're currently on
                                        artist_string = artist['name']
                                    else:
                                        # Else, we add the current artist to the existing artist string
                                        artist_string = f"{artist_string}, {artist['name']}"
                                
                                # If there's nothing in the current page, make a new one
                                if pageStr == "":
                                    pageStr = f"**{i}: {playlist_item['track']['name'].replace('*', '-')}** - {artist_string}"
                                # Else, add string to existing page
                                else:
                                    pageStr = f"{pageStr}\n**{i}: {playlist_item['track']['name'].replace('*', '-')}** - {artist_string}"
                            elif playlist_item['track']['type'] == "episode":
                                # Item is a podcast
                                if pageStr == "":
                                    pageStr = f"**{i}: {playlist_item['track']['album']['name'].replace('*', '-')}** - {playlist_item['track']['name'].replace('*', '-')} (Podcast)"
                                else:
                                    pageStr = f"{pageStr}\n**{i}: {playlist_item['track']['album']['name'].replace('*', '-')}** - {playlist_item['track']['name'].replace('*', '-')} (Podcast)"
                            else:
                                # Item type is unknown / unsupported
                                # If there's nothing in the current page, make a new one
                                if pageStr == "":
                                    pageStr = f"**{i}:** *(Unknown Media Type)*"
                                # Else, add string to existing page
                                else:
                                    pageStr = f"{pageStr}\n**{i}:** *(Unknown Media Type)*"

                            # If there's 25 items in the current page, we split it into a new page
                            if i % 25 == 0:
                                pages.append(pageStr)
                                pageStr = ""

                        # If there is still data in pageStr, add it to a new page
                        if pageStr != "":
                            pages.append(pageStr)
                            pageStr = ""

                        # If there are more than 100 items in the playlist, we add a notice to the final page
                        if result_info['tracks']['total'] > 100:
                            pages[-1] = f"{pages[-1]}\n\n**+{result_info['tracks']['total'] - 100} items**"
                        # Define page view
                        class PlaylistPagesController(View):
                            # Init
                            def __init__(self, pages):
                                super().__init__()
                                self.page = 0
                                self.pages = pages
                                
                                # Add Dismiss Embed Button
                                async def deleteCallback(interaction: discord.Interaction):
                                    await interaction.response.defer()
                                    
                                    # If attempt is from message creator...
                                    if interaction.user.id == message.author.id:
                                        # We delete the message
                                        await msg.delete()
                                    # Else...
                                    else:
                                        # Display permission error that deletes after 3 seconds
                                        embed = discord.Embed(title = f"Error", description = f"{interaction.user.mention}, you are not the message OP.", color = Color.red())
                                        await message.channel.send(embed = embed, delete_after=3)
                                
                                # Add Dismiss button, define callback as deleteCallback
                                delete_button = discord.ui.Button(label=f'Dismiss Embed', style=discord.ButtonStyle.red)
                                delete_button.callback = deleteCallback
                                view.add_item(delete_button)
                        
                            # Previous page button
                            @discord.ui.button(label="<", style=ButtonStyle.green, custom_id="prev")
                            async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                await interaction.response.defer()
                                if self.page > 0:
                                    self.page -= 1
                                else:
                                    self.page = len(self.pages) - 1
                                embed = discord.Embed(title = f"{result_info['name']} (Playlist)", description = f"by {result_info['owner']['display_name']} - {result_info['tracks']['total']} items\n\n{self.pages[self.page]}", color = Color.random())
                                embed.set_thumbnail(url = result_info['images'][0]['url'])
                                embed.set_footer(text = f"Requested by {interaction.user.name} - Page {self.page + 1}/{len(pages)}")
                                await msg.edit(embed = embed)

                            # Next page button
                            @discord.ui.button(label=">", style=ButtonStyle.green, custom_id="next")
                            async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                                await interaction.response.defer()
                                if self.page < len(self.pages) - 1:
                                    self.page += 1
                                else:
                                    self.page = 0
                                embed = discord.Embed(title = f"{result_info['name']} (Playlist)", description = f"by {result_info['owner']['display_name']} - {result_info['tracks']['total']} items\n\n{self.pages[self.page]}", color = Color.random())
                                embed.set_thumbnail(url = result_info['images'][0]['url'])
                                embed.set_footer(text = f"Message by {message.author.name} - Page {self.page + 1}/{len(pages)}")
                                await msg.edit(embed = embed)

                        # Create embed, populate it with information
                        embed = discord.Embed(title = f"{result_info['name']} (Playlist)", description = f"by {result_info['owner']['display_name']} - {result_info['tracks']['total']} items\n\n{pages[0]}", color = Color.random())
                        embed.set_thumbnail(url = result_info['images'][0]['url'])
                        embed.set_footer(text = f"Message by {message.author.name} - Page 1/{len(pages)}", icon_url = message.author.avatar.url)
                        
                        # If there's only 1 page, make embed without page buttons
                        if len(pages) == 1:
                            # Add Open in Spotify button
                            view = View()
                            spotify_button = discord.ui.Button(label=f'Show on Spotify', style=discord.ButtonStyle.url, url=result_info["external_urls"]["spotify"])
                            view.add_item(spotify_button)
                            
                            msg = await message.reply(embed = embed, view = view)
                        # Else, make embed with page buttons
                        else:
                            msg = await message.reply(embed = embed, view = PlaylistPagesController(pages))     
                    else:
                        pass
                except Exception:
                    pass
                await asyncio.sleep(2)

# --- UTIL COMMANDS ---

# Ping command
@tree.command(name = "ping", description = "Ping the bot.")
async def self(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(title = "Pong!")
    embed.add_field(name = "Latency", value = f"{round(client.latency*1000, 2)}ms")
    await interaction.followup.send(embed = embed)

# Restart Bot command
@tree.command(name = "restart", description = "Restart the bot.")
async def self(interaction: discord.Interaction):
    await interaction.response.defer()
    if interaction.user.id == restart_id:
        embed = discord.Embed(title = "The bot will restart.", color = Color.green())
        await interaction.followup.send(embed = embed, ephemeral = True)
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        embed = discord.Embed(title = "You do not have permission to run this command.", color = Color.red())
        await interaction.followup.send(embed = embed, ephemeral = True)

# Info command
@tree.command(name = "info", description = "Info about the bot.")
async def self(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(title = "Info")
    embed.add_field(name = "Credit", value = "Bot created by Restart (<@563372552643149825>)\n\nBot Framework\n[discord.py](https://github.com/Rapptz/discord.py)\n\nAPIs and Modules:\n[Cat API](https://thecatapi.com/)\n[Dog API](https://dog.ceo/dog-api/)\n[Lyrics API](https://lrclib.net/)\n[Spotipy Module](https://github.com/spotipy-dev/spotipy)\n[Wikipedia Module](https://github.com/goldsmith/Wikipedia)")
    await interaction.followup.send(embed = embed)

# PFP command
@tree.command(name = "pfp", description = "Show a user's PFP.")
async def self(interaction: discord.Interaction, user: discord.User):
	await interaction.response.defer()
	# Idea: set embed colour to user's banner colour'
	embed = discord.Embed(title = f"PFP - {user.name}")
	embed.set_image(url = user.avatar.url)
	embed.set_footer(text = f"Requested by {interaction.user.name} - right click or long press to save image", icon_url = interaction.user.avatar.url)
	# Send Embed
	await interaction.followup.send(embed = embed)

# Host Info command
@tree.command(name = "host-info", description = "Info about the bot host.")
async def self(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(title = "Host Info", color=Color.random())

    sec = timedelta(seconds=int(time.monotonic()))
    d = datetime(1,1,1) + sec

    embed.add_field(name = "CPU Name", value = cpuinfo.get_cpu_info()['brand_raw'], inline = False)
    #embed.add_field(name = "Percent CPU Usage", value = psutil.cpu_percent(), inline = False)
    #embed.add_field(name = "Percent RAM Usage", value = psutil.virtual_memory().percent, inline = False)
    embed.add_field(name = "Percent CPU Usage", value = "Temporarily Disabled", inline = False)
    embed.add_field(name = "Percent RAM Usage", value = "Temporarily Disabled", inline = False)
    embed.add_field(name = "System Uptime", value = ("%d:%d:%d:%d" % (d.day-1, d.hour, d.minute, d.second)), inline = False)
    embed.add_field(name = "OS Name", value = os.name, inline = False)
    embed.add_field(name = "Bot Latency", value = f"{round(client.latency*1000, 2)}ms", inline = False)
    embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)

    await interaction.followup.send(embed = embed)

# --- ANIMAL COMMANDS ---

# Cat command
@tree.command(name = "cat", description = "Get a random cat picture.")
@app_commands.checks.cooldown(1, 5)
async def self(interaction: discord.Interaction):
    await interaction.response.defer()
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    response.json()
    embed_title = random.choice(cat_titles)
    embed = discord.Embed(title = embed_title)
    embed.set_image(url = response.json()[0]["url"])
    await interaction.followup.send(embed = embed)

# Dog command
@tree.command(name = "dog", description = "Get a random dog picture.")
@app_commands.checks.cooldown(1, 5)
async def self(interaction: discord.Interaction):
    await interaction.response.defer()
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    response.json()
    embed_title = random.choice(dog_titles)
    embed = discord.Embed(title = embed_title)
    embed.set_image(url = response.json()["message"])
    await interaction.followup.send(embed = embed)

# --- SONG COMMANDS ---

# Lyrics command
@tree.command(name = "lyrics", description = "Find Lyrics to a song.")
@app_commands.checks.cooldown(1, 10)
async def self(interaction: discord.Interaction, search: str):
    try:    
        await interaction.response.defer()

        # Define lists
        options = []
        song_list = []
        artist_list = []
        album_list = []
        id_list = []
        lyrics_list = []

        # Clean up user input
        search = search.replace(" ", "%20")
        search = search.lower()

        # Send initial embed
        embed = discord.Embed(title = "Searching...")
        embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
        await interaction.followup.send(embed = embed)

        # Create URL
        request_url = f"https://lrclib.net/api/search?q={search}"

        # Change %20 back to " "
        search = search.replace("%20", " ")

        # Send request to LRCLib
        request = requests.get(request_url)
        request_data = request.json()
        
        # Check if result is blank
        if request_data == []:
            embed = discord.Embed(title = "Error", description="No results were found.", color = Color.red())
            await interaction.edit_original_response(embed = embed)
        else:
            # Sort through request data, add required info to lists
            for song in request_data:
                song_list.append(song['name'])
                artist_list.append(song['artistName'])
                album_list.append(song['albumName'])
                id_list.append(song['id'])
                lyrics_list.append(song['plainLyrics'])

            # Generate dropdown values
            if len(song_list) > 5:
                embed = discord.Embed(title = "Select Song", description = f'Found 5 results for "{search}"', color = Color.random())
                embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
                for i in range(0,5):
                    # Handle strings being too long
                    if len(song_list[i]) > 100:
                        song_name = song_list[i][:97] + "..."
                    else:
                        song_name = song_list[i]
                    if len(f"{artist_list[i]} - {album_list[i]}") > 100:
                        list_description = f"{artist_list[i]} - {album_list[i]}"[:97] + "..."
                    else:
                        list_description = f"{artist_list[i]} - {album_list[i]}"
                    options.append(discord.SelectOption(label = song_name, description = list_description, value = id_list[i]))
            else:
                embed = discord.Embed(title = "Select Song", description = f'Found {len(song_list)} results for "{search}"', color = Color.random())
                embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
                for i in range(0, len(song_list)):
                    # Handle strings being too long
                    if len(song_list[i]) > 100:
                        song_name = song_list[i][:97] + "..."
                    else:
                        song_name = song_list[i]
                    if len(f"{artist_list[i]} - {album_list[i]}") > 100:
                        list_description = f"{artist_list[i]} - {album_list[i]}"[:97] + "..."
                    else:
                        list_description = f"{artist_list[i]} - {album_list[i]}"
                    options.append(discord.SelectOption(label = song_name, description = list_description, value = id_list[i]))

            # Define options
            select = Select(options=options)

            # Response to user selection
            async def response(interaction: discord.Interaction):
                await interaction.response.defer()
                # Find unique ID of selection in the list
                list_place = id_list.index(int(select.values[0]))
                
                try:
                    lyrics_split = lyrics_list[list_place].split("\n\n")

                    paged_lyrics = []
                    current_page = ""

                    for paragraph in lyrics_split:
                        if len(paragraph) + len(current_page) < 2200:
                            current_page = current_page + "\n\n" + paragraph
                        else:
                            paged_lyrics.append(current_page)
                            current_page = ""
                            current_page = current_page + paragraph

                    paged_lyrics.append(current_page)

                    # Create lyric embed
                    embed = discord.Embed(title = f"{song_list[list_place]} - {artist_list[list_place]}", description = paged_lyrics[0], color = Color.random())
                    
                    class PaginationView(View):
                        def __init__(self, pages):
                            super().__init__()
                            self.page = 0
                            self.pages = pages
                            google_button = discord.ui.Button(label='Search on Google', style=discord.ButtonStyle.url, url=f'https://www.google.com/search?q={song_list[list_place].replace(" ", "+")}+{artist_list[list_place].replace(" ", "+")}')
                            self.add_item(google_button)
                    
                        @discord.ui.button(label="<", style=ButtonStyle.green, custom_id="prev")
                        async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                            if self.page > 0:
                                self.page -= 1
                            else:
                                self.page = len(self.pages) - 1
                            embed = discord.Embed(title = f"{song_list[list_place]} - {artist_list[list_place]}", description = self.pages[self.page], color = Color.random())
                            embed.set_footer(text = f"Page {self.page + 1}/{len(paged_lyrics)}")
                            await interaction.response.edit_message(embed = embed)

                        @discord.ui.button(label=">", style=ButtonStyle.green, custom_id="next")
                        async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                            if self.page < len(self.pages) - 1:
                                self.page += 1
                            else:
                                self.page = 0
                            embed = discord.Embed(title = f"{song_list[list_place]} - {artist_list[list_place]}", description = self.pages[self.page], color = Color.random())
                            embed.set_footer(text = f"Page {self.page + 1}/{len(paged_lyrics)}")
                            await interaction.response.edit_message(embed = embed)

                    if len(paged_lyrics) == 1:
                        google_button = discord.ui.Button(label='Search on Google', style=discord.ButtonStyle.url, url=f'https://www.google.com/search?q={(quote(song_list[list_place])).replace("%2B", "+")}+{(quote(artist_list[list_place])).replace("%2B", "+")}')
                        view = View()
                        view.add_item(google_button)
                        embed.set_footer(text = f"Lryics - Page 1/1")
                        await interaction.edit_original_response(embed = embed, view = view)
                    else:
                        embed.set_footer(text = f"Lyrics - Page 1/{len(paged_lyrics)}")
                        await interaction.edit_original_response(embed = embed, view = PaginationView(paged_lyrics))
                except AttributeError:
                    google_button = discord.ui.Button(label='Search on Google', style=discord.ButtonStyle.url, url=f'https://www.google.com/search?q={(quote(song_list[list_place])).replace("%2B", "+")}+{(quote(artist_list[list_place])).replace("%2B", "+")}')
                    view = View()
                    view.add_item(google_button)
                    embed = discord.Embed(title = f"{song_list[list_place]} - {artist_list[list_place]}", description = "The song has no lyrics.", color = Color.red())
                    await interaction.edit_original_response(embed = embed, view = view)
            
            # Set up list with provided values
            select.callback = response
            view = View()
            view.add_item(select)

            # Edit initial message to show dropdown
            await interaction.edit_original_response(embed = embed, view = view)
    except Exception as error:
        embed = discord.Embed(title = "Lyrics - Error", description = "An unknown error has occurred. The error has been logged.")
        print("[LYRICS] Error has occurred. Error below:")
        print(error)
        await interaction.edit_original_response(embed = embed, view = None, ephemeral = True)

# Spotify Search command
@tree.command(name = "spotify", description = "Search Spotify.")
@app_commands.checks.cooldown(1, 10)
@app_commands.choices(search_type=[
        app_commands.Choice(name="Song", value="song"),
        app_commands.Choice(name="Artist", value="artist"),
        ])
async def self(interaction: discord.Interaction, search_type: app_commands.Choice[str], search: str):
    await interaction.response.defer()
    try:
        if search_type.value == "song":
            # Define lists
            options = []
            song_list = []
            artist_list = []
            album_list = []
            explicit_list = []
            duration_list = []
            art_list = []
            url_list = []
            id_list = []
            artist_string = ""

            # Send initial embed
            embed = discord.Embed(title = "Searching...")
            embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
            await interaction.followup.send(embed = embed)

            # Search Spotify
            result = sp.search(search, type = 'track')
            
            # Check if result is blank
            if len(result['tracks']['items']) == 0:
                embed = discord.Embed(title = "Error", description="No results were found.", color = Color.red())
                await interaction.edit_original_response(embed = embed)
            else:
                # Sort through request data, add required info to lists
                for i in range(0,len(result['tracks']['items'])):
                    song_list.append(result['tracks']['items'][i]['name'])
                    for artist in result['tracks']['items'][i]['artists']:
                        if artist_string == "":
                            artist_string = artist['name']
                        else:
                            artist_string = f"{artist_string}, {artist['name']}"
                    artist_list.append(artist_string)
                    album_list.append(result['tracks']['items'][i]['album']['name'])
                    explicit_list.append(result['tracks']['items'][i]['explicit'])
                    duration_list.append(result['tracks']['items'][i]['duration_ms'])
                    art_list.append(result['tracks']['items'][i]['album']['images'][0]['url'])
                    url_list.append(result['tracks']['items'][i]['external_urls']['spotify'])
                    id_list.append(result['tracks']['items'][i]['id'])

                # Generate dropdown values
                if len(song_list) > 5:
                    embed = discord.Embed(title = "Select Song", description = f'Found 5 results for "{search}"', color = Color.random())
                    embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
                    for i in range(0,5):
                        # Handle description being too long
                        if len(f"{artist_list[i]} - {album_list[i]}") > 100:
                            list_description = f"{artist_list[i]} - {album_list[i]}"[:97] + "..."
                        else:
                            list_description = f"{artist_list[i]} - {album_list[i]}"
                        # Add explicit label if song is explicit, handle title being too long
                        if explicit_list[i] == True:
                            if len(song_list[i]) > 86:
                                song_name = song_list[i][:86] + "... (Explicit)"
                            else:
                                song_name = song_list[i] + " (Explicit)"
                        else:
                            if len(song_list[i]) > 100:
                                song_name = song_list[i][:97] + "..."
                            else:
                                song_name = song_list[i]
                        options.append(discord.SelectOption(label = song_name, description = list_description, value = id_list[i]))
                else:
                    embed = discord.Embed(title = "Select Song", description = f'Found {len(song_list)} results for "{search}"', color = Color.random())
                    embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
                    for i in range(0, len(song_list)):
                        # Handle description being too long
                        if len(f"{artist_list[i]} - {album_list[i]}") > 100:
                            list_description = f"{artist_list[i]} - {album_list[i]}"[:97] + "..."
                        else:
                            list_description = f"{artist_list[i]} - {album_list[i]}"
                        # Add explicit label if song is explicit, handle title being too long
                        if explicit_list[i] == True:
                            if len(song_list[i]) > 86:
                                song_name = song_list[i][:86] + "... (Explicit)"
                            else:
                                song_name = song_list[i] + " (Explicit)"
                        else:
                            if len(song_list[i]) > 100:
                                song_name = song_list[i][:97] + "..."
                            else:
                                song_name = song_list[i]
                        options.append(discord.SelectOption(label = song_name, description = list_description, value = id_list[i]))

                # Define options
                select = Select(options=options)

                # Response to user selection
                async def response(interaction: discord.Interaction):
                    await interaction.response.defer()
                    # Find unique ID of selection in the list
                    list_place = id_list.index(select.values[0])
                    
                    # Set up new embed
                    if explicit_list[list_place] == True:
                        embed = discord.Embed(title = f"{song_list[list_place]} (Explicit)", color = Color.random())
                    else:
                        embed = discord.Embed(title = song_list[list_place], color = Color.random())
                    embed.set_thumbnail(url = art_list[list_place])
                    embed.add_field(name = "Artists", value = artist_list[list_place], inline = True)
                    embed.add_field(name = "Album", value = album_list[list_place], inline = True)
                    embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)

                    # Define View
                    view = View()
                    
                    seconds, duration_list[list_place] = divmod(duration_list[list_place], 1000)
                    minutes, seconds = divmod(seconds, 60)

                    # Add Open in Spotify button
                    spotify_button = discord.ui.Button(label=f'Play on Spotify ({int(minutes):02d}:{int(seconds):02d})', style=discord.ButtonStyle.url, url=url_list[list_place])
                    view.add_item(spotify_button)
                    
                    # Add Search on YT Music button
                    ytm_button = discord.ui.Button(label='Search on YT Music', style=discord.ButtonStyle.url, url=f'https://music.youtube.com/search?q={(quote(song_list[list_place])).replace("%2B", "+")}+{(quote(artist_list[list_place])).replace("%2B", "+")}')
                    view.add_item(ytm_button)

                    # Add Search on Google button
                    google_button = discord.ui.Button(label='Search on Google', style=discord.ButtonStyle.url, url=f'https://www.google.com/search?q={(quote(song_list[list_place])).replace("%2B", "+")}+{(quote(artist_list[list_place])).replace("%2B", "+")}')
                    view.add_item(google_button)
                    
                    # Send new embed
                    await interaction.edit_original_response(embed = embed, view = view)
                
                # Set up list with provided values
                select.callback = response
                view = View()
                view.add_item(select)

                # Edit initial message to show dropdown
                await interaction.edit_original_response(embed = embed, view = view)
        elif search_type.value == "artist":
            artist_list = []
            id_list = []
            options = []
            
            # Send initial embed
            embed = discord.Embed(title = "Searching...")
            embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
            await interaction.followup.send(embed = embed)

            # Search Spotify
            result = sp.search(search, type = 'artist')
            
            # Check if result is blank
            if len(result['artists']['items']) == 0:
                embed = discord.Embed(title = "Error", description="No results were found.", color = Color.red())
                await interaction.edit_original_response(embed = embed)
            else:
                for i in range(0,len(result['artists']['items'])):
                    # Sort through request data, add required info to lists
                    artist_list.append(result['artists']['items'][i]['name'])
                    id_list.append(result['artists']['items'][i]['id'])

                # Generate dropdown values
                if len(artist_list) > 5:
                    embed = discord.Embed(title = "Select Artist", description = f'Found 5 results for "{search}"', color = Color.random())
                    embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
                    for i in range(0,5):
                        options.append(discord.SelectOption(label = artist_list[i], value = id_list[i]))
                else:
                    embed = discord.Embed(title = "Select Artist", description = f'Found {len(song_list)} results for "{search}"', color = Color.random())
                    embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
                    for i in range(0, len(song_list)):
                        embed = discord.Embed(title = "Select Artist", description = f'Found 5 results for "{search}"', color = Color.random())
                        embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
                        for i in range(0,5):
                            options.append(discord.SelectOption(label = artist_list[i], value = id_list[i]))
            
            # Define options
            select = Select(options=options)

            # Response to user selection
            async def response(interaction: discord.Interaction):
                await interaction.response.defer()

                list_place = id_list.index(select.values[0])
                
                # Fetch artist info
                result_info = sp.artist(id_list[list_place])
                print(result_info)

                # Fetch artist top songs
                result_top_tracks = sp.artist_top_tracks(id_list[list_place])

                embed = discord.Embed(title = f"{result_info['name']}")
                embed.add_field(name = "Followers", value = f"{result_info['followers']['total']:,}")
                embed.set_thumbnail(url = result_info["images"][0]["url"])
                
                topsong_string = ""
                for i in range(0,5):
                    artist_string = ""
                    for artist in result_top_tracks['tracks'][i]['artists']:
                        if artist_string == "":
                            artist_string = artist['name'] 
                        else:
                            artist_string = f"{artist_string}, {artist['name']}"
                            
                    if topsong_string == "":
                        topsong_string = f"**{i + 1}: {result_top_tracks['tracks'][i]['name']}** - {artist_string}"
                    else:
                        topsong_string = f"{topsong_string}\n**{i + 1}: {result_top_tracks['tracks'][i]['name']}** - {artist_string}"
                
                embed.add_field(name = "Top Songs", value = topsong_string, inline = False)

                view = View()
                
                # Add Open in Spotify button
                spotify_button = discord.ui.Button(label=f'Show on Spotify', style=discord.ButtonStyle.url, url=result_info["external_urls"]["spotify"])
                view.add_item(spotify_button)

                # Add Search on YT Music button
                ytm_button = discord.ui.Button(label='Search on YT Music', style=discord.ButtonStyle.url, url=f'https://music.youtube.com/search?q={(quote(result_info["name"])).replace("%2B", "+")}')
                view.add_item(ytm_button)

                # Add Search on Google button
                google_button = discord.ui.Button(label='Search on Google', style=discord.ButtonStyle.url, url=f'https://www.google.com/search?q={(quote(result_info["name"])).replace("%2B", "+")}')
                view.add_item(google_button)

                await interaction.edit_original_response(embed = embed, view = view)

            # Set up list with provided values
            select.callback = response
            view = View()
            view.add_item(select)

            # Edit initial message to show dropdown
            await interaction.edit_original_response(embed = embed, view = view)

    except Exception as error:
        embed = discord.Embed(title = "Spotify - Error", description = "An unknown error has occurred. The error has been logged.")
        print("[SPOTIFY] Error has occurred. Error below:")
        print(error)
        await interaction.edit_original_response(embed = embed, view = None, ephemeral = True)

# Spotify URL command
@tree.command(name = "spotify_url", description = "Get info about a Spotify song, artist, album or playlist.")
@app_commands.checks.cooldown(1, 10)
async def self(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    
    embed = discord.Embed(title = "Searching...")
    embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
    await interaction.followup.send(embed = embed)

    artist_string = ""

    try:
        if "track" in url:
            result = sp.track(url)
            
            if result['explicit'] == True:
                embed = discord.Embed(title = f"{result['name']} (Explicit)", color = Color.random())
            else:
                embed = discord.Embed(title = f"{result['name']}", color = Color.random())

            for artist in result['artists']:
                if artist_string == "":
                    artist_string = artist['name']
                else:
                    artist_string = f"{artist_string}, {artist['name']}"
            
            embed.add_field(name = "Artists", value = artist_string, inline = True)
            embed.add_field(name = "Album", value = result['album']["name"], inline = True)
            embed.set_thumbnail(url = result["album"]["images"][0]["url"])
            embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)

            view = View()
                        
            seconds, result['duration_ms'] = divmod(result['duration_ms'], 1000)
            minutes, seconds = divmod(seconds, 60)

            # Add Open in Spotify button
            spotify_button = discord.ui.Button(label=f'Play on Spotify ({int(minutes):02d}:{int(seconds):02d})', style=discord.ButtonStyle.url, url=result["external_urls"]["spotify"])
            view.add_item(spotify_button)
            
            # Add Search on YT Music button
            ytm_button = discord.ui.Button(label='Search on YT Music', style=discord.ButtonStyle.url, url=f'https://music.youtube.com/search?q={(quote(result["name"])).replace("%2B", "+")}+{(quote(artist_string)).replace("%2B", "+")}')
            view.add_item(ytm_button)

            # Add Search on Google button
            google_button = discord.ui.Button(label='Search on Google', style=discord.ButtonStyle.url, url=f'https://www.google.com/search?q={(quote(result["name"])).replace("%2B", "+")}+{(quote(artist_string)).replace("%2B", "+")}')
            view.add_item(google_button)
            
            # Send new embed
            await interaction.edit_original_response(embed = embed, view = view)
        elif "artist" in url:
            # Fetch artist info
            result_info = sp.artist(url)

            # Fetch artist top songs
            result_top_tracks = sp.artist_top_tracks(url)

            embed = discord.Embed(title = f"{result_info['name']}", color = Color.random())
            embed.add_field(name = "Followers", value = f"{result_info['followers']['total']:,}")
            embed.set_thumbnail(url = result_info["images"][0]["url"])
            embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
            
            topsong_string = ""
            for i in range(0,5):
                artist_string = ""
                for artist in result_top_tracks['tracks'][i]['artists']:
                    if artist_string == "":
                        artist_string = artist['name'] 
                    else:
                        artist_string = f"{artist_string}, {artist['name']}"
                        
                if topsong_string == "":
                    topsong_string = f"**{i + 1}: {result_top_tracks['tracks'][i]['name']}** - {artist_string}"
                else:
                    topsong_string = f"{topsong_string}\n**{i + 1}: {result_top_tracks['tracks'][i]['name']}** - {artist_string}"
            
            embed.add_field(name = "Top Songs", value = topsong_string, inline = False)

            view = View()
            
            # Add Open in Spotify button
            spotify_button = discord.ui.Button(label=f'Show on Spotify', style=discord.ButtonStyle.url, url=result_info["external_urls"]["spotify"])
            view.add_item(spotify_button)

            # Add Search on YT Music button
            ytm_button = discord.ui.Button(label='Search on YT Music', style=discord.ButtonStyle.url, url=f'https://music.youtube.com/search?q={(quote(result_info["name"])).replace("%2B", "+")}+{(quote(artist_string)).replace("%2B", "+")}')
            view.add_item(ytm_button)

            # Add Search on Google button
            google_button = discord.ui.Button(label='Search on Google', style=discord.ButtonStyle.url, url=f'https://www.google.com/search?q={(quote(result_info["name"])).replace("%2B", "+")}+{(quote(artist_string)).replace("%2B", "+")}')
            view.add_item(google_button)

            await interaction.edit_original_response(embed = embed, view = view)
        elif "album" in url:
            # Fetch artist info
            result_info = sp.album(url)

            songlist_string = ""
            for i in range(len(result_info['tracks']['items'])):
                artist_string = ""
                for artist in result_info['tracks']['items'][i]['artists']:
                    if artist_string == "":
                        artist_string = artist['name'] 
                    else:
                        artist_string = artist_string + ", " + artist['name']
                        
                if songlist_string == "":
                    songlist_string = f"**{i + 1}: {result_info['tracks']['items'][i]['name']}** - {artist_string}"
                else:
                    songlist_string = f"{songlist_string}\n**{i + 1}: {result_info['tracks']['items'][i]['name']}** - {artist_string}"

            artist_string = ""
            for artist in result_info['artists']:
                if artist_string == "":
                    artist_string = artist['name'] 
                else:
                    artist_string = artist_string + ", " + artist['name']
            
            embed = discord.Embed(title = f"{result_info['name']} - {artist_string}", description = songlist_string, color = Color.random())
            embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)

            embed.set_thumbnail(url = result_info["images"][0]["url"])

            view = View()
            
            # Add Open in Spotify button
            spotify_button = discord.ui.Button(label=f'Show on Spotify', style=discord.ButtonStyle.url, url=result_info["external_urls"]["spotify"])
            view.add_item(spotify_button)

            # Add Search on YT Music button
            ytm_button = discord.ui.Button(label='Search on YT Music', style=discord.ButtonStyle.url, url=f'https://music.youtube.com/search?q={(quote(result_info["name"])).replace("%2B", "+")}+{(quote(artist_string)).replace("%2B", "+")}')
            view.add_item(ytm_button)

            # Add Search on Google button
            google_button = discord.ui.Button(label='Search on Google', style=discord.ButtonStyle.url, url=f'https://www.google.com/search?q={(quote(result_info["name"])).replace("%2B", "+")}+{(quote(artist_string)).replace("%2B", "+")}')
            view.add_item(google_button)

            await interaction.edit_original_response(embed = embed, view = view)
        elif "playlist" in url:
            # Search playlist on Spotify
            result_info = sp.playlist(url, market="GB")
            
            # Variables
            i = 0
            pages = []
            pageStr = ""

            # Work through all tracks in playlist, adding them to a page
            for playlist_item in result_info['tracks']['items']:
                i += 1
                artist_string = ""

                # Check if item is a track, podcast, unavailable in current reigon or unknown
                if playlist_item['track'] == None:
                    # Item type is unavailable in the GB reigon
                    # If there's nothing in the current page, make a new one
                    if pageStr == "":
                        pageStr = f"**{i}:** *(Media Unavailable)*"
                    # Else, add string to existing page
                    else:
                        pageStr = f"{pageStr}\n**{i}:** *(Media Unavailable)*"
                elif playlist_item['track']['type'] == "track":
                    # Item is a track
                    # Work through all artists of item
                    for artist in playlist_item['track']['artists']:
                        # If there is no artists already in the artist string
                        if artist_string == "":
                            # We set the artist string to the artist we're currently on
                            artist_string = artist['name']
                        else:
                            # Else, we add the current artist to the existing artist string
                            artist_string = f"{artist_string}, {artist['name']}"
                    
                    # If there's nothing in the current page, make a new one
                    if pageStr == "":
                        pageStr = f"**{i}: {playlist_item['track']['name']}** - {artist_string}"
                    # Else, add string to existing page
                    else:
                        pageStr = f"{pageStr}\n**{i}: {playlist_item['track']['name']}** - {artist_string}"
                elif playlist_item['track']['type'] == "episode":
                    # Item is a podcast
                    if pageStr == "":
                        pageStr = f"**{i}: {playlist_item['track']['album']['name']}** - {playlist_item['track']['name']} (Podcast)"
                    else:
                        pageStr = f"{pageStr}\n**{i}: {playlist_item['track']['album']['name']}** - {playlist_item['track']['name']} (Podcast)"
                else:
                    # Item type is unknown / unsupported
                    # If there's nothing in the current page, make a new one
                    if pageStr == "":
                        pageStr = f"**{i}:** *(Unknown Media Type)*"
                    # Else, add string to existing page
                    else:
                        pageStr = f"{pageStr}\n**{i}:** *(Unknown Media Type)*"

                # If there's 25 items in the current page, we split it into a new page
                if i % 25 == 0:
                    pages.append(pageStr)
                    pageStr = ""

            # If there is still data in pageStr, add it to a new page
            if pageStr != "":
                pages.append(pageStr)
                pageStr = ""

            # If there are more than 100 items in the playlist, we add a notice to the final page
            if result_info['tracks']['total'] > 100:
                pages[-1] = f"{pages[-1]}\n\n**+{result_info['tracks']['total'] - 100} items**"

            # Define page view
            class PlaylistPagesController(View):
                def __init__(self, pages):
                    super().__init__()
                    self.page = 0
                    self.pages = pages
                    spotify_button = discord.ui.Button(label=f'Show on Spotify', style=discord.ButtonStyle.url, url=result_info["external_urls"]["spotify"])
                    self.add_item(spotify_button)
            
                @discord.ui.button(label="<", style=ButtonStyle.green, custom_id="prev")
                async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if self.page > 0:
                        self.page -= 1
                    else:
                        self.page = len(self.pages) - 1
                    embed = discord.Embed(title = f"{result_info['name']} (Playlist)", description = f"by {result_info['owner']['display_name']} - {result_info['tracks']['total']} items\n\n{self.pages[self.page]}", color = Color.random())
                    embed.set_thumbnail(url = result_info['images'][0]['url'])
                    embed.set_footer(text = f"Requested by {interaction.user.name} - Page {self.page + 1}/{len(pages)}")
                    await interaction.response.edit_message(embed = embed)

                @discord.ui.button(label=">", style=ButtonStyle.green, custom_id="next")
                async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if self.page < len(self.pages) - 1:
                        self.page += 1
                    else:
                        self.page = 0
                    embed = discord.Embed(title = f"{result_info['name']} (Playlist)", description = f"by {result_info['owner']['display_name']} - {result_info['tracks']['total']} items\n\n{self.pages[self.page]}", color = Color.random())
                    embed.set_thumbnail(url = result_info['images'][0]['url'])
                    embed.set_footer(text = f"Requested by {interaction.user.name} - Page {self.page + 1}/{len(pages)}")
                    await interaction.response.edit_message(embed = embed)

            embed = discord.Embed(title = f"{result_info['name']} (Playlist)", description = f"by {result_info['owner']['display_name']} - {result_info['tracks']['total']} items\n\n{pages[0]}", color = Color.random())
            embed.set_thumbnail(url = result_info['images'][0]['url'])
            embed.set_footer(text = f"Requested by {interaction.user.name} - Page 1/{len(pages)}", icon_url = interaction.user.avatar.url)
            
            # If there's only 1 page, make embed without page buttons
            if len(pages) == 1:
                # Add Open in Spotify button
                view = View()
                spotify_button = discord.ui.Button(label=f'Show on Spotify', style=discord.ButtonStyle.url, url=result_info["external_urls"]["spotify"])
                view.add_item(spotify_button)
                
                await interaction.edit_original_response(embed = embed, view = view)
            # Else, make embed with page buttons
            else:
                await interaction.edit_original_response(embed = embed, view = PlaylistPagesController(pages))     
        else:
            embed = discord.Embed(title = "Spotify - Error", description = "Error while searching URL. Is it a valid and supported Spotify URL?", color = Color.red())
            embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
            await interaction.edit_original_response(embed = embed)
    except Exception:
        embed = discord.Embed(title = "Spotify - Error", description = "Error while searching URL. Is it a valid and supported Spotify URL?", color = Color.red())
        await interaction.edit_original_response(embed = embed)

# Spotify Image command
@tree.command(name = "spotify_image", description = "Get album art from a Spotify URL.")
@app_commands.checks.cooldown(1, 10)
async def self(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    
    embed = discord.Embed(title = "Searching...")
    embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
    await interaction.followup.send(embed = embed)

    artist_string = ""

    if "track" in url:
        result = sp.track(url)
        
        for artist in result['artists']:
            if artist_string == "":
                artist_string = artist['name'] 
            else:
                artist_string = f"{artist_string}, {artist['name']}"

        if result["album"]["images"] != None:
            if result["album"]["images"][0]['height'] == None or result["album"]["images"][0]['width'] == None:
                embed = discord.Embed(title = f"{result['name']} ({artist_string}) - Album Art", description = "Viewing highest quality (Resolution unknown)")
            else:
                embed = discord.Embed(title = f"{result['name']} ({artist_string}) - Album Art", description = f"Viewing highest quality ({result['album']['images'][0]['width']}x{result['album']['images'][0]['height']})")
            
            embed.set_image(url = result["album"]["images"][0]["url"])
            embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
            await interaction.edit_original_response(embed = embed)
        else:
            embed = discord.Embed(title = "No album art available.", color = Color.red)
            embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
            await interaction.edit_original_response(embed = embed)
    elif "album" in url:
        result = sp.album(url)
        
        for artist in result['artists']:
            if artist_string == "":
                artist_string = artist['name'] 
            else:
                artist_string = f"{artist_string}, {artist['name']}"

        if result["images"] != None:
            if result["images"][0]['height'] == None or result["images"][0]['width'] == None:
                embed = discord.Embed(title = f"{result['name']} ({artist_string}) - Album Art", description = "Viewing highest quality (Resolution unknown)")
            else:
                embed = discord.Embed(title = f"{result['name']} ({artist_string}) - Album Art", description = f"Viewing highest quality ({result['images'][0]['width']}x{result['images'][0]['height']})")
            embed.set_image(url = result["images"][0]["url"])
            embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
            await interaction.edit_original_response(embed = embed)
        else:
            embed = discord.Embed(title = "No album art available.", color = Color.red)
            embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
            await interaction.edit_original_response(embed = embed)

# --- MISC COMMANDS ---

# Equation Solver command (broken)
# @tree.command(name = "equation_solver", description= "Solve an equation or expression.")
# @app_commands.checks.cooldown(1, 10)
# async def self(interaction: discord.Interaction, equation: str):
#     await interaction.response.defer()
    
#     try:
#         # Send request to mathjs
#         request_url = f"http://api.mathjs.org/v4/?expr={equation.replace(' ', '%20')}"
#         request = requests.get(request_url)
#         request_data = request.json()

#         # Generate embed
#         embed = discord.Embed(title = "Equation Solver")
#         embed.add_field(name = "Equation / Expression", value = equation)
#         embed.add_field(name = "Solution", value = request_data)
#         embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)

#         # Edit loading message with new embed
#         await interaction.edit_original_response(embed = embed)
#     except Exception:
#         embed = discord.Embed(title = "Error", description = "An error has occured. Solutions:\n\n**1.** Is the expression / equation valid?\n**2.** Are you using any forbidden characters?\n**3.** Try again later.")
#         embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
#         await interaction.edit_original_response(embed = embed)

# Urban Dictionary command
@tree.command(name = "urban_dictionary", description = "Search Urban Dictionary.")
@app_commands.checks.cooldown(1,10)
async def self(interaction: discord.Interaction, query: str):
    await interaction.response.defer()

    embed = discord.Embed(title = "Searching...")
    embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
    await interaction.followup.send(embed = embed)

    try:
        query = query.replace(" ", "%20")
        request = requests.get(f"https://api.urbandictionary.com/v0/define?term={query}")
        request_data = request.json()

        item_list = []

        if len(request_data['list']) != 0:
            for item in request_data['list']:
                item_list.append(item)
            
            class UrbanDictPageView(View):
                def __init__(self, pages):
                    super().__init__(timeout = None)
                    self.page = 0
                    self.pages = pages
            
                @discord.ui.button(label="<", style=ButtonStyle.green, custom_id="prev")
                async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if self.page > 0:
                        self.page -= 1
                    else:
                        self.page = len(self.pages) - 1
                    embed = discord.Embed(title = f"{self.pages[self.page]['word']}", description = f"**Author: {self.pages[self.page]['author']}**\n\n{(self.pages[self.page]['definition'].replace('[', '')).replace(']', '')}", color = Color.random())
                    embed.set_footer(text = f"Requested by {interaction.user.name} - Page {self.page + 1}/{len(item_list)}", icon_url = interaction.user.avatar.url)
                    await interaction.response.edit_message(embed = embed)

                @discord.ui.button(label=">", style=ButtonStyle.green, custom_id="next")
                async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                    if self.page < len(self.pages) - 1:
                        self.page += 1
                    else:
                        self.page = 0
                    embed = discord.Embed(title = f"{self.pages[self.page]['word']}", description = f"**Author: {self.pages[self.page]['author']}**\n\n{(self.pages[self.page]['definition'].replace('[', '')).replace(']', '')}", color = Color.random())
                    embed.set_footer(text = f"Requested by {interaction.user.name} - Page {self.page + 1}/{len(item_list)}")
                    await interaction.response.edit_message(embed = embed)

            embed = discord.Embed(title = f"{item_list[0]['word']}", description = f"**Author: {item_list[0]['author']}**\n\n{(item_list[0]['definition'].replace('[', '')).replace(']', '')}", color = Color.random())
            embed.set_footer(text = f"Requested by {interaction.user.name} - Page 1/{len(item_list)}", icon_url = interaction.user.avatar.url)
            
            if len(item_list) == 1:
                await interaction.edit_original_response(embed = embed)
            else:
                await interaction.edit_original_response(embed = embed, view = UrbanDictPageView(item_list))
        else:
            embed = discord.Embed(title = "No results found.", color = Color.red())
            embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
            await interaction.edit_original_response(embed = embed)
    except Exception:
        embed = discord.Embed(title = "An error has occured.", description = "Please try again later or message <@563372552643149825> for assistance.")
        embed.set_footer(text = f"Requested by {interaction.user.name}", icon_url = interaction.user.avatar.url)
        await interaction.edit_original_response(embed = embed, view = None)

# Wikipedia command
@tree.command(name = "wikipedia", description = "Search Wikipedia for information.")
@app_commands.checks.cooldown(1, 5)
async def self(interaction: discord.Interaction, search: str):
    await interaction.response.defer()
    try:
        page = wikipedia.page(search)
        embed = discord.Embed(title = f"Search: {search}")
        embed.add_field(name = f"{page.title}", value = wikipedia.summary(search, sentences = 3))
        embed.add_field(name = "Read More", value = page.url)
        embed.set_footer(text = "Wikipedia", icon_url = "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png")
        await interaction.followup.send(embed = embed)
    except wikipedia.exceptions.PageError:
        embed = discord.Embed(title = "Error", description = f"No page was found on Wikipedia matching {search}. Try another search.", color = Color.red())
        embed.set_footer(text = "Wikipedia", icon_url = "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png")
        await interaction.followup.send(embed = embed, ephemeral = True)
    except wikipedia.exceptions.DisambiguationError as error:
        embed = discord.Embed(title = "Please be more specific with your query.", color = Color.red())
        embed.add_field(name = "Information", value = error)
        embed.set_footer(text = "Wikipedia", icon_url = "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png")
        await interaction.followup.send(embed = embed, ephemeral = True)
    except GuessedAtParserWarning:
        pass

# Cooldown Handler
@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
    await interaction.response.defer()
    if isinstance(error, app_commands.errors.CommandOnCooldown):
        embed = discord.Embed(title = "Cooldown", description = error, color = Color.red())
        msg = await interaction.followup.send(embed = embed, ephemeral = True)
        await asyncio.sleep(5)
        await msg.delete()

# Run bot with token
client.run(discord_token)
