import json
from ...__version__ import __core__
from ...codebase import providers
from ...config import CHECK_FOR_UPDATES, DEFAULT_PROVIDER
from .. import helpers
from ..http_client import client

def animdl_grab(query, provider):
    """
    Stream the stream links to the stdout stream for external usage.

    Parameters:
        query (str): The search query for the anime.
        provider (str): The provider to use for fetching the anime.

    Returns:
        dict: A dictionary containing the anime title, episode number, and stream URLs.
    """
    anime, selected_provider = helpers.process_query(
        client, query, None, auto_index=1, provider=provider
    )

    if not anime:
        return {}

    episode_streams = []
    for stream_url_caller, episode in providers.get_appropriate(
        client, anime.get("anime_url")
    ):
        stream_url = list(helpers.ensure_extraction(client, stream_url_caller))
        try:
            title = anime.get("name")
        except Exception as e:
            title = ''
        episode_data = {"title": title, "episode": episode, "streams": stream_url}
        episode_streams.append(episode_data)

    return {"anime_data": episode_streams}

# Example usage:
