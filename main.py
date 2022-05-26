import asyncio
from msilib import type_string
import os, sys
import time
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QFileDialog, QSystemTrayIcon
from PyQt5.QtGui import QColor, QImageReader
from PyQt5.QtCore import QThread, pyqtSignal
import json
import shutil
from zipfile import ZipFile
import moviepy.editor as mp

global datas
datas = {}


def defaultThemeFolder() -> str:
    """returns path to opera's theme folder's default location"""
    #                                         
    return fr"C:\Users\{os.getlogin()}\AppData\Roaming\Opera Software\Opera GX Stable\themes"


def setup():
    path = ""
    try:
        os.mkdir(defaultThemeFolder())
        path = defaultThemeFolder()
    except FileExistsError:
        path = defaultThemeFolder()
    except:
        path = getPath()
        if path != "":
            path = path + "\themes"
        else:
            os.system("cscript notif.vbs \"Couldn't fetch Opera GX profile directory automaticly, please specify it.")
            app.exit()
            quit()
    config = open("assets\config.json", "w")
    json.dump({"path": path, "infos": ["", ""]}, config)
    config.close()


class Setup(QDialog):

    def __init__(self):

        super(Setup, self).__init__()
        uic.loadUi(r"assets\ui\getPath.ui", self)

        self.setWindowIcon(app_icon)
        print('ui loaded')
        self.ok.clicked.connect(self.returnPath)

    def seemsCorrect(self):
        if ("Opera GX Stable" and "C:") in self.path.text():
            # self.ok.setEnabled = True
            print('ok')
            return True
        else:
            # self.ok.setEnabled = False
            return False

    def returnPath(self):
        if self.seemsCorrect():
            global userPath
            userPath = self.path.text()
            self.close()
        else:
            print('Not ok')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Invalid path")
            msg.setInformativeText("The path you choosed doesn't match with an Opera GX folder")
            msg.setWindowTitle("Error - Invalid path")
            msg.setDetailedText("""So as to run ThemeMaker smoothly, you need to set a path to the Opera GX profile directory. This path will be stored on your local machine ONLY.
                                \n You can find this path by opening Opera GX, then typing opera://about in the search bar. Then copy the path named Profile.""")
            msg.exec()


global userPath
userPath = ""


def getPath():
    global userPath
    print("test")
    window = Setup()
    window.exec()
    del window
    return userPath


class Updater(QThread):
    updater = pyqtSignal()

    def run(self):
        while True:
            self.updater.emit()
            time.sleep(0.3)


class Credits(QDialog):
    def __init__(self) -> None:
        super(Credits, self).__init__()
        uic.loadUi(fr'assets\ui\credits.ui', self)
        self.setWindowIcon(app_icon)
        self.ok.clicked.connect(self.close)


class mainWindow(QDialog):
    currentTextColor = "ffffff"
    currentShadowColor = "ffffff"

    def __init__(self) -> None:
        super(mainWindow, self).__init__()
        uic.loadUi(fr'assets\ui\main.ui', self)
        self.setWindowIcon(app_icon)
        self.thread = Updater()
        self.thread.updater.connect(self.updateGUI)
        self.thread.start()
        self.photoBrowse.clicked.connect(self.findPicture)
        self.videoBrowse.clicked.connect(self.findVideo)
        self.closeBtn.clicked.connect(app.exit)
        self.credits.clicked.connect(self.seeCredits)
        self.build.clicked.connect(self.nextStep)
        self.build.setEnabled(False)
        self.folder.clicked.connect(self.directory)
        self.bug.clicked.connect(self.reportBug)

        # get previous datas
        try:
            with open("assets\config.json", "r") as save:
                datas = json.load(save)
            datas = datas["infos"]
            # attribuer les infos
            self.themeName.setText(datas[0])
            self.author.setText(datas[1])
            self.version.setText(str(datas[2]))
            self.url.setText(datas[3])
            self.currentTextColor = datas[4]
            self.currentShadowColor = datas[5]
        except:
            pass
        self.textColor.setStyleSheet(f"background-color:#{self.currentTextColor};")
        self.textColor.clicked.connect(self.changeTextColor)
        self.shadowColor.setStyleSheet(f"background-color:#{self.currentShadowColor};")
        self.shadowColor.clicked.connect(self.changeShadowColor)

    def reportBug(self):
        os.system("@start https://github.com/PetchouDev/ThemeMaker/issues/new")

    def updateGUI(self):

        version_ok = False
        try:
            int(self.version.text())
            version_ok = True
        except:
            version_ok == False

        if (self.author.text() == "") or (self.version.text() == "") or (not version_ok) or (
                self.themeName.text() == "") or (self.photoPath.text() == ""):
            self.build.setEnabled(False)

        else:
            self.build.setEnabled(True)

    def findPicture(self):
        supportedFormats = QImageReader.supportedImageFormats()
        text_filter = "Images ({})".format(" ".join(["*.{}".format(fo.data().decode()) for fo in supportedFormats]))
        filename = QFileDialog.getOpenFileName(self, "Choose your main wallpaper",
                                               fr"C:\Users\{os.getlogin()}\Pictures", text_filter)
        self.photoPath.setText(filename[0])

    def findVideo(self):
        text_filter = "Videos ({*.mov *.mp4 *.wmv *.avi *.avchd *.flv *.f4v *.swf *.mkv *.webm})"
        filename = QFileDialog.getOpenFileName(self, "Choose your main wallpaper", fr"C:\Users\{os.getlogin()}\Videos",
                                               text_filter)
        self.videoPath.setText(filename[0])

    def seeCredits(self):
        window = Credits()
        window.exec()
        del window

    def nextStep(self):
        global datas
        datas["name"] = self.themeName.text()
        datas["author"] = self.author.text()
        datas["version"] = int(self.version.text())
        datas["url"] = self.url.text()
        datas["photo"] = self.photoPath.text()
        datas["video"] = self.videoPath.text()
        datas["tc"] = self.currentTextColor
        datas["sc"] = self.currentShadowColor
        with open("assets\config.json", "r") as file:
            config = json.load(file)
        config["infos"] = [datas["name"], datas["author"], datas["version"], datas["url"], datas["tc"], datas["sc"]]
        with open("assets\config.json", "w") as nexConfig:
            json.dump(config, nexConfig)
        self.close()

    def directory(self):
        with open("assets\config.json", "r") as saveFie:
            temp = json.load(saveFie)
        path = temp["path"]
        del temp
        print(path)
        open("assets\showFolder.bat", "w").write(f'cd "{path}"\nstart . && exit')
        os.system(f'@start assets\showFolder.bat')

    def changeTextColor(self):
        picker = ColorPicker(lightTheme=True, useAlpha=True)
        result = picker.rgb2hex(picker.getColor())
        self.currentTextColor = result
        print(self.currentTextColor)
        self.textColor.setStyleSheet(f"background-color:#{self.currentTextColor};")

    def changeShadowColor(self):
        picker = ColorPicker(lightTheme=True, useAlpha=True)
        self.currentShadowColor = picker.rgb2hex(picker.getColor())
        self.shadowColor.setStyleSheet(f"background-color:#{self.currentShadowColor};")


class maker(QThread):
    updater = pyqtSignal(int, str)
    error = pyqtSignal(str, str)

    def run(self):
        global datas
        self.datas = datas
        try:
            asyncio.sleep(1)
            self.updater.emit(0, "Creating temporary folder.")
            try:
                os.mkdir(r"assets\temp")
            except:
                pass
            os.chdir(r"assets\temp")
            time.sleep(1)
            self.updater.emit(10, "Copying main wallpaper picture.")
            separated = self.datas["photo"].split(".")
            pictureFormat = separated[-1]
            shutil.copyfile(self.datas["photo"], f"image.{pictureFormat}")
            print('photo done !')
            if self.datas["video"] == "":
                self.updater.emit(40, "writing persona.ini file.")
            else:
                self.updater.emit(30, "Setting up video for theme (convertion to webm can take a few minutes).")
                convert(self.datas["video"], "video.webm")
                print('Video done !')
                asyncio.sleep(1)
                self.updater.emit(40, "writing persona.ini file")
            open("persona.ini", "w").write(
                persona(self.datas["name"], self.datas["author"], self.datas["url"], self.datas["version"],
                        pictureFormat, self.datas["video"], self.datas["tc"], self.datas["sc"]))
            time.sleep(0.5)
            self.updater.emit(50, "Building archive for theme.")
            # shutil.make_archive(self.datas["name"], format='zip', root_dir='.')
            files = os.listdir()
            archive = ZipFile("archive.zip", "w")
            print(os.listdir())
            for file in files:
                archive.write(file)
                print(file + " added to package")

            archive.close()

            print('archive done')
            with open("..\config.json", "r") as file:
                config = json.load(file)
            time.sleep(2)
            self.updater.emit(85, "Moving theme to Opera GX themes folder.")
            name = self.datas['name'].replace(" ", "-")
            shutil.copyfile("archive.zip", config["path"] + f"\{name}.zip")
            time.sleep(1)
            self.updater.emit(95, "Clearing things up.")
            for file in os.listdir():
                os.remove(file)
                print(file + " added to package")
            time.sleep(1)
            os.chdir("..\..\ ".replace(" ", ""))
            try:
                os.rmdir(r"assets\temp")
            except:
                pass
            print("temporary folder removed successfully")
            self.updater.emit(100, "All Done.")



        except Exception as error:
            self.error.emit("An error occured, please check your entries.", str(error))


class running(QDialog):
    def __init__(self) -> None:
        super(running, self).__init__()
        uic.loadUi(r"assets\ui\running.ui", self)
        self.setWindowIcon(app_icon)
        self.progress.setValue(0)
        self.task.setText("Wainting...")
        self.maker = maker()
        self.maker.error.connect(self.error)
        self.maker.updater.connect(self.update)
        self.maker.start()

    def update(self, value, task):
        self.progress.setValue(value)
        self.task.setText(task)
        if value == 100:
            time.sleep(1)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Build complete")
            msg.setInformativeText("Restart Opera GX then open quick configuration to apply it.")
            msg.setWindowTitle("Complete")
            msg.exec()
            self.close()

    def error(self, log, detailled):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Entry error")
        msg.setInformativeText(log)
        msg.setWindowTitle("Error")
        msg.setDetailedText(detailled)
        msg.exec()
        self.close()


def main():
    while True:
        window = mainWindow()
        window.exec()
        del window
        global datas
        if datas["photo"] == "{}" or str(datas["version"]) == "" or datas["author"] == "{}" or datas["name"] == "{}":
            app.exit()
            quit()
        window = running()
        window.exec()
        del window


if __name__ == '__main__':

    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(application_path)
    from assets.tools import convert, persona
    from assets.colorpicker import ColorPicker

    app = QApplication([])
    app.setApplicationName("ThemeMaker for OperaGX")
    app_icon = QtGui.QIcon()
    app_icon.addFile('assets\icon.png', QtCore.QSize(16, 16))
    app_icon.addFile('assets\icon.png', QtCore.QSize(24, 24))
    app_icon.addFile('assets\icon.png', QtCore.QSize(32, 32))
    app_icon.addFile('assets\icon.png', QtCore.QSize(48, 48))
    app_icon.addFile('assets\icon.png', QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)
    try:
        with open("assets\config.json", "r") as test:
            pass
    except:
        setup()

    main()

# button2.setStyleSheet("background-color:#ffffff;"
