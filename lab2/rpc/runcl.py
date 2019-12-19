import rpc
from context import lab_logging
import time
import logging

lab_logging.setup()


logger = logging.getLogger('vs2lab.lab2.rpc.runcl')
cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})
result_list = cl.append('bar', base_list)
logger.debug('OK received')
print("OK received")

print('Hello, I am an async thread!')
logger.debug('Hello, I am an async thread!')
result_list = []
asyncT = rpc.AsyncThread(cl, result_list)
asyncT.start()

while result_list == []:
    time.sleep(2)
    print("We still waiting!")
    logger.debug('We still waiting!')

logger.debug('Result: {}'.format(result_list[0].value))
print("Result: {}".format(result_list[0].value))
cl.stop()
