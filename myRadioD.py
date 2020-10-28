#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import requests
#import base64
#from subprocess import call
from PyQt5.QtCore import (QUrl, pyqtSignal, Qt, QMimeData, QSize, QPoint, QProcess, 
                            QStandardPaths, QFile, QDir, QSettings, QByteArray, QEvent)
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QSlider, 
                            QMainWindow, QFileDialog, QMenu, qApp, QAction, QLineEdit, 
                             QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QSpacerItem, QSizePolicy, 
                            QMessageBox, QPlainTextEdit, QSystemTrayIcon, QInputDialog, QToolButton, )
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QIcon, QPixmap, QStandardItem, QTextOption, QTextCursor

changed = pyqtSignal(QMimeData)
btnwidth = 100

class Editor(QWidget):
    def __init__(self):
        super(Editor, self).__init__()
        self.setAttribute(Qt.WA_QuitOnClose, False)
        self.radiofile = ""
        self.radio_editor = QPlainTextEdit()
        self.radio_editor.textChanged.connect(self.setModified)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.radio_editor)
        self.setLayout(self.layout)
        self.setGeometry(0, 0, 650, 500)
        self.setStyleSheet("QPlainTextEdit {background-color: #eeeeec;}")

    def closeEvent(self, event):
        if self.isModified:
            quit_msg = "<b>Datei wurde verändert.<br>Speichern?</ b>\
                        <br><br><span style='color: #a40000;'>neue Sender sind beim nächsten Start von myRadio verfügbar</span>"
            reply = QMessageBox.question(None, 'Speichern', 
                     quit_msg, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                if self.saveFile():
                    print("Datei gespeichert\nschließe Editor")
                    event.accept()
                else:
                    print("Editor geschlossen")
            
    def saveFile(self):
        with open(self.radiofile, 'w', encoding='utf8') as f:
            f.write(str(self.radio_editor.toPlainText()))
            f.close()
            return True
            
    def setModified(self):
        self.isModified = True
        

class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        imgstring = b"iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAFG3pUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjarVbpkSO9Df3PKBwCQRwkwwFJoMoZOHw/Sq3Zmf3W5fLRmpY0PAAQ72iV+Mffs/wNFwlZEe3DplnFJVNmc3wZ9X3d7wt3ez7vlNXPRXW+3l9XIfka/jHxGaf2c/xr3n8LJE92Wj8nPuNt/BaovT/4Jmi/Epb5TBBj+A+ZbY5e5df//hwtnwCKFX20Wri1YMFNTO9M/L4dd8d7Yyx7RhSrnIVv8ldAZO63fFT02nwXNgSiSZ+JpyrEeLr+bRzrcQB+NepzivL9GLX9mvjecBTz5/HPZTcQY5q/BbM/o/LvQCn/CpXXsb41Wdrzrf0c53wfuHyqyzwjM14rxMVATnvY9Tk8PetATeFn7utVfv7737/+g0Bftfyvgf4PFWXu2xK6Yr7Q40Zd7cLS6K5guoGw7E5+kOOvBv/pMgSbIKe/d7W3HEDb8trUXi/+LcB7RK6caqf2rglKEtKGep4Cxjtx+cv271d/hUENT/5J9CSoLxpfRvWHkN9s6j3xzk8Q021AI2nQISnZLcVahx6B37W8/RRx+8Tl5gA765kndzPNwaxr6urW0iR5+jnHqp9p2S36lCUIvbbRhj0MsqkzRxk8dO9gnfOsyLxKP2oyfNLYA06MP+sOjCY3mbwUKnSeJ5rHWOxH5fQovW+hQ0c9xQNpQxtvW0f6gOqPqewUYtxrIyqt2ZF0eXqf2NVsS/CJwthtY4xbS6tHWs+evHNm0Ox9bT+STYI0VvaOufTceyl43kldp2yX8CLk2KTnpvaVYse6njyTw525Gslubq0OcbJNqEajb8A4Bk6259rUJ0WZibzatq/ZNjKO6D58od/hSxwZz4zVHeuX9nMiraKVYjitA4F5LAPIlq1gGlrfPOs620G2nKIbe/ea63Ae4s1AjqXHbMmG9t5WuoZqM07Feamc4znOlrOGqi7bQEBsrwSEpnSCF0kEOkYVhz/o93GBohbASlfeaMseq7imdTxQzn2YoBTLecRn5444fTIdPGaATO8HzCGa01Sl2Vg2yQzvdSkewwV9NK3KU/X0atmoNw0Gl2ItdH2jA76coxNySEdnsNAodEZKyBZ0gDVK7I6GAnrhubOOoVzV9szVd5si0XSs6HxAcOA2wAGl9DbGdrW6rU48DjoXvgSyDsFUA/VTq+gVnnJ2vjaRABsxdZFe+qOWPZorMuwOMREQBo+0KNCBFhh6a2Tqh+H9fQEABD+GqatJnXzRuU9f6NAEJGyRw/CcRvq2GH60xmh9jbpgMU2u6+QNtMAXXhkgcBM4JLD0ACh2YkfsVbcPiODSrNtMKRKpOldXW/iYEoYzTHIQAodlWBiqkkG9B9RJeeTiTrlAALQMfK5ofAWz1xwxGREm20Hh0PdiTTkwCR8KnEkssN8v4gymHoGpsKAJONqCTYRvL3AaA06sR0Qja46c3sB+WECOiAEFDJhBbtq6FkQRERWoGWxngxfWBaKXAmUv/NgZDsXtgRM7jKYzjcBvQsUULetswgvQoInwsJrgqBB8xqPDQhr0MwpchWBc+/KYW6ChVzSQYkjsCiti0MVQf1aHubDWKa5D3UEFEG1BlgvIFvxWID4VPVs9oXPocKLDLke5gTB7XtPRcYuqB+nge9RgDLBuYCAV3JYhs3QMyZ6X6iIc96U2YaIgCJh8oYcfdDQVvtFBT/iUQZFd7jF7g/4iJFeZDNGGy5vgeVLxjIBkyj8BDaSvNiWQDikAAAAEc0JJVAgICAh8CGSIAAAES0lEQVQ4jU2V22+VRRTFf3tmvtOe0562pz2lHNtaKwSxSoCAUdAHAQVM5KL4pi88+aT/hjExPhmeNSYaEyMhPngJGhEIEqJCUC6xJUIvlN57Ts/1+2a2D1+J7GSSSSazsmettdfI+z8cuBJZdjqLtaI4A06UyAhZ205HlKfdZQFo+RqNpEzs6yjKo6WqXpBzzgezW0QBBSM4m6GU38TW3hcY7hqjK1MksilgHOqsNeeYqVznzsolFmoT+BADICIW1ZedDwCCImzoGGbfyAnGinvJujxNX2WttUS1MYsItNtO+ju2MNS1k2cHjjK+eI4/Z79mpTGdNiRiXOJTwKf6dnBi67sMdI4wX5vk4tRp7pavEvsKkRisKEJCLuriie5dbOk7wLaBo5TyY5y7e4rp8jVAcUkQrHE8P3iYvlyJS1Pfc2n6DL3ZPnZsOMhgfjM51w0E6skqD9ZuMbF0nvHlC+zceIItfft4pv8w9yt/ETRB3v7moDoRRgubKOaKLNSn2D96nN2lfWRMO2vxMtV4GYDOqJeOTA8tX+Xm/I9cf3CGvtwoq40Z5msTaYfegxrlzvI4k+UJ3ho7yd6h15irTnNx6lvurV6naKcIxlKjxKae7ewuHWHHxjdo+iqXpz5N+VsvlwSwj8h/e+EGTjJcuX+WQraXfY8fY6j1EWp6mc0c5+r8L5y+/QHbB15lqnwLr4IRRdbvy7EvDqk1qf+sBWeEyMBzgy/xzrb3yMbn8XMnQXLYjV9RN1s488/HTCz/hpWARXFGsYCIYrwH74XEs76UllfQiEr9Hq2VUxAq4OeoLn1CuTkLRLSCEgdIEJIgJApBBTn82SG1BpyBHhfTE8UUck02tnvG8p4RP0Oba5F4Q7COu3aIew1Y9Za6Opoa4dViRbGiuNgrqoJBeTFa5Eh+lo7+Gq4jZqWc5cyvT7N5eJHb/xbJtsW8+coNdvUmJGqohAznK8PcrBcJCAqYJEDslaYXzlaLXK72Ei1FuJohBCGfa/Lk4DKduSYiSuJTkwNcW+vn72ofrSAkKsQquJZPnwvKsjo+rwzSQnhdH2CsYWY+z53pAjPzXXR1NIlcoBEsPy8Nc6E8SBBDZNMsUBFM7FNyWwGSoKwmli/Lj/F7rQez5igVK4wOLpNrj+nON4ic5+JKiZ+WhqgnltgLLS8kPhXHtYISAFVQFSJVGghGFTKBSq2Nydluij01rA3EiaWRWOqxwdqHHhZQCKq4xINqKoyiKEK3Tdhgm3QX6ry6Z5wgwujIEhkTyESegbYaQZXgBV0fEiXduySkIKyDqSr5TEzBxiSRsiCWs3Ml2m3g4MAM3dKgGDWIxFMPEWgatU5J8zRJQK2CpmCo0C0xE60s390Z5I+1AvUQ4QxcWy2wp2+eXYVF2iShEiKQ1C6oogoy8uH+SWNk6OHYOQMDmQRnoKyZ9Esw/585C8W2JjGWltqURwFnUGP01n8z3Rt7XXup1wAAAABJRU5ErkJggg=="
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray.fromBase64(imgstring))
        self.er_icon = QIcon(pixmap)
        self.settings = QSettings("myRadioDeutsch", "settings")
        self.setStyleSheet(mystylesheet(self))
        self.radioNames = []
        self.radiolist = []
        self.channels = []
        self.radiofile = ""
        self.radioStations = ""
        self.rec_name = ""
        self.rec_url = ""
        self.old_meta = ""
        self.notificationsEnabled = True
        self.wg = QWidget()
        self.fr = RadioFinder()
        self.flabel = QLabel("Radio-Suche")
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10 ,6, 10, 6)
        self.layout1 = QHBoxLayout()

        self.outfile = QStandardPaths.standardLocations(QStandardPaths.TempLocation)[0] + "/radio.mp3"
        self.recording_enabled = False
        self.is_recording = False
        ### combo box
        self.urlCombo = QComboBox()

        self.play_btn = QPushButton("Wiedergabe", self)
        self.play_btn.setFixedWidth(btnwidth)
        self.play_btn.setFlat(True)
        self.play_btn.setIcon(QIcon.fromTheme("media-playback-start"))
        self.layout1.addWidget(self.play_btn)

        self.pause_btn = QPushButton("Pause", self)
        self.pause_btn.setFixedWidth(btnwidth)
        self.pause_btn.setFlat(True)
        self.pause_btn.setIcon(QIcon.fromTheme("media-playback-pause"))
        self.layout1.addWidget(self.pause_btn)

        self.stop_btn = QPushButton("Stop", self)
        self.stop_btn.setFixedWidth(btnwidth)
        self.stop_btn.setFlat(True)
        self.stop_btn.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.layout1.addWidget(self.stop_btn)
        ### record
        self.rec_btn = QPushButton("Aufnahme", self)
        self.rec_btn.setFixedWidth(btnwidth)
        self.rec_btn.setFlat(True)
        self.rec_btn.setIcon(QIcon.fromTheme("media-record"))
        self.rec_btn.clicked.connect(self.recordRadio1)
        self.rec_btn.setToolTip("Record Station")
        self.layout1.addWidget(self.rec_btn)
        ### stop record
        self.stoprec_btn = QPushButton("Aufnahme stoppen", self)
        self.stoprec_btn.setFixedWidth(btnwidth + 60)
        self.stoprec_btn.setFlat(True)
        self.stoprec_btn.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.stoprec_btn.clicked.connect(self.stop_recording)
        self.stoprec_btn.setToolTip("Aufnahme stoppen")
        self.layout1.addWidget(self.stoprec_btn)
        ### edit Radiio List
        self.edit_btn = QPushButton("", self)
        self.edit_btn.setFixedWidth(26)
        self.edit_btn.setFlat(True)
        self.edit_btn.setToolTip("Sender Editor")
        self.edit_btn.setIcon(QIcon.fromTheme("preferences-system"))
        self.edit_btn.clicked.connect(self.edit_Channels)
        self.layout1.addWidget(self.edit_btn)
        ### hide Main Window
        self.hide_btn = QPushButton("", self)
        self.hide_btn.setFixedWidth(26)
        self.hide_btn.setFlat(True)
        self.hide_btn.setToolTip("Fenster verbergen")
        self.hide_btn.setIcon(QIcon.fromTheme("window-hide"))
        self.hide_btn.clicked.connect(self.showMain)
        self.layout1.addWidget(self.hide_btn)        
        


        spc1 = QSpacerItem(6, 10, QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.level_sld = QSlider(self)
        self.level_sld.setTickPosition(1)
        self.level_sld.setOrientation(Qt.Horizontal)
        self.level_sld.setValue(65)
        self.level_lbl = QLabel(self)
        self.level_lbl.setAlignment(Qt.AlignHCenter)
        self.level_lbl.setText("Lautstärke 65")
        #self.layout.addWidget(self.urlCombo)
        self.layout.addLayout(self.layout1)
        self.layout.addItem(spc1)
        self.layout.addWidget(self.level_sld)
        self.layout.addWidget(self.level_lbl)

        self.player = RadioPlayer(self)
        self.player.metaDataChanged.connect(self.metaDataChanged)
        self.player.error.connect(self.handleError)
        self.play_btn.clicked.connect(self.playRadioStation)
        self.pause_btn.clicked.connect(self.pause_preview)
        self.stop_btn.clicked.connect(self.stop_preview)
        self.level_sld.valueChanged.connect(self.set_sound_level)
        self.urlCombo.currentIndexChanged.connect(self.url_changed)
        self.current_station = ""

        self.process = QProcess()
        self.process.started.connect(self.getPID)

        self.wg.setLayout(self.layout)
        self.setCentralWidget(self.wg)

        self.stoprec_btn.setVisible(False)
        self.readStations()

        self.createStatusBar()
        self.setAcceptDrops(True)
        self.setWindowTitle("myRadio")
        
        self.tIcon = QIcon(os.path.join(os.path.dirname(sys.argv[0]), "radio_bg.png"))
        
        self.setWindowIcon(self.tIcon)
        self.stationActs = []


        self.setMinimumHeight(180)
        self.setFixedWidth(600)
        self.move(0, 30)

        # Init tray icon
        trayIcon = QIcon(self.tIcon)

        self.trayIcon = QSystemTrayIcon()
        self.trayIcon.setIcon(trayIcon)
        self.trayIcon.installEventFilter(self)
        self.trayIcon.activated.connect(self.setTrayTrigger)
        self.trayIcon.show()
                
        self.metaLabel = QLabel()
        
        self.geo = self.geometry()
        self.findRadioAction = QAction(QIcon.fromTheme("edit-find"), "Radiostationen suchen", 
                                    triggered = self.findRadio)
        self.editAction = QAction(QIcon.fromTheme("preferences-system"), "Senderliste bearbeiten", 
                                    triggered = self.edit_Channels)
        self.showWinAction = QAction(QIcon.fromTheme("view-restore"), "Hauptfenster anzeigen", triggered = self.showMain)
        self.notifAction = QAction(QIcon.fromTheme("dialog-information"), "Tray Meldungen ausschalten", triggered = self.toggleNotif)
        self.togglePlayerAction = QAction("Wiedergabe stoppen", triggered = self.togglePlay)
        self.togglePlayerAction.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.recordAction = QAction(QIcon.fromTheme("media-record"), "Sender aufnehmen", triggered = self.recordRadio1)
        self.stopRecordAction = QAction(QIcon.fromTheme("media-playback-stop"), "Aufnahme stoppen", 
                                triggered = self.stop_recording)
        self.findExecutable()
        self.readSettings()
        self.makeTrayMenu()
        self.createWindowMenu()
        if QSystemTrayIcon.isSystemTrayAvailable():
            print("System Tray Icon ist verfügbar")
        else:
            print("System Tray Icon ist nicht verfügbar")
        if self.player.state() == QMediaPlayer.StoppedState:
            self.togglePlayerAction.setText("Wiedergabe starten")
            self.togglePlayerAction.setIcon(QIcon.fromTheme("media-playback-start"))            
        elif self.player.state() == QMediaPlayer.PlayingState:
            self.togglePlayerAction.setText("Wiedergabe stoppen")
            self.togglePlayerAction.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.flabel.setFixedSize(180, 26)
        self.flabel.setStyleSheet("QLabel {font-size: 11px; font-weight: bold; \
        color: #555753} QLabel::hover {color: #eeeeec; background-color: #1c87c9; border: 1px solid #babdb6;}")
        self.flabel.mousePressEvent = self.labelClicked
        self.flabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.flabel, 0, Qt.AlignCenter)            
        self.findRadio()
        
    def eventFilter(self, source, event):
        if source is self.trayIcon:
            if event.type() == QEvent.Wheel:
                vol = self.level_sld.value()
                if event.angleDelta().y() > 1:
                    self.level_sld.setValue(int(vol) + 5)
                else:
                    self.level_sld.setValue(int(vol) - 5)
                self.showTrayMessage("myRadio", f"Lautstärke {self.level_sld.value()}", self.tIcon, 1000)
        return super(MainWin, self).eventFilter(source, event)
        
    def setTrayTrigger(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showMainfromTray()
        elif reason == QSystemTrayIcon.MiddleClick:
            self.muteFromTray()

        
    def muteFromTray(self):
        if self.player.isMuted():
            self.player.setMuted(False)
            print("Player nicht stummgeschaltet")
        else:
            self.player.setMuted(True)
            print("Player stummgeschaltet")
        
    def showTrayMessage(self, title, message, icon, timeout = 4000):
        self.trayIcon.showMessage(title, message, icon, timeout)
            
    def findRadio(self):
        self.fr.setStyleSheet(mystylesheet(self))
        self.fr.startButton.clicked.connect(lambda: self.player.stop())
        self.fr.stopButton.clicked.connect(lambda: self.playRadioStation())
        self.fr.findfield.setFocus()
        self.layout.addWidget(self.fr)
        self.fg = QVBoxLayout()
        self.fg.addWidget(self.fr)
        self.layout.addLayout(self.fg)
        self.setFixedHeight(600)
        vol = self.level_sld.value()
        self.fr.player.setVolume(vol)
        self.flabel.setText("Radio-Suche anzeigen")
        self.fr.hide()
        self.setFixedHeight(260)
        
    def labelClicked(self, event):
        if self.fr.isVisible():
            self.fr.hide()
            self.setFixedHeight(260)
            self.flabel.setText("Radio-Suche anzeigen")
        else:
            self.setFixedHeight(600)
            self.fr.show()
            self.flabel.setText("Radio-Suche ausblenden")
            
    def handleError(self):
        print("Fehler: " + self.player.errorString())
        self.showTrayMessage("Error", self.player.errorString(), self.tIcon, 3000)
        self.msglbl.setText(f"Fehler:\n{self.player.errorString()}")
           
    def togglePlay(self):          
        if self.togglePlayerAction.text() == "Wiedergabe stoppen":
            self.stop_preview()
            self.togglePlayerAction.setText("Wiedergabe starten")
            self.togglePlayerAction.setIcon(QIcon.fromTheme("media-playback-start"))
        else:
            self.playRadioStation()
            self.togglePlayerAction.setText("Wiedergabe stoppen")
            self.togglePlayerAction.setIcon(QIcon.fromTheme("media-playback-stop"))

    def getURLfromPLS(self, inURL):
        print("prüfe", inURL)
        response = requests.get(inURL)
        html = response.text.replace("https", "http").splitlines()
        playlist = []

        for line in html:

            if line.startswith("File") == True:
                    list = line.split("=", 1)
                    playlist.append(list[1])

        print("URL:", playlist[0])
        return(playlist[0])


    def getURLfromM3U(self, inURL):
        print("prüfe", inURL)
        response = requests.get(inURL)
        html = response.text.replace("https", "http").splitlines()
        playlist = []

        for line in html:
            if not line.startswith("#") and len(line) > 0 and line.startswith("http"):
                playlist.append(line)

        print("URL:", playlist[0])
        return(playlist[0])
        
    def createWindowMenu(self):
        self.tb = self.addToolBar("Menu")
        self.tb_menu = QMenu()
        self.tb.setIconSize(QSize(20, 20))
        
        ##### submenus from categories ##########
        b = self.radioStations.splitlines()
        for x in reversed(range(len(b))):
            line = b[x]
            if line == "":
                print(f"empty line {x} removed")
                del(b[x])
               
        i = 0
        for x in range(0, len(b)):
            line = b[x]
            while True:
                if line.startswith("--"):
                    chm = self.tb_menu.addMenu(line.replace("-- ", "").replace(" --", ""))
                    chm.setIcon(self.tIcon)
                    break
                    continue

                elif not line.startswith("--"):
                    chm.addAction(self.stationActs[i])
                    i += 1
                    break
        ####################################
        toolButton = QToolButton()
        toolButton.setIcon(self.tIcon)
        toolButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        toolButton.setText("   Stationen")
        toolButton.setMenu(self.tb_menu)
        toolButton.setPopupMode(QToolButton.InstantPopup)
        self.tb.addWidget(toolButton)

        self.tb.setContextMenuPolicy(Qt.PreventContextMenu)
        self.tb.setMovable(False)
        self.tb.setAllowedAreas(Qt.TopToolBarArea)
        
    def makeTrayMenu(self):
        self.tray_menu = QMenu()
        self.tray_menu.addAction(self.togglePlayerAction)
        self.tray_menu.setStyleSheet("font-size: 7pt;")
        ##### submenus from categories ##########
        b = self.radioStations.splitlines()
        for x in reversed(range(len(b))):
            line = b[x]
            if line == "":
                print("leere Zeile", x, "entfernt")
                del(b[x])
                
        i = 0
        for x in range(0, len(b)):
            line = b[x]
            while True:
                if line.startswith("--"):
                    chm = self.tray_menu.addMenu(line.replace("-- ", "").replace(" --", ""))
                    if "Exclusive" in line:
                        chm.setIcon(self.er_icon)
                    else:
                        chm.setIcon(self.tIcon)
                    break
                    continue

                elif  not line.startswith("--"):
                    ch = line.partition(",")[0]
                    
                    self.stationActs.append(QAction(QIcon.fromTheme("browser"), ch, triggered = self.openTrayStation))
                    self.stationActs[i].setData(str(i))
                    chm.addAction(self.stationActs[i])
                    i += 1
                    break
        ####################################
        self.tray_menu.addSeparator()
        if not self.is_recording:
            if not self.urlCombo.currentText().startswith("--"):
                self.tray_menu.addAction(self.recordAction)
                self.recordAction.setText("%s %s: %s" % ("starte Aufnahme von", "channel", self.urlCombo.currentText()))
        if self.is_recording:
            self.tray_menu.addAction(self.stopRecordAction)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.editAction)
        self.tray_menu.addAction(self.showWinAction)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.notifAction)
        self.tray_menu.addSeparator()
        exitAction = self.tray_menu.addAction(QIcon.fromTheme("application-exit"), "Beenden")
        exitAction.triggered.connect(self.exitApp)
        self.trayIcon.setContextMenu(self.tray_menu)

    def showMain(self):
        if self.isVisible() ==False:
            self.showWinAction.setText("Hauptfenster verbergen")
            self.setVisible(True)
        elif self.isVisible() ==True:
            self.showWinAction.setText("Hauptfenster anzeigen")
            self.setVisible(False)

    def showMainfromTray(self):
        buttons = qApp.mouseButtons()
        if buttons == Qt.LeftButton:
            if self.isVisible() == False:
                self.showWinAction.setText("hide Main Window")
                self.setVisible(True)
            elif self.isVisible() == True:
                self.showWinAction.setText("show Main Window")
                self.setVisible(False)
                
    def toggleNotif(self):
        if self.notifAction.text() == "Tray Meldungen ausschalten":
            self.notifAction.setText("Tray Meldungen einschalten")
            self.notificationsEnabled = False
        elif self.notifAction.text() == "Tray Meldungen einschalten":
            self.notifAction.setText("Tray Meldungen ausschalten")
            self.notificationsEnabled = True
        print("Notifications", self.notificationsEnabled )
        self.metaDataChanged()

    def openTrayStation(self):
        action = self.sender()
        if action:
            ind = action.data()
            name = action.text()     
            self.urlCombo.setCurrentIndex(self.urlCombo.findText(name))
            print("%s %s %s" % ("umschalten zu Station:", ind, self.urlCombo.currentText()))

    def exitApp(self):
        self.close()
        QApplication.quit()

    def message(self, message):
        QMessageBox.information(
                None, 'Meldung', message)

    def closeEvent(self, e):
        self.writeSettings()
        print("schreibe Konfigurationsdatei ...\nAuf Wiedersehen ...")
        QApplication.quit()
        

    def readSettings(self):
        print("lese Konfigurationsdatei ...")
        if self.settings.contains("pos"):
            pos = self.settings.value("pos", QPoint(200, 200))
            self.move(pos)
        else:
            self.move(0, 26)
        if self.settings.contains("lastChannel"):
            lch = self.settings.value("lastChannel")
            self.urlCombo.setCurrentIndex(self.urlCombo.findText(lch))
        if self.settings.contains("notifications"):
            self.notificationsEnabled = self.settings.value("notifications")
            if self.settings.value("notifications") == "false":
                self.notificationsEnabled = False
                self.notifAction.setText("Tray Meldungen einschalten")
            else:
                self.notifAction.setText("Tray Meldungen ausschalten")
                self.notificationsEnabled = True
        if self.settings.contains("windowstate"):
            print(self.settings.value("windowstate"))
            if self.settings.value("windowstate") == "Hauptfenster anzeigen":
                self.show()
                self.showWinAction.setText("Hauptfenster verbergen")
            else:
                self.hide()
                self.showWinAction.setText("Hauptfenster anzeigen")
        if self.settings.contains("volume"):
            vol = self.settings.value("volume")
            print("setze Lautstärke auf", vol)
            self.level_sld.setValue(int(vol))
        if self.settings.contains("muted"):
            if self.settings.value("muted") == "false":
                self.player.setMuted(False)
                print("Player nicht stummgeschaltet")
            else:
                self.player.setMuted(True)
                print("Player stummgeschaltet")
        if self.settings.contains("playerstate"):
            if self.settings.value("playerstate") == "0":
                self.player.stop()
            else:
                self.player.play()
                
    def writeSettings(self):
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("index", self.urlCombo.currentIndex())
        self.settings.setValue("lastChannel", self.urlCombo.currentText())
        self.settings.setValue("notifications", self.notificationsEnabled)
        if self.isVisible():
            self.settings.setValue("windowstate", "Hauptfenster anzeigen")
        else:
            self.settings.setValue("windowstate", "Hauptfenster nicht anzeigen")
        self.settings.setValue("volume", self.level_sld.value())
        self.settings.setValue("muted", self.player.isMuted())
        self.settings.setValue("playerstate", self.player.state())
        self.settings.sync()

    def readStations(self):
        menuSectionIcon = QIcon(os.path.join(os.path.dirname(sys.argv[0]), "radio_bg.png"))
        self.urlCombo.clear()
        self.radiolist = []
        self.channels = []
        dir = os.path.dirname(sys.argv[0])
        self.radiofile = os.path.join(dir, "myradio.txt")
        with open(self.radiofile, 'r') as f:
            self.radioStations = f.read()
            f.close()
            for t in self.radioStations:
                self.channels.append(t)
            for lines in self.radioStations.split("\n"):
                if not lines.startswith("--"):
                    self.urlCombo.addItem(QIcon.fromTheme("browser"), lines.partition(",")[0],Qt.UserRole - 1)
                elif lines.startswith("--"):
                    m = QStandardItem(menuSectionIcon,lines.partition(",")[0])
                    m.setEnabled(False)
                    self.urlCombo.model().appendRow(m)            
                self.radiolist.append(lines.partition(",")[2])

    def edit_Channels(self):
        dir = os.path.dirname(sys.argv[0])
        self.radiofile = os.path.join(dir, "myradio.txt")
        self.showTrayMessage("Achtung", "Änderungen sind nach einem Neustart von myRadio verfügbar", self.tIcon)
        self.edWin = Editor()
        self.edWin.setWindowTitle("Sender-Editor")
        self.edWin.radiofile = self.radiofile
        t = open(self.radiofile, 'r').read()
        self.edWin.radio_editor.setPlainText(t)
        self.edWin.isModified = False
        self.edWin.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F5:
            self.playURL()
        elif e.key() == Qt.Key_F1:
            QMessageBox.information(self, "Information", "F5 -> URL aus der Zwischenablage abspielen").exec_()
        else:
            e.accept()

    def findExecutable(self):
        wget = QStandardPaths.findExecutable("wget")
        if wget != "":
            print("%s %s %s" % ("wget gefunden in ", wget, " *** Aufnahmen möglich"))
            self.msglbl.setText("Aufnahmen möglich")
            self.showTrayMessage("Note", "wget gefunden\nAufnahmen möglich", self.tIcon)
            self.recording_enabled = True
        else:
            self.showTrayMessage("Note", "wget nicht gefunden\nkeine Aufnahmen möglich", self.tIcon)
            print("wget nicht gefunden\nkeine Aufnahmen möglich")
            self.recording_enabled = False

    def remove_last_line_from_string(self, s):
        return s[:s.rfind('\n')]

    def createStatusBar(self):
        self.msglbl = QLabel()
        self.msglbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.msglbl.setWordWrap(True)
        self.msglbl.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.msglbl)
        self.msglbl.setText("Willkommen bei myRadio")

    def metaDataChanged(self):
        if self.player.isMetaDataAvailable():
            trackInfo = (self.player.metaData("Title"))
            description = (self.player.metaData("Description"))
            comment = (self.player.metaData("Comment"))
            if trackInfo is None:
                self.msglbl.setText("%s %s" % ("spiele", self.urlCombo.currentText()))
            new_trackInfo = ""
            new_trackInfo = str(trackInfo)
            if len(new_trackInfo) > 200:
                new_trackInfo = str(new_trackInfo).partition('{"title":"')[2].partition('","')[0].replace('\n', " ")[:200]
            if not new_trackInfo == "None":
                self.msglbl.setText(new_trackInfo)
                self.msglbl.adjustSize()
                self.adjustSize()
            else:
                self.msglbl.setText("%s %s" % ("spiele", self.urlCombo.currentText()))
            mt = (f"Titel:{new_trackInfo}\nBeschreibung:{description}\nKommentar:: {comment}")
            if description == None:
                mt = (f"Titel:{new_trackInfo}\nKommentar: {comment}")
            if comment == None:
                mt = (f"Titel:{new_trackInfo}\nKommentar: {description}")
            if description == None and comment == None:
                mt = (f"{new_trackInfo}")
            if not mt == "None":
                if self.notificationsEnabled:
                    if not mt == self.old_meta:
                        print(mt)
                        self.showTrayMessage("myRadio", mt, self.tIcon)
                        self.old_meta = mt
                    self.trayIcon.setToolTip(mt)
                else:
                    self.trayIcon.setToolTip(mt)
                    self.old_meta = mt
        else:
            self.msglbl.setText("%s %s" % ("spiele", self.urlCombo))

    def url_changed(self):
        if self.urlCombo.currentIndex() < self.urlCombo.count() - 1:
            if not self.urlCombo.currentText().startswith("--"):
                ind = self.urlCombo.currentIndex()
                url = self.radiolist[ind]
                
                if url.endswith(".m3u") or url.endswith(".m3u8"):
                    url = self.getURLfromM3U(url)
                if url.endswith(".pls"):
                    url = self.getURLfromPLS(url)
                
                self.current_station = url
                self.player.stop()
                self.rec_btn.setVisible(True)
                self.stop_btn.setVisible(True)
                self.play_btn.setVisible(True)
                self.pause_btn.setVisible(True)
                print("%s %s" %("spiele", url))
                self.playRadioStation()
                if self.togglePlayerAction.text() == "Wiedergabe stoppen":
                    self.togglePlayerAction.setText("Wiedergabe starten")
                    self.togglePlayerAction.setIcon(QIcon.fromTheme("media-playback-start"))
                else:
                    self.togglePlayerAction.setText("Wiedergabe stoppen")
                    self.togglePlayerAction.setIcon(QIcon.fromTheme("media-playback-stop"))
            else:
                self.rec_btn.setVisible(False)
                self.stop_btn.setVisible(False)
                self.play_btn.setVisible(False)
                self.pause_btn.setVisible(False)
 
    def playRadioStation(self):
        if self.player.is_on_pause:
            self.set_running_player()
            self.player.start()
            self.pause_btn.setFocus()
            self.togglePlayerAction.setText("Wiedergabe stoppen")
            self.togglePlayerAction.setIcon(QIcon.fromTheme("media-playback-stop"))
 
        if not self.current_station:
            return
 
        self.player.set_media(self.current_station)
        self.set_running_player()
        self.player.start()
        if self.is_recording:
            self.recordAction.setText(f"stoppe Aufnahme von {self.rec_name}")
            self.recordAction.setIcon(QIcon.fromTheme("media-playback-stop"))
        else:
            self.recordAction.setText("%s %s: %s" % ("starte Aufnahme", "von", self.urlCombo.currentText()))
            self.recordAction.setIcon(QIcon.fromTheme("media-record"))
        self.msglbl.setText("%s %s" % ("spiele", self.urlCombo.currentText()))
        self.setWindowTitle(self.urlCombo.currentText())   

    def playURL(self):
        clip = QApplication.clipboard()
        if not clip.text().endswith(".pls") and not clip.text().endswith(".m3u"):
            self.current_station = clip.text()
        elif clip.text().endswith(".pls") :
            print("is a pls")
            url = self.getURLfromPLS(clip.text())
            self.current_station = url
        elif clip.text().endswith(".m3u") or clip.text().endswith(".m3u8"):
            print("is a m3u")
            url = self.getURLfromM3U(clip.text())
            self.current_station = url
        print(self.current_station)

        if self.player.is_on_pause:
            self.set_running_player()
            self.player.start()
            self.pause_btn.setFocus()
            return
 
        if not self.current_station:
            return
 
        self.player.set_media(self.current_station)
        self.set_running_player()
        self.player.start()
        self.msglbl.setText("%s %s" % ("spiele", self.urlCombo.currentText()))
        self.metaDataChanged()
 
    def set_running_player(self):
        self.play_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        self.rec_btn.setEnabled(True)
 
    def pause_preview(self):
        self.player.set_on_pause()
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.rec_btn.setEnabled(False)
        self.play_btn.setFocus(True)
        self.msglbl.setText("Pause")
 
    def stop_preview(self):
        self.player.finish()
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.rec_btn.setEnabled(False)
        self.msglbl.setText("gestoppt")
        self.togglePlayerAction.setText("Wiedergabe starten")
        self.togglePlayerAction.setIcon(QIcon.fromTheme("media-playback-start"))

 
    def set_sound_level(self, level):
        self.player.set_sound_level(level)
        self.level_lbl.setText("Lautstärke " + str(level))
        self.player.setVolume(level)
 
    def update_volume_slider(self, level):
        self.level_lbl.setText("Lautstärke " + str(level))
        self.level_sld.blockSignals(True)
        self.level_sld.setValue(level)
        self.level_lbl.setText("Lautstärke " + str(level))
        self.level_sld.blockSignals(False)

    def recordRadio1(self):
        if not self.is_recording:
            self.deleteOutFile()
            self.rec_url = self.current_station
            self.rec_name = self.urlCombo.currentText()
            cmd = ("wget -q "  + self.rec_url + " -O " + self.outfile)
            print(cmd)         
            self.is_recording = True   
            self.process.startDetached(cmd)
            self.recordAction.setText(f"stoppe Aufnahme von {self.rec_name}")
            self.recordAction.setIcon(QIcon.fromTheme("media-playback-stop"))
            self.rec_btn.setVisible(False)
            self.stoprec_btn.setVisible(True)
        else:
            self.stop_recording()

    def stop_recording(self):
        if self.is_recording:
            self.process.close()
            print("stoppe Aufnahme")
            self.is_recording = False
            QProcess.execute("killall wget")
            self.saveMovie()
            self.stoprec_btn.setVisible(False)
            self.rec_btn.setVisible(True)
            self.recordAction.setText("%s %s: %s" % ("starte Aufnahme", "von", self.urlCombo.currentText()))
            self.recordAction.setIcon(QIcon.fromTheme("media-record"))
        else:
            self.showTrayMessage("Note", "keine Aufnahme gastartet", self.tIcon)

    def saveMovie(self):
        if not self.is_recording:
            print("Aufnahme speichern")
            infile = QFile(self.outfile)
            savefile, _ = QFileDialog.getSaveFileName(None, "Speichern als...", 
                            QDir.homePath() + "/Musik/" + self.rec_name
                            .replace("-", " ").replace(" - ", " ") + ".mp3", "Audio (*.mp3)")
            if (savefile != ""):
                if QFile(savefile).exists:
                    QFile(savefile).remove()
                print("%s %s" % ("speichere", savefile))
                if not infile.copy(savefile):
                    QMessageBox.warning(self, "Fehler",
                        "Datei %s:\n%s." % (savefile, infile.errorString())) 
                print("%s %s" % ("Prozess-Status: ", str(self.process.state())))
                if QFile(self.outfile).exists:
                    print("%s %s" % ("lösche Datei", self.outfile))
                    QFile(self.outfile).remove()

    def deleteOutFile(self):
        if QFile(self.outfile).exists:
            print("%s %s" % ("lösche Datei", self.outfile)) 
            QFile(self.outfile).remove()
            print("%s %s" % (self.outfile, "gelöscht"))  

    def getPID(self):
        print("%s %s" % (self.process.pid(), self.process.processId()))

 
class RadioPlayer(QMediaPlayer):
    def __init__(self, driver):
        super(RadioPlayer, self).__init__()
        self.driver = driver
        self.url = None
        self.auto_sound_level = True
        self.is_running = False
        self.is_on_pause = False
        self.volumeChanged.connect(self.on_volume_changed)
        self.stateChanged.connect(self.on_state_changed)
 
    def set_media(self, media):
        if isinstance(media, QUrl):
            self.url = media
 
        elif isinstance(media, str):
            self.url = QUrl(media)
 
        self.setMedia(QMediaContent(self.url))
 
    def start(self):
        self.is_running = True
        self.is_on_pause = False
        self.play()
 
    def set_on_pause(self):
        self.is_running = False
        self.is_on_pause = True
        self.pause()

 
    def finish(self):
        self.is_running = False
        self.is_on_pause = False
        self.stop()
            
    def set_sound_level(self, level):
        self.auto_sound_level = False
        self.setVolume(level)
 
    def on_volume_changed(self, value):
        if self.auto_sound_level:
            self.update_volume_slider(value)
        self.auto_sound_level = True
 
    def on_state_changed(self, state):
        if not state:
            self.driver.stop_preview()
    
################################################
BASE_URL = "https://de1.api.radio-browser.info/"

endpoints = {
    "countries": {1: "{fmt}/countries", 2: "{fmt}/countries/{filter}"},
    "codecs": {1: "{fmt}/codecs", 2: "{fmt}/codecs/{filter}"},
    "states": {
        1: "{fmt}/states",
        2: "{fmt}/states/{filter}",
        3: "{fmt}/states/{country}/{filter}",
    },
    "languages": {1: "{fmt}/languages", 2: "{fmt}/languages/{filter}"},
    "tags": {1: "{fmt}/tags", 2: "{fmt}/tags/{filter}"},
    "stations": {1: "{fmt}/stations", 3: "{fmt}/stations/{by}/{search_term}"},
    "playable_station": {3: "{ver}/{fmt}/url/{station_id}"},
    "station_search": {1: "{fmt}/stations/search"},
}

def request(endpoint, **kwargs):

    fmt = kwargs.get("format", "json")

    if fmt == "xml":
        content_type = f"application/{fmt}"
    else:
        content_type = f"application/{fmt}"

    headers = {"content-type": content_type, "User-Agent": "getRadiolist/1.0"}

    params = kwargs.get("params", {})

    url = BASE_URL + endpoint

    resp = requests.get(url, headers=headers, params=params)

    if resp.status_code == 200:
        if fmt == "xml":
            return resp.text
        return resp.json()

    return resp.raise_for_status()

genres = """Classic Rock
Acoustic
Bluegrass 
Country
Folk
Folk Rock
Grunge
Hard Rock
Blues
Oldies
60's
70's
80's
90's
Nachrichten
Swing
Pop
Rock
Classic
Beat
Metal
Techno
Disco
Schlager
Hits
Hip Hop"""

class EndPointBuilder:
    def __init__(self, fmt="json"):
        self.fmt = fmt
        self._option = None
        self._endpoint = None

    @property
    def endpoint(self):
        return endpoints[self._endpoint][self._option]

    def produce_endpoint(self, **parts):
        self._option = len(parts)
        self._endpoint = parts["endpoint"]
        parts.update({"fmt": self.fmt})
        return self.endpoint.format(**parts)


class RadioBrowser:
    def __init__(self, fmt="json"):
        self.fmt = fmt
        self.builder = EndPointBuilder(fmt=self.fmt)

    def countries(self, filter=""):
        endpoint = self.builder.produce_endpoint(endpoint="countries")
        return request(endpoint)

    def codecs(self, filter=""):
        endpoint = self.builder.produce_endpoint(endpoint="codecs")
        return request(endpoint)

    def states(self, country="", filter=""):
        endpoint = self.builder.produce_endpoint(
            endpoint="states", country=country, filter=filter
        )
        return request(endpoint)

    def languages(self, filter=""):
        endpoint = self.builder.produce_endpoint(endpoint="languages", filter=filter)
        return request(endpoint)

    def tags(self, filter=""):
        endpoint = self.builder.produce_endpoint(endpoint="tags", filter=filter)
        return request(endpoint)

    def stations(self, **params):
        endpoint = self.builder.produce_endpoint(endpoint="stations")
        kwargs = {}
        if params:
            kwargs.update({"params": params})
        return request(endpoint, **kwargs)

    def stations_byid(self, id):
        endpoint = self.builder.produce_endpoint(
            endpoint="stations", by="byid", search_term=id
        )
        return request(endpoint)

    def stations_byuuid(self, uuid):
        endpoint = self.builder.produce_endpoint(
            endpoint="stations", by="byuuid", search_term=uuid
        )
        return request(endpoint)

    def stations_byname(self, name):
        endpoint = self.builder.produce_endpoint(
            endpoint="stations", by="byname", search_term=name
        )
        return request(endpoint)

    def stations_bynameexact(self, nameexact):
        endpoint = self.builder.produce_endpoint(
            endpoint="stations", by="bynameexact", search_term=nameexact
        )
        return request(endpoint)

    def stations_bycodec(self, codec):
        endpoint = self.builder.produce_endpoint(
            endpoint="stations", by="bycodec", search_term=codec
        )
        return request(endpoint)

    def stations_bycodecexact(self, codecexact):
        endpoint = self.builder.produce_endpoint(
            endpoint="stations", by="bycodecexact", search_term=codecexact
        )
        return request(endpoint)

    def stations_bycountry(self, country):
        endpoint = self.builder.produce_endpoint(
            endpoint="stations", by="bycountry", search_term=country
        )
        return request(endpoint)

    def stations_bycountryexact(self, countryexact):
        endpoint = self.builder.produce_endpoint(
            endpoint="stations", by="bycountryexact", search_term=countryexact
        )
        return request(endpoint)

    def stations_bystate(self, state):
        endpoint = self.builder.produce_endpoint(
            endpoint="stations", by="bystate", search_term=state
        )
        return request(endpoint)

    def stations_bystateexact(self, stateexact):
        endpoint = self.builder.produce_endpoint(
            endpoint="stations", by="bystateexact", search_term=stateexact
        )
        return request(endpoint)

    #
    def stations_bylanguage(self, language):
        endpoint = self.builder.produce_endpoint(
            endpoint="stations", by="bylanguage", search_term=language
        )
        return request(endpoint)

    def stations_bylanguageexact(self, languageexact):
        endpoint = self.builder.produce_endpoint(
            endpoint="stations", by="bylanguageexact", search_term=languageexact
        )
        return request(endpoint)

    def stations_bytag(self, tag):
        endpoint = self.builder.produce_endpoint(
            endpoint="stations", by="bytag", search_term=tag
        )
        return request(endpoint)

    def stations_bytagexact(self, tagexact):
        endpoint = self.builder.produce_endpoint(
            endpoint="stations", by="bytagexact", search_term=tagexact
        )
        return request(endpoint)

    def playable_station(self, station_id):
        endpoint = self.builder.produce_endpoint(
            endpoint="playable_station", station_id=station_id, ver="v2"
        )

        return request(endpoint)

    def station_search(self, params, **kwargs):
        # http://www.radio-browser.info/webservice#Advanced_station_search
        assert isinstance(params, dict), "params must be a dictionary."
        kwargs["params"] = params
        endpoint = self.builder.produce_endpoint(endpoint="station_search")
        return request(endpoint, **kwargs)
    

class RadioFinder(QMainWindow):
    def __init__(self):
        super(RadioFinder, self).__init__()
        
        self.setAttribute(Qt.WA_QuitOnClose, False)
        self.tIcon = QIcon(os.path.join(os.path.dirname(sys.argv[0]), "radio_bg.png"))
        self.setWindowIcon(self.tIcon)
        self.setContentsMargins(6, 6, 6, 6)
        self.genreList = genres.splitlines()
        
        self.findfield = QLineEdit()
        self.findfield.setFixedWidth(250)
        self.findfield.addAction(QIcon.fromTheme("edit-find"), 0)
        self.findfield.setPlaceholderText("Suchbegriff eingeben und RETURN ")
        self.findfield.returnPressed.connect(self.findStations)
        self.findfield.setClearButtonEnabled(True)
        self.field = QPlainTextEdit()
        self.field.setContextMenuPolicy(Qt.CustomContextMenu)
        self.field.customContextMenuRequested.connect(self.contextMenuRequested)
        self.field.cursorPositionChanged.connect(self.selectLine)
        self.field.setWordWrapMode(QTextOption.NoWrap)
        ### genre box
        self.combo = QComboBox()
        self.combo.currentIndexChanged.connect(self.comboSearch)
        self.combo.addItem("wähle Genre")
        for m in self.genreList:
            self.combo.addItem(m)
        self.combo.setFixedWidth(150)
        ### toolbar ###
        self.tb = self.addToolBar("tools")
        self.tb.setContextMenuPolicy(Qt.PreventContextMenu)
        self.tb.setMovable(False)
        self.setCentralWidget(self.field)
        self.tb.addWidget(self.findfield)
        self.tb.addSeparator()
        self.tb.addWidget(self.combo)
        ### player ###
        self.player = QMediaPlayer()
        self.player.metaDataChanged.connect(self.metaDataChanged)
        self.startButton = QPushButton("Wiedergabe")
        self.startButton.setFlat(True)
        self.startButton.setIcon(QIcon.fromTheme("media-playback-start"))
        self.startButton.clicked.connect(self.getURLtoPlay)
        self.startButton.setEnabled(False)
        self.stopButton = QPushButton("Stop")
        self.stopButton.setFlat(True)
        self.stopButton.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.stopButton.clicked.connect(self.stopPlayer)
        self.stopButton.setEnabled(False)
        self.statusBar().addPermanentWidget(self.startButton)
        self.statusBar().addPermanentWidget(self.stopButton)
        ## actions
        self.addToRadiolistAction = QAction(QIcon.fromTheme("add"), "zu myRadio Senderliste hinzufügen", self, triggered=self.addToRadiolist)
        self.getNameAction = QAction(QIcon.fromTheme("edit-copy"), "Sendername kopieren", self, triggered=self.getName)
        self.getUrlAction = QAction(QIcon.fromTheme("edit-copy"), "Sender-URL kopieren", self, triggered=self.getURL)
        self.getNameAndUrlAction = QAction(QIcon.fromTheme("edit-copy"), "Name,URL kopieren", self, triggered=self.getNameAndUrl)
        self.getURLtoPlayAction = QAction(QIcon.fromTheme("media-playback-start"), "Sender spielen", self, shortcut="F6", triggered=self.getURLtoPlay)
        self.addAction(self.getURLtoPlayAction)
        self.stopPlayerAction = QAction(QIcon.fromTheme("media-playback-stop"), "Wiedergabe stoppen", self, shortcut="F7", triggered=self.stopPlayer)
        self.addAction(self.stopPlayerAction)
        self.helpAction = QAction(QIcon.fromTheme("help-info"), "Hilfe", self, shortcut="F1", triggered=self.showHelp)
        self.addAction(self.helpAction)
        self.statusBar().showMessage("Welcome", 0)
        self.modified = False
        self.old_meta = ''
        
        
    def addToRadiolist(self):
        text = ""
        filename = os.path.join(os.path.dirname(sys.argv[0]), "myradio.txt")
        print(filename)
        with open(filename, 'r') as f:
            text = f.read()
            text = text[:text.rfind('\n')]
            f.close()
            textlist = text.splitlines()
        mycat = []
        for line in textlist:
            if line.startswith("--"):
                mycat.append(line.replace("-- ", "").replace(" --", ""))
        ind = 1
        for x in range(len(mycat)):
            if mycat[x] == self.combo.currentText():
                ind = x
                break
        dlg = QInputDialog()
        mc,_ = dlg.getItem(self, "", "wähle Genre für den Sender", mycat, ind)
        entry = self.getNameAndUrl()
        print(mc, entry)
        filename = os.path.dirname(sys.argv[0]) + os.sep + "myradio.txt"
        print(filename)
        with open(filename, 'r') as f:
            text = f.read()
            text = text[:text.rfind('\n')]
            f.close()
            textlist = text.splitlines()
            if mc in mycat:
                for x in range(len(textlist)):
                    if textlist[x] == f"-- {mc} --":
                        textlist.insert(x + 1, entry)
            else:
                textlist.append(f"-- {mc} --")
                textlist.append(entry)
        with open(filename, 'w') as f:
            for x in reversed(range(len(textlist))):
                if textlist[x] == "\n":
                    print(x)
                    del textlist[x]
            text = '\n'.join(textlist)
            f.write(text)
            f.write('\n\n')
            f.close()
            self.modified = True
            if self.modified:
                self.statusBar().showMessage("saved!", 0)
                self.msgbox("neue Sender sind nach einem Neustart von myRadio verfügbar")            
            
    def msgbox(self, message):
        msg = QMessageBox(1, "Information", message, QMessageBox.Ok)
        msg.exec()

    def comboSearch(self):
        if self.combo.currentIndex() > 0:
            self.findfield.setText(self.combo.currentText())
            self.findStations()

    def getName(self):
        t = self.field.textCursor().selectedText().partition(",")[0]
        clip = QApplication.clipboard()
        clip.setText(t)

    def getURL(self):
        t = self.field.textCursor().selectedText().partition(",")[2]
        clip = QApplication.clipboard()
        clip.setText(t)

    def getNameAndUrl(self):
        t = self.field.textCursor().selectedText()
        clip = QApplication.clipboard()
        clip.setText(t)
        return(t)
        
    def selectLine(self):
        tc = self.field.textCursor()
        tc.select(QTextCursor.LineUnderCursor)
        self.field.setTextCursor(tc)
        self.field.horizontalScrollBar().setValue(self.field.horizontalScrollBar().minimum())

    def showHelp(self):
        QMessageBox.information(self, "Information", "F6 -> Sender spielen\nF7 -> Wiedergabe stoppen")

    def stopPlayer(self):
        if self.player.state() == 1:
            self.player.stop()
            self.statusBar().showMessage("Wiedergabe gestoppt", 0)

    ### QPlainTextEdit contextMenu
    def contextMenuRequested(self, point):
        cmenu = QMenu()
        if not self.field.toPlainText() == "":
            cmenu.addAction(self.getNameAction)
            cmenu.addAction(self.getUrlAction)
            cmenu.addAction(self.getNameAndUrlAction)
            cmenu.addSeparator()
            cmenu.addAction(self.addToRadiolistAction)
            cmenu.addSeparator()
            cmenu.addAction(self.getURLtoPlayAction)
            cmenu.addAction(self.stopPlayerAction)
            cmenu.addSeparator()
            cmenu.addAction(self.helpAction)
        cmenu.exec_(self.field.mapToGlobal(point))  

    def getURLtoPlay(self):
        url = ""
        tc = self.field.textCursor()
        rtext = tc.selectedText().partition(",")[2]
        stext = tc.selectedText().partition(",")[0]
        if not rtext == "":
            if rtext.endswith(".pls") :
                url = self.getURLfromPLS(rtext)
            elif rtext.endswith(".m3u") :
                url = self.getURLfromM3U(rtext)
            elif rtext.endswith(".m3u8") :
                url = self.getURLfromM3U(rtext)
            else:
                url = rtext
            print("stream url=", url)
            self.player.setMedia(QMediaContent(QUrl(url)))
            self.player.play()
            #print("V:", self.player.volume())
            self.statusBar().showMessage("%s %s" % ("spiele", stext), 0)

    def metaDataChanged(self):
        if self.player.isMetaDataAvailable():
            trackInfo = (self.player.metaData("Title"))
            trackInfo2 = (self.player.metaData("Comment"))
            my_metadata = f'{trackInfo}\n{trackInfo2}'
            if trackInfo is not None:
                if not trackInfo == self.old_meta:
                    self.statusBar().showMessage(trackInfo, 0)
                    self.old_meta = trackInfo
                if trackInfo2 is not None:
                    if not self.old_meta == my_metadata:
                        self.statusBar().showMessage(my_metadata)
                        self.old_meta = my_metadata

    def getURLfromPLS(self, inURL):
        print("prüfe", inURL)
        response = requests.get(inURL)
        html = response.text.replace("https", "http").splitlines()
        playlist = []

        for line in html:

            if line.startswith("File") == True:
                    list = line.split("=", 1)
                    playlist.append(list[1])

        print("URL:", playlist[0])
        return(playlist[0])
    
    def getURLfromM3U(self, inURL):
        print("prüfe", inURL)
        response = requests.get(inURL)
        html = response.text.replace("https", "http").splitlines()
        playlist = []

        for line in html:
            if not line.startswith("#") and len(line) > 0  and line.startswith("http"):
                playlist.append(line)

        print("URL:", playlist[0])
        return(playlist[0])

    def findStations(self):
        self.field.setPlainText("")
        mysearch = self.findfield.text()
        self.statusBar().showMessage("searching ...")
        rb = RadioBrowser()
        myparams = {'name': 'search', 'nameExact': 'false'}
        
        for key in myparams.keys():
                if key == "name":
                    myparams[key] = mysearch
        
        r = rb.station_search(params=myparams)
        
        n = ""
        m = ""
        for i in range(len(r)):
            for key,value in r[i].items():
                if str(key) == "name":
                    n = value.replace(",", " ")
                if str(key) == "url":
                    m = value
                    self.field.appendPlainText("%s,%s" % (n, m))
        if not self.field.toPlainText() == "":
            self.statusBar().showMessage(str(self.field.toPlainText().count('\n')+1) \
                                        + " '" + self.findfield.text() + "' Stationen gefunden")
            self.field.textCursor().setPosition(0)
            self.startButton.setEnabled(True)
            self.stopButton.setEnabled(True)
        else:
            self.statusBar().showMessage("nothing found", 0)

################################################

def mystylesheet(self):
    return """
QToolBar
{
background: transparent;
color: #2e3436;
border: 0px;
}
QLineEdit
{
background: #eeeeec;
color: #2e3436;
font-size: 8pt;
}
QPlainTextEdit
{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
color: #2e3436;
font-size: 9pt;
}
QPushButton
{
color: #1f3c5d;
}
QPushButton::hover
{
background: #729fcf;
color: #a40000;
}
QComboBox
{
height: 18px;
background: #d3d7cf;
color: #2e3436;
font-size: 8pt;
}
QComboBox::item
{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #729fcf, stop: 1.0 #204a87);
selection-color: #eeeeec;
}
QStatusBar
{
height: 32px;
color: #888a85;
font-size: 8pt;
background: transparent;
}
QLabel
{
border: 0px;
color: #1f3c5d;
font-size: 9pt;
}
QMainWindow
{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
}
QSlider::handle:horizontal 
{
background: transparent;
width: 8px;
}

QSlider::groove:horizontal {
border: 1px solid #444;
height: 8px;
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #babdb6, stop: 1.0 #D3D3D3);
border-radius: 4px;
}
QSlider::sub-page:horizontal {
background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
    stop: 0 #66e, stop: 1 #bbf);
background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
    stop: 0 #bbf, stop: 1 #55f);
border: 1px solid #777;
height: 8px;
border-radius: 4px;
}
QSlider::handle:horizontal:hover {
background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
    stop:0 #fff, stop:1 #ddd);
border-radius: 4px;
}

QSlider::sub-page:horizontal:disabled {
background: #bbb;
border-color: #999;
}

QSlider::add-page:horizontal:disabled {
background: #eee;
border-color: #999;
}

QSlider::handle:horizontal:disabled {
background: #eee;
border-radius: 4px;
}
QSystemTrayIcon::message { 
font-size: 7pt;
color: #2e3436; 
background: #c4a000; 
border: 1px solid #1f3c5d; }
    """    


if __name__ == "__main__":
    app = QApplication([])
    win = MainWin()
    app.setQuitOnLastWindowClosed(False)
    #win.show()
    sys.exit(app.exec_())
