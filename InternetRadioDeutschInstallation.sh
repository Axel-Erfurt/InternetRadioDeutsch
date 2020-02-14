#!/bin/sh
filename=$HOME/.local/share/InternetRadioDeutsch/myradio.txt
if [ -e "$filename" ]
then
    echo "$filename found, copying to /tmp"
    cp $filename /tmp
else
    echo "$filename not found"
fi
sharedapps=$HOME/.local/share/applications/
if [ -d "$sharedapps" ]
 then
    echo "$sharedapps found"
else
    echo "$sharedapps not found"
    mkdir $sharedapps
fi
echo "removing InternetRadioDeutsch"
rm -rf ~/.local/share/InternetRadioDeutsch
cd ~/.local/share/
echo "downloading InternetRadioDeutsch ..."
wget https://github.com/Axel-Erfurt/InternetRadioDeutsch/archive/master.zip
echo "unzip InternetRadioDeutsch"
unzip -o master.zip
sleep 1
echo "remove zip file"
rm master.zip
mv ~/.local/share/InternetRadioDeutsch-master ~/.local/share/InternetRadioDeutsch
desktopfile=$HOME/.local/share/applications/InternetRadioDeutsch.desktop
if [ -e "$desktopfile" ]
then
    echo "$desktopfile already exists"
else
    echo "$desktopfile not found"
    cp $HOME/.local/share/InternetRadioDeutsch/InternetRadioDeutsch.desktop $HOME/.local/share/applications
fi
rf=/tmp/myradio.txt
if [ -e "$rf" ]
then
    echo "restore myradio.txt"
    cp $rf $HOME/.local/share/InternetRadioDeutsch
else
    echo "$filename not found"
fi
rm ~/Downloads/InternetRadioDeutschInstallation.sh
cd ~/.local/share/applications/
mv InternetRadioDeutsch.desktop InternetRadioDeutsch.desktop-bak
icon=$(echo ~)/.local/share/InternetRadioDeutsch/radio_bg.png
sed -e "s,Icon=.*,Icon=$icon,g" InternetRadioDeutsch.desktop-bak > InternetRadioDeutsch.desktop
rm InternetRadioDeutsch.desktop-bak
echo "starting InternetRadio ... please use tray icon context menu with right mouse button"
python3 ~/.local/share/InternetRadioDeutsch/myRadioD.py
exit
