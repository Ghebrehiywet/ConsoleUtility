import pytest
from console_utility import args_main, Parser


@pytest.mark.parametrize("path_to_save_files, files_count, file_name, file_prefix, multiprocessing, data_schema, "
                         "clear_path, data_lines", [
                             ("data/", "3", "super_data", "count", "4", "data/schema.json", "True", "2"),
                             ("data/", "3", "super_data", "count", "4", '{"date":"timestamp:", "name": "str:rand", '
                                                                        '"type":"[\'client\', \'partner\', '
                                                                        '\'government\']", "age": "int:rand(1, '
                                                                        '90)"}', "True", "2"),
                         ])
def test_load_argument_parser(path_to_save_files, files_count, file_name, file_prefix, multiprocessing, data_schema,
                              clear_path, data_lines):
    parserObj = Parser()
    parser = parserObj.argument_parser([path_to_save_files, "--files_count=" + files_count, "--file_name=" + file_name,
                              "--file_prefix=" + file_prefix, "--multiprocessing=" + multiprocessing,
                              "--data_schema=" + data_schema, "--clear_path", "--data_lines=" + data_lines])
    assert parser.path_to_save_files == path_to_save_files
    assert str(parser.files_count) == files_count
    assert parser.file_name == file_name
    assert parser.file_prefix == file_prefix
    assert str(parser.multiprocessing) == multiprocessing
    assert parser.data_schema == data_schema
    assert bool(parser.clear_path) == bool(clear_path)
    assert str(parser.data_lines) == data_lines


@pytest.mark.parametrize("path_to_save_files, files_count, file_name, file_prefix, multiprocessing, data_schema, "
                         "clear_path, data_lines", [
                             ("data/", "3", "super_data", "count", "4", "data/schema.json", "True", "2"),
                             ("data/", "3", "super_data", "count", "4", '{"date":"timestamp:", "name": "str:rand", '
                                                                        '"type":"[\'client\', \'partner\', '
                                                                        '\'government\']", "age": "int:rand(1, '
                                                                        '90)"}', "True", "2"),
                         ])
def test_args_main(path_to_save_files, files_count, file_name, file_prefix, multiprocessing, data_schema,
                   clear_path, data_lines):
    result = args_main([path_to_save_files, "--files_count=" + files_count, "--file_name=" + file_name,
                        "--file_prefix=" + file_prefix, "--multiprocessing=" + multiprocessing,
                        "--data_schema=" + data_schema, "--clear_path", "--data_lines=" + data_lines])
    assert type(result) == dict
