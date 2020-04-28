import sys
import inflection
from json import dumps

class Event(object):
    STR_VALUES = ['event', 'block_number']

    def __init__(self, event):
        json = dumps(event)
        self.__dict__ = event['data']
        self.event = event['event']
        self.block_number = event.get('block_number', -1)
        self.txhash = event.get('txhash', '')
        self.json = json

    @classmethod
    def from_event(cls, event):
        cls = getattr(sys.modules[__name__], inflection.camelize(event['event']), Event)
        return cls(event)

    def __str__(self):
        return ', '.join(f'{k}: {self.__dict__.get(k, "")}' for k in self.STR_VALUES)


class Bounty(Event):
    STR_VALUES = Event.STR_VALUES + ['author', 'sha256', 'artifact_type', 'amount', 'filename', 'extended_type', 'guid']

    def __init__(self, event):
        super().__init__(event)
        # assumes single-artifact bounty
        self.__dict__.update(self.metadata[0])


class Assertion(Event):
    STR_VALUES = Event.STR_VALUES + ['author', 'bid', 'bounty_guid']

    def __init__(self, event):
        super().__init__(event)
        try:
            if type(self.bid) == list:
                self.bid = int(self.bid[0])
        except AttributeError:
            print('attr error')
            pass


class Vote(Event):
    STR_VALUES = Event.STR_VALUES + ['voter', 'votes', 'bounty_guid']

    def __init__(self, event):
        super().__init__(event)
        try:
            if type(self.votes) == list:
                self.votes = int(self.votes[0])
        except AttributeError:
            print('attr error')
            pass
