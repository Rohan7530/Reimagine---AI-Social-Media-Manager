import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from typing import Callable

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback

    def on_created(self, event):
        if not event.is_directory:
            # Wait a brief moment to ensure file write is complete
            time.sleep(1)
            print(f"New file detected: {event.src_path}")
            self.callback(event.src_path)

class FolderMonitor:
    def __init__(self, folder_path: str, callback: Callable[[str], None]):
        self.folder_path = folder_path
        self.callback = callback
        self.observer = Observer()

    def start(self):
        event_handler = NewFileHandler(self.callback)
        self.observer.schedule(event_handler, self.folder_path, recursive=False)
        self.observer.start()
        print(f"Monitoring {self.folder_path} for new files...")

    def stop(self):
        self.observer.stop()
        self.observer.join()
