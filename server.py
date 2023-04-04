import socket
import sys
import threading

from PySide2.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, \
    QLineEdit, QLabel


class ChatClient(QMainWindow):
    def accept_clients(self):
        # possible to accept multiple clients
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.chat_history.append(f"Client connected from {client_address}")
            self.clients.append(client_socket)

            listening_thread = threading.Thread(target=self.listen_to_client, args=(client_socket, client_address))
            listening_thread.start()

    def listen_to_client(self, client_socket, client_address):
        while True:
            try:
                # when message is received its being send to all other clients with name of sender attached
                data = client_socket.recv(1024)
                message = data.decode('utf-8')
                if ":" in message:
                    name, text = message.split(":", 1)
                    self.chat_history.append(f"{name}: " + text)
                    message_with_name = f"{name}: " + text
                    for client in self.clients:
                        if client != client_socket:
                            client.sendall(message_with_name.encode('utf-8'))
                else:
                    self.chat_history.append(f"{client_address[1]}" + ": " + message)
                    message_with_name = f"{client_address[1]}" + ": " + message
                    for client in self.clients:
                        if client != client_socket:
                            client.sendall(message_with_name.encode('utf-8'))

            except:
                self.clients.remove(client_socket)
                break

    def __init__(self):
        self.nickname = "Server"
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("localhost", 9999))
        self.server_socket.listen()

        self.accept_clients_thread = threading.Thread(target=self.accept_clients)
        self.accept_clients_thread.start()

        super().__init__()

        self.setWindowTitle('Chat - server')
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

    def send_message(self):
        message = self.message_input.text()
        self.message_input.clear()
        self.send_button.clicked.connect(self.chat_history.append('You: ' + message))
        name = self.nickname
        for client in self.clients:
            client.sendall((name + ": " + message).encode('utf-8'))

    def set_nickname(self):
        nick = self.nickname_input.text()
        self.nickname_input.clear()
        self.nickname_input.setReadOnly(True)
        self.nickname = nick


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatClient()
    window.show()
    sys.exit(app.exec_())