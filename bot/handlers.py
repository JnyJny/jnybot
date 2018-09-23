'''
'''

SLACK_EVENT = 'event_callback'
SLACK_ACTION = 'action_callback'
SLACK_COMMAND = 'command_callback'

handlers = { SLACK_EVENT: lambda c,i: logging.info(f'E {i}'),
             SLACK_ACTION: lambda c,i: logging.info(f'A {i}'),
             SLACK_COMMAND: lambda c,i: logging.info(f'C {i}'),}
