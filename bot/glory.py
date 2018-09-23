'''a simple reputation backend

glory = Glory('sqlite///path/to/glory.db')

>> glory.reward('alice', 'bob')
>> glory.punish('alice', 'charlie')
>> glory.punish('charlie', 'bob')
>> glory.reward('alice', 'bob')
>> glory.punish('bob', 'charlie')
>> glory.reward('bob', 'alice')

>> the_tally = glory.standing('bob')
'''

import dataset
import time

class TheRecord:
    '''The roll call of glory and shame.
    '''
    
    def __init__(self, backingstore: str = None):
        self.backingstore = backingstore or 'sqlite:///glory.db'
        self.db = dataset.connect(self.backingstore)
        self._history = self.db['history']
        self._summary = self.db['summary']
        
    def _transaction(self,
             from_user: str,
             to_user: str,
             amount: int,
             timestamp: int = None) -> dict:
        '''Adds a transaction to the history table, recording the
        initiating user, the target user, the amount of change and an
        optional timestamp.

        :param from_user: str
        :param to_user: str
        :param amount: int
        :param timestamp: optional int
        :return: dict('name'=str, 'balance'=int)
        '''
        
        row = { 'from': from_user,
                'to': to_user,
                'amount': amount,
                'timestamp': timestamp or time.time(), }
        
        self._history.insert(row)

        row = self._summary.find_one(name=to_user)
        if row:
            row['balance'] += amount
        else:
            row = { 'name': to_user, 'balance': amount}
        self._summary.upsert(row, ['name'])

        return row

    def reward(self, grantee: str, acclaimed: str) -> dict:
        '''Records glory the grantee heaped upon the acclaimed.'''
        return self._transaction(grantee, acclaimed, 1)

    def punish(self, accuser: str, offender: str) -> dict:
        '''Records scorn the accuser heaped upon the offender.'''
        return self._transcation(accuser, offender, -1)

    def standing(self, user : str) -> int:
        '''Returns the user's standing as an integer.
        '''
        row = self._summary.find_one(name=user)
        if row:
            return row.get('balance', 0)
        return 0
        
    
