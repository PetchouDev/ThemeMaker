import moviepy.editor as mp


def convert(video:str, output:str):
    """Create a webm file from a video file"""
    clip = mp.VideoFileClip(video)
    clip.write_videofile(output)

def rgba2hex(r:int, g:int, b:int, a:int):
    """Convert rgba color to its hex"""
    return '#{:02x}{:02x}{:02x}{:02x}'.format( r, g , b, a)

def persona(name:str, author:str, url:str, version:int, photo:str, video:str, textColor:str, shadowColor:str)->str:
    """returns the persona.ini file content"""
    if video != "":
        return f"""
[Info]
name = {name}
author = {author}
url = {url}
version = {version}

[Start Page]
background = video.webm
position = center center
title text color = #{textColor}
title text shadow = #{shadowColor}
first frame image = image.png
"""
    else:
        return f"""
[Info]
name = {name}
author = {author}
url = {url}
version = {version}

[Start Page]
background = image.png
position = center center
title text color = #{textColor}
title text shadow = #{shadowColor}

"""