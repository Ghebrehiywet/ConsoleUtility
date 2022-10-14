import json
import os
import shutil
import tempfile
import unittest
from os import path, getcwd

import pytest
from parameterized import parameterized

from console_utility import destination_path, clear_path
import console_utility


class TestFilesAndDirs(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    @parameterized.expand([
        ['super_data_1.json', '{"age": "20", "date": 1665762514.3698308, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "client"}'],
    ])
    def test_write_to_file(self, file_name, sample_output_dict):
        # Create a file in the temporary directory
        file_path = path.join(self.test_dir, file_name)
        f = open(file_path, 'w')
        output = console_utility.Output(sample_output_dict)
        result = output.write_to_file(file_path)
        assert result

        # Reopen the file and check if what we read back is the same
        f = open(file_path)
        content = json.load(f)
        self.assertEqual(str(content), sample_output_dict)

    @parameterized.expand([
        ('.', getcwd()),
        ('data/', 'data/'),
    ])
    def test_destination_path(self, given_path, return_path):
        actual = destination_path(given_path)
        assert return_path == actual

    @parameterized.expand([
        ('data/schema.json', 'data/')
    ])
    def test_destination_path_raises(self, given_path, return_path):
        with pytest.raises(SystemExit) as exc_info:
            result = destination_path(given_path)
        assert str(exc_info.value) == '1'

    @parameterized.expand([
        ('super_data', './data/')
    ])
    def test_clear_files_under_destination_folder(self, file_name, destination_folder):
        dir_list_before_clearing = os.listdir(destination_folder)
        dir_list_before_clearing = [f for f in dir_list_before_clearing if
                                    os.path.isfile(destination_folder + '/' + f) and f.startswith(file_name)]

        result = clear_path(file_name, destination_folder)
        assert result

        dir_list_after_clearing = os.listdir(destination_folder)
        dir_list_after_clearing = [f for f in dir_list_after_clearing if
                                   os.path.isfile(destination_folder + '/' + f) and f.startswith(file_name)]
        assert len(dir_list_after_clearing) == 0

    @parameterized.expand([
        'super_data',
        'schema_data'
    ])
    def test_clear_files_temp_folder(self, file_name):
        # Create three file in the temporary directory
        file_path = path.join(self.test_dir, file_name)
        for i in range(1, 4):
            f = open(file_path + str(i), 'w')

        result = clear_path(file_name, self.test_dir)
        assert result

        dir_list_after_clearing = os.listdir(self.test_dir)
        dir_list_after_clearing = [f for f in dir_list_after_clearing if
                                   os.path.isfile(self.test_dir + '/' + f) and f.startswith(file_name)]
        assert len(dir_list_after_clearing) == 0


if __name__ == '__main__':
    unittest.main()
