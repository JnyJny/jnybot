
'''
'''

import os
from dataclasses import dataclass
import json

@dataclass
class Secrets:
    client_id : str
    secret : str
    signing : str
    bot_token : str
    app_token : str    
    
    def __init__(self, configfile=None):

        if configfile:
            with open(configfile) as fp:
                config = json.load(fp)
        else:
            config = os.environ
            
        self.client_id = config['CLIENT_ID']
        self.secret = config['CLIENT_SECRET']        
        self.signing = config['SIGNING_SECRET']
        self.bot_token = config['BOT_TOKEN']
        self.app_token = config['APP_TOKEN']

    def to_dict(self):
        '''
        '''
        return { 'CLIENT_ID':self.client_id,
                 'CLIENT_SECRET': self.secret,
                 'SIGNING_SECRET': self.signing,
                 'BOT_TOKEN': self.bot_token,
                 'APP_TOKEN': self.app_token,}

    def write(self, filename):
        '''
        '''
        with open(filename, 'w') as fp:
            json.dump(self.to_dict(), fp)
