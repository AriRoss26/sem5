import os

def format_size(size_in_bytes):
    units = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']
    i = 0
    size = float(size_in_bytes)
    while size > 1023 and i < len(units) - 1:
        size /= 1024.0
        i += 1
    return f"{round(size)}{units[i]}"

def get_top_10_dirs(target_path):
    dir_sizes = {}
    # topdown=False позволяет считать размер вложенных папок "снизу вверх"
    for root, dirs, files in os.walk(target_path, topdown=False):
        size = sum(os.path.getsize(os.path.join(root, name)) for name in files if os.path.isfile(os.path.join(root, name)))
        # Добавляем размеры уже посчитанных подпапок
        size += sum(dir_sizes[os.path.join(root, d)] for d in dirs if os.path.join(root, d) in dir_sizes)
        dir_sizes[root] = size
    # Сортируем по убыванию размера
    sorted_dirs = sorted(dir_sizes.items(), key=lambda x: x[1], reverse=True)
    # Берем ТОП-10
    for dir_path, dir_size in sorted_dirs[:10]:
        dir_name = os.path.basename(dir_path)
        if not dir_name: # Если это корень диска/папки
            dir_name = dir_path
        # Выравнивание вывода
        print(f"{dir_name:<35} - {format_size(dir_size)}")

if __name__ == "__main__":
    # Для проверки укажите путь к папке (например, текущую папку '.')
    get_top_10_dirs('.')