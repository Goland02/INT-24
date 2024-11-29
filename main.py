import pytest
import subprocess
import requests

path = "OptimusMuneris.exe"

def run(path, params):
    # Запускает OptimusMuneris.exe по заданному пути path и с параметрами params
    try:
        process = subprocess.Popen([path] + params, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if stderr:
            print(f"Ошибка при выполнении программы: {stderr}")
            return None

        return stdout.strip()

    except FileNotFoundError:
        print(f"EXE-файл не найден: {path}")
        return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


def test_add():
    # Проверка функции add
    params = ["--add", "6", "2"]
    output = run(path, params)
    assert output == "8", f"Сложение работает неверно, 6+2=8, а не {output}"


def test_divide_by_0():
    # Проверка деления на 0
    params = ["--divide", "1", "0"]
    output = run(path, params)
    assert output == "Incorrect input", f"Отсутствует обработка ошибки деления на 0, ожидался вывод \"Incorrect input\""

def test_minus_0():
    # Проверка обработки числа -0
    params = ["--add", "-0", "2"]
    output = run(path, params)
    assert output == "Incorrect input", f"Программа обрабатывает -0 как 0"


def test_meaning_0():
    # Проверка вывода функции meaning при 0
    params = ["--meaning", "0"]
    output = run(path, params)
    assert output == "42", f"Ожидалось 42, получено {output}"

def test_meaning_100():
    # Проверка вывода функции meaning при 100
    params = ["--meaning", "100"]
    output = run(path, params)
    assert output == "42", f"Ожидалось 42, получено {output}"

def test_help():
    # Проверка работы help с дополнительными аргументами
    params = ["--help", "100"]
    output = run(path, params)
    assert output == "Incorrect command", f"Ожидался вывод \"Incorrect command\""

def test_encrypt_without_key():
    # Проверка шифрования без ключа
    params = ["--encrypt", "100"]
    output = run(path, params)
    assert output == "Please, use your key", f"Ожидался вывод \"Please, use your key\""

def test_decrypt_without_key():
    # Проверка дешифрования без ключа
    params = ["--decrypt", "d197"]
    output = run(path, params)
    assert output == "Please, use your key", f"Ожидался вывод \"Please, use your key\""

def test_weather():
    # Проверка отображения правильной температуры воздуха
    params = ["--weather", "moscow"]
    output = run(path, params)
    response = requests.get(
        "http://api.weatherapi.com/v1/current.json?key=0ac16edc9db7426a9e442714241211&q=moscow&lang=en")

    if response.status_code != 200:
        raise ValueError(f"Ошибка API: {response.status_code}")

    temp = response.json()["current"]["temp_c"]
    assert temp in output, f"Температура воздуха различается, на самом деле {temp}, а вывод программы {output.split()[-1]}"


