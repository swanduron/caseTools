from PyQt5.Qt import *
import sys, os
import yaml
import json


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Integrated Message Box')
        self.setFixedSize(600, 400)
        self.resize(200, 150)
        self.data = self.startLoadYaml()
        self.setup_ui()
        self.freshComponentStats()

    def setup_ui(self):
        self.templatePath = QLabel(self)
        self.config_status = QLabel(self)
        self.config_status.setAlignment(Qt.AlignCenter)
        self.btn = QPushButton()
        self.btn.setText('Load config')
        self.btn.clicked.connect(self.openNewTemplate)
        self.treeView = QTreeWidget(self)
        self.treeView.clicked.connect(self.freshTextBox)
        self.treeView.setColumnCount(1)
        self.treeView.setHeaderLabels(['Content'])
        self.textBlock = QPlainTextEdit(self)
        self.layout_info = QHBoxLayout()
        self.layout_info.addWidget(self.treeView)
        self.layout_info.addWidget(self.textBlock)

        self.layout_config = QHBoxLayout()
        self.layout_config.addWidget(self.btn)
        self.layout_config.addWidget(self.config_status)
        self.vbox = QVBoxLayout(self)
        self.vbox.addLayout(self.layout_info)
        self.vbox.addLayout(self.layout_config)
        self.vbox.addWidget(self.templatePath)

    def freshComponentStats(self):
        if self.data:
            self.templatePath.setText(os.getcwd() + '/content_set.yaml')
            self.config_status.setText('Config is loaded')
            self.config_status.setStyleSheet('background-color: green;')
        else:
            self.templatePath.setText('No template file is loaded.')
            self.config_status.setText('Blank template.')
            self.config_status.setStyleSheet('background-color: red;')

        rootList = []

        self.treeGenerator(self.data, rootList)

        self.treeView.insertTopLevelItems(0, rootList)

    def treeGenerator(self, data, rootList, root=None):
        for k, v in data.items():
            if isinstance(v, str):
                if root:
                    elementPoint = QTreeWidgetItem(root)
                    elementPoint.setText(0, k)
                    elementPoint.setText(1, v)
                else:
                    elementPoint = QTreeWidgetItem()
                    elementPoint.setText(0, k)
                    elementPoint.setText(1, v)
                    rootList.append(elementPoint)
            elif isinstance(v, dict):
                if root:
                    elementPoint = QTreeWidgetItem(root)
                    elementPoint.setText(0, k)
                    self.treeGenerator(v, rootList, elementPoint)
                else:
                    elementPoint = QTreeWidgetItem()
                    elementPoint.setText(0, k)
                    rootList.append(elementPoint)
                    self.treeGenerator(v, rootList, elementPoint)


    def file_warning(self):
        QMessageBox.information(self, "File unexpected!", "This file is not regular YAML file.")

    def openNewTemplate(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.')
        if fname[0]:
            try:
                with open(fname[0], 'r') as file_obj:
                    file_data = file_obj.read()
                    data = yaml.load(file_data, Loader=yaml.FullLoader)
                self.data.update(data)
                print(self.data)
                self.treeView.clear()
                self.freshComponentStats()
                self.templatePath.setText(fname[0])
            except Exception as e:
                print(e)
                self.file_warning()

    def startLoadYaml(self):
        path = 'content_set.yaml'
        try:
            with open(path, encoding='utf-8') as file_obj:
                file_data = file_obj.read()
                data = yaml.load(file_data, Loader=yaml.FullLoader)
            return data
        except:
            return {}


    def freshTextBox(self, qmodelindex):
        # How to use QModelIndex?
        self.textBlock.clear()
        # Below command can get certain item that is clicked, model is QTreeWidgetItem
        item = self.treeView.currentItem()
        print(item.text(0),'<---->',item.text(1))
        # childLevel = path.data()
        # parentLevel = path.parent().data()
        # if not parentLevel:
        #     return
        # textContent = self.data[parentLevel][childLevel]
        if item.text(1):
            self.textBlock.setPlainText(item.text(1))
            clipboard = QApplication.clipboard()
            clipboard.setText(item.text(1))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())