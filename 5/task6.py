import sys

def main():
    args = sys.argv[1:]
    should_sort = False
    # Проверяем наличие ключа сортировки
    if '--sort' in args:
        should_sort = True
        args.remove('--sort')  
    pairs = []
    for arg in args:
        if '=' in arg:
            # Разбиваем по первому знаку '='
            key, value = arg.split('=', 1)
            pairs.append((key, value))     
    if should_sort:
        # Сортируем по ключу (первому элементу кортежа)
        pairs.sort(key=lambda x: x[0])  
    for key, value in pairs:
        print(f"Key: {key} Value: {value}")

if __name__ == "__main__":
    main()