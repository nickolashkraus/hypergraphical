from unittest.mock import mock_open, patch

from .base import BaseTestCase
from .. import utils


class UtilsTestCase(BaseTestCase):
    def setUp(self):
        super(UtilsTestCase, self).setUp()
        self.mock_open = mock_open()
        self.mock_json_dump = patch.object(utils.json, 'dump').start()
        self.mock_yaml_dump = patch.object(utils.yaml, 'dump').start()

    def test_read_json_file(self):
        read_data = '{"a": 1, "b": 2, "c": 3}'
        self.mock_open = mock_open(read_data=read_data)
        with patch('builtins.open', self.mock_open):
            result = utils.read_json_file('filename')
        self.mock_open.assert_called_once_with('filename', 'r')
        self.assertEqual({'a': 1, 'b': 2, 'c': 3}, result)

    def test_write_json_file(self):
        data = {'a': 1, 'b': 2, 'c': 3}
        with patch('builtins.open', self.mock_open) as mock_file:
            utils.write_json_file(data, 'filename')
        self.mock_open.assert_called_once_with('filename', 'w')
        self.mock_json_dump.assert_called_once_with(
            data, mock_file.return_value)

    def test_append_file(self):
        data = 'data'
        with patch('builtins.open', self.mock_open):
            utils.append_file(data, 'filename')
        self.mock_open.assert_called_once_with('filename', 'a')
        self.mock_open.return_value.write.assert_called_once_with('data')

    def test_write_file(self):
        data = 'data'
        with patch('builtins.open', self.mock_open):
            utils.write_file(data, 'filename')
        self.mock_open.assert_called_once_with('filename', 'w')
        self.mock_open.return_value.write.assert_called_once_with('data')

    def test_read_yaml_file(self):
        read_data = \
            """
            a: 1
            b: 2
            c: 3
            """
        self.mock_open = mock_open(read_data=read_data)
        with patch('builtins.open', self.mock_open):
            result = utils.read_yaml_file('filename')
        self.mock_open.assert_called_once_with('filename', 'r')
        self.assertEqual({'a': 1, 'b': 2, 'c': 3}, result)

    def test_write_yaml_file(self):
        data = {'a': 1, 'b': 2, 'c': 3}
        with patch('builtins.open', self.mock_open) as mock_file:
            utils.write_yaml_file(data, 'filename')
        self.mock_open.assert_called_once_with('filename', 'w')
        self.mock_yaml_dump.assert_called_once_with(
            data, mock_file.return_value, default_flow_style=False)

    def test_slugify(self):
        string = 'This is a string - let\'s slugify it!'
        self.assertEqual(
            'this-is-a-string-lets-slugify-it', utils.slugify(string))
