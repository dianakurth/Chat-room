import sys
import threading
import socket

from PySide2.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, \
    QLineEdit, QLabel


class ChatClient(QMainWindow):
    def __init__(self):
        super().__init__()

        # initial nickname is number of port client is connected from
        self.nickname = str(sock.getsockname()[1])

        self.setWindowTitle('Chat - client')
        self.resize(500, 500)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)

        self.message_input = QLineEdit()
        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_message)

        self.nickname_input = QLineEdit()
        self.nickname = QLabel('Set your nickname: ')
        self.nick_button = QPushButton('Set')
        self.nick_button.clicked.connect(self.set_nickname)

        self.message_layout = QHBoxLayout()
        self.message_layout.addWidget(self.message_input)
        self.message_layout.addWidget(self.send_button)

        self.nickname_layout = QHBoxLayout()
        self.nickname_layout.addWidget(self.nickname)
        self.nickname_layout.addWidget(self.nickname_input)
        self.nickname_layout.addWidget(self.nick_button)

        self.chat_layout = QVBoxLayout()
        self.chat_layout.addLayout(self.nickname_layout)
        self.chat_layout.addWidget(self.chat_history)
        self.chat_layout.addLayout(self.message_layout)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.chat_layout)
        self.setCentralWidget(self.central_widget)

        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.start()

    def receive_data(self):
        while True:
            data = sock.recv(1024)
            data_decoded = data.decode('utf-8')
            # checking if message is from different client or the server
            if ":" in data_decoded:
                name, text = data_decoded.split(":", 1)
                self.chat_history.append(f"{name}: " + text)
            else:
                self.chat_history.append('Server: ' + data.decode('utf-8'))

    def send_message(self):
        message = self.message_input.text().strip()
        name = self.nickname
        if message:
            self.chat_history.append('You: ' + message)
            self.message_input.clear()
            sock.sendall((name + ": " + message).encode('utf-8'))

    def set_nickname(self):
        nick = self.nickname_input.text()
        self.nickname_input.clear()
        self.nickname_input.setReadOnly(True)
        self.nickname = nick


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sock = socket.socket()
    # host and port to connect
    sock.connect(('localhost', 9999))
    window = ChatClient()
    window.show()
    sys.exit(app.exec_())
