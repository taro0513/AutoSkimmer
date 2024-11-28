from pathlib import Path
import psutil
import time

import obsws_python
from obsws_python import ReqClient
import pyautogui


class OBSClient:
    OBS_KEY_WORD = "OBS Studio (64bit)"
    PROCESS_NAME = "obs64.exe"
    RECORDING_SCENE = "AutoSkimmer"

    def __init__(self, host: str = "localhost", port: int = 4455):
        self.client = None
        self.exe_path = Path(r"C:\Program Files\obs-studio\bin\64bit\obs64.exe")
        self.host = host
        self.port = port

    def start(self, latency: int = 0):
        if not self.exe_path.exists():
            raise FileNotFoundError(f"Zoom exe not found at {self.exe_path}")

        if latency > 0:
            time.sleep(latency)

        pyautogui.press("esc")
        pyautogui.press("win")
        pyautogui.typewrite(self.OBS_KEY_WORD)
        pyautogui.press("enter")

    def connect_to_server(self):
        try:
            self.client = obsws_python.ReqClient(
                host=self.host, port=self.port
            )
        except:
            print("Failed to connect to OBS server")

    def set_scene(self, scene_name: str):
        self.client.set_current_program_scene(scene_name)

    def set_recording_scene(self):
        self.client.set_current_program_scene(self.RECORDING_SCENE)

    def create_scene(self, scene_name: str):
        try:
            self.client.create_scene(scene_name)
        except Exception as e:
            print(f"Failed to create scene: {scene_name}")

    def create_scene_source(self, scene_name: str, source_name: str, enable: bool = True):
        try:
            self.client.create_scene_item(scene_name, source_name, enable)
        except Exception as e:
            print(f"Failed to create scene item: {source_name}")

    def start_record(self):
        self.client.start_record()

    def stop_record(self):
        self.client.stop_record()

    def shutdown(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] == self.PROCESS_NAME:
                    print(f"Terminating process: {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.terminate()
                    proc.wait()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

if __name__ == "__main__":
    obs_client = OBSClient()
    obs_client.connect_to_server()
    obs_client.connect_to_server()
    # obs_client.create_scene("AutoSkimmer")
    obs_client.set_scene("AutoSkimmer")
    obs_client.start_record()
    time.sleep(5)
    obs_client.stop_record()

    # obs_client.shutdown()
    # time.sleep(5)
    # obs_client.start()
    # pyautogui.press("enter")
    # time.sleep(5)
    # obs_client.connect_to_server()
    # time.sleep(10)
    # obs_client.shutdown()
    # del obs_client