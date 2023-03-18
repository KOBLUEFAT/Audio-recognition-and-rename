import os
import shutil
from tkinter import *
from tkinter import filedialog
import librosa
import joblib

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.select_model_btn = Button(self, text="选择模型文件", command=self.select_model)
        self.select_model_btn.pack()

        self.select_audio_btn = Button(self, text="选择音频文件", command=self.select_audio)
        self.select_audio_btn.pack()

        self.select_target_btn = Button(self, text="选择目标文件夹", command=self.select_target)
        self.select_target_btn.pack()

        self.run_btn = Button(self, text="运行", command=self.run)
        self.run_btn.pack()

        self.quit_btn = Button(self, text="退出", command=self.master.destroy)
        self.quit_btn.pack()

        self.status_label = Label(self, text="")
        self.status_label.pack()

    def select_model(self):
        self.model_file = filedialog.askopenfilename(title='请选择模型文件')
        self.status_label.config(text=f"已选择模型文件: {self.model_file}")

    def select_audio(self):
        self.audio_files = filedialog.askopenfilenames(title='请选择音频文件')
        self.status_label.config(text=f"已选择音频文件: {len(self.audio_files)} 个")

    def select_target(self):
        self.target_dir = filedialog.askdirectory(title='请选择目标文件夹')
        self.status_label.config(text=f"已选择目标文件夹: {self.target_dir}")

    def run(self):
        if not hasattr(self, 'model_file'):
            self.status_label.config(text="请选择模型文件")
            return
        if not hasattr(self, 'audio_files'):
            self.status_label.config(text="请选择音频文件")
            return
        if not hasattr(self, 'target_dir'):
            self.status_label.config(text="请选择目标文件夹")
            return

        # 在目标文件夹中创建 male 和 female 子文件夹
        male_dir = os.path.join(self.target_dir, 'male')
        female_dir = os.path.join(self.target_dir, 'female')
        os.makedirs(male_dir, exist_ok=True)
        os.makedirs(female_dir, exist_ok=True)

        # 加载保存的模型
        clf = joblib.load(self.model_file)

        # 遍历音频文件进行分类
        for file in self.audio_files:
            # 加载音频文件
            audio, sr = librosa.load(file)

            # 提取 MFCC 特征
            mfcc = librosa.feature.mfcc(y=audio, sr=sr)
            X = mfcc.mean(axis=1)

            # 使用模型进行预测
            y_pred = clf.predict([X])

            # 根据预测结果将音频文件复制到相应子文减价
            if y_pred == 0:
                shutil.copy(file, male_dir)
            else:
                shutil.copy(file, female_dir)

        self.status_label.config(text=f"处理完毕: {len(self.audio_files)} 个音频文件已分类到 {male_dir} 和 {female_dir}")

root = Tk()
app = Application(master=root)
app.mainloop()
