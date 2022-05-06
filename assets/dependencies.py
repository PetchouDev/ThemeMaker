import os
import time

EXTERNAL_MODULES = ["PyQt5", "shutil", "moviepy"]
isTriggered = False


for module in EXTERNAL_MODULES:
    try:
        if module == "PyQt5":
            import PyQt5
            print('PyQt5 found.')
        elif module == "shutil":
            import shutil
            print('shutil found.')
        elif module == "moviepy":
            import moviepy
            print('moviepy found.')
    except:
        if not isTriggered:
            os.system("cscript notif.vbs \"additionnal packages are insatlling, it might take some time. Please wait for completion.\"")
            isTriggered = True
        os.system(f"python -m pip install {module}")
time.sleep(0.5)
print('Ready for starting ThemeMaker')