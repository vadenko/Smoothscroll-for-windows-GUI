import argparse
import easing_functions
from win32con import VK_SHIFT

from smoothscroll import (SmoothScroll,
                          SmoothScrollConfig, AppConfig, ScrollConfig)

def get_default_config():
    return SmoothScrollConfig(
        app_config=[
            AppConfig(
                regexp=r'.*',
                scroll_config=ScrollConfig(
                    distance=None,  # [px] None - automatic detection by the system (default=120)
                    acceleration=1.,  # [x] scroll down acceleration
                    opposite_acceleration=1.2,  # [x] scroll up acceleration
                    acceleration_delta=70,  # [ms]
                    acceleration_max=14,  # [x] max acceleration steps
                    duration=200,  # [ms]
                    pulse_scale=3,  # [x] tail to head ratio
                    ease=easing_functions.LinearInOut,  # Easing function
                    inverted=False,  # down, up = up, down
                    horizontal_scroll_key=VK_SHIFT  # VK_SHIFT, VK_CONTROL, VK_MENU
                ),
            ),
            AppConfig(
                regexp=r'.*pycharm64\.exe.*',
                enabled=False
            ),
        ]
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="SmoothScroll for Windows")
    parser.add_argument('--console', action='store_true', help='Запустить в консольном режиме')
    parser.add_argument('--tray', action='store_true', help='Запустить свернутым в трей с автозапуском сервиса')
    args = parser.parse_args()

    if args.console:
        SmoothScroll(config=get_default_config()).start(is_block=True)
    elif args.tray:
        import customtkinter as ctk
        from gui import SmoothScrollGUI
        root = ctk.CTk()
        app = SmoothScrollGUI(root, auto_start=True, start_minimized=True)
        root.mainloop()
    else:
        import customtkinter as ctk
        from gui import SmoothScrollGUI
        root = ctk.CTk()
        app = SmoothScrollGUI(root)
        root.mainloop()
