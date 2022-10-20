import json
import os
import shutil
import tempfile
import time
import unittest
from os import path, getcwd

import pytest
from parameterized import parameterized

from console_utility_main import destination_path, clear_existing_files
import console_utility_main


class TestFilesAndDirs(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    @parameterized.expand([
        ['super_data_1.json', '[{"age": "20", "date": 1665762514.97979, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "client"},'
                              '{"age": "30", "date": 1665762514.32423, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "partner"},'
                              '{"age": "50", "date": 1665762514.56767, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "government"}]'],
    ])
    def test_write_to_file(self, file_name, sample_output_dict):
        # Create a file in the temporary directory
        file_path = path.join(self.test_dir, file_name)

        output = console_utility_main.Output(sample_output_dict)
        output.write_to_file(file_path, "count", 6, 4, self.test_dir, True)
        result = output.dump_to_file(file_path)
        assert result

        # Reopen the file and check if what we read back is the same
        f = open(file_path)
        content = json.load(f)
        self.assertEqual(str(content), sample_output_dict)

    @parameterized.expand([
        ['super_data_2.json', '[{"age": "20", "date": 1665762514.97979, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "client"},'
                              '{"age": "30", "date": 1665762514.32423, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "partner"},'
                              '{"age": "50", "date": 1665762514.56767, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "government"}]'],
    ])
    def test_sequential_write_to_file(self, file_name, sample_output_dict):
        # Create a file in the temporary directory
        file_path = path.join(self.test_dir, file_name)

        output = console_utility_main.Output(sample_output_dict)
        output_filenames = console_utility_main.get_output_filenames(file_path, "count", 1)
        result = output.sequencial_writing_to_file(output_filenames)
        assert result

    @parameterized.expand([
        ['super_data_3.json', '[{"age": "20", "date": 1665762514.97979, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "client"},'
                              '{"age": "30", "date": 1665762514.32423, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "partner"},'
                              '{"age": "50", "date": 1665762514.56767, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "government"}]'],
    ])
    def test_multiprocess_writing_to_file(self, file_name, sample_output_dict):
        # Create a file in the temporary directory
        file_path = path.join(self.test_dir, file_name)

        output = console_utility_main.Output(sample_output_dict)
        output_filenames = console_utility_main.get_output_filenames(file_path, "count", 1)
        result = output.multiprocess_writing_to_file(4, output_filenames)
        assert result

    @parameterized.expand([
        ['super_data_1.json', '[{"age": "20", "date": 1665762514.97979, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "client"},'
                              '{"age": "30", "date": 1665762514.32423, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "partner"},'
                              '{"age": "30", "date": 1665762514.32423, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "partner"},'
                              '{"age": "30", "date": 1665762514.32423, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "partner"},'
                              '{"age": "30", "date": 1665762514.32423, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "partner"},'
                              '{"age": "50", "date": 1665762514.56767, "name": '
                              '"5bc76b1a-fcf6-4a26-93d3-c631bde7a6ee", "type": "government"}]'],
    ])
    def test_seq_vs_multiprocess_write_to_file(self, file_name, sample_output_dict):
        # Create a file in the temporary directory
        file_path = path.join(self.test_dir, file_name)

        output = console_utility_main.Output(sample_output_dict)
        output_filenames = console_utility_main.get_output_filenames(file_path, "count", 20)

        st1 = time.time()
        output.sequencial_writing_to_file(output_filenames)
        end1 = time.time()
        diff1 = end1 - st1

        st2 = time.time()
        output.multiprocess_writing_to_file(4, output_filenames)
        end2 = time.time()
        diff2 = end2 - st2
        assert diff1 > diff2


if __name__ == '__main__':
    unittest.main()
