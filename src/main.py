import tkinter
import tkinter.filedialog
import tkinter.messagebox
from customtkinter import *
import pprint
import queue

from helper import YoutubeManager

set_appearance_mode("System")
set_default_color_theme("blue")


ym = YoutubeManager()

class App(CTk):
    def __init__(self):
        super().__init__()

        # CONFIGURE WINDOW
        self.title("Media Downloader")
        self.geometry(f"{1000}x{720}")
        
        # CONFIGURE GRID
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        
        # CREATE INPUT FRAME
        self.input_frame = CTkFrame(self)
        self.input_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=0)
        self.input_frame.grid_rowconfigure(0, weight=1)

        # INPUT FRAME WIDGETS
        self.url_entry = CTkEntry(self.input_frame)
        self.url_entry.insert(0, 'https://www.youtube.com/watch?v=434pz9XIf_U')
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.button = CTkButton(self.input_frame, text="Get Video", command=self.get_video)
        self.button.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        
        # OUTPUT FRAME
        self.output_frame = CTkFrame(self)
        self.output_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(1, weight=0)
        self.output_frame.grid_rowconfigure(2, weight=0)
        
        # STATUS BAR
        self.status_bar_frame = CTkFrame(self, corner_radius=0)
        self.status_bar_frame.grid(row=2, column=0, sticky="ew", columnspan=2)
        
        # STATUS BAR WIDGETS
        self.status_label = CTkLabel(self.status_bar_frame, text="Ready", anchor=tkinter.W)
        self.status_label.grid(row=0, column=0, sticky="ew")
        
        # QUEUE FOR LOG MESSAGES
        self.log_queue = queue.Queue()
        self.after(100, self.process_log_queue)
        
    # FUNCTIONS
    # periodically checks the queue for new log messages and updates the status bar.
    def process_log_queue(self):
        while not self.log_queue.empty():
            log_message = self.log_queue.get()
            self.status_label.configure(text=log_message)
        self.after(100, self.process_log_queue)
    
    # GET VIDEO
    def get_video(self):
        url = self.url_entry.get()
        ym.get_data_by_url(url, self.on_data_extraction, self.log_queue)
        
    # DOWNLOAD VIDEO
    def download_video(self):
        self.video_download_button.configure(state="disabled")
        desired_format = self.video_formats_combobox.get()
        extension = desired_format.split(",")[1].strip()
        video_title = self.video_title_lable.get("1.0", tkinter.END).strip()
        
        video_url = self.url_entry.get()
        
        video_id = desired_format.split(",")[-1].strip()
        output_path = tkinter.filedialog.asksaveasfilename(initialfile=video_title, defaultextension=f".{extension}", filetypes=[("MP4 Files", "*.mp4"), ("WEBP Files", "*.webp"), ("WEBM Files", "*.webm")])
        
        ym.download_video_by_id(video_id, video_url, output_path, self.log_queue)
        
        
    # CALLBACK
    def on_data_extraction(self, data):
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        
        # LABLE
        self.video_title_lable = CTkTextbox(self.output_frame, height=1)
        self.video_title_lable.insert(tkinter.END, text=data.get('title', 'No Title'))
        self.video_title_lable.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        # FORMAT_FRAME
        self.select_video_format_frame = CTkFrame(self.output_frame)
        self.select_video_format_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        
        self.select_video_format_frame.grid_columnconfigure(0, weight=1)
        self.select_video_format_frame.grid_columnconfigure(1, weight=0)
        self.select_video_format_frame.grid_rowconfigure(0, weight=1)
        
        # FORMAT_FRAME WIDGETS
        values = [f"{format.get('resolution')}, {format.get('ext')}, {format.get('fps')}fps, {format.get('id')}" for format in data.get('formats', [])]
        self.video_formats_combobox = CTkComboBox(self.select_video_format_frame, values=values, state="readonly")
        self.video_formats_combobox.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.video_formats_combobox.set(values[-1])

        self.video_download_button = CTkButton(self.select_video_format_frame, text="Download", command=self.download_video)
        self.video_download_button.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        
        # DOWNLOAD PROGRESS BAR
        test_var = tkinter.Variable(value=0.1)
        self.video_download_progress_bar = CTkProgressBar(self.output_frame, variable=test_var)
        self.video_download_progress_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        return data
    
    def on_video_download(self):
        
        # DOWNLOAD PROGRESS BAR
        test_var = tkinter.Variable(value=0.1)
        self.video_download_progress_bar = CTkProgressBar(self.output_frame, variable=test_var)
        self.video_download_progress_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        



if __name__ == "__main__":
    app = App()
    app.mainloop()