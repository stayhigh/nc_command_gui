#!/usr/bin/env python3

from tkinter import *
import subprocess
from threading import Thread
import time
import shlex

# init with window title and icon
root = Tk()
root.title('nc command line GUI')
root.iconbitmap('c:/gui/codemy.ico')


# set window size
root.geometry("800x600")
#width = root.winfo_screenwidth()
#height = (root.winfo_screenheight() - 70)
#root.geometry(f"{width}x{height}+0+0")

# create frame
frame = LabelFrame(root, padx=50, pady=50)
frame.pack(padx=10, pady=10)

# entry and label
ipLabel = Label(frame, text="IP:").grid(row=0, column=0)
ip_entry = Entry(frame, width=30)
ip_entry.grid(row=0, column=1)
#ip_entry.insert(0, "ss.helloworldml.com")
ip_entry.insert(0, "127.0.0.1")

portLabel = Label(frame, text="PORT:").grid(row=1, column=0)
port_entry = Entry(frame, width=30, text='80')
port_entry.grid(row=1, column=1)
#port_entry.insert(0, "443")
port_entry.insert(0, "8888")

# result var
var = StringVar()

# run subprocess run command
def runcmd(command):
    ret = subprocess.run(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",timeout=1)
    if ret.returncode == 0:
        print("success:",ret)
    else:
        print("error:",ret)


# run subprocess popen check
def popencmd(command):
    subp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    try:
        subp.wait(10)
    except:
        return "subprocess timeout"

    if subp.poll() == 0:
        print("failed")
        mystderr = subp.communicate()[1]
        print(mystderr)
        return mystderr
    else:
        mystdout = subp.communicate()[0]
        print(mystdout)
        return mystdout

# subprocess run
def subprocess_callback(command):
    proc = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8") # shell=True will fail
    try:
        outs, errs = proc.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    result = "STDOUT:{}\t" \
    "STDERR:{}\n".format(outs, errs)
    return result

# non-blocking test function
def print_hello():
    outputText.insert(END, "Hello" + '\n')
    time.sleep(3)
    outputText.insert(END, "Done" + '\n')

non_occupied_session_id = 0
# buttion actions
def run_nc(var, ip, port):
    # make timestamp and session id
    run_ts = time.time()
    global non_occupied_session_id
    thread_session_id = non_occupied_session_id
    thread_session_id += 1
    non_occupied_session_id = thread_session_id

    # run command
    run_leading_tag = "RUN_{} run_ts={}>>".format(thread_session_id, run_ts)
    var.set("{} {} {}".format("nc -w 2 -vvv", str(ip), str(port))) # -w option is for 2 sec timeout
    outputText.insert(END, "{} {} {}".format(run_leading_tag, var.get(), '\n'))

    # collect the result
    result = subprocess_callback(shlex.split(var.get()))
    result_ts = time.time()
    result_leading_tag = "RESULT_{} result_ts={}>>".format(thread_session_id, result_ts)
    outputText.insert(END, "{} {} {}".format(result_leading_tag, result, '\n'))

# non-blocking test
#submit_btn = Button(frame, text="exec", command=lambda: Thread(target=print_hello).start())

# Create Submit Button
submit_btn = Button(frame, text="exec", command=lambda: Thread(target=run_nc, args=(var, ip_entry.get(), port_entry.get())).start())
submit_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


# create text
outputText = Text(root, height=20,
              width=100,
              bg="light yellow")
outputText.pack()


# run main func
root.attributes('-topmost',True)
root.mainloop()
