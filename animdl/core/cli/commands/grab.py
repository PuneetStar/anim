import json
import click

from ...__version__ import __core__
from ...codebase import providers
from ...config import CHECK_FOR_UPDATES, DEFAULT_PROVIDER
from .. import helpers
from ..http_client import client


@click.command(
    name="grab", help="Stream the stream links to the stdout stream for external usage."
)
@click.option("--name", help="Name of the episode to retrieve stream links for")
@helpers.decorators.automatic_selection_options()
@helpers.decorators.logging_options()
@helpers.decorators.setup_loggers()
@helpers.decorators.banner_gift_wrapper(
    client, __core__, check_for_updates=CHECK_FOR_UPDATES
)
def animdl_grab(query, index, name, **kwargs):
    console = helpers.stream_handlers.get_console()
    console.print(
        "The content is outputted to [green]stdout[/] while these messages are outputted to [red]stderr[/]."
    )

    anime, provider = helpers.process_query(
        client, query, console, auto_index=index, provider=DEFAULT_PROVIDER
    )

    if not anime:
        return

    stream_urls = []
    for stream_url_caller, episode in providers.get_appropriate(
        client, anime.get("anime_url"), check=kwargs.get("range")
    ):
        stream_urls.extend(helpers.ensure_extraction(client, stream_url_caller))

    if name:
        stream_urls = helpers.filter_streams_by_name(stream_urls, name)

    click.echo(json.dumps({"streams": stream_urls}))


def filter_streams_by_name(streams, name):
    filtered_streams = []
    for stream in streams:
        if stream.get("name") == name:
            filtered_streams.append(stream)
    return filtered_streams
