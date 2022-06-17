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
        print('Downloaded, converting...')


OPTIONS = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
    }],
    "logger": Logger(),
    "progress_hooks": [hook],
}
