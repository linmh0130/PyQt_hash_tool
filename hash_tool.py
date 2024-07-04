####################################
#  Simple Hash Tool Based on PyQt5
#  
#  author: HML @ EIE, XJTU
#  email: linmh0130@stu.xjtu.edu.cn
####################################

import sys
import os
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from toolui import *
import hashlib

class main_dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.show()
        self.ui.pushButton_opn.released.connect(self.push_opn_callback)
        self.ui.pushButton_gen.released.connect(self.push_gen_callback)
        self.ui.pushButton_cln.released.connect(self.push_cln_callback)
        self.filename = str('')
        self.filesize = 0
        self.file_lastModifyTime = 0
        self.hash_md5 = hashlib.md5()
        self.hash_sha256 = hashlib.sha256() # 初始化时生成hash编码器对象，提升运行时速度
        self.str_showText = str('')

    def push_opn_callback(self):
        if file_name_tuple := QFileDialog.getOpenFileName(self,"Select File"):
            self.filename = file_name_tuple[0]
            self.ui.lineEdit_FileName.setText(self.filename)
            self.filesize = os.path.getsize(self.filename)
            self.file_lastModifyTime = os.path.getmtime(self.filename)

    def push_gen_callback(self):
        buf_len = 1024
        try:
            with open(self.filename,"rb") as file_obj: # rb，按字节读取可避免UnicodeDecodeError
                while buffer := file_obj.read(buf_len):
                    self.hash_md5.update(buffer)
                    self.hash_sha256.update(buffer)
            self.str_showText = self.str_showText + "PATH: " + self.filename + "\n" +\
                                "Size: " + str(round(self.filesize/1024)) + " kB\n" +\
                                "Last Modify Time: " + time.ctime(self.file_lastModifyTime) +"\n" +\
                                "MD5: " + self.hash_md5.hexdigest() + "\n" +\
                                "SHA256: " + self.hash_sha256.hexdigest() + "\n\n"
            self.ui.textBrowser.setText(self.str_showText)
        except:
            self.str_showText = self.str_showText + "FILE: " + self.filename + "\n" +\
                                "Cannot open the file. Please check the file address.\n\n"
            self.ui.textBrowser.setText(self.str_showText)

    def push_cln_callback(self):
        self.str_showText = ""
        self.ui.textBrowser.setText(self.str_showText)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    w = main_dialog()
    w.show()
    sys.exit(app.exec_())
