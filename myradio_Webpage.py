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
            #result.append(f'<tr><a href="#top"><button type="button">↑</button></a></tr>')
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
  <html>
    <head>
      <title>Exclusive Radio Player</title>
      <script type="text/javascript" src="https://cdn.jsdelivr.net/g/jquery@3.1.0,mark.js@8.6.0(jquery.mark.min.js)"></script>
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
            padding-left: 2px;
            margin-bottom: -2px;
            text-decoration: underline;
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
            border: 1px inset #c4a000;
            width: 26px;
            height: 26px;
            line-height: 1;
            padding: 0;
            margin-bottom: 5px;
            font-size: 14px;
            text-align: center;
            color: #cf0;
            text-shadow: 1px 1px 1px #000;
            border-radius: 13px;
            background-color: #353;
        }

        button:hover {
            background-color: green;
        }

        button:active {
            box-shadow: inset -2px -2px 3px rgba(255, 255, 255, .6),
                        inset 2px 2px 3px rgba(0, 0, 0, .6);
        }
        .buttontop {
            border: 1px inset #c4a000;
            width: 52px;
            height: 26px;
            line-height: 1;
            margin-bottom: 5px;
            font-size: 14px;
            text-align: center;
            color: #cf0;
            text-shadow: 1px 1px 1px #000;
            border-radius: 0px;
            background-color: darkgreen;
        }
        mark {
          background: #c4a000;
        }

        mark.current {
          background: #c4a000;
        }

        .header {
          padding: 10px;
          width: 100%;
          background: #eee;
          position: fixed;
          top: 0;
          left: 0;
        }
        .content {
            position:absolute;
            top: 5px;
            left:4px;
        }
        .header{
            background-color: transparent;
            color: #c4a000;
            height:40px;
            position:fixed;
            top:5;
            left: 500px;
            width:auto;
            z-index:10;
            font-size: 10pt; color: #aa0;
        }
        input {
            background-color: #202F1F;
            color: #c4a000;
            font-family: Helvetica,Verdana;
            width: 150px;
            text-align: left;
            height: 26px;
            border: 1px inset #c4a000;
            border-radius: 3px;
        }
      </style>
      <script>
        $(document).ready(function(){
        $(function() {

          // the input field
          var $input = $("input[type='search']"),
            // clear button
            $clearBtn = $("button[data-search='clear']"),
            // prev button
            $prevBtn = $("button[data-search='prev']"),
            // next button
            $nextBtn = $("button[data-search='next']"),
            // the context where to search
            $content = $(".content"),
            // jQuery object to save <mark> elements
            $results,
            // the class that will be appended to the current
            // focused element
            currentClass = "current",
            // top offset for the jump (the search bar)
            offsetTop = 50,
            // the current index of the focused element
            currentIndex = 0;

          /**
           * Jumps to the element matching the currentIndex
           */
          function jumpTo() {
            if ($results.length) {
              var position,
                $current = $results.eq(currentIndex);
              $results.removeClass(currentClass);
              if ($current.length) {
                $current.addClass(currentClass);
                position = $current.offset().top - 2;
                window.scrollTo(0, position);
              }
            }
          }

          /**
           * Searches for the entered keyword in the
           * specified context on input
           */
          $input.on("input", function() {
            var searchVal = this.value;
            $content.unmark({
              done: function() {
                $content.mark(searchVal, {
                  separateWordSearch: true,
                  done: function() {
                    $results = $content.find("mark");
                    currentIndex = 0;
                    jumpTo();
                  }
                });
              }
            });
          });

          /**
           * Clears the search
           */
          $clearBtn.on("click", function() {
            $content.unmark();
            $input.val("").focus();
          });

          /**
           * Next and previous search jump to
           */
          $nextBtn.add($prevBtn).on("click", function() {
            if ($results.length) {
              currentIndex += $(this).is($prevBtn) ? -1 : 1;
              if (currentIndex < 0) {
                currentIndex = $results.length - 1;
              }
              if (currentIndex > $results.length - 1) {
                currentIndex = 0;
              }
              jumpTo();
            }
          });
        });
        //<![CDATA[
        window.addEventListener("play", function(evt) {
          if (window.$_currentlyPlaying) {
            window.$_currentlyPlaying.pause();
          }
          window.$_currentlyPlaying = evt.target;
        }, true);
        //]]>
        });
      </script>
    </head>
      <div class="header">
        <a href="#top"><button class="buttontop" type="button">↑↑</button></a>
        Search:
        <input type="search" placeholder="find ...">
        <button data-search="next">&darr;</button>
        <button data-search="prev">&uarr;</button>
        <button data-search="clear">✖</button>

      </div>
      <div class="content">
<table style="margin-left: auto; margin-right: auto;">
"""

html_bottom = """</table>
</div>
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
