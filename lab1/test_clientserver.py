import logging
import threading
import unittest

import auskunft_schnittstelle
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestEchoService(unittest.TestCase):
    _server = auskunft_schnittstelle.Auskunft()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = auskunft_schnittstelle.Schnittstelle()  # create new client for each test


    def test_getall(self):  # getall
        print("1")
        msg = self.client.call()
        self.assertEqual(msg, "{'Tim': 1111, 'Stefan': 2222, 'Lisa': 3333}")

    def test_get_Tim(self):  #get Tim
        print("2")
        msg = self.client.call()
        self.assertEqual(msg, "1111")
        
    def test_get_NoEntry(self):  #get abc
        print("3")
        msg = self.client.call()
        self.assertEqual(msg, "No entry found!")


    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop
        cls._server_thread.join()  # wait for server thread to terminate


if __name__ == '__main__':
    unittest.main()




