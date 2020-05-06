import time

from redistimeseries.client import Client
from libpolyd.api import PolydAPI


class EventHandler(Client):
    COMMUNITIES = {
        'nu': 'https://nu.k.polyswarm.network/v1',
        'lima': 'https://lima.polyswarm.network'
    }

    GRACE_PERIOD = 30

    def __init__(self, polyd_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apis = {}
        self.polyd_key = polyd_key

    def get_api_by_community(self, community):
        if community in self.apis:
            return self.apis[community]
        self.apis[community] = PolydAPI(self.polyd_key, self.COMMUNITIES[community])

    def handle_event(self, e):
        handler = getattr(self, f'handle_{e.event}', None)

        if not handler:
            return

        handler(e)

    def handle_bounty(self, bounty):
        api = self.get_api_by_community(bounty.community)
        full_bounty = api.get_bounty(bounty.guid)

        # schedule quorum event
        # TODO this should be coming from the websocket...
        # for now, we hack around it with a delay queue
        self.zadd(f'{bounty.community}:pending_quorum', bounty.vote_expiration+self.GRACE_PERIOD, bounty.guid)
        self

    def handle_assertion(self, assertion):
        pass

    def handle_vote(self, vote):
        pass


class RedisTSClient(Client):
    def __init__(self, name, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.create(name)
        self.create(f'{name}:bounty_nct')
        self.create(f'{name}:vote')
        self.create(f'{name}:assertion_nct')
        self.create(f'{name}:bounty6')
        self.name = name

    def add_event(self, event):
        handler = getattr(self, f'add_{event.event}', None)

        if handler:
            handler(event)

        self.add(self.name, )

    def add_bounty(self, bounty):
        pass

    def add_assertion(self, assertion):
        pass

    def add_vote(self, vote):
        pass