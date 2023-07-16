import os
from ...__version__ import __core__
from ...codebase import providers
from ...config import DEFAULT_PROVIDER
from .. import helpers
from ..http_client import client

def animdl_grab(query, provider, episode_number=None):
    anime, selected_provider = helpers.process_query(
        client, query, None, auto_index=1, provider=provider
    )
    if not anime:
        return {}

    episode_streams = []
    for stream_url_caller, episode in providers.get_appropriate(
        client, anime.get("anime_url")
    ):
        if episode_number is None or (episode_number is not None and episode == episode_number):
            stream_url = list(helpers.ensure_extraction(client, stream_url_caller))
            try:
                title = anime.get("name")
            except Exception as e:
                title = ''
            episode_data = {"title": title, "episode": episode, "streams": stream_url}
            episode_streams.append(episode_data)

    data_to_return = {"anime_data": episode_streams}

    return data_to_return
