import os
import tkinter as tk
from tkinter import filedialog
import librosa
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.male_audio_button = tk.Button(self)
        self.male_audio_button["text"] = "选择男性音频文件夹"
        self.male_audio_button["command"] = self.choose_male_audio_dir
        self.male_audio_button.pack(side="top")

        self.female_audio_button = tk.Button(self)
        self.female_audio_button["text"] = "选择女性音频文件夹"
        self.female_audio_button["command"] = self.choose_female_audio_dir
        self.female_audio_button.pack(side="top")

        self.train_button = tk.Button(self)
        self.train_button["text"] = "训练模型"
        self.train_button["command"] = self.train_model
        self.train_button.pack(side="top")

    def choose_male_audio_dir(self):
        self.male_audio_dir = filedialog.askdirectory(title='请选择男性音频文件夹')

    def choose_female_audio_dir(self):
        self.female_audio_dir = filedialog.askdirectory(title='请选择女性音频文件夹')

    def train_model(self):
        # 加载数据
        X = []
        y = []
        for file in os.listdir(self.male_audio_dir):
            audio, sr = librosa.load(os.path.join(self.male_audio_dir, file))
            mfcc = librosa.feature.mfcc(y=audio, sr=sr)
            X.append(mfcc.mean(axis=1))
            y.append(0) # 男性标签为 0

        for file in os.listdir(self.female_audio_dir):
            audio, sr = librosa.load(os.path.join(self.female_audio_dir, file))
            mfcc = librosa.feature.mfcc(y=audio, sr=sr)
            X.append(mfcc.mean(axis=1))
            y.append(1) # 女性标签为 1

        # 划分训练集和测试集
        X_train, X_test, y_train, y_test = train_test_split(X, y)

        # 训练模型
        clf = SVC()
        clf.fit(X_train, y_train)

        # 测试模型
        y_pred = clf.predict(X_test)
        print('Accuracy:', accuracy_score(y_test, y_pred))

        # 让用户选择模型保存文件夹并保存模型
        model_dir = filedialog.askdirectory(title='请选择模型保存文件夹')
        model_path = os.path.join(model_dir,'gender_classifier.joblib')
        joblib.dump(clf,model_path)

root = tk.Tk()
app = Application(master=root)
app.mainloop()

