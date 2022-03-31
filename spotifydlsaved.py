#!/usr/bin/python3

# TODO: arguments
# TODO: figure out what version id3 is being used

#   Copyright 2019 codeo
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from auth import spotifysecret
from auth import youtubeapikey

import ytdl_options

import spotipy
import spotipy.util as util

import youtube_dl

import requests
import mutagen.id3 as id3

import json
import re
import subprocess
import os


LIMIT = 20
ENCODING = 2


def set_id3(filename, title, artists, album):
    """
    Sets TIT2, TPE1 and TALB ID3v2 tags for filename 
    """
    print("Setting ID3 tag for " + filename)

    audio = id3.ID3(filename)

    audio.add(id3.TIT2(encoding=ENCODING, text=title))
    print("Set title " + track["name"])

    audio.add(id3.TPE1(encoding=ENCODING, text=artists))
    print("Set artists " + artists)

    audio.add(id3.TALB(encoding=ENCODING, text=album))
    print("Set album " + album)

    audio.save()
    print("Done")


if os.path.isdir("playlist"):
    print("Playlist directory exists")
else:
    subprocess.call(["mkdir", "playlist"])
    print("Playlist directory created")
print()

# spotify authentication and request
scope = "user-library-read"

token = util.prompt_for_user_token(spotifysecret.USERNAME, scope,
                                   spotifysecret.CLIENT_ID,
                                   spotifysecret.CLIENT_SECRET,
                                   spotifysecret.REDIRECT_URI)

if not token:
    print("Can't get token for", spotifysecret.USERNAME)
    exit(1)

sp = spotipy.Spotify(auth=token)

playlist_id = input("Paste playlist ID here (or \"favourites\" for saved tracks)\n> ")
if not playlist_id == "favourites":
    playlist_id = playlist_id.split(':')
    user_id = playlist_id[2]
    playlist_id = playlist_id[4]

    items = sp.user_playlist(user_id, playlist_id)

    items = items["tracks"]["items"]
else:
    res = sp.current_user_saved_tracks(limit=LIMIT)

    items = res["items"][:]

    i = 1
    while not res["next"] is None:
        res = sp.current_user_saved_tracks(limit=LIMIT, offset=(LIMIT * i))
        items += res["items"]
        i += 1

for item in items:
    track = item["track"]
    album = track["album"]["name"]

    dir_name = "playlist/" + album
    print("Creating directory " + dir_name)

    if os.path.isdir(dir_name):
        print("Directory exists")
    else:
        subprocess.call(["mkdir", dir_name])
        print("Directory created")

    # album art
    album_cover_url = track["album"]["images"][1]["url"]
    album_cover = requests.get(album_cover_url, allow_redirects=True)

    print("Album cover url:")
    print("    " + album_cover_url)

    album_cover_filename = \
            "playlist/" + album + '/' + "cover.jpg"

    if os.path.isfile(album_cover_filename):
        print("Album cover file exists, continuing")
    else:
        with open(album_cover_filename, "wb") as f:
            f.write(album_cover.content)
        print("Downloaded album cover")
    print()

    # file name
    artists = ''
    for i, a in enumerate(track["artists"]):
        artists += a["name"]
        if i < len(track["artists"]) - 1:
            artists += '/'
        """if i == len(track["artists"]) - 2:
            artists += " & "
        elif i < len(track["artists"]) - 2:
            artists += ", " """

    filename = track["name"]
    filename = filename.replace("\\", "_").replace("/", "_")
    filename = "playlist/" + album.replace("\\", "_").replace("/", "_") +\
            '/' + filename

    print("New file name:")
    print("    " + filename + ".mp3")

    print()
    if os.path.isfile(filename + ".mp3"):
        print("File exists")
        set_id3(filename + ".mp3", track["name"], artists, album)
        print()
        continue

    ytdl_options.OPTIONS["outtmpl"] = filename + ".%(ext)s"

    # youtube search
    search_string = track["artists"][0]["name"] + " - " + track["name"]

    query = {
            "part":       "snippet",
            "type":       "video",
            "q":          search_string,
            "key":        youtubeapikey.DEVELOPER_KEY,
            "maxResults": 1
            }

    req = requests.get("https://www.googleapis.com/youtube/v3/search",
                       params=query)

    res = json.loads(req.text)

    url = "https://youtube.com/watch?v=" + \
        res["items"][0]["id"]["videoId"]

    print("Got result for " + search_string + ':')
    print("    " + url)

    # download
    with youtube_dl.YoutubeDL(ytdl_options.OPTIONS) as ytdl:
        # info = ytdl.extract_info(url, download=False)
        # title = info.get("title", None)

        # filename = "playlist/" + album + '/' + title + ".mp3"

        print("Downloading url...")

        """try:
        except KeyboardInterrupt:
            print("Skipping song")
            print("Press Ctrl-C twice to quit")
            continue"""

        ytdl.download([url])

        print()

    set_id3(filename + ".mp3", track["name"], artists, album)
