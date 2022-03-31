###### spotify-dl-saved 20/01/2019

Searches YouTube for the user's Spotify saved/favourites songs and downloads
them as MP3s.

# Instructions:

## Setup
I don't know how to set up the Spotify and YouTube Data API to use my authentication
credentials so you'll need a project able to access the Spotify user data with
the Authorisation Code flow and a YouTube Data API key to search for videos.

Create two files in the `auth` subdirectory: `spotifysecret.py` and
`youtubeapikey.py`. These will contain the necessary keys to authenticate the
project's requests to Spotify and YouTube. Refer to the
[section on the format for these files](#authformat) for more information.

To log errors, warnings and debug messages from youtube-dl, set `USE_LOGFILE`
to `True` in `ytdl_options.py` and set `LOGFILE_NAME` to whatever you want
(default `ytdl.log`). There are other options for program logs in
`ytdl_options.py` as well.

// TODO: Figure out project authentication

## Execution
Run `spotifydlsaved.py` and follow the instructions to login to Spotify.

It will search YouTube for the songs in your Spotify saved/favourites list,
then create subdirectories for the songs' albums under the playlist directory
in the current working directory.

Requires [Python 3](https://python.org), latest version of
[youtube-dl](https://youtube-dl.org/),
[Spotipy](https://spotipy.readthedocs.io/en/latest/),
[Requests](http://docs.python-requests.org/en/master/)
and [Mutagen](https://mutagen.readthedocs.io/en/latest/). Uses the Spotify
Web API and YouTube Data API v3 to make requests.

# <a name="authformat" id="authformat"></a>API key/Spotify client info format
## Spotify client information
`auth/spotifysecret.py` should contain 4 values:
0. `CLIENT_ID`: your project client ID
0. `CLIENT_SECRET`: your project client secret
0. `REDIRECT_URI`: a URI to redirect to. Must be whitelisted in your project
settings, but does not have to be valid or related. e.g.
https://example.com/callback
0. `USERNAME`: your Spotify auto-generated username (not display name)

## YouTube API key
`auth/youtubeapikey.py` only needs one value: <br>
`DEVELOPER_KEY` = your YouTube Data API v3 key. Find it under the Credentials tab in
your Google Developers project dashboard. OAuth 2.0 is not needed for this
application, as it does not access user data. I will not write a guide to using
the OAuth protocol here.

# Bugs
- Downloads an extra file for the first song in the list, into the playlist
parent directory.
- Doesn't download the song file for the last song, but creates the album name
directory and youtube-dl outputs that it successfully downloaded and
converted.

# License

        Copyright 2019 codeo

        Licensed under the Apache License, Version 2.0 (the "License");
        you may not use this file except in compliance with the License.
        You may obtain a copy of the License at

                http://www.apache.org/licenses/LICENSE-2.0

        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.
