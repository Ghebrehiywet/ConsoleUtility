import argparse
import ast
import glob
import json
import logging
import os
import pprint
import shutil
import uuid
import random
import time
from json import JSONDecodeError
from os import getcwd
from os.path import exists
from typing import Optional, Sequence
import configparser

DATA_DIR = './data/'
DEFAULT_INI = DATA_DIR + 'default.ini'


def rand_generator(_type: type) -> str:
    if _type == int:
        return str(random.randint(0, 10000))
    elif _type == str:
        return str(uuid.uuid4())


def rand_within_range(_from: int, _to: int) -> str:
    return str(random.randint(_from, _to))


def rand_choice_from_list(_input: list) -> list:
    return random.choice(_input)


def schema_deserialization(data_schema: str) -> dict:
    # load JSON schema
    logging.info("Data schema parsing STARTED.")
    try:
        is_schema_from_file = exists(data_schema)
        if is_schema_from_file:
            with open(data_schema, 'r') as f:
                data_schema = json.load(f)
        else:
            data_schema = json.loads(data_schema)
    except JSONDecodeError as er:
        logging.error(f"Data schema parse error, {er=}")
        exit(1)
    except BaseException as er:
        logging.error(f"Data schema unknown error, {er=}, {type(er)=}")
        exit(1)
    logging.info("Data schema parsing FINISHED.")
    return data_schema


def argument_parser(argv):
    try:
        logging.info("Default values loading has STARTED.")

        config = configparser.ConfigParser()
        # parse existing file to get default values
        config.read(DEFAULT_INI)
        # read values from section `console_utility_defaults`
        files_count = config.getint('console_utility_defaults', 'files_count')
        data_lines = config.getint('console_utility_defaults', 'data_lines')
        multiprocessing = config.getint('console_utility_defaults', 'multiprocessing')

        logging.info("Default values loading has FINISHED.")
    except configparser.ParsingError as er:
        logging.error(f'Default value parsing error. {er=}')
        exit(1)
    except ValueError as er:
        logging.error(f'Invalid default value error. {er=}')
        exit(1)
    except BaseException as er:
        logging.error(f"Unexpected error {er=}, {type(er)=}")
        exit(1)

    logging.info("Argument parsing has STARTED.")
    parser = argparse.ArgumentParser(
        description="Imagine that you have a data pipeline and you need some test data to check "
                    "correctness of data transformations and validations on this data pipeline. "
                    "You need to generate different input data. "
                    "  Format - only JSON.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('path_to_save_files', type=str, help="Path where all files need to save")
    parser.add_argument('--files_count', type=int, help="The number of json files to generate", default=files_count)
    parser.add_argument('--file_name', type=str, help="Base file_name of the files to generate", required=True)
    parser.add_argument('--file_prefix', type=str, help="Prefix for file name to use if more than 1 file "
                                                        "needs to be generated", choices=['count', 'random', 'uuid'])
    parser.add_argument('--data_schema', type=str, help="The json input schema (it can be a path to json file "
                                                        "with a schema OR the json schema itself", required=True)

    parser.add_argument('--data_lines', type=int, help="Number of lines for each file.", default=data_lines)
    parser.add_argument('--clear_path', help="Flag to delete all existing files that match file_name.",
                        action='store_true')
    parser.add_argument('--multiprocessing', type=int, metavar='', help="The number of processes used to create files.",
                        default=multiprocessing)
    # parser.add_argument('--file_logging', help="Flag to choose file logging option (default is to the console).",
    #                     action='store_true')
    args = parser.parse_args(argv)
    logging.info("Argument parsing FINISHED.")

    return args


def destination_path(path_to_save_files: str) -> str:
    check_folder = os.path.isdir(path_to_save_files)
    # If folder doesn't exist, then create it.
    if not check_folder:
        check_file = os.path.isfile(path_to_save_files)
        if check_file:
            logging.error("There is a file with the same name (duplication occurred).")
            exit(1)
        os.makedirs(path_to_save_files)

    if path_to_save_files == '.':
        return getcwd()
    return path_to_save_files


def get_output_filenames(file_name: str, prefix: str, files_count: int):
    logging.info("Generating an output file/s has STARTED.")

    output_filenames = []
    for count in range(0, files_count):
        if prefix == 'count':
            output_file = file_name + '-' + str(count) + '.json'
        elif prefix == 'random':
            output_file = file_name + '-' + str(random.randint(0, 10000)) + '.json'
        elif prefix == 'uuid':
            output_file = file_name + '-' + str(uuid.uuid4()) + '.json'
        output_filenames.append(output_file)
    logging.info("Generating an output file/s FINISHED.")

    return output_filenames


def clear_path(file_name, destination_folder) -> bool:
    logging.info("Removing/clearing an existing file/s has STARTED.")
    for f in glob.glob(destination_folder + '/' + file_name + '*'):
        os.remove(f)
    logging.info("Removing/clearing an existing file/s FINISHED.")
    return True


def colsole_display(output_dict):
    pprint.pprint(output_dict)


def write_to_file(filename: str, output_dict: dict) ->bool:
    with open(filename, 'w') as f:
        f.write(json.dumps(output_dict))
    return True


def rand_value(_type):
    if _type == "int":
        return random.randint(0, 10000)
    elif _type == "str":
        return str(uuid.uuid4())
    else:
        logging.error(f"rand only works for int and str data types. [{_type}]")
        exit(1)


def empty_value(_type, _value):
    if _type == "int":
        return None
    elif _type == "str":
        return ""
    elif _type == "timestamp":
        if len(_value) > 0:
            logging.warning(f"timestamp does not support any values and it will be ignored. [{_value}]")
        return time.time()
    else:
        logging.error(f"Invalid type (int, str and timestamp are the only supported data types). [{_type}]")
        exit(1)


def generating_test_data(key: str, value: str):

    _output = ""
    value_splited = value.split(':')
    if len(value_splited) == 2:
        _type, _value = value_splited[0], value_splited[1]
        if _type in ('timestamp', 'str', 'int'):
            if len(_value.strip()) == 0 or _type == 'timestamp':
                _output = empty_value(_type, _value)
            elif _value == 'rand':
                _output = rand_value(_type)
            elif "rand(" in _value and _type == 'int':
                rand_range_values = _value.strip().replace('rand(', '').replace(')', '').split(',')
                if len(rand_range_values) == 2 and rand_range_values[0].strip().isdigit() \
                        and rand_range_values[1].strip().isdigit():
                    _output = rand_within_range(int(rand_range_values[0]), int(rand_range_values[1]))
                else:
                    logging.error(f"The provided data schema has an invalid format. [{_value}]")
                    exit(1)
            elif "[" in _value and "]" in _value:
                choices = ast.literal_eval(_value)
                _output = rand_choice_from_list(choices)
                if type(_output).__name__ != _type:
                    logging.error(f"There is a type mismatch in [{key}] between [{_type}] and {_value}")
                    exit(1)
            elif 'rand' not in _value:
                if (_value.isdigit() and _type == 'int') or (not _value.isdigit() and _type == 'str'):
                    _output = _value
                else:
                    logging.error(f"Invalid data type (int, str and timestamp are the only supported data "
                                  f"types) [{key}]")
                    exit(1)
            else:
                logging.error(f"The provided data schema has an invalid format. [{key}]")
                exit(1)
        else:
            logging.error(
                f"Invalid data type (int, str and timestamp are the only supported data types). [{key}]")
            exit(1)
    elif "[" in value and "]" in value:
        choices = ast.literal_eval(value)
        _output = rand_choice_from_list(choices)
    else:
        logging.error(f"Invalid data schema format. [{key}]")
        exit(1)

    return _output


def args_main(argv: Optional[Sequence[str]] = None) -> dict:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', encoding='utf-8', level=logging.INFO)
    #     logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', filename='data/log_file.log',
    #                         encoding='utf-8', level=logging.INFO)

    args = argument_parser(argv)

    schema_dict = schema_deserialization(args.data_schema)

    output_dict = {}
    logging.info("Generating test data has STARTED.")
    for key in schema_dict:
        value = generating_test_data(key, schema_dict[key])
        output_dict[key] = value
    logging.info("Generating test data FINISHED.")

    if args.files_count == 0:
        colsole_display(output_dict)
    elif args.files_count > 0:
        logging.info("Writing an output to a file has STARTED.")

        destination_folder = destination_path(args.path_to_save_files)
        if args.clear_path:
            clear_path(args.file_name, destination_folder)
        output_filenames = get_output_filenames(args.file_name, args.file_prefix, args.files_count)
        for filename in output_filenames:
            write_to_file(destination_folder + filename, output_dict)

        logging.info("Writing an output to a file FINISHED.")
    else:
        logging.error("Invalid file count. count must be greater than 0")
        exit(1)
    return output_dict


if __name__ == '__main__':
    try:
        args_main()
    except BaseException as er:
        logging.error(f"{er=}, {type(er)=}")
