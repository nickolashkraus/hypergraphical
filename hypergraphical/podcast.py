import os
import requests

from .utils import read_yaml_file, slugify


class Podcast:
    """Object representation of a podcast."""
    PATH_TO_PODCASTS_YAML = \
        os.path.join(os.path.dirname(__file__), 'podcasts.yaml')

    def __init__(
            self,
            key: str,
            index: str) -> None:
        self.key = key
        self.index = index
        self.name = self.get_name_from_key(key)
        self.episode = self.get_episode_from_index(key, index)

    def __repr__(self) -> str:
        return '{} - {} - {}'.format(
            self.episode.index, self.name, self.episode.title)

    @property
    def filename(self) -> str:
        filename = '{} {} {}'.format(
            self.episode.index, self.key, self.episode.title)
        return '{}{}'.format(slugify(filename), '.mp3')

    @classmethod
    def get_name_from_key(cls, key: str) -> str:
        """Get the podcast name from podcast.yaml."""
        podcasts = read_yaml_file(cls.PATH_TO_PODCASTS_YAML)
        podcast = podcasts.get(key)
        return podcast.get('name')

    @classmethod
    def get_episode_from_index(cls, key: str, index: str) -> str:
        """Get the podcast episode from podcast.yaml."""
        podcasts = read_yaml_file(cls.PATH_TO_PODCASTS_YAML)
        podcast = podcasts.get(key)
        episodes = podcast.get('episodes')
        return Episode(**episodes[int(index) - 1])

    def download_remote_media(self) -> None:
        """Download the podcast."""
        r = requests.get(self.episode.remote_media_uri)
        r.raise_for_status()
        filename = self.filename
        with open(filename, 'wb') as f:
            f.write(r.content)


class Episode:
    """Object representation of a podcast episode."""

    def __init__(
            self,
            index: str,
            title: str,
            date: str,
            duration: int,
            remote_media_uri: str,
            speakers: dict,
            description: str) -> None:
        self.index = index
        self.title = title
        self.date = date
        self.duration = duration
        self.remote_media_uri = remote_media_uri
        self.speakers = speakers
        self.description = description

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
