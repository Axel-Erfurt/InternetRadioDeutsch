#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import shutil
import pandas as pd
from PyQt5.QtCore import Qt, QDir, QAbstractTableModel, QModelIndex, QVariant, QSize, QFile
from PyQt5.QtWidgets import (QMainWindow, QTableView, QApplication, QLineEdit, QWidget,  
                             QFileDialog, QAbstractItemView, QMessageBox, QToolButton, QSizePolicy)
from PyQt5.QtGui import QIcon, QKeySequence

class PandasModel(QAbstractTableModel):
    def __init__(self, df = pd.DataFrame(), parent=None): 
        QAbstractTableModel.__init__(self, parent=None)
        self._df = df
        self.setChanged = False
        self.dataChanged.connect(self.setModified)

    def setModified(self):
        self.setChanged = True
        print(self.setChanged)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QVariant()
        elif orientation == Qt.Vertical:
            try:
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QVariant()

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if (role == Qt.EditRole):
                return self._df.values[index.row()][index.column()]
            elif (role == Qt.DisplayRole):
                return self._df.values[index.row()][index.column()]
        return None

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        self._df.values[row][col] = value
        self.dataChanged.emit(index, index)
        return True

    def rowCount(self, parent=QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=QModelIndex()): 
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

class Viewer(QMainWindow):
    def __init__(self, parent=None):
      super(Viewer, self).__init__(parent)
      self.df = None
      self.filename = ""
      self.fname = ""
      self.csv_file = ''
      self.mychannels_file = f'{QDir.homePath()}/.local/share/InternetRadioDeutsch/myradio.txt'
      self.mychannels_file_backup = f'{QDir.homePath()}/.local/share/InternetRadioDeutsch/myradio.txt_backup'
      self.setGeometry(0, 0, 1000, 600)
      self.lb = QTableView()
      self.lb.horizontalHeader().hide()
      self.model =  PandasModel()
      self.lb.setModel(self.model)
      self.lb.setEditTriggers(QAbstractItemView.DoubleClicked)
      self.lb.setSelectionBehavior(self.lb.SelectRows)
      self.lb.setSelectionMode(self.lb.SingleSelection)
      self.lb.setDragDropMode(self.lb.InternalMove)
      self.setStyleSheet(stylesheet(self))
      self.lb.setAcceptDrops(True)
      self.setCentralWidget(self.lb)
      self.setContentsMargins(10, 10, 10, 10)
      self.statusBar().showMessage("Willkommen", 0)
      self.setWindowTitle("myRadio Listeneditor")
      self.setWindowIcon(QIcon.fromTheme("multimedia-playlist"))
      self.createMenuBar()
      self.createToolBar()
      self.create_backup()
      if QFile.exists(self.mychannels_file):
          self.open_channels(self.mychannels_file)
      else:
          self.msgbox('myradio.txt nicht gefunden')
      self.lb.setFocus()
      
    def msgbox(self, message):
        msg = QMessageBox(2, "Information", message, QMessageBox.Ok)
        msg.exec()

      
    def create_backup(self):
        if shutil.copyfile(self.mychannels_file, self.mychannels_file_backup):
            self.msgbox('myradio.txt_backup wurde erstellt')

    def closeEvent(self, event):
        print(self.model.setChanged)
        if  self.model.setChanged == True:
            quit_msg = "<b>Das Dokument wurde geändert.<br>Wollen Sie die Änderungen speichern?</ b>"
            reply = QMessageBox.question(self, 'Speichern', 
                     quit_msg, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
                if self.filename == "":
                    self.writeCSV()
                else:
                    self.save_file(self.filename)
        else:
            print("keine Änderungen. Auf Wiedersehen")

    def createMenuBar(self):
        bar=self.menuBar()
        self.filemenu=bar.addMenu("Datei")
        self.separatorAct = self.filemenu.addSeparator()
        self.filemenu.addAction(QIcon.fromTheme("document-open"), "Datei öffnen",  self.openFile, QKeySequence.Open) 
        self.filemenu.addAction(QIcon.fromTheme("document-save-as"), "Speichern als ...",  self.writeCSV, QKeySequence.SaveAs) 

    def createToolBar(self):
        tb = self.addToolBar("Werkzeuge")
        tb.setIconSize(QSize(16, 16))
        
        self.findfield = QLineEdit(placeholderText = "finden ...")
        self.findfield.setClearButtonEnabled(True)
        self.findfield.setFixedWidth(200)
        tb.addWidget(self.findfield)
        
        tb.addSeparator()
        
        self.replacefield = QLineEdit(placeholderText = "ersetzen mit ...")
        self.replacefield.setClearButtonEnabled(True)
        self.replacefield.setFixedWidth(200)
        tb.addWidget(self.replacefield)
        
        tb.addSeparator()
        
        btn = QToolButton()
        btn.setText("alles ersetzen")
        btn.setToolTip("alles ersetzen")
        btn.clicked.connect(self.replace_in_table)
        tb.addWidget(btn)
        
        tb.addSeparator()

        del_btn = QToolButton()
        del_btn.setIcon(QIcon.fromTheme("edit-delete"))
        del_btn.setToolTip("Zeile löschen")
        del_btn.clicked.connect(self.del_row)
        tb.addWidget(del_btn)
        
        tb.addSeparator()
        
        add_btn = QToolButton()
        add_btn.setIcon(QIcon.fromTheme("add"))
        add_btn.setToolTip("Zeile hinzufügen")
        add_btn.clicked.connect(self.add_row)
        tb.addWidget(add_btn)

        move_down_btn = QToolButton()
        move_down_btn.setIcon(QIcon.fromTheme("down"))
        move_down_btn.setToolTip("nach unten bewegen")
        move_down_btn.clicked.connect(self.move_down)
        tb.addWidget(move_down_btn)
        
        move_up_up = QToolButton()
        move_up_up.setIcon(QIcon.fromTheme("up"))
        move_up_up.setToolTip("nach oben bewegen")
        move_up_up.clicked.connect(self.move_up)
        tb.addWidget(move_up_up)
        
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, 0)
        tb.addWidget(spacer)
        
        self.filter_field = QLineEdit(placeholderText = "Filtern (Enter drücken)")
        self.filter_field.setClearButtonEnabled(True)
        self.filter_field.setToolTip("Suchbegriff einfügen und Enter drücken")
        self.filter_field.setFixedWidth(200)
        self.filter_field.returnPressed.connect(self.filter_table)
        self.filter_field.textChanged.connect(self.update_filter)
        tb.addWidget(self.filter_field)
        
        
    def move_down(self):
        if self.model.rowCount() < 1:
            return
        i = self.lb.selectionModel().selection().indexes()[0].row()
        b, c = self.df.iloc[i].copy(), self.df.iloc[i+1].copy()
        self.df.iloc[i],self.df.iloc[i+1] = c,b
        self.model.setChanged = True
        self.lb.selectRow(i+1)
        
    def move_up(self):
        if self.model.rowCount() < 1:
            return
        i = self.lb.selectionModel().selection().indexes()[0].row()
        b, c = self.df.iloc[i].copy(), self.df.iloc[i-1].copy()
        self.df.iloc[i],self.df.iloc[i-1] = c,b
        self.model.setChanged = True
        self.lb.selectRow(i-1)
        
    def del_row(self): 
        if self.model.rowCount() < 1:
            return
        i = self.lb.selectionModel().selection().indexes()[0].row()
        if len(self.df.index) > 0:
            self.df = self.df.drop(self.df.index[i])
            self.model = PandasModel(self.df)
            self.lb.setModel(self.model)
            self.model.setChanged = True
            self.lb.selectRow(i)
            
    def add_row(self): 
        if self.model.rowCount() < 1:
            return
        print("Zeile hinzufügen")
        newrow = {0:'name', 1:'url'}       
        self.df = self.df.append(newrow, ignore_index=True)
        self.model = PandasModel(self.df)
        self.lb.setModel(self.model)
        self.model.setChanged = True
        self.lb.selectRow(self.model.rowCount() - 1)
                

    def load_channels_file(self):
        if self.model.setChanged == True:
            save_msg = "<b>Das Dokument wurde geändert.<br>Wollen Sie die Änderungen speichern?</ b>"
            reply = QMessageBox.question(self, 'Speichern', 
                     save_msg, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.writeCSV()
                self.open_channels()
            else:
                self.model.setChanged = False
                self.open_channels()
        else:
            self.model.setChanged = False
            self.open_channels()
            
    def openFile(self, path=None):
        tvplayer_folder = f'{QDir.homePath()}/.local/share/InternetRadioDeutsch/'
        path, _ = QFileDialog.getOpenFileName(self, "Datei öffnen", tvplayer_folder,"myRadio Listen (*.txt)")
        if path:
            self.open_channels(path)
        
    def open_channels(self, fileName):
        if fileName:
            self.convert_to_csv()
            print(fileName + " geladen")
            f = open(self.csv_file, 'r+b')
            with f:
                self.filename = fileName
                self.df = pd.read_csv(f, delimiter = '\t', keep_default_na = False, low_memory=False, header=None)
                self.model = PandasModel(self.df)
                self.lb.setModel(self.model)
                self.lb.resizeColumnsToContents()
                self.lb.selectRow(0)
                self.statusBar().showMessage(f"{fileName} loaded", 0)
                self.model.setChanged = False
                self.lb.verticalHeader().setMinimumWidth(24)
             
    def convert_to_csv(self):
        mychannels_file = f'{QDir.homePath()}/.local/share/InternetRadioDeutsch/myradio.txt'
        channels_list = open(mychannels_file, 'r').read().splitlines()
        csv_content = ""
        group = ""
        name = ""
        url = ""

        for x in reversed(range(len(channels_list))):
            line = channels_list[x]
            if line == "":
                print(f"empty line {x} removed")
                del(channels_list[x])
               
        i = 0
        for x in range(0, len(channels_list)):
            line = channels_list[x]
            while True:
                if line.startswith("--"):
                    group = line.replace("-- ", "").replace(" --", "")
                    break
                    continue

                elif not line.startswith("--"):
                    ch_line = line.split(",")
                    name = ch_line[0]
                    url = ch_line[1]
                    i += 1
                    break
                    
            if not name == "" and not name == channels_list[x-1].partition(",")[0]:        
                csv_content += (f'{name}\t{group}\t{url}\n')

        self.csv_file = '/tmp/mychannels.csv'
        with open(self.csv_file, 'w') as f:        
            f.write(csv_content)
            
    def writeCSV(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Datei speichern", self.mychannels_file,"TVPlayer2 List (*.txt)")
        if fileName:
            self.save_file(fileName)
            
    def save_file(self, fileName):
            # save temporary csv
            f = open(self.csv_file, 'w')
            newModel = self.model
            dataFrame = newModel._df.copy()
            dataFrame.to_csv(f, sep='\t', index = False, header = False)  
            f.close()
            
            # convert to txt
            channels_list = open(self.csv_file, 'r').read().splitlines()

            group = ""
            name = ""
            url = ""
            out_list = []

            for x in range(len(channels_list)):
                line = channels_list[x].split('\t')
                name = line[0]
                group = line[1]
                url = line[2]
                
                out_list.append(f"-- {group} --")
                out_list.append(f'{name},{url}')
                

            tlist = self.ordered_set(out_list)
            m3u_content = '\n'.join(tlist)

            with open(fileName, 'w') as f:        
                f.write(m3u_content)

            print(fileName + " gespeichert")
            self.model.setChanged = False
            
    def ordered_set(self, in_list):
        out_list = []
        added = set()
        for val in in_list:
            if not val in added:
                out_list.append(val)
                added.add(val)
        return out_list


    def replace_in_table(self):
        if self.model.rowCount() < 1:
            return
        searchterm = self.findfield.text()
        replaceterm = self.replacefield.text()
        if searchterm == "":
            return
        else:
            if len(self.df.index) > 0:
                self.df.replace(searchterm, replaceterm, inplace=True, regex=True)
                self.lb.resizeColumnsToContents()
                self.model.setChanged = True
                
    def filter_table(self):
        if self.model.rowCount() < 1:
            return
        index = 0
        searchterm = self.filter_field.text()
        df_filtered = self.df[self.df[index].str.contains(searchterm, case=False)]
        self.model = PandasModel(df_filtered)
        self.lb.setModel(self.model)
        self.lb.resizeColumnsToContents()       
       
    def update_filter(self):
        if self.filter_field.text() == "":
            self.filter_table()

def stylesheet(self):
        return """
    QMenuBar
        {
            background: transparent;
            border: 0px;
        }
        
    QMenuBar:hover
        {
            background: #d3d7cf;
        }
        
    QTableView
        {
            border: 1px solid #d3d7cf;
            border-radius: 0px;
            font-size: 8pt;
            background: #eeeeec;
            selection-color: #ffffff
        }
    QTableView::item:hover
        {   
            color: black;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #729fcf, stop:1 #d3d7cf);           
        }
        
    QTableView::item:selected {
            color: #F4F4F4;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #6169e1, stop:1 #3465a4);
        } 

    QTableView QTableCornerButton::section {
            background: #D6D1D1;
            border: 0px outset black;
        }
        
    QHeaderView:section {
            background: #d3d7cf;
            color: #555753;
            font-size: 8pt;
        }
        
    QHeaderView:section:checked {
            background: #204a87;
            color: #ffffff;
        }
        
    QStatusBar
        {
        font-size: 7pt;
        color: #555753;
        }
        
    """
 
if __name__ == "__main__":
 
    app = QApplication(sys.argv)
    main = Viewer()
    main.show()
sys.exit(app.exec_())