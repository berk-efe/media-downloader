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
        self.ydl = yt_dlp.YoutubeDL({
            "quiet": True,
            "postprocessors": [{"key": "FFmpegVideoConvertor"}],
            "logger": DEBUG_LOGGER,
            "progress_hooks": [my_hook],
        })


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
            data = self.ydl.extract_info(url, download=False)
            title = data.get("title", None)
            
            thumbnails = data.get("thumbnails", None)
            for thumbnail in thumbnails:
                if thumbnail.get("preference") == 0:
                    thumbnail = thumbnail.get("url", None)
                    break
            
            formats = []
            for format in data["formats"]:
                if format.get('ext') != 'mp4' or format.get('fps') == None:
                    continue
                
                simplyfied_format = {
                    'ext': format.get('ext', None),
                    'fps': format.get('fps', None),
                    'resolution': format.get('resolution', None), 
                    'id': format.get('format_id', None),             
                }
                formats.append(simplyfied_format)
                
            for f in formats:
                if f.get('ext') == "mp4":
                    for f2 in formats:
                        if f.get('resolution') == f2.get('resolution') and f.get('fps') == f2.get('fps'):
                            formats.remove(f2)
                            break
            
            result = {
                "title": title,
                "thumbnail": thumbnail,
                "formats": formats,
            }
            
            callback(result)
            
            MAIN_QUEUE.put("Data extracted successfully.")
        
        thread = threading.Thread(target=run)
        thread.start()
        
    # DOWNLOAD VIDEO BY ID
    def download_video_by_id(self, id, url, output_path):
        def run():
            
            
            def progress_hook(d):
                if d['status'] == 'downloading':
                    progress = d['_percent_str']
                    total_bytes = self.format_bytes(d.get('total_bytes', 0))
                    downloaded_bytes = self.format_bytes(d.get('downloaded_bytes', 0))
                    speed = self.format_speed(d.get('speed', 0))
                    
                    try:
                        eta = self.format_time(d.get('eta', 0))
                    except:
                        eta = "calculating..."
                    
                    log_message = (f"Download progress: {progress} "
                                f"({downloaded_bytes}/{total_bytes}) "
                                f"at {speed}, ETA: {eta}")
                    MAIN_QUEUE.put(log_message)
                elif d['status'] == 'finished':
                    MAIN_QUEUE.put("Download finished.")
                elif d['status'] == 'error':
                    MAIN_QUEUE.put(f"Download error: {d['error']}")
                     

                
            ydl_opts = {
            'format': id,
            'outtmpl': output_path,
            'progress_hooks': [progress_hook],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([url])
                    MAIN_QUEUE.put("[Success] Download completed successfully!")
                     
                except Exception as e:
                    MAIN_QUEUE.put(f"[Error] {str(e)}")
                     
        
        thread = threading.Thread(target=run)
        thread.start()


if __name__ != "__main__":
    pass
