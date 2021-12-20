#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import json
import os
import sys


def selecting(line, flights, nom):
    """Выбор рейсов по типу самолёта"""
    count = 0
    print(line)
    print(
        '| {:^4} | {:^20} | {:^15} | {:^16} |'.format(
            "№",
            "Место прибытия",
            "Номер самолёта",
            "Тип"))
    print(line)
    for i, num in enumerate(flights, 1):
        if nom == num.get('value', ''):
            count += 1
            print(
                '| {:<4} | {:<20} | {:<15} | {:<16} |'.format(
                    count,
                    num.get('stay', ''),
                    num.get('number', ''),
                    num.get('value', 0)))
    print(line)


def table(line, flights):
    """Вывод скиска рейсов"""
    print(line)
    print(
        '| {:^4} | {:^20} | {:^15} | {:^16} |'.format(
            "№",
            "Место прибытия",
            "Номер самолёта",
            "Тип"))
    print(line)
    for i, num in enumerate(flights, 1):
        print(
            '| {:<4} | {:<20} | {:<15} | {:<16} |'.format(
                i,
                num.get('stay', ''),
                num.get('number', ''),
                num.get('value', 0)
            )
        )
    print(line)


def adding(flights, stay, number, value):
    flights.append(
        {
            'stay': stay,
            'number': number,
            'value': value
        }
    )
    return flights


def saving(file_name, flights):
    with open(file_name, "w", encoding="utf-8") as file_out:
        json.dump(flights, file_out, ensure_ascii=False, indent=4)


def opening(file_name):
    with open(file_name, "r", encoding="utf-8") as f_in:
        return json.load(f_in)


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-d",
        "--data",
        action="store",
        required=False,
        help="The data file name"
    )
    parser = argparse.ArgumentParser("flights")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new worker"
    )
    add.add_argument(
        "-s",
        "--stay",
        action="store",
        required=True,
        help="The place"
    )
    add.add_argument(
        "-v",
        "--value",
        action="store",
        required=True,
        help="The name"
    )
    add.add_argument(
        "-n",
        "--number",
        action="store",
        required=True,
        help="The number"
    )
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all workers"
    )
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the workers"
    )
    select.add_argument(
        "-t",
        "--type",
        action="store",
        required=True,
        help="The required place"
    )
    args = parser.parse_args(command_line)
    data_file = args.data
    if not data_file:
        data_file = os.environ.get("WORKERS_DATA")
    if not data_file:
        print("The data file name is absent", file=sys.stderr)
        sys.exit(1)
    is_dirty = False
    if os.path.exists(data_file):
        flights = opening(data_file)
    else:
        flights = []
    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 20,
        '-' * 15,
        '-' * 16
    )
    if args.command == "add":
        flights = adding(flights, args.stay, args.number, args.value)
        is_dirty = True
    elif args.command == 'display':
        table(line, flights)
    elif args.command == "select":
        selecting(line, flights, args.type)
    if is_dirty:
        saving(data_file, flights)


if __name__ == '__main__':
    main()
