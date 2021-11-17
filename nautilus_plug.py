import threading 
import socket
import time
import sys
import os

# Main class
class NautilusPlug:

    def __init__(self, gateway_ip, gateway_port):

        self.__BUF_SIZE = 4096

        self.__gateway_ip = gateway_ip
        self.__gateway_port = gateway_port
        self.__this_id = ""

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__connect_to_gateway()
        self.__register_client()

        threading.Thread(target=self.__recv_message).start()


    #Private:

    def __connect_to_gateway(self):
        self.__sock.connect((self.__gateway_ip, self.__gateway_port))

    
    def __disconnect_from_gateway(self):
        self.__sock.close()

    
    def __register_client(self):
        message = f"version: 1.0\r\nto: {self.__gateway_ip}:{self.__gateway_port}\r\nfrom: client\r\n"
        message += f"action: register-client\r\ntype: request\r\nbody-size: 0\r\n\r\n"
        self.__sock.send(message.encode("utf-8"))
        return_message = self.__sock.recv(self.__BUF_SIZE)
        self.__this_id = return_message.decode("utf-8").split("\r\n\r\n")[1]
        

    def __recv_message(self):
        while True:
            message = self.__sock.recv(self.__BUF_SIZE)
            print(message) # melhorar o recv e filtrar mensagens pro client e mensagens para a aplicação

   
    def __send_message(self, message):
        self.__sock.send(message)


    #Public:

    def get_this_id():
        return self.__this_id


    def send_text_message_to_client(self, remote_client, msg):
        message = f"version: 1.0\r\nto: {remote_client}\r\nfrom: {self.__this_id}\r\naction: send-to-client\r\n"
        message += f"type: text\r\nbody-size: {len(msg)}\r\n\r\n{msg}"

        self.__send_message(message.encode("utf-8"))

    


app = NautilusPlug("127.0.0.1", 10000)


while True:
    time.sleep(2)
    to = input("To: ")
    msg = input("Msg: ")
    if to != "" and msg != "":
        app.send_text_message_to_client(to, msg)
    to = ""
    msg = ""