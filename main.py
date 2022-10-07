import argparse
import glob
import json
import os
import pprint
import shutil
import uuid
import random
from json import JSONDecodeError
from os import getcwd
from os.path import exists
from typing import Optional, Sequence
import configparser


def rand_generator(_type: type) -> str:
    if _type == int:
        return str(random.randint(0, 10000))
    elif _type == str:
        return str(uuid.uuid4())


def rand_int(_from: int, _to: int) -> str:
    return str(random.randint(_from, _to))


def rand_from_list(_input: list) -> list:
    return random.choice(_input)


def default():
    # print(rand_generator(str))
    # print(rand_generator(int))
    print(rand_from_list(['client', 'partner', 'government']))
    print(rand_from_list([0, 9, 10, 4]))
    # instantiate
    config = configparser.ConfigParser()

    # parse existing file
    config.read('default.ini')
    # print(config['DEFAULT']['path'])  # -> "/path/name/"

    # read values from a section
    string_val = config.get('section_a', 'string_val')
    bool_val = config.getboolean('section_a', 'bool_val')
    int_val = config.getint('section_a', 'int_val')
    float_val = config.getfloat('section_a', 'pi_val')

    # update existing value
    config.set('section_a', 'string_val', 'world')

    # add a new section and some values
    config.add_section('section_b')
    config.set('section_b', 'meal_val', 'spam')
    config.set('section_b', 'not_found_val', '404')

    # save to a file
    with open('test_update.ini', 'w') as configfile:
        config.write(configfile)


def schema_loader(data_schema):
    # load JSON schema
    try:
        is_schema_from_file = exists(data_schema)
        if is_schema_from_file:
            with open(data_schema, 'r') as f:
                data_schema = json.load(f)
        else:
            data_schema = json.loads(data_schema)
    except JSONDecodeError:
        print("json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 95 (char 94)")
    except:
        print("Exception")
    finally:
        print("---" * 50)
        # pprint.pprint(data_schema)


def argument_parser(argv):
    parser = argparse.ArgumentParser(
        description="Imagine that you have a data pipeline and you need some test data to check "
                    "correctness of data transformations and validations on this data pipeline. "
                    "You need to generate different input data. "
                    "  Format - only JSON.")

    parser.add_argument('path_to_save_files', type=str, help="Enter the path where all files need to save")
    parser.add_argument('--files_count', type=int, help="Enter the number of json files to generate")
    parser.add_argument('--file_name', type=str, help="Enter base file_name")
    parser.add_argument('--file_prefix', type=str, help="Enter the prefix for file name to use if more than 1 file "
                                                        "needs to be generated")
    parser.add_argument('--data_schema', type=str, help="Enter the json input schema")

    parser.add_argument('--data_lines', type=int, help="Enter number of lines for each file.", default=1000)
    parser.add_argument('--clear_path', help="Flag to delete all existing files that match file_name.",
                        action='store_true')
    parser.add_argument('--multiprocessing', type=int, metavar='', help="Enter the number of processes used to create "
                                                                        "files.", default=1)
    # parser.add_argument('-o', '--operation', type=str, metavar='', help="Operation", default="add",
    #                     choices=['add', 'subtract', 'multiply', 'division'])
    # parser.add_argument('-c', '--count', action='count', help='Count')
    # parser.add_argument('--log', action='append', help='Appended logs')
    # # sub-commands
    # subparsers = parser.add_subparsers(dest='command')
    # subparsers.required = True
    #
    # status_parser = subparsers.add_parser('status', help='show status')
    # status_parser.add_argument('--force', action='store_true')
    #
    # checkout_parser = subparsers.add_parser('checkout', help='show checkout')
    # checkout_parser.add_argument('--force', action='store_true')
    #
    # group = parser.add_mutually_exclusive_group()
    # group.add_argument('-q', '--quite', action='store_true', help='Print quite')
    # group.add_argument('-v', '--verbose', action='store_true', help='Print verbose')
    args = parser.parse_args(argv)
    # pprint.pprint(vars(args))

    return args


def destination_path(path_to_save_files: str) -> str:
    check_folder = os.path.isdir(path_to_save_files)
    print(check_folder)
    # If folder doesn't exist, then create it.
    if not check_folder:
        check_file = os.path.isfile(path_to_save_files)
        if check_file:
            print("ERROR: ")
            exit()
        os.makedirs(path_to_save_files)

    if path_to_save_files == '.':
        return getcwd()
    return path_to_save_files


def get_output_filenames(file_name: str, prefix: str, files_count: int):
    prefixes = []
    for count in range(0, files_count):
        if prefix == 'count':
            output_file = file_name + '-' + str(count) + '.json'
        elif prefix == 'random':
            output_file = file_name + '-' + str(random.randint(0, 10000)) + '.json'
        elif prefix == 'uuid':
            output_file = file_name + '-' + str(uuid.uuid4()) + '.json'
        prefixes.append(output_file)
        with open(output_file, 'w') as f:
            f.close()
    print(prefixes)
    return prefixes


def clear_path(args, destination_folder):
    if args.clear_path:
        for f in glob.glob(destination_folder + '/' + args.file_name + '*'):
            os.remove(f)
        pass


def colsole_display():
    pass


def write_to_file():
    pass


def main(argv: Optional[Sequence[str]] = None) -> int:
    # default()
    args = argument_parser(argv)
    destination_folder = destination_path(args.path_to_save_files)
    clear_path(args, destination_folder)

    if args.files_count == 0:
        colsole_display()
    elif args.files_count > 0:
        write_to_file()
    else:
        print("ERROR: ")
        exit()
        
    schema_loader(args.data_schema)
    get_output_filenames(args.file_name, args.file_prefix, args.files_count)
    # if args.operation == 'add':
    #     print('Sum=' + str(args.number1 + args.number2))
    # elif args.operation == 'subtract':
    #     print('Difference=' + str(args.number1 - args.number2))
    # elif args.operation == 'multiply':
    #     print('Product=' + str(args.number1 * args.number2))
    # else:
    #     print("unknown operation")


if __name__ == '__main__':
    exit(main())
