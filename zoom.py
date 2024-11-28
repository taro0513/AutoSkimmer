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

class ZoomLayoutEnum(StrEnum):
    SPEAKER = "speaker"
    GALLERY = "gallery"
    MULTIPLE_SPEAKER = "multiple_speaker"

class ZoomClient:
    ZOOM_KEY_WORD = "Zoom Workplace"
    JOIN_MEETING_BUTTON_PATH = r"image/zoom/join_meeting_button.png"
    LAYOUT_BUTTON_PATH = r"image/zoom/layout_button.png"
    SPEAKER_BUTTON_PATH = r"image/zoom/speaker_button.png"
    GALLERY_BUTTON_PATH = r"image/zoom/gallery_button.png"
    MULTIPLE_SPEAKER_BUTTON_PATH = r"image/zoom/multiple_speaker_button.png"
    ERROR_ROOM_ID_PATH = r"image/zoom/error_message.png"
    ENTER_PASSWORD_WINDOW_PATH = r"image/zoom/enter_password_window.png"
    CHAT_ROOM_PATH = r"image/zoom/chat_room.png"
    DISPLAY_SELF_AWARE_PATH = r"image/zoom/display_self_aware.png"
    HIDE_SELF_AWARE_PATH = r"image/zoom/hide_self_aware.png"
    DISPLAY_NO_VIDEO_PEOPLE_PATH = r"image/zoom/display_no_video_people.png"
    HIDE_NO_VIDEO_PEOPLE_PATH = r"image/zoom/hide_no_video_people.png"
    PROCESS_NAME = "Zoom.exe"

    def __init__(self):
        self.exe_path = Path(r"C:\Program Files\Zoom\bin\Zoom.exe")
    def start(self, latency: int = 0):
        if not self.exe_path.exists():
            raise FileNotFoundError(f"Zoom exe not found at {self.exe_path}")

        if latency > 0:
            time.sleep(latency)

        pyautogui.press("esc")
        pyautogui.press("win")
        pyautogui.typewrite(self.ZOOM_KEY_WORD)
        pyautogui.press("enter")

    def stop(self):
        with pyautogui.hold('alt'):
            pyautogui.press('q')
        pyautogui.press("enter")

    def press_join_meeting_button(self):
        join_meeting_button_location = self._locate_join_meeting_button()
        pyautogui.click(join_meeting_button_location)

    def _locate_join_meeting_button(self, confidence: float = 0.8) -> Point:
        return self._locate_button(self.JOIN_MEETING_BUTTON_PATH, "join meeting", confidence, 5, 0.1)

    def type_meeting_information(self, meeting_id: str, username: str):
        time.sleep(3)
        pyperclip.copy(str(meeting_id))
        with pyautogui.hold('ctrl'):
            pyautogui.press('v')
        time.sleep(1)
        pyautogui.press("tab")
        pyautogui.press("tab")
        time.sleep(1)
        with pyautogui.hold('ctrl'):
            pyautogui.press('a')
        pyautogui.press("backspace")
        time.sleep(1)
        pyperclip.copy(username)
        with pyautogui.hold('ctrl'):
            pyautogui.press('v')
        pyautogui.press("enter")




    def check_room_id_is_correct(self, retry_times: int = 10, retry_interval: float = 5, check_count: int = 5):
        error_room_id = cv2.imread(self.ERROR_ROOM_ID_PATH)
        _check_count = 0
        for i in range(retry_times):
            print("Checking room id error... ", i)
            if _check_count >= check_count:
                return True
            try:
                error_room_id_location = pyautogui.locateCenterOnScreen(
                    error_room_id, confidence=0.8
                )
                print("Error room id found")
            except:
                error_room_id_location = None
                _check_count += 1
                print("Error room id not found")
            time.sleep(retry_interval)
        return False

    def type_meeting_password(self, meeting_password: str):
        time.sleep(1)
        pyperclip.copy(meeting_password)
        with pyautogui.hold('ctrl'):
            pyautogui.press('v')
        pyautogui.press("enter")

    def maximize_window(self):
        pyautogui.click(pyautogui.position(), clicks=1, interval=2)
        with pyautogui.hold('alt'):
            pyautogui.press('f')

    def press_layout_button_and_select_layout(self, layout: str):
        self.locate_layout_button_and_click()
        time.sleep(1)
        self._select_layout(layout)

    def locate_layout_button_and_click(self):
        layout_button_location = self._locate_layout_button()
        pyautogui.moveTo(layout_button_location)  # 2510, 28
        pyautogui.click(layout_button_location)

    def _select_layout(self, layout: str):
        if layout == MeetingRoomLayoutMode.MODE_A:
            self.locate_speaker_button()
        elif layout == MeetingRoomLayoutMode.MODE_B:
            self.locate_speaker_button(default_mode=True)
        elif layout == MeetingRoomLayoutMode.MODE_C:
            self.locate_multiple_speaker_button()
        elif layout == MeetingRoomLayoutMode.MODE_D:
            self.locate_gallery_button()
        else:
            raise ValueError(f"Invalid layout {layout}")


    def locate_speaker_button(self, default_mode: bool = False):
        layout_button_location = self._locate_speaker_button()
        pyautogui.click(layout_button_location)

        if default_mode:
            self.locate_layout_button_and_click()
            display_no_video_people = self._locate_button(
                self.DISPLAY_NO_VIDEO_PEOPLE_PATH, "display no video people", 0.9, 5, 0, raise_error=False
            )
            if display_no_video_people:
                pyautogui.click(display_no_video_people)
            else:
                self.cancel_window()

        else:
            self.locate_layout_button_and_click()
            hide_self_aware = self._locate_button(
                self.HIDE_SELF_AWARE_PATH, "hide self aware", 0.9, 5, 0, raise_error=False
            )
            if hide_self_aware:
                pyautogui.click(hide_self_aware)
            else:
                self.cancel_window()
            self.locate_layout_button_and_click()
            hide_no_video_people = self._locate_button(
                self.HIDE_NO_VIDEO_PEOPLE_PATH, "hide no video people", 0.9, 5, 0, raise_error=False
            )
            if hide_no_video_people:
                pyautogui.click(hide_no_video_people)
            else:
                self.cancel_window()

    def locate_gallery_button(self):
        layout_button_location = self._locate_gallery_button()
        pyautogui.click(layout_button_location)
        self.locate_layout_button_and_click()
        display_no_video_people = self._locate_button(
            self.DISPLAY_NO_VIDEO_PEOPLE_PATH, "display no video people", 0.9, 5, 0, raise_error=False
        )
        if display_no_video_people:
            pyautogui.click(display_no_video_people)
        else:
            self.cancel_window()

    def locate_multiple_speaker_button(self):
        layout_button_location = self._locate_multiple_speaker_button()
        pyautogui.click(layout_button_location)
        self.locate_layout_button_and_click()
        display_no_video_people = self._locate_button(
            self.DISPLAY_NO_VIDEO_PEOPLE_PATH, "display no video people", 0.9, 5, 0, raise_error=False
        )
        if display_no_video_people:
            pyautogui.click(display_no_video_people)
        else:
            self.cancel_window()



    def _locate_speaker_button(self, confidence: float = 0.8) -> Point:
        return self._locate_button(self.SPEAKER_BUTTON_PATH, "speaker", confidence, 5, 0.1)

    def _locate_gallery_button(self, confidence: float = 0.8) -> Point:
        return self._locate_button(self.GALLERY_BUTTON_PATH, "gallery", confidence, 5, 0.1)

    def _locate_multiple_speaker_button(self, confidence: float = 0.8) -> Point:
        return self._locate_button(self.MULTIPLE_SPEAKER_BUTTON_PATH, "multiple speaker", confidence, 5, 0.1)

    def _locate_layout_button(self, confidence: float = 0.8) -> Point:
        return self._locate_button(self.LAYOUT_BUTTON_PATH, "layout", confidence, 5, 0.1, mouse_reset=True)


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

    def shutdown(self):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] == self.PROCESS_NAME:
                    print(f"Terminating process: {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.terminate()
                    proc.wait()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def cancel_window(self):
        pyautogui.press("esc")

    def reset_mouse_position(self):
        pyautogui.moveTo(0, 0, duration=0.2)

    def wait_for_enter_password_window(self):
        return self._locate_button(self.ENTER_PASSWORD_WINDOW_PATH, "enter password window", 0.8, 5, 0.05, raise_error=False)

    def open_chat_room(self):
        with pyautogui.hold('alt'):
            pyautogui.press('h')

    def move_chat_room_to_left_button(self, move_to: int = 300):
        with pyautogui.hold('alt'):
            with pyautogui.hold('shift'):
                pyautogui.press('h')
        chat_room_position = self._locate_button(self.CHAT_ROOM_PATH, "chat room", 0.8, 5, 0.05, raise_error=False)
        pyautogui.moveTo(chat_room_position)
        pyautogui.dragTo(move_to, chat_room_position.y, duration=0.5)

if __name__ == '__main__':
    zoom = ZoomClient()
    zoom.shutdown()
    time.sleep(5)
    zoom.start()
    time.sleep(5)
    zoom.press_join_meeting_button()

    zoom.type_meeting_information("https://zoom.us/j/94345039088?pwd=deUSpmasIx9LVcze2gz5moVn7SEzlx.1", "username")

    while True:
        zoom.reset_mouse_position()
        if zoom.wait_for_enter_password_window():
            break
        time.sleep(3)
        zoom.cancel_window()
        zoom.press_join_meeting_button()
        zoom.type_meeting_information("https://zoom.us/j/94345039088?pwd=deUSpmasIx9LVcze2gz5moVn7SEzlx.1", "username")

    zoom.type_meeting_password("vSU0h4")
    time.sleep(5)
    zoom.maximize_window()
    zoom.press_layout_button_and_select_layout(ZoomLayoutEnum.GALLERY)
    time.sleep(2)
    zoom.open_chat_room()
    zoom.move_chat_room_to_left_button()

    time.sleep(10)
    zoom.stop()