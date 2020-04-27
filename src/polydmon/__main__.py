#!/usr/bin/env python
import click
import asyncio
import json
import inflection
import websockets
import sys
import threading
import queue
import signal
from json import dumps


class Event(object):
    STR_VALUES = ['event', 'block_number']

    def __init__(self, event):
        self.__dict__ = event['data']
        self.event = event['event']
        self.block_number = event.get('block_number', '')
        self.txhash = event.get('txhash', '')
        self.json = dumps(event)

    @classmethod
    def from_event(cls, event):
        cls = getattr(sys.modules[__name__], inflection.camelize(event['event']), Event)
        return cls(event)

    def __str__(self):
        return ', '.join(f'{k}: {self.__dict__.get(k, "")}' for k in self.STR_VALUES)


class Bounty(Event):
    STR_VALUES = Event.STR_VALUES + ['author', 'sha256', 'artifact_type', 'amount', 'extended_type', 'bounty_guid']


class Assertion(Event):
    STR_VALUES = Event.STR_VALUES + ['author', 'bid', 'extended_type', 'bounty_guid']


class Vote(Event):
    STR_VALUES = Event.STR_VALUES + ['voter', 'votes', 'bounty_guid']


class WSThread(threading.Thread):
    def __init__(self, uri, queue):
        super().__init__()
        self.uri = uri
        self.q = queue
        self.stop = False

    async def _main_loop(self):
        try:
            async with websockets.connect(self.uri) as websocket:
                while not (websocket.closed or self.stop):
                    try:
                        self.q.put(Event.from_event(json.loads(await
                               asyncio.wait_for(websocket.recv(), 1))))
                    except asyncio.TimeoutError:
                        continue
                    except Exception as e:
                        print(e)
                        break
        except Exception as e:
            print(e)

        self.q.put(None)

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().run_until_complete(self._main_loop())


event_types = [inflection.underscore(cls.__name__) for cls in Event.__subclasses__()]

polyd_uris = [
    'wss://nu.k.polyswarm.network/v1/events/?chain=side',
    'wss://lima.polyswarm.network/events?chain=side',
]


@click.command()
@click.option('--event', multiple=True, type=click.Choice(event_types+['all']), default=['all'])
@click.option('--uri', multiple=True, type=click.Choice(polyd_uris+['all']), default=['all'])
@click.option('--json', is_flag=True, default=False)
def polydmon(event, uri, json):
    uris = uri if 'all' not in uri else polyd_uris

    q = queue.Queue(maxsize=100)
    threads = [WSThread(u, q) for u in uris]

    for t in threads:
        t.start()

    events = event

    def handler(_, __):
        for t in threads:
            t.stop = True

    signal.signal(signal.SIGINT, handler)

    for event in iter(q.get, None):
        if event.event in events or 'all' in events:
            if json:
                print(event.json)
            else:
                print(str(event))

    for t in threads:
        t.join()


if __name__ == "__main__":
    polydmon()
