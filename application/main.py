import sys, glob, serial
import tkinter as tk
import tkinter.ttk as ttk
import serial.tools.list_ports
import redirectors as redirectors
import SDM630 as hardware
import threading


class MeterTester(threading.Thread):
    def __init__(self, port):
        """
        Setup thread for checking connected meters.
        """
        threading.Thread.__init__(self)
        self.port = port
        self.stop_request = threading.Event()

    def run(self):
        print("Testing Meters 1-36\nPort: %s\n\n" % self.port)

        for i in range(1, 37):
            if not self.stop_request.is_set():
                meter = hardware.Meter(i, i, self.port)
                if i == 1:
                    print(meter.instrument)
                if meter.is_reachable():
                    print("✅ Meter %d is connected" % i)
                else:
                    print("❌ Can't reach Meter %d" % i)


class Application(tk.Tk):
    def __init__(self):
        """
        Setup all required GUI elements binding methods.
        """
        tk.Tk.__init__(self)
        self.title("MMetering - Tester")
        self.selected = tk.StringVar()
        self.checking_thread = None

        top_frame = tk.Frame(self, bd=2)
        bottom_frame = tk.Frame(self, bd=2)
        top_frame.pack(fill="x")
        bottom_frame.pack(fill="x")

        label = tk.Label(top_frame, text="Select Port: ")
        label.pack(side="left")
        self.cb = ttk.Combobox(top_frame, textvariable=self.selected, values=self.get_ports())
        self.cb.pack(side="left", fill="x")

        scrollbar = tk.Scrollbar(bottom_frame)
        scrollbar.pack(side="right", fill="y")
        self.text_box = tk.Text(bottom_frame, wrap = "word", borderwidth="1")
        self.text_box.pack(side="bottom", fill="both", expand=True)

        self.text_box.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_box.yview)

        self.stop_btn = tk.Button(top_frame, text='Stop', command=self.stop_thread)
        self.stop_btn.pack(side="right")
        self.start_btn = tk.Button(top_frame, text='Start', command=self.start_thread)
        self.start_btn.pack(side="right")

        sys.stdout = redirectors.TextRedirector(self.text_box, "stdout")
        sys.stderr = redirectors.TextRedirector(self.text_box, "stderr")

    def start_thread(self):
        if self.selected.get() is not '':
            self.checking_thread = MeterTester(self.selected.get())
            self.checking_thread.start()
        else:
            print("Select port.")

    def stop_thread(self):
        self.checking_thread.stop_request.set()
        print('Stopping...')

    def get_ports(self):
        """ 
        List serial port names on multiple platforms.

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result


if __name__ == '__main__':
    app = Application()
    app.mainloop()
