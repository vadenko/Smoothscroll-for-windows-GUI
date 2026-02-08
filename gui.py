import json
import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Optional
import easing_functions
import pystray
from PIL import Image, ImageDraw
import threading
import winreg
import os
import sys
import webbrowser
import tempfile
import psutil


def get_app_directory():
    """ Get the application directory (where the app is installed) """
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller executable
        return os.path.dirname(sys.executable)
    else:
        # Running as Python script
        return os.path.dirname(os.path.abspath(__file__))


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = get_app_directory()

    return os.path.join(base_path, relative_path)

from smoothscroll import SmoothScroll, SmoothScrollConfig, AppConfig, ScrollConfig
from win32con import VK_SHIFT, VK_CONTROL, VK_MENU

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Lang:
    def __init__(self, lang='en'):
        self.lang = lang
        self.texts = {
            'en': {
                'title': 'SmoothScroll GUI',
                'global_settings': 'Global Settings',
                'apps': 'Applications (exceptions)',
                'app_settings': 'App Settings',
                'save': 'Save',
                'start': 'Start',
                'stop': 'Stop',
                'appearance_mode': 'Appearance Mode',
                'language': 'Language',
                'autostart': 'Autostart with Windows',
                'start_minimized': 'Start minimized to tray',
                'distance': 'Distance (px, None for auto):',
                'acceleration': 'Acceleration:',
                'opposite_acceleration': 'Opposite Acceleration:',
                'acceleration_delta': 'Acceleration Delta (ms):',
                'acceleration_max': 'Acceleration Max:',
                'duration': 'Duration (ms):',
                'pulse_scale': 'Pulse Scale:',
                'inverted': 'Inverted',
                'easing_function': 'Easing Function:',
                'horizontal_scroll_key': 'Horizontal Scroll Key:',
                'add': 'Add',
                'remove': 'Remove',
                'edit': 'Edit',
                'path': 'Path:',
                'regexp': 'Regexp:',
                'enabled': 'Enabled',
                'save_btn': 'Save',
                'success': 'Success',
                'error': 'Error',
                'warning': 'Warning',
                'config_saved': 'Config saved to',
                'smoothscroll_started': 'SmoothScroll started',
                'smoothscroll_stopped': 'SmoothScroll stopped',
                'already_running': 'Already running',
                'not_running': 'Not running',
                'autostart_enabled': 'Autostart enabled',
                'autostart_disabled': 'Autostart disabled',
                'appearance_applied': 'Appearance changes applied.',
                'restart_for_lang': 'Restart the application to apply language changes. Dont forget press "Save" button.',
                'select_app': 'Select an application to',
                'add_app': 'Add Application',
                'edit_app': 'Edit Application',
                'load_config_error': 'Error loading config',
                'config_load_success': 'Config loaded successfully',
                'info': 'Information',
                'about_title': 'About',
                'about_desc': 'This application provides smooth scrolling in all applications (except exceptions in settings) on Windows, with many settings, and most importantly - a graphical interface.',
                'about_fork': 'This application is a fork of the',
                'about_original': 'Smoothscroll-for-windows',
                'about_improvements': 'project by re1von, main improvements - GUI.',
                'about_link': 'Project link:',
                'about_project_url': 'https://github.com/vadenko/Smoothscroll-for-windows-GUI',
                'about_version': 'Version: 1.0.2'
            },
            'ru': {
                'title': 'SmoothScroll GUI',
                'global_settings': 'Глобальные настройки',
                'apps': 'Приложения (исключения)',
                'app_settings': 'Настройки приложения',
                'save': 'Сохранить',
                'start': 'Запустить',
                'stop': 'Остановить',
                'appearance_mode': 'Режим внешнего вида',
                'language': 'Язык',
                'autostart': 'Автозагрузка с Windows',
                'start_minimized': 'Запускать свернутым',
                'distance': 'Расстояние (px, None для авто):',
                'acceleration': 'Ускорение:',
                'opposite_acceleration': 'Обратное ускорение:',
                'acceleration_delta': 'Дельта ускорения (мс):',
                'acceleration_max': 'Максимальное ускорение:',
                'duration': 'Длительность (мс):',
                'pulse_scale': 'Масштаб импульса:',
                'inverted': 'Инвертировано',
                'easing_function': 'Функция easing:',
                'horizontal_scroll_key': 'Клавиша горизонтальной прокрутки:',
                'add': 'Добавить',
                'remove': 'Удалить',
                'edit': 'Редактировать',
                'path': 'Путь:',
                'regexp': 'Регулярное выражение:',
                'enabled': 'Включено',
                'save_btn': 'Сохранить',
                'success': 'Успех',
                'error': 'Ошибка',
                'warning': 'Предупреждение',
                'config_saved': 'Конфиг сохранен в',
                'smoothscroll_started': 'SmoothScroll запущен',
                'smoothscroll_stopped': 'SmoothScroll остановлен',
                'already_running': 'Уже запущено',
                'not_running': 'Не запущено',
                'autostart_enabled': 'Автозагрузка включена',
                'autostart_disabled': 'Автозагрузка отключена',
                'appearance_applied': 'Изменения режима внешнего вида применены.',
                'restart_for_lang': 'Перезапустите приложение для применения изменений языка. Не забудьте нажать кнопку "Сохранить"',
                'select_app': 'Выберите приложение для',
                'add_app': 'Добавить приложение',
                'edit_app': 'Редактировать приложение',
                'load_config_error': 'Ошибка загрузки конфига',
                'config_load_success': 'Конфиг загружен успешно',
                'info': 'Информация',
                'about_title': 'О приложении',
                'about_desc': 'Это приложение для придания плавной прокрутки во всех приложениях (кроме исключений в настройках) в Windows, имеет множество настроек, и самое главное - графический интерфейс.',
                'about_fork': 'Это приложение является форком проекта',
                'about_original': 'Smoothscroll-for-windows',
                'about_improvements': 'от re1von, основные улучшения - GUI.',
                'about_link': 'Ссылка на проект:',
                'about_project_url': 'https://github.com/vadenko/Smoothscroll-for-windows-GUI',
                'about_version': 'Версия: 1.0.2'
            }
        }

    def get(self, key):
        return self.texts[self.lang].get(key, key)

class SmoothScrollGUI:
    def __init__(self, root, auto_start=False, start_minimized=False):
        # Check for single instance
        self.lock_file = os.path.join(tempfile.gettempdir(), "smoothscroll.lock")
        if os.path.exists(self.lock_file):
            try:
                with open(self.lock_file, 'r') as f:
                    pid = int(f.read().strip())
                
                # Try to check if process is still running using psutil
                if psutil.pid_exists(pid):
                    messagebox.showerror("Error", "Application is already running.")
                    sys.exit(1)
                else:
                    # Stale lock file, remove it
                    os.remove(self.lock_file)
            except (ValueError, OSError):
                # Invalid PID or file read error, remove lock file
                try:
                    os.remove(self.lock_file)
                except OSError:
                    pass

        # Create new lock file
        with open(self.lock_file, 'w') as f:
            f.write(str(os.getpid()))

        self.root = root
        self.root.title("SmoothScroll for Windows GUI")
        self.root.geometry("900x780")
        try:
            self.root.iconbitmap(resource_path('icon.ico'))
        except:
            pass  # Icon not found, use default

        self.smooth_scroll: Optional[SmoothScroll] = None
        self.config = self.get_default_config()
        self.auto_start = auto_start
        self.start_minimized = start_minimized
        self.lang = Lang('en')  # Default language

        self.create_tray_icon()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.load_config()  # Load config first to set language
        self.create_widgets()
        self.populate_apps_list()  # Populate after widgets are created
        self.update_gui_from_config()  # Update GUI after widgets are created

        if self.auto_start:
            self.start_smooth_scroll()
        if self.start_minimized:
            self.on_close()

    def get_default_config(self):
        return SmoothScrollConfig(
            app_config=[
                AppConfig(
                    regexp=r'.*',
                    scroll_config=ScrollConfig(
                        distance=None,
                        acceleration=1.,
                        opposite_acceleration=1.2,
                        acceleration_delta=70,
                        acceleration_max=14,
                        duration=200,
                        pulse_scale=3,
                        ease=easing_functions.LinearInOut,
                        inverted=False,
                        horizontal_scroll_key=VK_SHIFT
                    ),
                ),
            ]
        )

    def create_widgets(self):
        # Tabview for tabs
        self.tabview = ctk.CTkTabview(self.root, width=880, height=600)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)

        # Global settings tab
        self.tabview.add(self.lang.get('global_settings'))
        self.global_frame = self.tabview.tab(self.lang.get('global_settings'))
        self.create_global_settings()

        # Apps tab
        self.tabview.add(self.lang.get('apps'))
        self.apps_frame = self.tabview.tab(self.lang.get('apps'))
        self.create_apps_settings()

        # App settings tab
        self.tabview.add(self.lang.get('app_settings'))
        self.app_settings_frame = self.tabview.tab(self.lang.get('app_settings'))
        self.create_app_settings()

        # About tab
        self.tabview.add(self.lang.get('about_title'))
        self.about_frame = self.tabview.tab(self.lang.get('about_title'))
        self.create_about_tab()

        # Control buttons
        self.control_frame = ctk.CTkFrame(self.root)
        self.control_frame.pack(fill="x", pady=10, padx=20)

        ctk.CTkButton(self.control_frame, text=self.lang.get('save'), command=self.save_config).pack(side="left", padx=5)
        ctk.CTkButton(self.control_frame, text=self.lang.get('start'), command=self.start_smooth_scroll).pack(side="left", padx=5)
        ctk.CTkButton(self.control_frame, text=self.lang.get('stop'), command=self.stop_smooth_scroll).pack(side="left", padx=5)

    def create_global_settings(self):
        # Assuming global config is the first AppConfig with regexp .*
        global_config = self.config.app_configs[0].scroll_config

        # Use pack with frames for better layout
        frame = ctk.CTkScrollableFrame(self.global_frame)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame, text=self.lang.get('distance')).pack(anchor="w", pady=2)
        self.distance_var = ctk.StringVar(value=str(global_config.distance))
        ctk.CTkEntry(frame, textvariable=self.distance_var).pack(fill="x", pady=2)

        ctk.CTkLabel(frame, text=self.lang.get('acceleration')).pack(anchor="w", pady=2)
        self.acceleration_var = ctk.DoubleVar(value=global_config.acceleration)
        ctk.CTkEntry(frame, textvariable=self.acceleration_var).pack(fill="x", pady=2)

        ctk.CTkLabel(frame, text=self.lang.get('opposite_acceleration')).pack(anchor="w", pady=2)
        self.opposite_acceleration_var = ctk.DoubleVar(value=global_config.opposite_acceleration)
        ctk.CTkEntry(frame, textvariable=self.opposite_acceleration_var).pack(fill="x", pady=2)

        ctk.CTkLabel(frame, text=self.lang.get('acceleration_delta')).pack(anchor="w", pady=2)
        self.acceleration_delta_var = ctk.IntVar(value=int(global_config.acceleration_delta * 1000))
        ctk.CTkEntry(frame, textvariable=self.acceleration_delta_var).pack(fill="x", pady=2)

        ctk.CTkLabel(frame, text=self.lang.get('acceleration_max')).pack(anchor="w", pady=2)
        self.acceleration_max_var = ctk.DoubleVar(value=global_config.acceleration_max)
        ctk.CTkEntry(frame, textvariable=self.acceleration_max_var).pack(fill="x", pady=2)

        ctk.CTkLabel(frame, text=self.lang.get('duration')).pack(anchor="w", pady=2)
        self.duration_var = ctk.IntVar(value=int(global_config.duration * 1000))
        ctk.CTkEntry(frame, textvariable=self.duration_var).pack(fill="x", pady=2)

        ctk.CTkLabel(frame, text=self.lang.get('pulse_scale')).pack(anchor="w", pady=2)
        self.pulse_scale_var = ctk.DoubleVar(value=global_config.pulse_scale)
        ctk.CTkEntry(frame, textvariable=self.pulse_scale_var).pack(fill="x", pady=2)

        self.inverted_var = ctk.BooleanVar(value=global_config.inverted)
        ctk.CTkCheckBox(frame, text=self.lang.get('inverted'), variable=self.inverted_var).pack(anchor="w", pady=2)

        ctk.CTkLabel(frame, text=self.lang.get('easing_function')).pack(anchor="w", pady=2)
        ease_options = ["LinearInOut", "QuadraticEaseInOut", "CubicEaseInOut", "QuarticEaseInOut", "QuinticEaseInOut"]
        self.ease_var = ctk.StringVar(value=global_config.ease.__name__ if hasattr(global_config.ease, '__name__') else "LinearInOut")
        ctk.CTkOptionMenu(frame, variable=self.ease_var, values=ease_options).pack(fill="x", pady=2)

        ctk.CTkLabel(frame, text=self.lang.get('horizontal_scroll_key')).pack(anchor="w", pady=2)
        key_options = ["VK_SHIFT", "VK_CONTROL", "VK_MENU"]
        current_key = {VK_SHIFT: "VK_SHIFT", VK_CONTROL: "VK_CONTROL", VK_MENU: "VK_MENU"}.get(global_config.horizontal_scroll_key, "VK_SHIFT")
        self.horizontal_key_var = ctk.StringVar(value=current_key)
        ctk.CTkOptionMenu(frame, variable=self.horizontal_key_var, values=key_options).pack(fill="x", pady=2)

        # Remove autostart from global settings

    def create_apps_settings(self):
        # Scrollable frame for apps
        self.apps_scrollable = ctk.CTkScrollableFrame(self.apps_frame)
        self.apps_scrollable.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons for apps
        apps_buttons = ctk.CTkFrame(self.apps_frame)
        apps_buttons.pack(fill="x", pady=5, padx=10)
        ctk.CTkButton(apps_buttons, text=self.lang.get('add'), command=self.add_app).pack(side="left", padx=5)
        ctk.CTkButton(apps_buttons, text=self.lang.get('remove'), command=self.remove_app).pack(side="left", padx=5)
        ctk.CTkButton(apps_buttons, text=self.lang.get('edit'), command=self.edit_app).pack(side="left", padx=5)

        self.app_buttons = []
        self.populate_apps_list()

    def populate_apps_list(self):
        for btn in self.app_buttons:
            btn.destroy()
        self.app_buttons = []
        for i, app in enumerate(self.config.app_configs):
            text = f"Path: {app.path or 'None'} | Regexp: {app.regexp.pattern if app.regexp else 'None'} | Enabled: {app.enabled}"
            btn = ctk.CTkButton(self.apps_scrollable, text=text, command=lambda idx=i: self.select_app(idx))
            btn.pack(fill="x", pady=2)
            self.app_buttons.append(btn)
        self.selected_app_index = None

    def select_app(self, index):
        self.selected_app_index = index
        for i, btn in enumerate(self.app_buttons):
            if i == index:
                btn.configure(fg_color="lightblue")  # Highlight selected
            else:
                btn.configure(fg_color=["#3B8ED0", "#1F6AA5"])  # Default

    def add_app(self):
        # Simple dialog for new app using ctk
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(self.lang.get('add_app'))
        dialog.geometry(f"250x150+{self.root.winfo_x() + 50}+{self.root.winfo_y() + 50}")
        dialog.attributes("-topmost", True)
        dialog.focus()

        ctk.CTkLabel(dialog, text=self.lang.get('path')).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        path_var = ctk.StringVar()
        ctk.CTkEntry(dialog, textvariable=path_var).grid(row=0, column=1, padx=5, pady=2)

        ctk.CTkLabel(dialog, text=self.lang.get('regexp')).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        regexp_var = ctk.StringVar()
        ctk.CTkEntry(dialog, textvariable=regexp_var).grid(row=1, column=1, padx=5, pady=2)

        enabled_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(dialog, text=self.lang.get('enabled'), variable=enabled_var).grid(row=2, column=0, columnspan=2, pady=2)

        def save():
            app = AppConfig(path=path_var.get() or None, regexp=regexp_var.get() or None, enabled=enabled_var.get())
            self.config.app_configs = self.config.app_configs + (app,)
            self.populate_apps_list()
            dialog.destroy()

        ctk.CTkButton(dialog, text=self.lang.get('save_btn'), command=save).grid(row=3, column=0, columnspan=2, pady=10)

    def remove_app(self):
        if self.selected_app_index is not None:
            self.config.app_configs = self.config.app_configs[:self.selected_app_index] + self.config.app_configs[self.selected_app_index+1:]
            self.populate_apps_list()
        else:
            messagebox.showwarning(self.lang.get('warning'), self.lang.get('select_app') + " " + self.lang.get('remove').lower())

    def edit_app(self):
        if self.selected_app_index is None:
            messagebox.showwarning(self.lang.get('warning'), self.lang.get('select_app') + " " + self.lang.get('edit').lower())
            return
        app = self.config.app_configs[self.selected_app_index]

        # Dialog for editing app
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(self.lang.get('edit_app'))
        dialog.geometry(f"250x150+{self.root.winfo_x() + 50}+{self.root.winfo_y() + 50}")
        dialog.attributes("-topmost", True)
        dialog.focus()

        ctk.CTkLabel(dialog, text=self.lang.get('path')).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        path_var = ctk.StringVar(value=app.path or "")
        ctk.CTkEntry(dialog, textvariable=path_var).grid(row=0, column=1, padx=5, pady=2)

        ctk.CTkLabel(dialog, text=self.lang.get('regexp')).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        regexp_var = ctk.StringVar(value=app.regexp.pattern if app.regexp else "")
        ctk.CTkEntry(dialog, textvariable=regexp_var).grid(row=1, column=1, padx=5, pady=2)

        enabled_var = ctk.BooleanVar(value=app.enabled)
        ctk.CTkCheckBox(dialog, text=self.lang.get('enabled'), variable=enabled_var).grid(row=2, column=0, columnspan=2, pady=2)

        def save():
            new_app = AppConfig(path=path_var.get() or None, regexp=regexp_var.get() or None, enabled=enabled_var.get())
            self.config.app_configs = self.config.app_configs[:self.selected_app_index] + (new_app,) + self.config.app_configs[self.selected_app_index+1:]
            self.populate_apps_list()
            dialog.destroy()

        ctk.CTkButton(dialog, text=self.lang.get('save_btn'), command=save).grid(row=3, column=0, columnspan=2, pady=10)

    def create_app_settings(self):
        frame = ctk.CTkScrollableFrame(self.app_settings_frame)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame, text=self.lang.get('appearance_mode')).pack(anchor="w", pady=2)
        appearance_options = ["System", "Light", "Dark"]
        self.appearance_var = ctk.StringVar(value="System")
        ctk.CTkOptionMenu(frame, variable=self.appearance_var, values=appearance_options, command=self.change_appearance_mode).pack(fill="x", pady=2)

        ctk.CTkLabel(frame, text=self.lang.get('language')).pack(anchor="w", pady=2)
        self.language_var = ctk.StringVar(value="en")
        ctk.CTkOptionMenu(frame, variable=self.language_var, values=["en", "ru"], command=self.change_language).pack(fill="x", pady=2)

        ctk.CTkLabel(frame, text="").pack(pady=5)  # Spacer
        ctk.CTkLabel(frame, text=self.lang.get('app_settings')).pack(anchor="w", pady=5, padx=10)
        self.autostart_var = ctk.BooleanVar(value=self.is_autostart_enabled())
        ctk.CTkCheckBox(frame, text=self.lang.get('autostart'), variable=self.autostart_var, command=self.toggle_autostart).pack(anchor="w", pady=2)
        
        self.start_minimized_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(frame, text=self.lang.get('start_minimized'), variable=self.start_minimized_var).pack(anchor="w", pady=2)

    def change_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode)
        messagebox.showinfo(self.lang.get('info'), self.lang.get('appearance_applied'))

    def change_language(self, lang):
        self.lang.lang = lang
        messagebox.showinfo(self.lang.get('info'), self.lang.get('restart_for_lang'))

    def change_color_theme(self, theme):
        if theme == "red":
            ctk.set_default_color_theme("red.json")
        else:
            ctk.set_default_color_theme(theme)
        messagebox.showinfo(self.lang.get('info'), self.lang.get('appearance_applied') + " Для полного обновления перезапустите приложение.")

    def load_config(self):
        config_path = os.path.join(get_app_directory(), "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    data = json.load(f)
                gui_settings = data.get("gui_settings", {})
                lang = gui_settings.get("language", "en")
                self.lang = Lang(lang)
                self.config = self.deserialize_config(data)
                self.gui_settings = gui_settings
            except Exception as e:
                messagebox.showerror(self.lang.get('load_config_error'), str(e))
        else:
            # Use default config
            self.gui_settings = {}
            pass

    def update_global_config(self):
        global_config = self.config.app_configs[0].scroll_config
        global_config.distance = None if self.distance_var.get() == "None" else float(self.distance_var.get())
        global_config.acceleration = self.acceleration_var.get()
        global_config.opposite_acceleration = self.opposite_acceleration_var.get()
        global_config.acceleration_delta = self.acceleration_delta_var.get() / 1000
        global_config.acceleration_max = self.acceleration_max_var.get()
        global_config.duration = self.duration_var.get() / 1000
        global_config.pulse_scale = self.pulse_scale_var.get()
        global_config.inverted = self.inverted_var.get()

        # Update ease
        ease_name = self.ease_var.get()
        global_config.ease = getattr(easing_functions, ease_name, easing_functions.LinearInOut)

        # Update horizontal key
        key_name = self.horizontal_key_var.get()
        global_config.horizontal_scroll_key = {"VK_SHIFT": VK_SHIFT, "VK_CONTROL": VK_CONTROL, "VK_MENU": VK_MENU}.get(key_name, VK_SHIFT)

    def save_config(self):
        self.update_global_config()
        config_path = os.path.join(get_app_directory(), "config.json")
        try:
            data = self.serialize_config()
            with open(config_path, 'w') as f:
                json.dump(data, f, indent=4)
            messagebox.showinfo(self.lang.get('success'), self.lang.get('config_saved') + f" {config_path}")
        except Exception as e:
            messagebox.showerror(self.lang.get('error'), str(e))

    def serialize_config(self):
        data = {
            "apps": [],
            "gui_settings": {
                "appearance_mode": self.appearance_var.get(),
                "language": self.lang.lang,
                "start_minimized": self.start_minimized_var.get()
            }
        }
        for app in self.config.app_configs:
            app_data = {
                "path": app.path,
                "regexp": app.regexp.pattern if app.regexp else None,
                "enabled": app.enabled
            }
            if app.scroll_config:
                app_data["scroll_config"] = {
                    "distance": app.scroll_config.distance,
                    "acceleration": app.scroll_config.acceleration,
                    "opposite_acceleration": app.scroll_config.opposite_acceleration,
                    "acceleration_delta": app.scroll_config.acceleration_delta,
                    "acceleration_max": app.scroll_config.acceleration_max,
                    "duration": app.scroll_config.duration,
                    "pulse_scale": app.scroll_config.pulse_scale,
                    "ease": app.scroll_config.ease.__name__ if hasattr(app.scroll_config.ease, '__name__') else "LinearInOut",
                    "inverted": app.scroll_config.inverted,
                    "horizontal_scroll_key": app.scroll_config.horizontal_scroll_key
                }
            data["apps"].append(app_data)
        return data

    def deserialize_config(self, data):
        apps = []
        for app_data in data.get("apps", []):
            scroll_config = None
            if "scroll_config" in app_data:
                sc = app_data["scroll_config"]
                ease_name = sc.get("ease", "LinearInOut")
                ease = getattr(easing_functions, ease_name, easing_functions.LinearInOut)
                scroll_config = ScrollConfig(
                    distance=sc.get("distance"),
                    acceleration=sc.get("acceleration", 1.0),
                    opposite_acceleration=sc.get("opposite_acceleration", 1.2),
                    acceleration_delta=int(sc.get("acceleration_delta", 0.07) * 1000),
                    acceleration_max=sc.get("acceleration_max", 14.0),
                    duration=int(sc.get("duration", 0.2) * 1000),
                    pulse_scale=sc.get("pulse_scale", 3.0),
                    ease=ease,
                    inverted=sc.get("inverted", False),
                    horizontal_scroll_key=sc.get("horizontal_scroll_key", VK_SHIFT)
                )
            app = AppConfig(
                path=app_data.get("path"),
                regexp=app_data.get("regexp"),
                enabled=app_data.get("enabled", True),
                scroll_config=scroll_config
            )
            apps.append(app)

        # Apply GUI settings
        gui_settings = data.get("gui_settings", {})
        appearance_mode = gui_settings.get("appearance_mode", "System")
        ctk.set_appearance_mode(appearance_mode)

        return SmoothScrollConfig(app_config=apps)

    def update_gui_from_config(self):
        if self.config.app_configs:
            global_config = self.config.app_configs[0].scroll_config
            self.distance_var.set(str(global_config.distance))
            self.acceleration_var.set(global_config.acceleration)
            self.opposite_acceleration_var.set(global_config.opposite_acceleration)
            self.acceleration_delta_var.set(int(global_config.acceleration_delta * 1000))
            self.acceleration_max_var.set(global_config.acceleration_max)
            self.duration_var.set(int(global_config.duration * 1000))
            self.pulse_scale_var.set(global_config.pulse_scale)
            self.inverted_var.set(global_config.inverted)

            # Update ease
            self.ease_var.set(global_config.ease.__name__ if hasattr(global_config.ease, '__name__') else "LinearInOut")

            # Update horizontal key
            current_key = {VK_SHIFT: "VK_SHIFT", VK_CONTROL: "VK_CONTROL", VK_MENU: "VK_MENU"}.get(global_config.horizontal_scroll_key, "VK_SHIFT")
            self.horizontal_key_var.set(current_key)

        # Update GUI settings
        self.appearance_var.set(self.gui_settings.get("appearance_mode", "System"))
        self.language_var.set(self.lang.lang)
        self.start_minimized_var.set(self.gui_settings.get("start_minimized", False))
        
        # Apply start_minimized from config if not explicitly set via command line
        if self.gui_settings.get("start_minimized", False) and not self.start_minimized:
            self.start_minimized = True
            self.auto_start = True  # Also auto-start SmoothScroll
            self.root.after(100, self.on_close)

    def start_smooth_scroll(self):
        if self.smooth_scroll:
            messagebox.showwarning(self.lang.get('warning'), self.lang.get('already_running'))
            return
        self.update_global_config()
        self.smooth_scroll = SmoothScroll(self.config)
        self.smooth_scroll.start(is_block=False)
        if not self.auto_start:
            messagebox.showinfo(self.lang.get('success'), self.lang.get('smoothscroll_started'))

    def stop_smooth_scroll(self):
        if self.smooth_scroll:
            self.smooth_scroll.join()
            self.smooth_scroll = None
            messagebox.showinfo(self.lang.get('success'), self.lang.get('smoothscroll_stopped'))
        else:
            messagebox.showwarning(self.lang.get('warning'), self.lang.get('not_running'))

    def create_tray_icon(self):
        # Load icon from file, or create default if not found
        try:
            image = Image.open(resource_path('icon.png'))
        except FileNotFoundError:
            # Create a simple icon if file not found
            image = Image.new('RGB', (64, 64), color='blue')
            draw = ImageDraw.Draw(image)
            draw.ellipse((16, 16, 48, 48), fill='white')

        # Create menu
        menu = pystray.Menu(
            pystray.MenuItem("Открыть", self.show_window),
            pystray.MenuItem("Закрыть", self.quit_app)
        )

        self.tray_icon = pystray.Icon("SmoothScroll", image, "SmoothScroll", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def on_close(self):
        self.root.withdraw()  # Hide window instead of closing

    def show_window(self):
        self.root.deiconify()  # Show window
        self.root.lift()  # Bring to front

    def quit_app(self):
        if self.smooth_scroll:
            self.smooth_scroll.join()
        self.tray_icon.stop()
        if os.path.exists(self.lock_file):
            os.remove(self.lock_file)
        self.root.quit()

    def is_autostart_enabled(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, "SmoothScroll")
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return False

    def toggle_autostart(self):
        if self.autostart_var.get():
            self.enable_autostart()
        else:
            self.disable_autostart()

    def enable_autostart(self):
        try:
            if getattr(sys, 'frozen', False):
                # Running as PyInstaller executable
                exe_path = os.path.abspath(sys.executable)
            else:
                # Running as Python script - need full path to pythonw.exe
                python_exe = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
                if not os.path.exists(python_exe):
                    python_exe = sys.executable
                script_path = os.path.join(get_app_directory(), os.path.basename(__file__))
                exe_path = f'"{python_exe}" "{script_path}" --tray'
            
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "SmoothScroll", 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
            messagebox.showinfo(self.lang.get('success'), self.lang.get('autostart_enabled'))
        except Exception as e:
            messagebox.showerror(self.lang.get('error'), str(e))
            self.autostart_var.set(False)

    def disable_autostart(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "SmoothScroll")
            winreg.CloseKey(key)
            messagebox.showinfo(self.lang.get('success'), self.lang.get('autostart_disabled'))
        except FileNotFoundError:
            pass  # Already disabled
        except Exception as e:
            messagebox.showerror(self.lang.get('error'), str(e))
            self.autostart_var.set(True)

    def open_link(self, url):
        webbrowser.open(url)

    def create_about_tab(self):
        frame = ctk.CTkScrollableFrame(self.about_frame)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame, text=self.lang.get('about_title'), font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=5)
        ctk.CTkLabel(frame, text=self.lang.get('about_desc'), wraplength=800, justify="left").pack(anchor="w", pady=10)
        ctk.CTkLabel(frame, text=self.lang.get('about_fork')).pack(anchor="w")
        link1 = ctk.CTkLabel(frame, text=self.lang.get('about_original'), cursor="hand2", text_color="blue", font=ctk.CTkFont(underline=True))
        link1.pack(anchor="w")
        link1.bind("<Button-1>", lambda e: self.open_link("https://github.com/re1von/Smoothscroll-for-windows"))
        ctk.CTkLabel(frame, text=self.lang.get('about_improvements')).pack(anchor="w")
        ctk.CTkLabel(frame, text=self.lang.get('about_link')).pack(anchor="w", pady=(10,0))
        link2 = ctk.CTkLabel(frame, text=self.lang.get('about_project_url'), cursor="hand2", text_color="blue", font=ctk.CTkFont(underline=True))
        link2.pack(anchor="w")
        link2.bind("<Button-1>", lambda e: self.open_link("https://github.com/vadenko"))
        ctk.CTkLabel(frame, text=self.lang.get('about_version')).pack(anchor="w", pady=(5,0))

if __name__ == "__main__":
    root = ctk.CTk()
    app = SmoothScrollGUI(root)
    root.mainloop()
