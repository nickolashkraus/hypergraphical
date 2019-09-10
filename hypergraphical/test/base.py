import logging
import unittest
from unittest.mock import Mock, patch

from .. import aws
from ..aws import AWS
from ..podcast import Podcast, Episode


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.addCleanup(patch.stopall)
        self.logging_info = patch.object(logging, 'info').start()


class AWSBaseTestCase(BaseTestCase):
    def setUp(self):
        super(AWSBaseTestCase, self).setUp()
        self.aws_access_key_id = 'aws_access_key_id'
        self.aws_secret_access_key = 'aws_secret_access_key'
        self.region = 'region'
        self.session = Mock()
        self.mock_session = patch.object(aws.boto3, 'Session').start()
        self.mock_session.return_value = self.session
        self.aws = AWS(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region=self.region
        )


class PodcastBaseTestCase(BaseTestCase):
    def setUp(self):
        super(PodcastBaseTestCase, self).setUp()
        self.key = 'podcast'
        self.index = '001'
        self.name = 'Podcast'
        self.episode = Episode(
            index=self.index,
            title='Title',
            date='1970-01-01',
            duration=1337,
            remote_media_uri='https://podcast.org/1',
            speakers={'spk_0': 'Speaker 0', 'spk_1': 'Speaker 1'},
            description='Description'
        )
        self.mock_get_name_from_key = patch.object(
            Podcast, 'get_name_from_key').start()
        self.mock_get_name_from_key.return_value = self.name
        self.mock_get_episode_from_index = patch.object(
            Podcast, 'get_episode_from_index').start()
        self.mock_get_episode_from_index.return_value = self.episode
        self.podcast = Podcast(
            key=self.key,
            index=self.index
        )
