from pathlib import Path
import pyautogui
from pyautogui import Point
import pyperclip
import time
import cv2
import retry
from enum import StrEnum
import psutil

from model import MeetingRoomLayoutMode

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
    READY_ENTER_PATH = r"image/webex/ready_enter.png"
    HIDE_NO_VIDEO_PEOPLE_CLICK_PATH = r"image/webex/hide_no_video_people_click.png"
    HIDE_NO_VIDEO_PEOPLE_UNCLICK_PATH = r"image/webex/hide_no_video_people_unclick.png"
    SETTING_PATH = r"image/webex/setting.png"
    CHAT_ROOM_PATH = r"image/webex/chat_room.png"
    CHAT_ROOM_JUMPER_PATH = r"image/webex/chat_room_jumper.png"
    PROCESS_NAME = "CiscoCollabHost.exe"
    HIDE_NO_VIDEO_PEOPLE_BUTTON_X_OFFSET = 130


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
        with pyautogui.hold('ctrl'):
            pyautogui.press('l')
        pyautogui.press("enter")

    def press_join_meeting_button(self):
        join_meeting_button_location = self._locate_join_meeting_button()
        pyautogui.click(join_meeting_button_location)

    def _locate_join_meeting_button(self, confidence: float = 0.8) -> Point:
        return self._locate_button(self.JOIN_MEETING_BUTTON_PATH, "join meeting", confidence, 5, 0.1)

    def _locate_button(self, button_path: str, button_name: str, confidence: float = 0.8, retry_times: int = 5, reduce_confidence: float = 0.1,
                       mouse_reset: bool = False, raise_error: bool = True) -> Point:
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
            if raise_error:
                raise Exception(f"{button_name} button not found")
            else:
                print(f"{button_name} button not found")
                return None

        return button_location

    def type_meeting_information(self, meeting_id: str):
        time.sleep(1)
        pyperclip.copy(meeting_id)
        with pyautogui.hold('ctrl'):
            pyautogui.press('v')
        pyautogui.press("enter")

    def enter_meeting(self):
        pyautogui.press("enter")

    def maximize_window(self):
        with pyautogui.hold('alt'):
            pyautogui.press('enter')

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
        self.locate_layout_button_and_click(press_enter=False)
        time.sleep(1)
        self._select_layout(layout)

    def locate_layout_button_and_click(self, press_enter: bool = False):
        layout_button_location = self._locate_layout_button()
        pyautogui.click(layout_button_location, clicks=1, interval=3)
        if press_enter:
            pyautogui.press("enter")

    def _locate_layout_button(self):
        return self._locate_button(self.LAYOUT_BUTTON_PATH, "layout", 0.8, 5, 0.1)

    def _select_layout(self, layout: str):
        if layout == MeetingRoomLayoutMode.MODE_A:
            self.locate_side_by_side_button(display_no_video_people=False)
        elif layout == MeetingRoomLayoutMode.MODE_B:
            self.locate_stack_button()
        elif layout == MeetingRoomLayoutMode.MODE_C:
            self.locate_side_by_side_button(display_no_video_people=True)
        elif layout == MeetingRoomLayoutMode.MODE_D:
            self.locate_grid_button()
        else:
            raise ValueError(f"Invalid layout {layout}")

    def locate_grid_button(self):
        layout_button_location = self._locate_grid_button()
        pyautogui.click(layout_button_location)

    def locate_stack_button(self):
        layout_button_location = self._locate_stack_button()
        pyautogui.click(layout_button_location)
        self.locate_layout_button_and_click()
        hide_no_video_people_click_location = self._locate_button(self.HIDE_NO_VIDEO_PEOPLE_CLICK_PATH, "hide no video people click", 0.9, 5, 0.0, raise_error=False)
        if hide_no_video_people_click_location:
            pyautogui.click(hide_no_video_people_click_location.x + self.HIDE_NO_VIDEO_PEOPLE_BUTTON_X_OFFSET, hide_no_video_people_click_location.y)
        else:
            self.cancel_window()

    def locate_side_by_side_button(self, display_no_video_people: bool = False):
        layout_button_location = self._locate_side_by_side_button()
        pyautogui.click(layout_button_location)
        self.locate_layout_button_and_click()
        if display_no_video_people:
            hide_no_video_people_unclick_location = self._locate_button(self.HIDE_NO_VIDEO_PEOPLE_UNCLICK_PATH, "hide no video people click", 0.9, 5, 0.0, raise_error=False)
            if hide_no_video_people_unclick_location:
                pyautogui.click(hide_no_video_people_unclick_location.x + self.HIDE_NO_VIDEO_PEOPLE_BUTTON_X_OFFSET, hide_no_video_people_unclick_location.y)
            else:
                self.cancel_window()
        else:
            hide_no_video_people_click_location = self._locate_button(self.HIDE_NO_VIDEO_PEOPLE_CLICK_PATH, "hide no video people click", 0.9, 5, 0.0, raise_error=False)
            if hide_no_video_people_click_location:
                pyautogui.click(hide_no_video_people_click_location.x + self.HIDE_NO_VIDEO_PEOPLE_BUTTON_X_OFFSET, hide_no_video_people_click_location.y)
            else:
                self.cancel_window()


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

    def wait_for_ready_enter_window(self):
        return self._locate_button(self.READY_ENTER_PATH, "ready enter", 0.8, 5, reduce_confidence=0.05, raise_error=False)

    def cancel_window(self):
        pyautogui.press("esc")

    def open_chat_room(self):
        chat_room_location = self._locate_button(self.CHAT_ROOM_PATH, "chat room jumper", 0.8, 5, 0.0, raise_error=False)
        if chat_room_location:
            pyautogui.click(chat_room_location)
        else:
            self.cancel_window()

        chat_room_jumper_location = self._locate_button(self.CHAT_ROOM_JUMPER_PATH, "chat room jumper", 0.8, 5, 0.0, raise_error=False)
        if chat_room_jumper_location:
            pyautogui.click(chat_room_jumper_location)
        else:
            self.cancel_window()



if __name__ == "__main__":
    webex_client = WebexClient()

    webex_client.shutdown()
    webex_client.start()
    time.sleep(5)
    webex_client.press_join_meeting_button()
    webex_client.type_meeting_information('https://meet1403.webex.com/meet/pr26425131474')

    while True:
        if webex_client.wait_for_ready_enter_window():
            break
        time.sleep(10)
        webex_client.cancel_window()
        webex_client.press_join_meeting_button()
        webex_client.type_meeting_information("https://meet1403.webex.com/meet/pr26425131474")

    webex_client.enter_meeting()
    time.sleep(1)
    webex_client.maximize_window()
    webex_client.wait_for_enter_meeting()
    time.sleep(5)
    webex_client.press_layout_button_and_select_layout(MeetingRoomLayoutMode.MODE_A)
    time.sleep(5)
    webex_client.open_chat_room()

    webex_client.stop()
    time.sleep(5)
    webex_client.shutdown()
