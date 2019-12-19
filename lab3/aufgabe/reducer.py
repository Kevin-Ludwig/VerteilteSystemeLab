import pickle
import sys
import zmq

import constPipe


class Reducer:

    def __init__(self, msg_in):
        self.msg_in = msg_in
        self.context = zmq.Context()
        print("Reducer {} started".format(self.msg_in) + "\n-----------------------------")

        reducer_port = constPipe.REDUCER1_PORT if msg_in == '1' else constPipe.REDUCER2_PORT  # check task src port
        address_reducer = "tcp://" + constPipe.SRC1 + ":" + reducer_port
        self.pull_reducer = self.context.socket(zmq.PULL)  # create a pull socket
        self.pull_reducer.bind(address_reducer)  # connect to task source 1


    def run(self):
        word_dictionary = {}
        while True:
            work = pickle.loads(self.pull_reducer.recv())  # receive work from a source
            word = work[1]

            if word == "###STOP###":
                break

            if word in word_dictionary:
                word_dictionary[word] = word_dictionary[word] + 1
                print("Word {} exists now {} times.".format(word, word_dictionary[word]))
            else:
                word_dictionary[word] = 1
                print("Word {} added for the first time to list.".format(word))

        print(word_dictionary)



reducer = Reducer(sys.argv[1])
reducer.run()
