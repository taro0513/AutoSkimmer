from pathlib import Path
import pyautogui
from pyautogui import Point
import pyperclip
import time
import cv2
import retry
from enum import StrEnum
import psutil

pyautogui.FAILSAFE = False

class WebexLayoutEnum(StrEnum):
    GRID = "grid"
    STACK = "stack"
    SIDE_BY_SIDE = "side_by_side"

class WebexClient:
    WEBEX_KEY_WORD = "Webex"
    JOIN_MEETING_BUTTON_PATH = r"image/webex/join_meeting_button.png"
    LAYOUT_BUTTON_PATH = r"image/webex/layout_button.png"
    GRID_BUTTON_PATH = r"image/webex/grid_button.png"
    GRID_BUTTON_CLICKED_PATH = r"image/webex/grid_button_clicked.png"
    STACK_BUTTON_PATH = r"image/webex/stack_button.png"
    STACK_BUTTON_CLICKED_PATH = r"image/webex/stack_button_clicked.png"
    SIDE_BY_SIDE_BUTTON_PATH = r"image/webex/side_by_side_button.png"
    SIDE_BY_SIDE_BUTTON_CLICKED_PATH = r"image/webex/side_by_side_button_clicked.png"
    WAITING_CONTEXT_PATH = r"image/webex/waiting_context.png"
    PROCESS_NAME = "CiscoCollabHost.exe"


    def __init__(self):
        self.exe_path = Path(r"C:\Users\hank9\AppData\Local\Programs\Cisco Spark\CiscoCollabHost.exe")

    def start(self, latency: int = 0):
        if not self.exe_path.exists():
            raise FileNotFoundError(f"Zoom exe not found at {self.exe_path}")

        if latency > 0:
            time.sleep(latency)

        pyautogui.press("esc")
        pyautogui.press("win")
        pyautogui.typewrite(self.WEBEX_KEY_WORD)
        pyautogui.press("enter")

    def stop(self):
        pyautogui.hotkey("cltr", "l")
        pyautogui.press("enter")

    def press_join_meeting_button(self):
        join_meeting_button_location = self._locate_join_meeting_button()
        pyautogui.click(join_meeting_button_location)

    def _locate_join_meeting_button(self, confidence: float = 0.8) -> Point:
        return self._locate_button(self.JOIN_MEETING_BUTTON_PATH, "join meeting", confidence, 5, 0.1)

    def _locate_button(self, button_path: str, button_name: str, confidence: float = 0.8, retry_times: int = 5, reduce_confidence: float = 0.1,
                       mouse_reset: bool = False) -> Point:
        print(f"Locating {button_name} button...")
        button = cv2.imread(button_path)
        button_location = None

        for _ in range(retry_times):
            if mouse_reset:
                pyautogui.move(100, 0, duration=0.2)
                pyautogui.move(-100, 0, duration=0.2)

            try:
                button_location = pyautogui.locateCenterOnScreen(
                    button, confidence=confidence
                )
                print(f"{button_name} button found")
                print(button_location)
                break
            except:
                print(f"{button_name} button not found")
                print("Trying again...")
                print("Reducing confidence..., confidence: ", confidence)
                button_location = None
                time.sleep(3)
                confidence -= reduce_confidence

        if button_location is None:
            raise Exception(f"{button_name} button not found")

        return button_location

    def type_meeting_information(self, meeting_id: str):
        time.sleep(1)
        pyperclip.copy(meeting_id)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")

    def enter_meeting(self):
        pyautogui.press("enter")

    def maximize_window(self):
        pyautogui.hotkey("alt", "enter")

    def wait_for_enter_meeting(self):
        waiting_context = cv2.imread(self.WAITING_CONTEXT_PATH)
        check_count = 0
        while True:
            try:
                pyautogui.locateCenterOnScreen(waiting_context, confidence=0.8)
                print("Waiting for entering meeting...")
                time.sleep(3)
            except:
                check_count += 1
                if check_count > 5:
                    break
        return True

    def press_layout_button_and_select_layout(self, layout: str):
        layout_button_location = self._locate_layout_button()
        pyautogui.click(layout_button_location, clicks=2, interval=1)
        time.sleep(1)
        self._select_layout(layout)

    def _locate_layout_button(self):
        return self._locate_button(self.LAYOUT_BUTTON_PATH, "layout", 0.8, 5, 0.1)

    def _select_layout(self, layout: str):
        if layout == WebexLayoutEnum.GRID:
            layout_button_location = self._locate_grid_button()
        elif layout == WebexLayoutEnum.STACK:
            layout_button_location = self._locate_stack_button()
        elif layout == WebexLayoutEnum.SIDE_BY_SIDE:
            layout_button_location = self._locate_side_by_side_button()
        else:
            raise ValueError(f"Invalid layout {layout}")

        pyautogui.click(layout_button_location)

    def _locate_grid_button(self):
        try:
            return self._locate_button(self.GRID_BUTTON_PATH, "grid layout", 0.8, 5, 0.0)
        except:
            return self._locate_button(self.GRID_BUTTON_CLICKED_PATH, "grid layout", 0.8, 5, 0.1)

    def _locate_stack_button(self):
        try:
            return self._locate_button(self.STACK_BUTTON_PATH, "stack layout", 0.8, 5, 0.0)
        except:
            return self._locate_button(self.STACK_BUTTON_CLICKED_PATH, "stack layout", 0.8, 5, 0.1)

    def _locate_side_by_side_button(self):
        try:
            return self._locate_button(self.SIDE_BY_SIDE_BUTTON_PATH, "side by side layout", 0.8, 5, 0.0)
        except:
            return self._locate_button(self.SIDE_BY_SIDE_BUTTON_CLICKED_PATH, "side by side layout", 0.8, 5, 0.1)

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
    webex_client = WebexClient()
    webex_client.shutdown()
    webex_client.start()
    time.sleep(5)
    webex_client.press_join_meeting_button()
    webex_client.type_meeting_information('https://meet1403.webex.com/meet/pr26425131474')
    time.sleep(1)
    webex_client.enter_meeting()
    time.sleep(1)
    webex_client.maximize_window()
    webex_client.wait_for_enter_meeting()
    webex_client.press_layout_button_and_select_layout(WebexLayoutEnum.SIDE_BY_SIDE)
    webex_client.stop()
    time.sleep(5)
    webex_client.shutdown()
