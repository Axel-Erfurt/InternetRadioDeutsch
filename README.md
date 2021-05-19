# InternetRadioDeutsch 🇩🇪
Tray Radio App Deutsch

### Voraussetzungen:

- python 3.6
- PyQt5
- PyQt5 Multimedia
- gstreamer

Anleitung -> [myRadio UbuntuUsers Wiki 🇩🇪](https://wiki.ubuntuusers.de/Howto/myRadio/)

### Installation Mint / Ubuntu

```
wget 'https://raw.githubusercontent.com/Axel-Erfurt/InternetRadioDeutsch/master/InternetRadioDeutschInstallation.sh' -O ~/Downloads/InternetRadioDeutschInstallation.sh && chmod +x ~/Downloads/InternetRadioDeutschInstallation.sh && ~/Downloads/InternetRadioDeutschInstallation.sh 
```

### Deinstallation Mint / Ubuntu

```
rm -rf ~/.local/share/applications/InternetRadioDeutsch.desktop && rm -rf ~/.local/share/InternetRadioDeutsch
```

### Editor

```
python3 ~/.local/share/InternetRadioDeutsch/myRadioEditorDE.py
```

- Spalte 1 -> Name
- Spalte 2 -> Gruppe
- Spalte 3 -> URL

![editor](https://raw.githubusercontent.com/Axel-Erfurt/InternetRadioDeutsch/master/editorshot.png)

### Web Version

Mit dem Script myradio_Webpage.py macht man aus der myradio.txt eine Website Version.

Style anpassen in *_player.css_*

[64bit App Version 🇩🇪](https://dl.dropbox.com/s/1nk20f6e31lzvav/myRadioD.tar.gz)

entpacken und im entpackten Ordner ***myRadioD*** starten. Läuft ohne PyQt5 Installation.
