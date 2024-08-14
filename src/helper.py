import logging
import threading
import yt_dlp
import queue

from datetime import timedelta

from logging import Logger

MAIN_QUEUE = queue.Queue()

class MyHandler(logging.Handler):
    def __init__(self, level=logging.DEBUG) -> None:
        super().__init__(level)
        
    def emit(self, record: logging.LogRecord) -> None:
        
        log_entry = self.format(record) # for now it just returns the record in string format
        MAIN_QUEUE.put(log_entry)
        print("CUSTOM HANDLER: ", log_entry)

DEBUG_LOGGER = Logger(name="debug_logger", level=logging.DEBUG)
DEBUG_LOGGER.addHandler(MyHandler())


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')

class YoutubeManager:
    def __init__(self):
        self.ydl_options = {
            "quiet": True,
            "ffmpeg_location": "tools/bin/ffmpeg.exe",
            "postprocessors": [{
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
                }],
            "logger": DEBUG_LOGGER,
            "progress_hooks": [my_hook],
        }


    def format_bytes(self, bytes):
        if bytes >= 1024*1024:  # 1 MB
            return f"{bytes / 1024*1024:.2f} MB"
        elif bytes >= 1024:  # 1 KB
            return f"{bytes / 1024:.2f} KB"
        else:
            return f"{bytes} bytes"

    def format_speed(self, speed):
        if speed >= 1024*1024:  # 1 MB
            return f"{speed / 1024*1024:.2f} MB/s"
        elif speed >= 1024:  # 1 KB
            return f"{speed / 1024:.2f} KB/s"
        else:
            return f"{speed} bytes/s"

    def format_time(self, seconds):
        delta = timedelta(seconds=seconds)
        hours, remainder = divmod(delta.seconds, 60 * 60)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    # GET DATA BY URL
    def get_data_by_url(self, url, callback):        
        def run():
            MAIN_QUEUE.put("Extracting data...")
            
            with yt_dlp.YoutubeDL(self.ydl_options) as ydl:    
                data = ydl.extract_info(url, download=False)
                title = data.get("title", None)
                
                thumbnails = data.get("thumbnails", None)
                for thumbnail in thumbnails:
                    if thumbnail.get("preference") == 0:
                        thumbnail = thumbnail.get("url", None)
                        break
                
                resolutions = []
                for format in data["formats"]:
                    if not format.get('ext') in ['mp4', 'webm'] or format.get('fps') == None or format.get('resolution') == None:
                        continue
                    
                    res = format.get('resolution').split("x")[-1] + "p"
                    if  res in resolutions:
                        continue
                    
                    resolutions.append(res)
                    
                
                result = {
                    "title": title,
                    "thumbnail": thumbnail,
                    "resolutions": resolutions,
                }
                
                callback(result)
                
                MAIN_QUEUE.put("Data extracted successfully.")
        
        thread = threading.Thread(target=run)
        thread.start()
        
    # DOWNLOAD VIDEO BY ID
    def download_video(self, res, url, output_path):
        def run():
            MAIN_QUEUE.put("Downloading video...")
            print("DEBUG", res[:-1])
            
            ydl_opts = self.ydl_options.copy()
            ydl_opts["format"] = f"bestvideo[height={res[:-1]}]+bestaudio/best[height={res[:-1]}]"
            ydl_opts["outtmpl"] = output_path

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                MAIN_QUEUE.put("[Success] Download completed successfully!")
            
                     
        
        thread = threading.Thread(target=run)
        thread.start()


if __name__ != "__main__":
    pass
