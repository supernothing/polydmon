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
import logging

from . import events

logger = logging.getLogger('polydmon')


class WSThread(threading.Thread):
    def __init__(self, uri, queue, retry=False):
        super().__init__()
        self.uri = uri
        self.q = queue
        self.stop = False
        self.retry = retry

    async def _main_loop(self):
        while True:
            try:
                async with websockets.connect(self.uri) as websocket:
                    while not (websocket.closed or self.stop):
                        try:
                            self.q.put(events.Event.from_event(json.loads(await
                                   asyncio.wait_for(websocket.recv(), 1))))
                        except asyncio.TimeoutError:
                            continue
                        except Exception as e:
                            print(e)
                            break
            except Exception as e:
                print(e)

            if not self.retry or self.stop:
                break

            logger.warning('Socket disconnected, retrying in 1s...')
            await asyncio.sleep(1)

        self.q.put(None)

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().run_until_complete(self._main_loop())


event_types = [inflection.underscore(cls.__name__) for cls in events.Event.__subclasses__()]

polyd_uris = [
    'wss://nu.k.polyswarm.network/v1/events/?chain=side',
    'wss://lima.polyswarm.network/events?chain=side',
]


def print_event(e):
    print(str(e))


def print_json(e):
    print(e.json)


@click.command()
@click.option('-e', '--event', multiple=True, type=click.Choice(event_types+['all']), default=['all'])
@click.option('--uri', '-u', multiple=True, type=click.Choice(polyd_uris+['all']), default=['all'])
@click.option('--json', '-j', is_flag=True, default=False)
@click.option('--sql', '-s', type=click.STRING, default='', help='connection string for sql backend')
@click.option('--retry', '-r', is_flag=True, default=False)
def polydmon(event, uri, json, sql, retry):
    uris = uri if 'all' not in uri else polyd_uris

    q = queue.Queue(maxsize=100)
    threads = [WSThread(u, q, retry) for u in uris]

    for t in threads:
        t.start()

    events = event
    ctrlc = False

    def handler(_, __):
        ctrlc = True
        for t in threads:
            t.stop = True

    signal.signal(signal.SIGINT, handler)

    event_handlers = [print_json if json else print_event]

    if sql:
        from .models import EventHandler
        sql_handler = EventHandler(sql)
        event_handlers.append(sql_handler.handle_event)

    # this will quit if either thread exits
    for event in iter(q.get, None):
        if event.event in events or 'all' in events:
            for handler in event_handlers:
                handler(event)

    for t in threads:
        t.join()


if __name__ == "__main__":
    polydmon()
