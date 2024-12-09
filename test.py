import win32gui

def get_all_window_names():
    def callback(hwnd, window_list):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if window_title:
                window_list.append(window_title)
        return True

    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

if __name__ == "__main__":
    window_names = get_all_window_names()
    for name in window_names:
        print(name)
