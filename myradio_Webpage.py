#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import webbrowser

result = []

myradio_file = os.path.join(os.path.expanduser("~"), ".local/share/InternetRadioDeutsch/myradio.txt")
myradio_webfile = os.path.join(os.path.expanduser("~"), ".local/share/InternetRadioDeutsch/myradio.html")

myradio_text = open(myradio_file, 'r').read()

theRadioList = myradio_text.splitlines()


def getValues():
    for line in theRadioList:
        if line.startswith("-- "):
            line = line.replace("-- ", "").replace(" --", "")
            result.append(f'<tr><h2 id="{line}">{line}</h2></tr>')
        else:
            textline = line.split(",")
            if len(textline) > 1:
                name = textline[0]
                url = textline[1]
                result.append(f"<li><a class='chlist' href='{url}'>{name}</a></li>") 

        
    return('\n'.join(result))
    

result = getValues()

### html
html_top = """<!DOCTYPE html>
<html>

  <head>
    <title>Radio Player</title>
    <script type="text/javascript" src="list.min.js"></script>
    <script type="text/javascript" src="jquery-1.10.1.js"></script>
    <link rel="stylesheet" href="player.css" media="all">
    <script src="player.js" async></script>
  </head>
  <div class="header">
    <a href="#top"><button class="buttontop" type="button">&#11121;</button></a>
  </div>

  <body>
    <div id='player'>
      <audio autoplay controls='' id='audio' preload='none' tabindex='0'>
        <source id="primarysrc" src='none' /></audio>
    </div>
    <div id="test">
      <input class="customSearch search" type="search" placeholder="Artist ..." />
      <ul id='playlist' class='list'>
"""

html_bottom = """      </ul>
    </div>
  </body>
</html>
"""
html_code = html_top
html_code += result
html_code += html_bottom

    
with open(myradio_webfile, 'w', encoding='utf8') as f:
    f.write(html_code)
    f.close()
    
webbrowser.open(myradio_webfile, 2)
