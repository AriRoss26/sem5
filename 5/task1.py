import os

def format_size(size_in_bytes):
    units = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']
    i = 0
    size = float(size_in_bytes)
    # Переход через единицы осуществляется через 1023
    while size > 1023 and i < len(units) - 1:
        size /= 1024.0
        i += 1
    # Округление до целого функцией round
    return f"{round(size)}{units[i]}"

def get_files_sizes():
    current_dir = '.'
    result_lines = []
    for item in os.listdir(current_dir):
        item_path = os.path.join(current_dir, item)
        # Пропускаем каталоги, берем только файлы
        if os.path.isfile(item_path):
            size = os.path.getsize(item_path)
            result_lines.append(f"{item} {format_size(size)}")  
    return "\n".join(result_lines)

if __name__ == "__main__":
    print(get_files_sizes())