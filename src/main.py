import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Media Downloader")
        self.geometry(f"{600}x{480}")
        
        # configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        # create input frame
        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=0)
        self.input_frame.grid_rowconfigure(0, weight=1)

        # input frame widgets
        self.url_entry = customtkinter.CTkEntry(self.input_frame)
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.button = customtkinter.CTkButton(self.input_frame, text="Download", command=self.download)
        self.button.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        
        # create progressbar frame
        self.output_frame = customtkinter.CTkFrame(self)
        self.output_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(0, weight=1)
        
        self.output_label = customtkinter.CTkLabel(self.output_frame, text="Output")
        self.output_label.grid(row=0, column=0, sticky="wn", padx=10, pady=10)
        

    def download(self):
        print("test")

if __name__ == "__main__":
    app = App()
    app.mainloop()