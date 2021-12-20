#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import click
import json
import os
import sys
from dotenv import load_dotenv


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


def adding(flights, stay, number, value, file_name):
    flights.append(
        {
            'stay': stay,
            'number': number,
            'value': value
        }
    )
    with open(file_name, "w", encoding="utf-8") as file_out:
        json.dump(flights, file_out, ensure_ascii=False, indent=4)
    return flights


def opening(file_name):
    with open(file_name, "r", encoding="utf-8") as f_in:
        return json.load(f_in)


@click.command()
@click.option("-c", "--command")
@click.option("-d", "--data")
@click.option("-s", "--stay")
@click.option("-v", "--value")
@click.option("-n", "--number")
@click.option("-t", "--typing")
def main(command, data, stay, value, number, typing):
    if os.path.exists(data):
        load_dotenv()
        dotenv_path = os.getenv("WORKERS_DATA")
        if not dotenv_path:
            click.secho('Такого файла нет', fg='red')
            sys.exit(1)
        if os.path.exists(dotenv_path):
            flights = opening(dotenv_path)
        else:
            flights = []
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 20,
            '-' * 15,
            '-' * 16
        )
        if command == 'add':
            adding(flights, stay, number, value, dotenv_path)
            click.secho('Рейс добавлен', fg='green')
        elif command == 'display':
            table(line, flights)
        elif command == 'select':
            selecting(line, flights, typing)
    else:
        click.secho('Такого файла нет', fg='red')


if __name__ == '__main__':
    main()
