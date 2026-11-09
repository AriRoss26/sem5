import schedule
import time
import datetime

def say_ku():
    now = datetime.datetime.now()
    # Преобразуем 24-часовой формат в 12-часовой (от 1 до 12)
    hour = now.hour % 12
    if hour == 0:
        hour = 12
    print("Ку " * hour)
# Запускаем функцию на 00 минутах каждого часа
schedule.every().hour.at(":00").do(say_ku)

if __name__ == "__main__":
    print("Программа запущена. Ожидание ровного часа...")
    while True:
        schedule.run_pending()
        time.sleep(1)