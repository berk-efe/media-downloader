import os
import sys
import asyncio
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QListWidget,
    QListWidgetItem,
)
from yt_dlp import YoutubeDL
from qasync import QEventLoop, asyncSlot


class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader (Async)")
        self.setFixedSize(800, 400)

        main_layout = QHBoxLayout()

        left_panel = QVBoxLayout()
        self.label = QLabel("Enter YouTube URL:")
        left_panel.addWidget(self.label)

        self.url_input = QLineEdit()
        left_panel.addWidget(self.url_input)

        self.status_label = QLabel("")
        left_panel.addWidget(self.status_label)

        self.download_btn = QPushButton("Download")
        self.download_btn.clicked.connect(self.download_video)
        left_panel.addWidget(self.download_btn)

        left_panel.addStretch()

        self.download_list = QListWidget()

        main_layout.addLayout(left_panel, 2)
        main_layout.addWidget(self.download_list, 3)

        self.setLayout(main_layout)

    @asyncSlot()
    async def download_video(self):
        url = self.url_input.text().strip()
        if not url:
            self.status_label.setText("Please enter a URL")
            return

        self.status_label.setText("Fetching video info...")

        try:
            info = await asyncio.to_thread(self.extract_info, url)
            if info is None:
                title = url
            else:
                title = f"{info.get('title', url)[:31]}..."
        except Exception as e:
            self.status_label.setText(f"Failed to get info: {e}")
            title = url

        list_item = QListWidgetItem(f"{title}  —  Downloading...")
        self.download_list.addItem(list_item)

        try:
            await asyncio.to_thread(self.run_yt_dlp, url)
            list_item.setText(f"{title}  —  Downloaded!")
            self.status_label.setText("Download complete!")
        except Exception as e:
            list_item.setText(f"{title}  —  Error!")
            self.status_label.setText(f"Error: {str(e)}")

    def extract_info(self, url):
        ydl_opts = {}
        with YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)

    def resource_path(self, relative_path):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def run_yt_dlp(self, url):
        ydl_opts = {
            "outtmpl": "%(title)s.%(ext)s",
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "ffmpeg_location": self.resource_path("ffmpeg/ffmpeg.exe"),
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = YouTubeDownloader()
    window.show()

    with loop:
        loop.run_forever()
