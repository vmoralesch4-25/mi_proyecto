import os
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).parent.parent

def main():
    base_path = get_base_path()
    model_path = base_path / 'data' / 'models' / 'ResNet50V2_final.tflite'
    static_path = base_path / 'data' / 'static'
    
    from server.http_server import start_server
    start_server(str(model_path), str(static_path), 8000)

if __name__ == '__main__':
    main()