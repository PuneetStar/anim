import json
from ...__version__ import __core__
from ...codebase import providers
from ...config import CHECK_FOR_UPDATES, DEFAULT_PROVIDER
from .. import helpers
from ..http_client import client

def animdl_grab(query, index, range_value=None):
    """
    Stream the stream links to the stdout stream for external usage.

    Parameters:
        query (str): The search query for the anime.
        index (bool): Whether to automatically select the first search result or prompt for selection.
        range_value (Optional[str]): A range of episodes to fetch.

    Returns:
        dict: A dictionary containing the anime title, episode number, and stream URLs.
    """
    anime, provider = helpers.process_query(
        client, query, None, auto_index=index, provider=DEFAULT_PROVIDER
    )

    if not anime:
        return {}

    episode_streams = []
    for stream_url_caller, episode in providers.get_appropriate(
        client, anime.get("anime_url"), check=range_value
    ):
        stream_url = list(helpers.ensure_extraction(client, stream_url_caller))
        try:
            title = anime.get("name")
        except Exception as e:
            title = ''
        episode_data = {"title": title, "episode": episode, "streams": stream_url}
        episode_streams.append(episode_data)

    return {"anime_data": episode_streams}

