'''responds to queued events
'''

import threading
from collections import deque
import logging

class Responder:
    '''
    '''
    
    def __init__(self, context=None, handlers=None):

        self._handlers = handlers
        self._context = context
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

            try:
                self._handlers[item.type](self._context, item)
                continue
            except TypeError:
                logging.info('handler table not installed')
            except KeyError:
                logging.info(f'no handlers found for "{item.type}"')

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
            
            logging.info(f'unhandled item {item}')            

            
