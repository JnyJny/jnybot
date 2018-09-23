'''Slack events/actions/command dispatcher
'''

import hug
from argparse import Namespace
from .responder import Responder
from .secrets import Secrets
from .glory import TheRecord


class Dispatcher:
    
    @hug.object.post('actions')
    def dispatch_actions(self, body, hug_responder):
        '''
        '''
        hug_responder.enque(Namespace(**body))
        return {}
    
    @hug.object.post('events')
    def dispatch_events(self, body, hug_responder):
        '''
        '''
        payload = Namespace(**body)
        if 'challenge' in body:
            return {'challenge': payload.challenge}
        event = Namespace(**payload.event)
        payload.event = event
        hug_responder.enque(payload)
        return {}

    @hug.object.post('commands')
    def dispatch_commands(self, body, hug_responder):
        '''
        '''
        body.setdefault('type', 'command_callback')
        hug_responder.enque(Namespace(**body))
        return {}

