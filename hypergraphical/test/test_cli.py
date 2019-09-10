import logging

from click.testing import CliRunner
from unittest.mock import patch

from .base import BaseTestCase
from ..cli import cli


class CliTestCase(BaseTestCase):
    def setUp(self):
        super(CliTestCase, self).setUp()
        self.runner = CliRunner()

    def test_cli_version(self):
        result = self.runner.invoke(cli, ['--version'])
        self.assertIs(None, result.exception)
        self.assertEqual(0, result.exit_code)
        self.assertEqual('Hypergraphical 0.1\n', result.output)

    def test_cli_no_subcommand(self):
        result = self.runner.invoke(cli)
        self.assertIsInstance(SystemExit(1), type(result.exception))
        self.assertEqual(1, result.exit_code)
        self.assertIn('Usage', result.output)

    def test_configure_logging_exception(self):
        self.get_logger = patch.object(logging, 'getLogger').start()
        self.get_logger.return_value.addHandler.side_effect = Exception
        result = self.runner.invoke(cli, [])
        self.assertIsInstance(result.exception, Exception)
        self.assertEqual(1, result.exit_code)
