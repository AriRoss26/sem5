import zipfile
import sys
import os

def format_size(size_in_bytes):
    units = ['Б', 'КБ', 'МБ', 'ГБ']
    i = 0
    size = float(size_in_bytes)
    while size > 1023 and i < len(units) - 1:
        size /= 1024.0
        i += 1
    return f"{round(size)}{units[i]}"

def print_tree(tree_node, indent=""):
    # Сортируем для красивого вывода
    for name, content in sorted(tree_node.items()):
        if isinstance(content, dict):
            # Это папка
            print(f"{indent}{name}")
            print_tree(content, indent + "  ")
        else:
            # Это файл
            print(f"{indent}{name} {format_size(content)}")

def process_archive(archive_path):
    if not os.path.exists(archive_path):
        print(f"Файл {archive_path} не найден.")
        return
    tree = {}
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        if not zip_ref.infolist():
            return # Архив пуст, ничего не выводим
        for file_info in zip_ref.infolist():
            parts = file_info.filename.strip('/').split('/')
            current_level = tree
            # Строим словарь-дерево
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    if not file_info.is_dir():
                        current_level[part] = file_info.file_size
                    else:
                        if part not in current_level:
                            current_level[part] = {}
                else:
                    if part not in current_level:
                        current_level[part] = {}
                    current_level = current_level[part]          
    print_tree(tree)

if __name__ == "__main__":
    # Замените 'example.zip' на имя вашего архива для проверки
    archive = "example.zip" 
    # Раскомментируйте код ниже, чтобы передавать имя архива через консоль:
    # if len(sys.argv) > 1: archive = sys.argv[1]
    process_archive(archive)