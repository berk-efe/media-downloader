import logging
import yt_dlp

from tkinter import Variable, StringVar
from logging import Logger

from threading import Thread

from queue import Queue

MAIN_QUEUE = Queue()
VAR_LIST = []

class MyHandler(logging.Handler):
    def __init__(self, level=logging.DEBUG) -> None:
        super().__init__(level)
        
    def emit(self, record: logging.LogRecord) -> None:
        
        log_entry = self.format(record) # for now it just returns the record in string format
        MAIN_QUEUE.put(log_entry)
        print("CUSTOM HANDLER: ", log_entry)
        
class VideoProgressHandler(logging.Handler):
    def __init__(self, queue, level=logging.DEBUG) -> None:
        super().__init__(level)
        self.queue = queue
    def emit(self, record: logging.LogRecord) -> None:
        
        log_entry = self.format(record)
        self.queue.put(log_entry)

DEBUG_LOGGER = Logger(name="debug_logger", level=logging.DEBUG)
DEBUG_LOGGER.addHandler(MyHandler())


# CHANGE IT
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')

class YoutubeManager:
    def __init__(self):
        self.ydl_options = {
            "quiet": True,
            "ffmpeg_location": "../tools/bin/ffmpeg.exe",
            "postprocessors": [{
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
                }],
            "logger": DEBUG_LOGGER,
            "progress_hooks": [my_hook],
        }

    # SIMPLE HELP STUFF GONNA CHANGE THE LOCATION
    
    

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
                
                MAIN_QUEUE.put(f"Succesfly extracted data for {title}")
        
        thread = Thread(target=run)
        thread.start()
        
    # DOWNLOAD VIDEO BY ID
    def download_video(self, res, url, output_path, callback):
        MAIN_QUEUE.put("[info] Downloading started...")
        progress_queue = Queue()
        
        progress_logger = Logger(name="progress_logger", level=logging.DEBUG)
        progress_logger.addHandler(VideoProgressHandler(progress_queue))
        
        
        progress_data = {
            "progress_var": Variable(value=0),
            "data_var": StringVar(value=""),
        }

        VAR_LIST.append([progress_data, progress_queue])
            
        def run():
            ydl_opts = self.ydl_options.copy()
            ydl_opts["format"] = f"bestvideo[height={res[:-1]}]+bestaudio/best[height={res[:-1]}]"
            ydl_opts["logger"] = progress_logger
            ydl_opts["outtmpl"] = output_path

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_title = ydl.extract_info(url, download=True).get("title", None)
                progress_queue.put(f"[success] Download completed successfully for {video_title}")
        
        process = Thread(target=run)
        process.start()
        
        callback(progress_data)

if __name__ != "__main__":
    pass
