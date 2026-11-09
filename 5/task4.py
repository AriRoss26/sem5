import os
import shutil
import datetime

def make_reserve_arc(source, dest):
    # Убедимся, что целевая папка существует
    if not os.path.exists(dest):
        os.makedirs(dest)
    # Формируем имя файла с текущей датой и временем до секунд
    time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_name = f"backup_{time_str}"
    # Полный путь к будущему архиву (без расширения)
    dest_path = os.path.join(dest, archive_name)
    # Создаем zip-архив из папки source
    shutil.make_archive(dest_path, 'zip', root_dir=source)
    print(f"Архив создан: {dest_path}.zip")

if __name__ == "__main__":
    # Указываем: что архивируем ('./my_folder') и куда сохраняем ('./backups')
    make_reserve_arc('./my_folder', './backups')