# **ThemeMaker for Opera GX**
## Summary

- What is ThemeMaker ?
- How to use ?
- Issues

## User's manual
### What is ThemeMaker ?
**Presentation**
ThemeMaker is a theme engine for Opera GX browser. It allows you to set a bunch of settings simply by entering a few datas (theme name, author pseudo, optional url). It allows you not only to set a classic wallpaper, but also a dynamic one, based on any common video format.

**How it works ?**
ThemeMaker is 100% written in python, the GUI have been designed with QtDesigner and is written as xml, and batch script (compiled using Bat to Exe Converter) makes sure everything runs smoothly.
At first use, the program will search for the directory where themes are stored. If it can't find it, you be prompted to specify it yourself (ThemeMaker tells you how to find it, so as you just have to copy/paste it).
Then, you'll see the main screen, where you can add items and informations to your theme. You can also open the themes directory to find your creations and share them.
Once you gave a name for the theme, an author's nickname, a version indicator (must be a integer) and a picture, you can click the build button.
The build creates a temporary folder in which :
- The picture is copied
- The video (if there is one) is copied and converted to .webm **|** *This step can take a few minutes, according to the video duration*
- the theme archive is built
then, the archive is moved to the themes folder and the temporary files are deleted.

### How to use ?
Download the **ThemeMaker.zip** archive, move it to wherever you want the program to be, and extract the files. Then, simply run **ThemeMaker.exe** which is the main application.
This will check your depedencies before lauching ThemeMaker. It will look for : 
- **Python**, if it's not installed and added to `path`, you'll be prompted to install it and it will open the application in the Microsoft Store.
- python libraries : 
     - **PyQt5**, which handles the whole GUI
     - **moviepy**, which allows to convert  videos to .webm
     - **shutil**, which makes python able to do lots of things

Due to these installations, the loading at first use might take some time. But it should be less than 2 minutes.

### Troubleshooting
I case you find a bug or an error, it will be appreciated that you report it >[here](https://github.com/PetchouDev/ThemeMaker/issues)< or by clicking the `report bug` button in the application.

# Thanks
**Special thanks to**
- **nlfmt** for his [ColorPicker](https://github.com/nlfmt/pyqt-colorpicker)
- **Zulko** for the [moviepy](https://github.com/Zulko/moviepy) library
- **Riverbank Computing** for making [PyQt5](https://riverbankcomputing.com/software/pyqt/download) possible
- **jdevries3133** for the awesome library [shutil](https://github.com/python/cpython/blob/main/Lib/shutil.py) that made my work much easier.

# Screenshots
![image_2022-05-06_174258525](https://user-images.githubusercontent.com/86736499/167166763-e02c1bf2-639b-4dda-9f5f-2c016c7182d5.png)
