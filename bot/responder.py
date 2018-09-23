'''responds to queued events
'''

import threading
from collections import deque
import logging

class Responder:
    '''
    '''
    
    def __init__(self, secrets, glory):
        self._secrets = secrets
        self._glory = glory
        self._fifo = deque()
        self._cv = threading.Condition()
        self._thrd = threading.Thread(target=self)
        self._thrd.start()

    def enque(self, item):
        with self._cv:
            self._fifo.append(item)
            self._cv.notify()

    def __call__(self):

        while True:
            with self._cv:
                if len(self._fifo) == 0:
                    self._cv.wait()
                try:
                    item = self._fifo.popleft()
                except IndexError:
                    continue

            if item.type == 'event_callback':
                logging.info(f'EVT {item}')
                continue
        
            if item.type == 'action_callback':
                logging.info(f'ACT {item}')
                print('A', item)
                continue
        
            if item.type == 'command_callback':
                logging.info(f'CMD {item}')                
                continue

            print(f'unhandled item {item}')
