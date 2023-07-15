import json
from ...__version__ import __core__
from ...codebase import providers
from ...config import CHECK_FOR_UPDATES, DEFAULT_PROVIDER
from .. import helpers
from ..http_client import client

def animdl_grab(query, range_value=None):
    """
    Stream the stream links to the stdout stream for external usage.

    Parameters:
        query (str): The search query for the anime.
        range_value (Optional[str]): A range of episodes to fetch.

    Returns:
        dict: A dictionary containing the anime title, episode number, and stream URLs.
    """
    anime, provider = helpers.process_query(
        client, query, None, auto_index=True, provider=DEFAULT_PROVIDER
    )

    if not anime:
        return {}

    episode_streams = []
    for stream_url_caller, episode in providers.get_appropriate(
        client, anime.get("anime_url"), check=lambda ep: ep in range_value.split('-') if range_value else None
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
