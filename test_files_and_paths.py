import json
import os
from os import getcwd
import pytest
from main import destination_path, clear_path, write_to_file


@pytest.mark.parametrize("given_path, return_path", [
    ('.', getcwd()),
    ('data/', 'data/'),
])
def test_destination_path(given_path, return_path):
    result = destination_path(given_path)
    assert return_path == result


@pytest.mark.parametrize("given_path, return_path", [
    ('data/schema.json', 'data/')
])
def test_destination_path_raises(given_path, return_path):
    with pytest.raises(SystemExit) as exc_info:
        result = destination_path(given_path)
    assert str(exc_info.value) == '1'


@pytest.mark.parametrize("file_name, destination_folder", [
    ('super_data', './data/')
])
def test_clear_files_under_destination_folder(file_name, destination_folder):
    dir_list_before_clearing = os.listdir(destination_folder)
    dir_list_before_clearing = [f for f in dir_list_before_clearing if
                                os.path.isfile(destination_folder + '/' + f) and f.startswith(file_name)]

    result = clear_path(file_name, destination_folder)
    assert result

    dir_list_after_clearing = os.listdir(destination_folder)
    dir_list_after_clearing = [f for f in dir_list_after_clearing if
                               os.path.isfile(destination_folder + '/' + f) and f.startswith(file_name)]
    assert len(dir_list_after_clearing) == 0


@pytest.mark.parametrize("file_name, sample_output_dict", [
    ('./data/super_data_1.json', "{'name': 'test', 'age': '20'}")
])
def test_write_to_file(file_name, sample_output_dict):
    result = write_to_file(file_name, sample_output_dict)
    assert result
    with open(file_name, 'r') as f:
        content = json.load(f)
        assert content == sample_output_dict
