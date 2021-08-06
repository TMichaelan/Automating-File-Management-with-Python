import sys
import time
import configparser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path[1:4] != "tmp":
            print('[*]',event.event_type, event.src_path)

    def on_modified(self, event):

        if event.src_path[1:4] != "tmp":
            print('[*]',event.event_type, event.src_path)

    def on_deleted(self, event):
        if event.src_path[1:4] != "tmp":
            print('[*]',event.event_type, event.src_path)

    def on_moved(self, event):
        if event.src_path[1:4] != "tmp":
            print('[*]',event.event_type, event.src_path, event.dest_path)

if __name__ == "__main__":
    print("[*] Starting...")
    path = r"C:\Google Drive"  # tracked folder
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