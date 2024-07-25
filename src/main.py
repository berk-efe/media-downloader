import tkinter
import tkinter.messagebox
import customtkinter
import pprint

from helper import YoutubeManager

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


ym = YoutubeManager()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # CONFIGURE WINDOW
        self.title("Media Downloader")
        self.geometry(f"{600}x{480}")
        
        # CONFIGURE GRID
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        # CREATE INPUT FRAME
        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=0)
        self.input_frame.grid_rowconfigure(0, weight=1)

        # INPUT FRAME WIDGETS
        self.url_entry = customtkinter.CTkEntry(self.input_frame)
        self.url_entry.insert(0, 'https://www.youtube.com/watch?v=434pz9XIf_U')
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.button = customtkinter.CTkButton(self.input_frame, text="Get Video", command=self.get_video)
        self.button.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        
        # OUTPUT FRAME
        self.output_frame = customtkinter.CTkFrame(self)
        self.output_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(1, weight=0)
        

    def get_video(self):
        url = self.url_entry.get()
        ym.get_data_by_url(url, self.on_data_extraction)

    # callback function (gonna modify more in the future)
    def on_data_extraction(self, data):
        # PRINT FOR NOW        
        pprint.pprint(data)
        
        self.video_title_lable = customtkinter.CTkLabel(self.output_frame, text=data.get('Title', 'No Title'))
        self.video_title_lable.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.video_formats_combobox = customtkinter.CTkComboBox(self.output_frame, values=[f"{format.get('resolution')}, {format.get('ext')}, {format.get('fps')}fps" for format in data.get('formats', [])])
        self.video_formats_combobox.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        
        return data



if __name__ == "__main__":
    app = App()
    app.mainloop()