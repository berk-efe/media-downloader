import yt_dlp
import threading

class YoutubeManager:
    def __init__(self):
        self.ydl = yt_dlp.YoutubeDL({
            "postprocessors": [{"key": "FFmpegVideoConvertor"}]
        })


    # GET DATA BY URL
    def get_data_by_url(self, url, callback):        
        def run():
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
        
        thread = threading.Thread(target=run)
        thread.start()


if __name__ != "__main__":
    pass
