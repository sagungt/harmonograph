import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np


class Model():
    def __init__(self):
        self.mode = tk.IntVar()


class FrameTitle(tk.Frame):
    def __init__(self, master=None, title=""):
        tk.Frame.__init__(self, master)
        self.__canvas_title = tk.Label(self, text=title)
        self.__canvas_title.pack()


class CanvasFrame(tk.Frame):
    def __init__(self, master=None, data=None):
        tk.Frame.__init__(self, master)
        self.__mode_height = Model()
        self.__mode_width = Model()
        self.__default_height = data['height']
        self.__default_width = data['width']
        self.__init()

    def __init(self):
        self.__width = self.__canvas_width(self.__default_width)
        self.__height = self.__canvas_height(self.__default_height)

    def __canvas_width(self, default):
        canvas_label = tk.Label(self, text="Width")
        canvas_value = tk.Entry(self, textvariable=self.__mode_width)
        self.__packing(canvas_label, canvas_value, default)
        return canvas_value

    def __canvas_height(self, default):
        canvas_label = tk.Label(self, text="Height")
        canvas_value = tk.Entry(self, textvariable=self.__mode_height)
        self.__packing(canvas_label, canvas_value, default)
        return canvas_value

    def __packing(self, label, value, default):
        label.pack(side='left', fill='x')
        value.insert(0, default)
        value.pack(side='left')

    def get_entry(self):
        return {
            'width': self.__width,
            'height': self.__height
        }

    def get_value(self):
        return {
            'width': int(self.__width.get()),
            'height': int(self.__height.get()),
        }


class HarmonographComponent(tk.Frame):
    def __init__(self, master=None, default={}, number=1):
        tk.Frame.__init__(self, master)
        self.__number = number
        self.__data = {
            'a'+str(self.__number): Model(),
            'd'+str(self.__number): Model(),
            'f'+str(self.__number): Model(),
            'p'+str(self.__number): Model(),
        }
        self.__default_data = default
        self.__init()

    def __init(self):
        self.__amplitude = tk.Label(self, text='a'+str(self.__number))
        self.__amplitude_value = tk.Entry(
            self, textvariable=self.__data['a'+str(self.__number)])
        self.__phase = tk.Label(self, text='p'+str(self.__number))
        self.__phase_value = tk.Entry(
            self, textvariable=self.__data['d'+str(self.__number)])
        self.__dumping = tk.Label(self, text='d'+str(self.__number))
        self.__dumping_value = tk.Entry(
            self, textvariable=self.__data['f'+str(self.__number)])
        self.__frequency = tk.Label(self, text='f'+str(self.__number))
        self.__frequency_value = tk.Entry(
            self, textvariable=self.__data['p'+str(self.__number)])
        self.__packing()

    def __packing(self):
        self.__amplitude.pack(side='left')
        self.__amplitude_value.insert(
            0, self.__default_data['a'+str(self.__number)])
        self.__amplitude_value.pack(side='left')
        self.__phase.pack(side='left')
        self.__phase_value.insert(
            0, self.__default_data['p'+str(self.__number)])
        self.__phase_value.pack(side='left')
        self.__dumping.pack(side='left')
        self.__dumping_value.insert(
            0, self.__default_data['d'+str(self.__number)])
        self.__dumping_value.pack(side='left')
        self.__frequency.pack(side='left')
        self.__frequency_value.insert(
            0, self.__default_data['f'+str(self.__number)])
        self.__frequency_value.pack(side='left')

    def get_entry(self):
        return {
            'a'+str(self.__number): self.__amplitude_value,
            'd'+str(self.__number): self.__dumping_value,
            'f'+str(self.__number): self.__frequency_value,
            'p'+str(self.__number): self.__phase_value
        }

    def get_value(self):
        return {
            'a'+str(self.__number): float(self.__amplitude_value.get()),
            'd'+str(self.__number): float(self.__dumping_value.get()),
            'f'+str(self.__number): float(self.__frequency_value.get()),
            'p'+str(self.__number): float(self.__phase_value.get())
        }


class Acceleration(tk.Frame):
    def __init__(self, master=None, default=None):
        tk.Frame.__init__(self, master)
        self.__var_logspace = tk.BooleanVar()
        self.__default = default['accelerator']
        self.__acceleration = Model()
        self.__init()
        self.get_value()

    def __init(self):
        self.__acceleration_label = tk.Label(self, text="Acceleration")
        self.__acceleration_entry = tk.Entry(
            self, textvariable=self.__acceleration)
        self.__logspace = tk.Checkbutton(
            self, text="Use Logspace", variable=self.__var_logspace, command=self.toggler)
        self.__packing()

    def __packing(self):
        self.__acceleration_label.pack(side='left')
        self.__acceleration_entry.insert(0, self.__default)
        self.__acceleration_entry.pack(side='left')
        self.__logspace.pack(side='left')

    def toggler(self):
        state = self.__var_logspace.get()
        parent = tk.Widget._nametowidget(self, self.winfo_parent())
        parent.toogle(state)

    def get_logspace(self):
        return self.__var_logspace.get()

    def get_entry(self):
        return {
            'accelerator': self.__acceleration_entry
        }

    def get_value(self):
        return {
            'accelerator': float(self.__acceleration_entry.get())
        }


class ControllerButton(tk.Frame):
    def __init__(self, master=None, main_app=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.main_app = main_app
        self.__init()

    def __init(self):
        self.start = tk.Button(self, text="Start", command=self.__start)
        self.create = tk.Button(
            self, text="Plot", state='disabled', command=self.create)
        self.__reset = tk.Button(self, text="Reset", command=self.reset)
        self.__default = tk.Button(
            self, text="Default", command=self.default)
        self.__packing()

    def __packing(self):
        self.start.pack(side='left')
        self.create.pack(side='left')
        self.__reset.pack(side='left')
        self.__default.pack(side='left')

    def __start(self):
        MainApp.start(self, self.main_app)

    def create(self):
        parent = tk.Widget._nametowidget(self, self.main_app)
        parent.plot()

    def reset(self):
        for x in self.main_app.get_all_entry().values():
            x.delete(0, 'end')

    def default(self):
        self.reset()
        self.main_app.default()
        for i, x in enumerate(self.main_app.get_all_entry().items()):
            x[1].insert(0, self.main_app.all_default[x[0]])


class HarmonographCanvas(tk.Frame):
    def __init__(self, master=None, canvas=None, data=None):
        self.new = tk.Toplevel(master)
        tk.Frame.__init__(self, self.new)
        self.data = data
        self.t = 0
        self.iter = 0
        self.id = self.after(1, self.callback)
        self.new.geometry(str(canvas['width'])+'x'+str(canvas['height']))
        self.new.resizable(0, 0)
        self.canvas = tk.Canvas(
            self.new, width=canvas['width'], height=canvas['height'])
        self.canvas.mainloop()

    def __point(self, xt, yt):
        self.canvas.create_line(xt, yt+1, xt+1, yt, fill='black')
        self.canvas.pack()

    def callback(self):
        d = self.data
        self.iter += 1
        xt = d['a1'] * np.sin(self.t * d['f1'] + d['p1']) * np.exp(-d['d1'] * self.t) + \
            d['a2'] * np.sin(self.t * d['f2'] + d['p2']
                             ) * np.exp(-d['d2'] * self.t)
        yt = d['a3'] * np.sin(self.t * d['f3'] + d['p3']) * np.exp(-d['d3'] * self.t) + \
            d['a4'] * np.sin(self.t * d['f4'] + d['p4']
                             ) * np.exp(-d['d4'] * self.t)
        self.__point(d['width'] / 2 + xt,
                     d['height'] / 2 + yt,)
        self.t += d['accelerator']
        self.id = self.after(1, self.callback)


class Message(tk.Frame):
    def __init__(self, type_message=None, message=None):
        self.__message_window = tk.Tk()
        self.__type = type_message
        self.__message_window.title(self.__type)
        self.__message = message
        self.__init()

    def __init(self):
        self.__message_label = tk.Label(
            self.__message_window, text=self.__message, bd=20)
        self.__message_label.pack()
        self.__message_window.mainloop()


class LogSpace(tk.Frame):
    def __init__(self, master=None, state=None, data=None):
        tk.Frame.__init__(self, master)
        self.__state = state
        self.__data = {
            'iteration': Model(),
            'log10_1': Model(),
            'log10_2': Model(),
            'linewidth': Model()
        }
        self.data = data
        self.__init()

    def __init(self):
        self.__iteration_label = tk.Label(self, text="Iteration")
        self.__iteration_entry = tk.Entry(
            self, width=10, textvariable=self.__data['iteration'])
        self.__logspace_label = tk.Label(self, text="Logspace = ")
        self.__log10_1_label = tk.Label(self, text="log10")
        self.__log10_1_entry = tk.Entry(
            self, width=3, textvariable=self.__data['log10_1'])
        self.__log10_2_label = tk.Label(self, text="log10")
        self.__log10_2_entry = tk.Entry(
            self, width=3, textvariable=self.__data['log10_2'])
        self.__linewidth_label = tk.Label(self, text="Linewidth")
        self.__linewidth_entry = tk.Entry(
            self, width=6, textvariable=self.__data['linewidth'])
        self.__preview_button = tk.Button(
            self, text="Preview", command=self.__preview)
        if self.__state:
            self.__show()
        else:
            self.__hide()

    def __show(self):
        self.__iteration_label.pack(side='left')
        self.__iteration_entry.insert(0, 1000000)
        self.__iteration_entry.pack(side='left')
        self.__logspace_label.pack(side='left')
        self.__log10_1_label.pack(side='left')
        self.__log10_1_entry.insert(0, 10)
        self.__log10_1_entry.pack(side='left')
        self.__log10_2_label.pack(side='left')
        self.__log10_2_entry.insert(0, 500)
        self.__log10_2_entry.pack(side='left')
        self.__linewidth_label.pack(side='left')
        self.__linewidth_entry.insert(0, .1)
        self.__linewidth_entry.pack(side='left')
        self.__preview_button.pack(side='left')

    def __hide(self):
        self.__iteration_label.pack_forget()
        self.__iteration_entry.pack_forget()
        self.__logspace_label.pack_forget()
        self.__log10_1_label.pack_forget()
        self.__log10_1_entry.pack_forget()
        self.__log10_2_label.pack_forget()
        self.__log10_2_entry.pack_forget()
        self.__linewidth_label.pack_forget()
        self.__linewidth_entry.pack_forget()
        self.__preview_button.pack_forget()

    def __preview(self):
        try:
            iteration = int(self.__iteration_entry.get())
            log10_1 = int(self.__log10_1_entry.get())
            log10_2 = int(self.__log10_2_entry.get())
            linewidth = float(self.__linewidth_entry.get())
            t = np.logspace(np.log10(log10_1), np.log10(log10_2), iteration)
            plt.plot(
                np.sin(t*self.data['f1'])*np.exp(-self.data['d1']*t), linewidth=linewidth)
            plt.show()
        except:
            Message("Error", "Value Incorrect. Please use int or float")

    def create(self):
        try:
            iteration = int(self.__iteration_entry.get())
            log10_1 = int(self.__log10_1_entry.get())
            log10_2 = int(self.__log10_2_entry.get())
            linewidth = float(self.__linewidth_entry.get())
            t = np.logspace(np.log10(log10_1), np.log10(log10_2), iteration)
            xt = self.data['a1'] * np.sin(t * self.data['f1'] + self.data['p1']) * np.exp(-self.data['d1'] * t) + \
                self.data['a2'] * np.sin(t * self.data['f2'] + self.data['p2']
                                         ) * np.exp(-self.data['d2'] * t)
            yt = self.data['a3'] * np.sin(t * self.data['f3'] + self.data['p3']) * np.exp(-self.data['d3'] * t) + \
                self.data['a4'] * np.sin(t * self.data['f4'] + self.data['p4']
                                         ) * np.exp(-self.data['d4'] * t)
            plt.figure(
                figsize=(self.data['width'] / 100, self.data['height'] / 100))
            plt.plot(xt, yt, 'k', linewidth=linewidth)
            plt.axis('off')
            plt.show()
        except:
            Message("Error", "Value Incorrect. Please use int or float")


class MainApp(tk.Frame):
    def __init__(self, master=None, default=None, canvas=None, acceleration=None):
        tk.Frame.__init__(self, master)
        self.__all_entry = {}
        self.__refactored_data = {}
        self.all_default = {}
        self.harmonograph_window = None
        self.master = master
        self.canvas_default = canvas
        self.harmonograph_default = default
        self.acceleration_default = acceleration
        self.__init()

    def __init(self):
        self.__canvas_title = FrameTitle(self, 'Canvas Size')
        self.__canvas = CanvasFrame(
            self,
            self.canvas_default)
        self.__controller = ControllerButton(self.__canvas, self)
        self.__harmonograph_title = FrameTitle(self, 'Harmonograph Data')
        self.__harmonograph_component_1 = HarmonographComponent(
            self,
            self.harmonograph_default,
            1)
        self.__harmonograph_component_2 = HarmonographComponent(
            self,
            self.harmonograph_default,
            2)
        self.__harmonograph_component_3 = HarmonographComponent(
            self,
            self.harmonograph_default,
            3)
        self.__harmonograph_component_4 = HarmonographComponent(
            self,
            self.harmonograph_default,
            4)
        self.__acceleration = Acceleration(self, self.acceleration_default)
        self.__author = tk.Label(self, text="github.com/sagungt")
        self.__packing()

    def __packing(self):
        self.__canvas_title.pack(fill='x')
        self.__canvas.pack(fill='both')
        self.__controller.pack()
        self.__harmonograph_title.pack(fill='x')
        self.__harmonograph_component_1.pack(fill='x')
        self.__harmonograph_component_2.pack(fill='x')
        self.__harmonograph_component_3.pack(fill='x')
        self.__harmonograph_component_4.pack(fill='x')
        self.__acceleration.pack(fill='x')
        self.__author.pack(side='bottom', anchor='se')

        self.pack(expand=True, fill='both')

    def __refactor_data(self, stored):
        self.__extract(self.__canvas.get_value(),
                       stored)
        self.__extract(self.__harmonograph_component_1.get_value(),
                       stored)
        self.__extract(self.__harmonograph_component_2.get_value(),
                       stored)
        self.__extract(self.__harmonograph_component_3.get_value(),
                       stored)
        self.__extract(self.__harmonograph_component_4.get_value(),
                       stored)
        self.__extract(self.__acceleration.get_value(),
                       stored)

    def __extract(self, data={}, stored={}):
        for x, y in data.items():
            stored[x] = y
        return stored

    def default(self):
        self.__extract(self.canvas_default, self.all_default)
        self.__extract(self.harmonograph_default, self.all_default)
        self.__extract(self.acceleration_default, self.all_default)

    def get_value(self):
        self.__refactor_data(self.__refactored_data)
        return self.__refactored_data

    def get_logspace(self):
        return self.__acceleration.get_logspace()

    def get_all_entry(self):
        self.__extract(self.__canvas.get_entry(), self.__all_entry)
        self.__extract(
            self.__harmonograph_component_1.get_entry(), self.__all_entry)
        self.__extract(
            self.__harmonograph_component_2.get_entry(), self.__all_entry)
        self.__extract(
            self.__harmonograph_component_3.get_entry(), self.__all_entry)
        self.__extract(
            self.__harmonograph_component_4.get_entry(), self.__all_entry)
        self.__extract(self.__acceleration.get_entry(), self.__all_entry)
        return self.__all_entry

    def start(self, main_app):
        try:
            parent = tk.Widget._nametowidget(self, name=self.winfo_parent())
            canvas = parent.get_value()
            HarmonographCanvas(master=self.master,
                               canvas=canvas,
                               data=main_app.get_value())
        except:
            Message("Error", "Value Incorrect. Please use int or float")

    def toogle(self, state):
        if state:
            self.__controller.start.config(state='disabled')
            self.__controller.create.config(state='normal')
        else:
            self.__controller.start.config(state='normal')
            self.__controller.create.config(state='disabled')
            self.logspace.pack_forget()
        self.logspace = LogSpace(self, state, self.get_value())
        self.logspace.pack(fill='x')

    def plot(self):
        self.get_value()
        self.logspace.create()


def main():
    root = tk.Tk()
    root.geometry("580x220")
    root.resizable(0, 0)
    root.title("Harmonograph")
    canvas = {
        'height': 500,
        'width': 500
    }
    data = {
        'a1': 100,
        'a2': 100,
        'a3': 100,
        'a4': 100,
        'd1': 0.005,
        'd2': 0.002,
        'd3': 0.003,
        'd4': 0.005,
        'f1': 1,
        'f2': 6,
        'f3': 5,
        'f4': 8,
        'p1': 1,
        'p2': 1,
        'p3': 1,
        'p4': 1
    }
    acceleration = {
        'accelerator': 0.001
    }
    app = MainApp(root, data, canvas, acceleration)
    root.mainloop()


if __name__ == '__main__':
    main()
