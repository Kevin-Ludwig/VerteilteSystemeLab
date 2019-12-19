import logging
import socket
import constCS
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab


class Auskunft:
    _logger = logging.getLogger("vs2lab.lab1.auskunft_schnittstelle.Auskunft")
    _serving = True
    telebook = {'Tim':1111, 'Stefan':2222, 'Lisa':3333}

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((constCS.HOST, constCS.PORT))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("\nServer bound to socket " + str(self.sock) + "\n")

    def serve(self):
        self.sock.listen(1)
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                (connection, address) = self.sock.accept()  # returns new socket and address of client
                while True:  # forever
                    data = connection.recv(1024)
                    data = data.decode('ascii')  # receive data from client
                    self._logger.info("\nMessage " + data + " recieved from Client\n")
                    
                    if not data:
                        break  # stop if client stopped
                    elif data == "getall":
                        data = str(self.telebook)
                    elif data in self.telebook:
                        data = str(self.telebook.get(data))
                    else:
                        data = "No entry found!"

                    connection.send(data.encode('ascii'))  # return sent data plus an "*"
                    self._logger.info("\nServer sends " + data + " over Socket" + str(self.sock) + "\n")
                    
                connection.close()  # close the connection
                self._logger.info("\nServer socket closed!\n")
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("\nServer down.\n")



class Schnittstelle:
    logger = logging.getLogger("vs2lab.a1_layers.auskunft_schnittstelle.Schnittstelle")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((constCS.HOST, constCS.PORT))
        self.logger.info("\nClient connected to socket " + str(self.sock) + "\n")

    def call(self):
        while True:
            msg_in = input("choose Operation: ")
            msg_in = msg_in.split(" ")
            
            if msg_in[0] == "getall" and len(msg_in) == 1:
                self.sock.send(msg_in[0].encode('ascii'))
                self.logger.info("\nClient sends " + msg_in[0] + " over Socket " + str(self.sock) + "\n")
                break;
            elif msg_in[0] == "get" and len(msg_in) == 2:
                self.sock.send(msg_in[1].encode('ascii'))
                self.logger.info("\nClient sends " + msg_in[1] + " over Socket " + str(self.sock) + "\n")
                break;
            else:
                print("Wrong input, try again!")

        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('ascii')
        print(data.decode('ascii'))  # print the result
        self.logger.info("\nAnswer is " + str(msg_out) + "\n")
        
      #  self.sock.close()  # close the connection
      #  self.logger.info("\nClient down.\n")
        return msg_out

    def close(self):
        self.sock.close()
        self.logger.info("\nClient down.\n")
