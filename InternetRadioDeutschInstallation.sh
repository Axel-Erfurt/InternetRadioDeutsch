#!/bin/sh
filename=$HOME/.local/share/InternetRadioDeutsch/myradio.txt
if [ -e "$filename" ]
then
    echo "$filename gefunden, kopiere nach /tmp"
    cp $filename /tmp
else
    echo "$filename nicht gefunden"
fi
sharedapps=$HOME/.local/share/applications/
if [ -d "$sharedapps" ]
 then
    echo "$sharedapps gefunden"
else
    echo "$sharedapps nicht gefunden"
    mkdir $sharedapps
fi
echo "lösche InternetRadioDeutsch"
rm -rf ~/.local/share/InternetRadioDeutsch
cd ~/.local/share/
echo "herunterladen von InternetRadioDeutsch ..."
wget https://github.com/Axel-Erfurt/InternetRadioDeutsch/archive/master.zip
echo "entpacke InternetRadioDeutsch"
unzip -qq -o master.zip
sleep 1
echo "lösche zip Datei"
rm master.zip
mv ~/.local/share/InternetRadioDeutsch-master ~/.local/share/InternetRadioDeutsch
desktopfile=$HOME/.local/share/applications/InternetRadioDeutsch.desktop
if [ -e "$desktopfile" ]
then
    echo "$desktopfile existiert schon"
else
    echo "$desktopfile nicht gefunden, wird nun angelegt."
    cp $HOME/.local/share/InternetRadioDeutsch/InternetRadioDeutsch.desktop $HOME/.local/share/applications
fi
rf=/tmp/myradio.txt
if [ -e "$rf" ]
then
    echo "restore myradio.txt"
    cp $rf $HOME/.local/share/InternetRadioDeutsch
else
    echo "$filename nicht gefunden"
fi
#cp ~/.local/share/InternetRadioDeutsch/InternetRadioDeutsch.desktop ~/.local/share/applications
rm ~/Downloads/InternetRadioDeutschInstallation.sh
cd ~/.local/share/applications/
mv InternetRadioDeutsch.desktop InternetRadioDeutsch.desktop-bak
icon=$(echo ~)/.local/share/InternetRadioDeutsch/radio_bg.png
sed -e "s,Icon=.*,Icon=$icon,g" InternetRadioDeutsch.desktop-bak > InternetRadioDeutsch.desktop
rm InternetRadioDeutsch.desktop-bak
echo "starte myRadio ... benutze Tray Kontextmenu mit rechter Maustaste"
python3 ~/.local/share/InternetRadioDeutsch/myRadioD.py
exit
