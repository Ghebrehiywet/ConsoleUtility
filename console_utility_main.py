import argparse
import ast
import glob
import json
import logging
import multiprocessing
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


class Rand:
    def rand_within_range(self, _from: int, _to: int) -> str:
        return str(random.randint(_from, _to))

    def rand_generator(self, _type: type) -> str:
        if _type == int:
            return self.rand_within_range(0, 10000)
        elif _type == str:
            return str(uuid.uuid4())

    def rand_choice_from_list(self, _input: list) -> list:
        return random.choice(_input)

    def rand_value(self, _type):
        if _type == "int":
            return self.rand_within_range(0, 10000)
        elif _type == "str":
            return str(uuid.uuid4())
        else:
            logging.error(f"rand only works for int and str data types. [{_type}]")
            exit(1)

    def empty_value(self, _type, _value):
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


class Parser:
    def schema_deserialization(self, data_schema: str) -> dict:
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

    def argument_parser(self, argv):
        try:
            logging.info("Default values loading has STARTED.")

            config = configparser.ConfigParser()
            # parse existing file to get default values
            config.read(DEFAULT_INI)
            # read values from section `console_utility_defaults`
            files_count = config.getint('console_utility_defaults', 'files_count')
            data_lines = config.getint('console_utility_defaults', 'data_lines')
            _multiprocessing = config.getint('console_utility_defaults', 'multiprocessing')

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
                                                            "needs to be generated",
                            choices=['count', 'random', 'uuid'])
        parser.add_argument('--data_schema', type=str, help="The json input schema (it can be a path to json file "
                                                            "with a schema OR the json schema itself", required=True)

        parser.add_argument('--data_lines', type=int, help="Number of lines for each file.", default=data_lines)
        parser.add_argument('--clear_path', help="Flag to delete all existing files that match file_name.",
                            action='store_true')
        parser.add_argument('--multiprocessing', type=int, metavar='',
                            help="The number of processes used to create files.",
                            default=_multiprocessing)
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


def clear_existing_files(file_name, destination_folder) -> bool:
    logging.info("Removing/clearing an existing file/s has STARTED.")
    for f in glob.glob(destination_folder + '/' + file_name + '*'):
        os.remove(f)
    logging.info("Removing/clearing an existing file/s FINISHED.")
    return True


class Output:
    def __init__(self, output_dict):
        self.output_dict = output_dict

    def colsole_display(self):
        pprint.pprint(self.output_dict)

    def dump_to_file(self, filename: str) -> bool:
        time.sleep(0.1)
        with open(filename, 'w') as f:
            f.write(json.dumps(self.output_dict))
        return True

    def write_to_file(self, file_name, file_prefix, files_count, _multiprocessing, path_to_save_files,
                      clear_path) -> bool:
        logging.info("Writing an output to a file has STARTED.")

        destination_folder = destination_path(path_to_save_files)
        if clear_path:
            clear_existing_files(file_name, destination_folder)
        output_filenames = get_output_filenames(os.path.join(destination_folder, file_name), file_prefix, files_count)

        self.multiprocess_writing_to_file(_multiprocessing, output_filenames)
        self.sequencial_writing_to_file(output_filenames)

        logging.info("Writing an output to a file FINISHED.")

    def sequencial_writing_to_file(self, output_filenames):
        st2 = time.time()
        for filename in output_filenames:
            self.dump_to_file(filename)
        end2 = time.time()
        logging.info(f"Finished in {end2 - st2} seconds")
        return True

    def multiprocess_writing_to_file(self, _multiprocessing, output_filenames):
        if _multiprocessing < 0:
            logging.error("Invalid multiprocessor count. count must be greater than 0")
            exit(1)

        if _multiprocessing > os.cpu_count():
            _multiprocessing = os.cpu_count()

        st2 = time.time()

        # Multiprocessing
        # files_count = args.files_count
        # chunk_size = files_count // _multiprocessing
        # slices = list(chunks(output_filenames, chunk_size))
        with multiprocessing.Pool(processes=_multiprocessing) as pool:
            pool.map(self.dump_to_file, output_filenames)

        end2 = time.time()
        logging.info(f"Finished in {end2 - st2} seconds")
        return True


def generating_test_data(key: str, value: str):
    rand_generator = Rand()
    _output = ""
    value_splited = value.split(':')
    if len(value_splited) == 2:
        _type, _value = value_splited[0], value_splited[1]
        if _type in ('timestamp', 'str', 'int'):
            if len(_value.strip()) == 0 or _type == 'timestamp':
                _output = rand_generator.empty_value(_type, _value)
            elif _value == 'rand':
                _output = rand_generator.rand_value(_type)
            elif "rand(" in _value and _type == 'int':
                rand_range_values = _value.strip().replace('rand(', '').replace(')', '').split(',')
                if len(rand_range_values) == 2 and rand_range_values[0].strip().isdigit() \
                        and rand_range_values[1].strip().isdigit():
                    _output = rand_generator.rand_within_range(int(rand_range_values[0]), int(rand_range_values[1]))
                else:
                    logging.error(f"The provided data schema has an invalid format. [{_value}]")
                    exit(1)
            elif "[" in _value and "]" in _value:
                choices = ast.literal_eval(_value)
                _output = rand_generator.rand_choice_from_list(choices)
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
        _output = rand_generator.rand_choice_from_list(choices)
    else:
        logging.error(f"Invalid data schema format. [{key}]")
        exit(1)

    return _output


# split a list into evenly sized chunks
def chunks(_list, size):
    for i in range(0, len(_list), size):
        yield _list[i:i + size]


def args_main(argv: Optional[Sequence[str]] = None) -> dict:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', encoding='utf-8', level=logging.INFO)
    #     logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', filename='data/log_file.log',
    #                         encoding='utf-8', level=logging.INFO)

    parserObj = Parser()
    args = parserObj.argument_parser(argv)

    schema_dict = parserObj.schema_deserialization(args.data_schema)

    output_dict = {}
    logging.info("Generating test data has STARTED.")
    for key in schema_dict:
        value = generating_test_data(key, schema_dict[key])
        output_dict[key] = value
    logging.info("Generating test data FINISHED.")

    output = Output(output_dict)
    if args.files_count == 0:
        output.colsole_display()
    elif args.files_count > 0:
        output.write_to_file(args.file_name, args.file_prefix, args.files_count, args.multiprocessing,
                             args.path_to_save_files, args.clear_path)
    else:
        logging.error("Invalid file count. count must be greater than 0")
        exit(1)
    return output_dict


if __name__ == '__main__':
    args_main()
