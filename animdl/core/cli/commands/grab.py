import json
import os
from ...__version__ import __core__
from ...codebase import providers
from ...config import CHECK_FOR_UPDATES, DEFAULT_PROVIDER
from .. import helpers
from ..http_client import client

CACHE_DIR = "anime_data_cache"

def animdl_grab(query, provider, episode_number=None):
    """
    Stream the stream links to the stdout stream for external usage.

    Parameters:
        query (str): The search query for the anime (should match the title).
        provider (str): The provider to use for fetching the anime.
        episode_number (int): The specific episode number to fetch. (Optional)

    Returns:
        dict: A dictionary containing the anime title, episode number, and stream URLs.
    """
    anime, selected_provider = helpers.process_query(
        client, query, None, auto_index=1, provider=provider
    )

    if not anime:
        return {}

    # Create cache directory if it doesn't exist
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    cache_filename = f"{CACHE_DIR}/{query}.json"

    # Try to load data from cache
    if os.path.exists(cache_filename):
        with open(cache_filename, "r") as cache_file:
            cached_data = json.load(cache_file)
        if cached_data.get("anime_data"):
            return cached_data

    episode_streams = []
    for stream_url_caller, episode in providers.get_appropriate(
        client, anime.get("anime_url")
    ):
        if episode_number is not None and episode == episode_number:
            stream_url = list(helpers.ensure_extraction(client, stream_url_caller))
            try:
                title = anime.get("name")
            except Exception as e:
                title = ''
            episode_data = {"title": title, "episode": episode, "streams": stream_url}
            episode_streams.append(episode_data)
            break  # Stop after finding the specific episode if provided

    data_to_cache = {"anime_data": episode_streams}

    # Save data to cache for future use
    with open(cache_filename, "w") as cache_file:
        json.dump(data_to_cache, cache_file)

    return data_to_cache

# Example usage:
