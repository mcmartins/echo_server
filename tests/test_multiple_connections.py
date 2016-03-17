import multiprocessing as mp
import unittest

from base import BaseEchoServerTest, setup_server, setup_client


class MultiConnectionsEchoServerTest(BaseEchoServerTest):
    def test_(self):
        self.test_multiple_connections()

    def test_multiple_connections(self):
        # start server in a different process
        #server = mp.Process(target=setup_server)
        #server.start()

        # start multiple connections
        workers = [mp.Process(target=setup_client) for i in range(0, 5)]
        for p in workers:
            p.daemon = True
            p.start()

        # wait for all to finish
        for p in workers:
            p.join()

        # stop the server
        #server.terminate()


if __name__ == '__main__':
    unittest.main()
