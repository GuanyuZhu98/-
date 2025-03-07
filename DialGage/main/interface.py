import tkinter as tk
from main.dialgage_reader import testPotCirc_oscillation
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter
import pandas as pd

class test_interface():
    def __init__(self):
        self.mytest = testPotCirc_oscillation()
        self.running = False
        self.data = []
        self.time_data = []
        # 窗口包含三个按钮，分别是开始、暂停、终止，以及一个实时更新对的折线图。
        self.window = tk.Tk()
        self.window.title('Potentiometer Circulation Oscillation Test')
        self.window.geometry('800x600')
        self.window.resizable(0,0)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)

    def format_func(self, value, tick_number):
        minutes = int(value // 60)
        seconds = int(value % 60)
        return f'{minutes}:{seconds}'

    def single_test(self):
        if self.running:
            self.mytest.send_data("01 03 00 00 00 02 C4 0B")
            result = self.mytest.receive_data()
            self.data.append(result)
            self.time_data.append(len(self.time_data) * 0.1)
            self.ax.clear()
            # self.ax.plot(self.time_data, self.data)
            # self.canvas.draw()
            self.ax.plot(self.time_data, self.data)
            self.ax.xaxis.set_major_formatter(FuncFormatter(self.format_func))
            self.canvas.draw()
            self.window.after(10, self.single_test)

    def start_test(self):
        self.running = True
        self.single_test()

    def pause_test(self):
        self.running = False

    def stop_test(self):
        self.running = False
        
        date_str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        ## 保存折线图
        self.fig.savefig(f'imgs/{date_str}.png')
        # 清空数据和折线图
        self.data.clear()
        self.time_data.clear()
        self.ax.clear()
        self.canvas.draw()
        # 保存数据到csv文件
        
        pd.DataFrame(zip(self.time_data, self.data), columns=['time', 'data']).to_csv(f'data/{date_str}.csv', index=False)
        # 关闭串口
        # self.mytest.ser.close()

    def main(self):
        
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        start_button = tk.Button(self.window, text="开始", command=self.start_test)
        start_button.pack(side=tk.LEFT)

        pause_button = tk.Button(self.window, text="暂停", command=self.pause_test)
        pause_button.pack(side=tk.LEFT)

        stop_button = tk.Button(self.window, text="终止", command=self.stop_test)
        stop_button.pack(side=tk.LEFT)

        self.window.mainloop()
        self.mytest.ser.close()