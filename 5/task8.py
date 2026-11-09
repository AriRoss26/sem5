import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    # Принимаем все позиционные аргументы в виде списка строк
    parser.add_argument('params', nargs='*')
    # Парсинг (ошибки парсера мы обошли за счет nargs='*')
    args = parser.parse_args()
    count = len(args.params)
    if count == 0:
        print("NO PARAMS")
    elif count == 1:
        print("TOO FEW PARAMS")
    elif count > 2:
        print("TOO MANY PARAMS")
    else:
        try:
            # Попытка сложить 2 целых числа
            result = int(args.params[0]) + int(args.params[1])
            print(result)
        except Exception as e:
            # Выводим ИМЯ КЛАССА исключения, как просят в задании
            print(type(e).__name__)

if __name__ == "__main__":
    main()