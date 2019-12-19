import pickle
import sys
import zmq

import constPipe


class Mapper:

    def __init__(self, msg_in):
        self.context = zmq.Context()
        self.msg_in = msg_in
        print("Mapper {} started".format(self.msg_in) + "\n-----------------------------")

        address_splitter = "tcp://" + constPipe.SRC1 + ":" + constPipe.SPLITTER_PORT
        self.pull_mapper = self.context.socket(zmq.PULL)  # create a pull socket
        self.pull_mapper.connect(address_splitter)  # connect to task source 1
        self.pull_mapper.setsockopt(zmq.RCVTIMEO, 4000)

        address_reducer1 = "tcp://" + constPipe.SRC1 + ":" + constPipe.REDUCER1_PORT
        self.push_to_reducer1 = self.context.socket(zmq.PUSH)
        self.push_to_reducer1.connect(address_reducer1)

        address_reducer2 = "tcp://" + constPipe.SRC1 + ":" + constPipe.REDUCER2_PORT
        self.push_to_reducer2 = self.context.socket(zmq.PUSH)
        self.push_to_reducer2.connect(address_reducer2)


    def run(self):
        while True:
            try:
                work = pickle.loads(self.pull_mapper.recv())  # receive work from a source
            except:
                break

            sentence = work[1]
            sentence = sentence.lower()
            sentence = sentence.replace(",", "")
            word = sentence.split(" ")
            word = list(filter(None, word))

            for i in range(len(word)):
                if (len(word[i]) % 2) == 0:
                    self.push_to_reducer1.send(pickle.dumps((self.msg_in, word[i])))
                    print("Word {}: ".format(i) + word[i])
                else:
                    self.push_to_reducer2.send(pickle.dumps((self.msg_in, word[i])))
                    print("Word {}: ".format(i) + word[i])
            print("-----------------------------")

        self.push_to_reducer1.send(pickle.dumps((self.msg_in, "###STOP###")))
        self.push_to_reducer2.send(pickle.dumps((self.msg_in, "###STOP###")))



mapper = Mapper(sys.argv[1])
mapper.run()
