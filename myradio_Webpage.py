#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import webbrowser

theList = []
urlList = []
nameList = []
genreList = []
result = []

myradio_file = os.path.join(os.path.expanduser("~"), ".local/share/InternetRadioDeutsch/myradio.txt")
myradio_webfile = os.path.join(os.path.expanduser("~"), ".local/share/InternetRadioDeutsch/myradio.html")

audio_element = """<figure>
    <figcaption>myname</figcaption>
    <audio
        preload="none" controls="controls" 
        src="mysource">
            Your browser does not support the
            <code>audio</code> element.
    </audio>
</figure>"""

myradio_text = open(myradio_file, 'r').read()
print(myradio_text)

theRadioList = myradio_text.splitlines()


def getValues():
    for line in theRadioList:
        if line.startswith("-- "):
            line = line.replace("-- ", "").replace(" --", "")
            genreList.append(line)
            result.append(f'<tr><h2 id="{line}">{line}</h2></tr>')
            result.append(f'<tr><a href="#top"><button type="button">↑</button></a></tr>')
        else:
            textline = line.split(",")
            if len(textline) > 1:
                name = textline[0]
                url = textline[1]
                result.append(f'<tr>{audio_element.replace("myname", name).replace("mysource", url)}</tr>') 
        
        
    return('\n'.join(result))
    

result = getValues()
mygenres = []

### Links oben
for genre in genreList:
    mygenres.append(f'<a href="#{genre}"><h5>{genre}</h5></a>')
###

html_top = """<!DOCTYPE html>
<html id="top">
<head meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {
    background-color: #202F1F;
    color: #e9e9e9;
    font-family: Helvetica,Verdana;
    width: auto;
    text-align: left;
}
h4 {
    text-shadow: #088 1px 1px 1px; font-size: 40pt; color: #cc0;
}
h2 {
    text-shadow: #088 1px 1px 1px; font-size: 20pt; color: #c4a000;
    padding-left: 20px;
    margin-bottom: -10px;
}
h5 {
    font-size: 10pt; color: #aa0;
    margin-bottom: -15px;
}
a { text-decoration: none; }
audio {
    width: 400px;
    height: 32px;
    border: 0px solid #808000;
    color: 80ff80;
    filter: sepia(100%) grayscale(0) contrast(100%) hue-rotate(44deg);
}
audio:hover {
    filter: sepia(100%) grayscale(0) contrast(100%) hue-rotate(88deg);
}

audio::-webkit-media-controls-timeline {
    display: none;
}
audio::-webkit-media-controls-current-time-display {
    display: none;
}

audio::-webkit-media-controls-time-remaining-display {
    display: none;
}
audio::-webkit-media-controls-timeline-container {
    display: none;
}
audio:focus {
    outline: none;
}
figure {
    margin: 0;
   text-shadow: #088 1px 1px 1px; font-size: 20pt; color: #aa0;
}
button {
    border: 1px white;
    width: 20px;
    height: 20px,
    line-height: 1;
    padding: 0;
    margin-bottom: 5px;
    font-size: 14px;
    text-align: center;
    color: #cf0;
    text-shadow: 1px 1px 1px #000;
    border-radius: 10px;
    background-color: #353;
}

button:hover {
    background-color: green;
}

button:active {
    box-shadow: inset -2px -2px 3px rgba(255, 255, 255, .6),
                inset 2px 2px 3px rgba(0, 0, 0, .6);
}
</style>
<script type="text/javascript">
//<![CDATA[
window.addEventListener("play", function(evt)
{
    if(window.$_currentlyPlaying)
    {
        window.$_currentlyPlaying.pause();
    }
    window.$_currentlyPlaying = evt.target;
}, true);
//]]>
</script>
<title>myRadio WebPlayer</title>
</head>
<body>
<div class="content">
<h2>Kategorien</h2>
<table style="margin-left: auto; margin-right: auto;">
"""

html_bottom = """</table>
</body>
</html>
"""
html_code = html_top
html_code += "\n".join(mygenres)
html_code += result
html_code += html_bottom

#print(html_code)
with open(myradio_webfile, 'w', encoding='utf8') as f:
    f.write(html_code)
    f.close()
    
webbrowser.open(myradio_webfile, 2)
