from pathlib import Path
import pyautogui
from pyautogui import Point
import pyperclip
import time
import cv2
import retry
from enum import StrEnum

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
        pyautogui.hotkey("alt", "q")
        pyautogui.press("enter")

    def press_join_meeting_button(self):
        join_meeting_button_location = self._locate_join_meeting_button()
        pyautogui.click(join_meeting_button_location)

    def _locate_join_meeting_button(self, confidence: float = 0.8) -> Point:
        return self._locate_button(self.JOIN_MEETING_BUTTON_PATH, "join meeting", confidence, 5, 0.1)

    def type_meeting_information(self, meeting_id: str, username: str):
        time.sleep(1)
        pyperclip.copy(meeting_id)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press("tab")
        pyautogui.press("tab")
        time.sleep(1)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("backspace")
        time.sleep(1)
        pyperclip.copy(username)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")

    def type_meeting_password(self, meeting_password: str):
        time.sleep(1)
        pyperclip.copy(meeting_password)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")

    def maximize_window(self):
        pyautogui.hotkey("alt", "f")

    def press_layout_button_and_select_layout(self, layout: str):
        layout_button_location = self._locate_layout_button()
        pyautogui.moveTo(layout_button_location) # 2510, 28
        pyautogui.click(layout_button_location)
        time.sleep(1)
        self._select_layout(layout)

    def _select_layout(self, layout: str):
        if layout == ZoomLayoutEnum.SPEAKER:
            layout_button_location = self._locate_speaker_button()
        elif layout == ZoomLayoutEnum.GALLERY:
            layout_button_location = self._locate_gallery_button()
        elif layout == ZoomLayoutEnum.MULTIPLE_SPEAKER:
            layout_button_location = self._locate_multiple_speaker_button()
        else:
            raise ValueError(f"Invalid layout {layout}")

        pyautogui.click(layout_button_location)

    def _locate_speaker_button(self, confidence: float = 0.8) -> Point:
        return self._locate_button(self.SPEAKER_BUTTON_PATH, "speaker", confidence, 5, 0.1)

    def _locate_gallery_button(self, confidence: float = 0.8) -> Point:
        return self._locate_button(self.GALLERY_BUTTON_PATH, "gallery", confidence, 5, 0.1)

    def _locate_multiple_speaker_button(self, confidence: float = 0.8) -> Point:
        return self._locate_button(self.MULTIPLE_SPEAKER_BUTTON_PATH, "multiple speaker", confidence, 5, 0.1)

    def _locate_layout_button(self, confidence: float = 0.8) -> Point:
        return self._locate_button(self.LAYOUT_BUTTON_PATH, "layout", confidence, 5, 0.1, mouse_reset=True)


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


if __name__ == '__main__':
    zoom = ZoomClient()
    zoom.start()
    time.sleep(8)
    zoom.press_join_meeting_button()
    zoom.type_meeting_information("https://zoom.us/j/99502411589?pwd=X8TCGMXSq6HwYOjb7w5yqu6axGbBR0.1", "username")
    zoom.type_meeting_password("3rhgcX")
    time.sleep(3)
    zoom.maximize_window()
    zoom.press_layout_button_and_select_layout(ZoomLayoutEnum.SPEAKER)
    time.sleep(2)
    zoom.stop()