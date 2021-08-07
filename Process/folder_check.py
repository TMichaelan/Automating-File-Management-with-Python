import os
import shutil
import time
import configparser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

config = configparser.ConfigParser()
config.read("settings.ini")


temp_folder = config["DEFAULT"]["temp_folder"]
formats_check = [".eps", ".psd"]
folder_list = ["2.5cm", "3.5cm", "4.5cm", "6.5cm", "9.5cm"]


def start_JSX_loader():
    time.sleep(2)
    os.system("JSXLoader.py")

class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path[1:4] != "tmp":

            if os.path.isdir(event.src_path):
                time.sleep(5)
                if str(event.src_path[-5:]) in folder_list:

                    try:
                        print("[*] Loading...1")
                        shutil.copytree(event.src_path, temp_folder + "\\" + event.src_path[-5:])
                        start_JSX_loader()
                    except Exception:
                        print("[*] Loading...2")
                        time.sleep(3)
                        try:
                            shutil.copytree(event.src_path, temp_folder + "\\" + event.src_path[-5:])
                            start_JSX_loader()
                        except Exception:
                            print("[*] ERROR...")


            # if event.src_path[-4:] in formats_check:
            #     try:

            #         shutil.copy(event.src_path, temp_folder)
            #         os.remove(event.src_path)
            #     except Exception:
            #         print("[*] Loading...")
            #         time.sleep(2)
            #         try:
            #             shutil.copy(event.src_path, temp_folder)
            #             os.remove(event.src_path)
            #         except Exception:
            #             print("[*] ERROR...")

    def on_modified(self, event):
        pass
        # if event.src_path[1:4] != "tmp":
        #     print('[*]',event.event_type, event.src_path)

    def on_deleted(self, event):
        if event.src_path[1:4] != "tmp":
            print('[*]',event.event_type, event.src_path)

    def on_moved(self, event):
        if event.src_path[1:4] != "tmp":
            print('[*]',event.event_type, event.src_path, event.dest_path)

if __name__ == "__main__":
    print("[*] Starting...")
    path = r"C:\Google Drive\ToDo"  # tracked folder
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("[*] Process...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()