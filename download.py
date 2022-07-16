from flask import Blueprint, request, send_file

from requests import request as python_request, get
from json import loads

from os.path import isdir, isfile, join, relpath
from os import makedirs, walk
from shutil import make_archive

from datetime import datetime

from youtube_dl import YoutubeDL
from ytdl_options import OPTIONS

from auth import youtubeapikey

download_page = Blueprint('download', __name__)


@download_page.route('/download')
def download():
    # API request
    playlist_id = request.args['playlist_id']
    authorization = 'Bearer ' + request.args['access_token']

    request_url = 'https://api.spotify.com/v1/me/tracks' \
        if playlist_id == 'favourites' \
        else 'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks'

    res = python_request('GET', request_url, headers={
        'Authorization': authorization,
        'Content-Type': 'application/json',
    })

    # TODO: if res
    data = res.json()

    # add all items in playlist (each request limited to 20 tracks by default)
    playlist_items = data['items']

    while data['next']:
        res = python_request('GET', data['next'], headers={
            'Authorization': authorization,
            'Content-Type': 'application/json',
        })
        data = res.json()

        playlist_items.extend(data['items'])

    for item in playlist_items:
        track = item['track']
        album = track['album']['name']

        dir_name = playlist_id + '/' + album
        print('Creating directory ' + dir_name)

        if isdir(dir_name):
            print('Directory exists')
        else:
            makedirs(dir_name)
            print('Directory created')
        print()

        # album art
        album_cover_url = track['album']['images'][1]['url']
        album_cover = get(album_cover_url, allow_redirects=True)

        print('Downloading album cover from ' + album_cover_url)

        album_cover_filename = \
            playlist_id + '/' + album + '/' + 'cover.jpg'

        if isfile(album_cover_filename):
            print('Album cover file exists, continuing')
        else:
            with open(album_cover_filename, 'wb') as f:
                f.write(album_cover.content)
            print('Downloaded album cover')
        print()

        # file name
        artists = ''
        for i, a in enumerate(track['artists']):
            artists += a['name']
            if i < len(track['artists']) - 1:
                artists += '/'
            '''if i == len(track['artists']) - 2:
                artists += ' & '
            elif i < len(track['artists']) - 2:
                artists += ', ' '''

        filename = track['name']
        filename = filename.replace('\\', '_').replace('/', '_')
        filename = playlist_id + '/' + album.replace('\\', '_').replace('/', '_') +\
            '/' + filename

        print('New file name:')
        print('    ' + filename + '.mp3')

        print()
        if isfile(filename + '.mp3'):
            print('File exists')
            set_id3(filename + '.mp3', track['name'], artists, album)
            print()
            continue

        # youtube search
        search_string = track['artists'][0]['name'] + ' - ' + track['name']

        query = {
            'part':       'snippet',
            'type':       'video',
            'q':          search_string,
            'key':        youtubeapikey.DEVELOPER_KEY,
            'maxResults': 1
        }

        req = get('https://www.googleapis.com/youtube/v3/search',
                  params=query)

        # TODO: if req
        res = loads(req.text)

        url = 'https://youtube.com/watch?v=' + \
            res['items'][0]['id']['videoId']

        print('Got result for ' + search_string + ':' + url)

        # download
        OPTIONS['outtmpl'] = filename + '.%(ext)s'

        with YoutubeDL(OPTIONS) as ytdl:
            print('Downloading track')

            ytdl.download([url])
            print()

        set_id3(filename + '.mp3', track['name'], artists, album)

    print('Zipping directory')
    make_archive(playlist_id, 'zip', playlist_id)
    print('Done')

    response = send_file(playlist_id + '.zip')
    response.headers.add('Access-Control-Allow-Origin',
                         'http://localhost:3000')
    return response


def set_id3(filename, title, artists, album):
    # TODO
    pass
