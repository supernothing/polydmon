#!/usr/bin/env python
import click
import inflection
import queue
import signal
import logging

from walrus import Database

from polyd_events import events, consumer

logger = logging.getLogger('polydmon')

event_types = [inflection.underscore(cls.__name__) for cls in events.Event.__subclasses__()]

polyd_communities = [
    'nu',
    'lima'
]


def print_event(e):
    print(str(e))


@click.command()
@click.option('-e', '--event', multiple=True, type=click.Choice(event_types+['all']), default=['all'])
@click.option('--community', '-c', multiple=True, type=click.Choice(list(polyd_communities)+['all']), default=['all'])
@click.option('--sql', '-s', type=click.STRING, envvar='POLYDMON_SQL', default='',
              help='connection string for sql backend')
@click.option('--redis', '-h', type=click.STRING, envvar='POLYDMON_REDIS', default='127.0.0.1',
              help='redis hostname')
@click.option('--retry', '-r', is_flag=True, default=False)
@click.option('--quiet', '-q', is_flag=True, default=False)
def polydmon(event, community, sql, redis, retry, quiet):
    db = Database(redis)
    communities = community if 'all' not in community else polyd_communities

    if 'all' in event:
        streams = [f'polyd-{c}-all' for c in communities]
    else:
        streams = []
        for c in communities:
            for e in events:
                streams.append(f'polyd-{c}-{e}')

    c = consumer.EventConsumer(streams, __name__, db)

    if not quiet:
        event_handlers = [print_event]
    else:
        event_handlers = []

    if sql:
        from .models import EventHandler
        sql_handler = EventHandler(sql)
        event_handlers.append(sql_handler.handle_event)

    # this will quit if either thread exits
    for event in c.iter_events():
        for handler in event_handlers:
            handler(event)


if __name__ == "__main__":
    polydmon()
