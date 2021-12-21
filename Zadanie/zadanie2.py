#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import click
import json
import os
import sys
from dotenv import load_dotenv


@click.group()
def cli():
    pass


@cli.command()
@click.argument('data')
@click.option("-s", "--stay")
@click.option("-v", "--value")
@click.option("-n", "--number")
def adding(data, stay, number, value):
    """
    Добавление нового рейса
    """
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
        flights.append(
            {
                'stay': stay,
                'number': number,
                'value': value
            }
        )
        with open(dotenv_path, "w", encoding="utf-8") as file_out:
            json.dump(flights, file_out, ensure_ascii=False, indent=4)
        click.secho("Рейс добавлен", fg='green')
    else:
        click.secho('Такого файла нет', fg='red')


@cli.command()
@click.argument('filename')
def table(filename):
    flights = opening(filename)
    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 20,
        '-' * 15,
        '-' * 16
    )
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


@cli.command()
@click.argument('filename')
@click.option("-t", "--typing")
def selecting(filename, typing):
    flights = opening(filename)
    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 20,
        '-' * 15,
        '-' * 16
    )
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
        if typing == num.get('value', ''):
            count += 1
            print(
                '| {:<4} | {:<20} | {:<15} | {:<16} |'.format(
                    count,
                    num.get('stay', ''),
                    num.get('number', ''),
                    num.get('value', 0)))
    print(line)


def opening(filename):
    with open(filename, "r", encoding="utf-8") as f_in:
        return json.load(f_in)


def main():
    cli()


if __name__ == '__main__':
    main()
