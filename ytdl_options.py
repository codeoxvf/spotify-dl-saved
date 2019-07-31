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

from datetime import timedelta

USE_LOGFILE = False
LOGFILE_NAME = "ytdl.log"


class Logger(object):
    def debug(self, msg):
        txt = "[DEBUG] " + msg + '\n'

        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            txt = txt + str(timedelta(seconds=uptime_seconds))

        if USE_LOGFILE:
            with open(LOGFILE_NAME, "a") as f:
                f.write(txt)

    def warning(self, msg):
        txt = "[WARNING] " + msg + '\n'

        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            txt = txt + str(timedelta(seconds=uptime_seconds))

        if USE_LOGFILE:
            with open(LOGFILE_NAME, "a") as f:
                f.write(txt)

        print(txt)

    def error(self, msg):
        txt = "[ERROR] " + msg + '\n'

        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            txt = txt + str(timedelta(seconds=uptime_seconds))

        if USE_LOGFILE:
            with open(LOGFILE_NAME, "a") as f:
                f.write(txt)

        print(txt)


def hook(dl_job):
    if dl_job['status'] == 'finished':
        print('Done downloading, now converting...')


OPTIONS = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            }],
        "logger": Logger(),
        "progress_hooks": [hook],
        }
