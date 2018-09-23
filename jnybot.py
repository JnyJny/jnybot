#!/usr/bin/env python3
'''a Slack Application & Chat Bot
'''

import hug
import logging
import os
import threading

from bot.dispatcher import Dispatcher
from bot.responder import Responder
from bot.glory import TheRecord
from bot.secrets import Secrets

def parse_commandline():
    '''
    '''
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-s', '--secrets',
                        type=str, default='jnybot.cfg')
    parser.add_argument('-H', '--host',
                        type=str, default='bots.xenolab.com')
    parser.add_argument('-p', '--port',
                        type=int, default=8000)
    parser.add_argument('-b', '--botname',
                        type=str, default='jnybot')
    parser.add_argument('-g', '--glorydb',
                        type=str, default='sqlite:///glory.db')
    parser.add_argument('-l', '--logfile',
                        type=str, default='bot.log')
    return parser.parse_args()

    
def main():
    '''
    '''
    args = parse_commandline()

    logging.basicConfig(level=logging.DEBUG,
                        filename=args.logfile)

    the_responder = Responder(Secrets(args.secrets),
                              TheRecord(args.glorydb))
    
    @hug.directive()
    def responder(default=False, **kwargs):
        '''Make a global Responder available to all routes as "hug_responder".
        '''
        return the_responder

    logging.info(f'{args.botname} started with {args}')
    
    api = hug.API(__name__)

    route = hug.route.API(__name__)
    
    route.object(f'/{args.botname}')(Dispatcher)

    api.http.serve(host=args.host, port=args.port)
    

if __name__ == '__main__':
    main()
            
        
    

    
