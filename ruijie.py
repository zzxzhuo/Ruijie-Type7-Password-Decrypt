from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QPushButton, QMainWindow, QMessageBox

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("锐捷 Type 7 密文解密")

        enc_field_layout = QHBoxLayout()
        clr_field_layout = QHBoxLayout()
        general_layout = QVBoxLayout()

        enc_field_layout.addWidget(QLabel("密文: "))
        self.ciphertext_input = QLineEdit()
        enc_field_layout.addWidget(self.ciphertext_input)

        clr_field_layout.addWidget(QLabel("明文: "))
        self.clr_txt = QLineEdit()
        self.clr_txt.setReadOnly(True)
        self.clr_txt.setPlaceholderText("解密后的明文将显示在这里")
        clr_field_layout.addWidget(self.clr_txt)
        
        general_layout.addLayout(enc_field_layout)
        general_layout.addLayout(clr_field_layout)
        decrypt_push_btn = QPushButton("解密")
        decrypt_push_btn.clicked.connect(self.decrypt)
        general_layout.addWidget(decrypt_push_btn)
        widget = QWidget()
        widget.setLayout(general_layout)
        self.setCentralWidget(widget)
    def decrypt(self):
        cleartext = ""
        ciphertext = self.ciphertext_input.text()
        ciphertext_len = len(ciphertext)
        if (ciphertext_len % 2 != 0 or ciphertext_len < 4 or ciphertext_len > 52):
            QMessageBox.about(self, "错误", "非锐捷 Type 7 密文，请检查后重试")
            self.clr_txt.setText("")
            return
        magic_string = "*@##Wxf^cOurGer*mArKLe%aIRwolf&^StarRdH#"
        magic_start_pos = int(ciphertext[0:2])
        password_len = int((len(ciphertext) - 2) / 2)
        for i in range(password_len):
            ciphertext_index = 2 + (i * 2)
            ciphertext_cur_hex = ciphertext[ciphertext_index:ciphertext_index + 2]
            magic_cur_char = magic_string[magic_start_pos + i]
            cur_char_ord = int(ciphertext_cur_hex, 16) ^ ord(magic_cur_char)
            if (cur_char_ord < 32 or cur_char_ord > 126):
                QMessageBox.about(self, "错误", "检测到非可打印字符，请尝试直接从配置文件复制密文")
                self.clr_txt.setText("")
                return
            cleartext += chr(cur_char_ord)
        self.clr_txt.setText(cleartext)
            


app = QApplication([])

window = MainWindow()
window.resize(300, 200)
window.show()

app.exec_()