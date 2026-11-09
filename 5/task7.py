import argparse

def main():
    parser = argparse.ArgumentParser()
    # nargs='*' позволяет принять от 0 до бесконечности аргументов
    parser.add_argument('args', nargs='*')
    parsed = parser.parse_args()
    if not parsed.args:
        print("no args")
    else:
        for arg in parsed.args:
            print(arg)

if __name__ == "__main__":
    main()