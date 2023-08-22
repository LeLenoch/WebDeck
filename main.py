import pystray
from pystray import MenuItem as item
from PIL import Image
import ctypes
import sys
import win32gui, win32con
import win32com.client
import time
import subprocess

wmi = win32com.client.GetObject("winmgmts:")
processes = wmi.InstancesOf("Win32_Process")

if_webdeck = False
wd_count = 0
for process in processes:
    if 'webdeck' in process.Properties_('Name').Value.lower().strip():
        wd_count += 1
if wd_count > 1:
    time.sleep(1)
    wmi = win32com.client.GetObject("winmgmts:")
    processes = wmi.InstancesOf("Win32_Process")

    if_webdeck = False
    wd_count = 0
    for process in processes:
        if 'webdeck' in process.Properties_('Name').Value.lower().strip():
            wd_count += 1
    if wd_count > 1:
        if_webdeck = True
    
if if_webdeck == False:

    icon = None

    subprocess.Popen(['WD_start.exe'])
    subprocess.Popen(['WD_main.exe'])
    
    def quit_program():
        global icon
        
        wmi = win32com.client.GetObject("winmgmts:")
        processes = wmi.InstancesOf("Win32_Process")
        
        for process in processes:
            if "webdeck" in process.Properties_('Name').Value.lower().strip() or \
                "WD_" in process.Properties_('Name').Value.strip():
                print(f"Stopping process: {process.Properties_('Name').Value.lower().strip()}")
                result = process.Terminate()
                if result == 0:
                    print("Process terminated successfully.")
                else:
                    print("Failed to terminate process.")
        
        icon.stop()  # Arrêter l'icône Tray
        
        try: sys.exit()
        except: exit()


    def create_tray_icon():
        global icon
        image = Image.open("static/files/icon.ico")

        # Créer le menu de l'icône Tray
        menu = (
            #item('Réouvrir', lambda: window.deiconify()),
            item('Quit', lambda: quit_program()),
        )

        # Créer l'icône Tray
        icon = pystray.Icon("name", image, "WebDeck", menu)
        return icon

    create_tray_icon()
    icon.run()