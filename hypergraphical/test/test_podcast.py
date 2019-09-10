from unittest.mock import Mock, mock_open, patch

from .base import BaseTestCase
from .. import podcast
from ..podcast import Podcast, Episode


class PodcastTestCase(BaseTestCase):
    def setUp(self):
        super(PodcastTestCase, self).setUp()
        self.key = 'podcast'
        self.index = '001'
        self.name = 'Podcast'
        self.episode = Episode(
            index=self.index,
            title='Title',
            date='1970-01-01',
            duration=1337,
            remote_media_uri='https://podcast.org/001',
            speakers={'spk_0': 'Speaker 0', 'spk_1': 'Speaker 1'},
            description='Description'
        )
        self.mock_open = mock_open()
        self.mock_requests = patch.object(podcast, 'requests').start()
        self.mock_requests.get.return_value = Mock(
            status_code=200, content=b'data')
        self.mock_read_yaml_file = patch.object(
            podcast, 'read_yaml_file').start()
        self.mock_read_yaml_file.return_value = {
            'podcast': {
                'name': 'Podcast',
                'episodes': [{
                    'index': '001',
                    'title': 'Title',
                    'date': '1970-01-01',
                    'duration': 1337,
                    'remote_media_uri': 'https://podcast.org/001',
                    'speakers': {
                        'spk_0': 'Speaker 0',
                        'spk_1': 'Speaker 1'
                    },
                    'description': 'Description'
                }]
            }
        }
        self.podcast = Podcast(
            key=self.key,
            index=self.index
        )

    def test_repr(self):
        self.assertEqual('001 - Podcast - Title', str(self.podcast))

    def test_filename(self):
        self.assertEqual('001-podcast-title.mp3', self.podcast.filename)

    def test_get_name_from_key(self):
        self.assertEqual('Podcast', Podcast.get_name_from_key('podcast'))

    def test_get_episode_from_index(self):
        expected = Podcast.get_episode_from_index('podcast', '001')
        self.assertTrue(expected == self.episode)

    def test_download_remote_media(self):
        with patch('builtins.open', self.mock_open):
            self.podcast.download_remote_media()
        self.mock_requests.get.assert_called_with('https://podcast.org/001')
        self.mock_open.assert_called_once_with('001-podcast-title.mp3', 'wb')
        self.mock_open.return_value.write.assert_called_once_with(b'data')
