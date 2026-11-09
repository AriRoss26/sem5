import argparse

def main():
    parser = argparse.ArgumentParser()
    # Флаг сортировки (store_true делает его boolean)
    parser.add_argument('--sort', action='store_true')
    # Остальные аргументы ключ=значение
    parser.add_argument('pairs', nargs='*')
    args = parser.parse_args()
    parsed_pairs = []
    for pair in args.pairs:
        if '=' in pair:
            key, val = pair.split('=', 1)
            parsed_pairs.append((key, val))  
    if args.sort:
        parsed_pairs.sort(key=lambda x: x[0])
    for key, value in parsed_pairs:
        print(f"Key: {key} Value: {value}")

if __name__ == "__main__":
    main()