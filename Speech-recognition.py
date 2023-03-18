import tkinter as tk
import tkinter.filedialog as fd
import os
import speech_recognition as sr
import azure.cognitiveservices.speech as speechsdk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.output_dir = ""

    def create_widgets(self):
        tk.Label(self, text="音频选择并重命名").pack()
        tk.Button(self, text="选择文件", command=self.select_files).pack()

        self.selected_files_label = tk.Label(self)
        self.selected_files_label.pack()

        tk.Button(self, text="选择输出文件夹", command=self.select_output_folder).pack()

        self.extract_button = tk.Button(self, text="开始转换", command=self.extract_speech, state=tk.DISABLED)
        self.extract_button.pack()

        self.status_label = tk.Label(self, text="")
        self.status_label.pack()

    def select_files(self):
        audio_files = fd.askopenfilenames(filetypes=[("Audio files", "*.wav;*.mp3;*.m4a")])
        self.selected_files_label.configure(text="\n".join(audio_files))
        self.extract_button.configure(state=tk.NORMAL if audio_files else tk.DISABLED)

    def select_output_folder(self):
        output_dir = fd.askdirectory()
        if output_dir:
            self.output_dir = output_dir

    def extract_speech(self):
        for audio_file in self.selected_files_label.cget("text").split("\n"):
            if not self.output_dir:
                self.status_label.configure(text="请选择输出文件夹")
                return
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)
            speech_config = speechsdk.SpeechConfig(subscription=self.api_key.get(), region=self.api_region.get())
            speech_config.speech_recognition_language = "zh-CN"
            audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
            result = speech_recognizer.recognize_once()
            recognized_text = "".join(e for e in result.text if (e.isalnum() or e.isspace()))
            new_filename = recognized_text + ".wav"
            output_file_path = os.path.join(self.output_dir, new_filename)
            with open(output_file_path, "wb") as file:
                file.write(audio_data.get_wav_data())
        self.status_label.configure(text="语音文件转换完成")

root = tk.Tk()
app = Application(master=root)
app.api_key = tk.StringVar()
app.api_region = tk.StringVar()
tk.Label(app, text="API Key:").pack()
tk.Entry(app, textvariable=app.api_key).pack()
tk.Label(app, text="Region:").pack()
tk.Entry(app, textvariable=app.api_region).pack()
app.mainloop()
