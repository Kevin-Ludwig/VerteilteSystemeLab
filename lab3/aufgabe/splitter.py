import pickle
import sys
import time
import zmq

import constPipe


class Splitter:

    def __init__(self):
        self.context = zmq.Context()
        print("Splitter started" + "\n-----------------------------")

        address = "tcp://" + constPipe.SRC1 + ":" + constPipe.SPLITTER_PORT
        self.push_splitter = self.context.socket(zmq.PUSH)  # create a push socket
        self.push_splitter.bind(address)  # bind socket to address
        time.sleep(1) # wait to allow all clients to connect


    def run(self, file):
        text = open(file,"r")
        text = text.read()
        print("Input Text:\n" + text)

        split_text = text.split(".")
        del split_text[-1]

        print("Sending parts to mappers:")
        for i in range(len(split_text)):
            print("Row {}: ".format(i) + split_text[i])
            self.push_splitter.send(pickle.dumps(("Splitter", split_text[i])))



splitter = Splitter()
splitter.run("file")

