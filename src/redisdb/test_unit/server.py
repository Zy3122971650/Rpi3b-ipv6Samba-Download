import subprocess
import time

def main():
    r = subprocess.Popen('redis --port=10086')
    while 1:
        time.sleep(3)