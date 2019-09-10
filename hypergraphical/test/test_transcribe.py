from unittest.mock import patch
from click.testing import CliRunner

from .base import PodcastBaseTestCase
from .. import podcast
from ..cli import cli


class TranscribeTestCase(PodcastBaseTestCase):
    def setUp(self):
        super(TranscribeTestCase, self).setUp()
        self.runner = CliRunner()
        self.mock_podcast = patch.object(podcast, 'Podcast').start()
        self.mock_podcast.return_value = self.podcast

    def test_transcribe(self):
        result = self.runner.invoke(cli, ['transcribe', 'podcast', '1'])
        self.assertIs(None, result.exception)
        self.assertEqual(0, result.exit_code)
        self.assertEqual('001 - Podcast - Title\n', result.output)
