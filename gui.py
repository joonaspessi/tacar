from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT, filedialog, StringVar
from tkinter.ttk import Frame, Label, Entry, Button
from record import Recorder


class Example(Frame):
    def __init__(self, root):
        super().__init__()
        self.master = root
        self.log_directory_text = StringVar()
        self.log_directory_text.set("please select log directory ->")
        self.record_button_text = StringVar()
        self.record_button_text.set("Start Recording")
        self.record_count_text = StringVar()
        self.record_count_text.set("0 records")


        self.recorder = Recorder()
        self.init_ui()
        self.is_recording = False

    def init_ui(self):
        self.master.title("TA Recorder")
        self.master.resizable(True, False)
        self.pack(fill=BOTH, expand=True)
        
        frame1 = Frame(self)

        frame1.pack(fill=X)
        
        lbl1 = Label(frame1, text="LOG DIR", width=10)
        lbl1.pack(side=LEFT, padx=5, pady=5)
        
        btn_dir = Button(frame1, text="...", width=4, command=self.select_dir)
        btn_dir.pack(side=RIGHT, padx=5, pady=5)             
       
        lbl_dir = Label(frame1, text="please select log directory ->", textvar=self.log_directory_text, width=10, borderwidth=2, relief="sunken")
        lbl_dir.pack(fill=X, padx=5, expand=True)
        self.lbl_dir = lbl_dir
        
        frame2 = Frame(self)
        frame2.pack(fill=X)

        btn_rec = Button(frame2, text="Start Recording", textvar=self.record_button_text, command=self.toggle_record)
        btn_rec.pack(side=RIGHT, padx=5, pady=5)   
        lbl_count = Label(frame2, text="0 data records", textvar=self.record_count_text, width=10)
        lbl_count.pack(fill=X, padx=5, pady=5)   

    def select_dir(self):
        dir_name = filedialog.askdirectory()
        current_id = self.recorder.set_directory(dir_name)
        self.log_directory_text.set(dir_name)
        self.update_record_count(current_id)

    def toggle_record(self):
        if self.is_recording:
            self.stop_rec()
            self.is_recording = False
            self.record_button_text.set("Start Recording")
        else:
            self.is_recording = True
            self.record_button_text.set("Stop")
            self.start_rec()

    def start_rec(self):
        self.recorder.init_rec()
        def step():
            while True:
                cur_id = self.recorder.store_rec()
                self.update_record_count(cur_id)
                self.nextstep_id = self.master.after(1, nextstep)
                yield

        nextstep = step().__next__
        self.nextstep_id = self.master.after(1, nextstep)

    def stop_rec(self):
        self.master.after_cancel(self.nextstep_id)
        print("stopped")

    def update_record_count(self, count):
        self.record_count_text.set('%i records' % count)

def main():
  
    root = Tk()
    root.geometry("300x70+300+70")
    Example(root)
    root.mainloop()  

if __name__ == '__main__':
    main()
