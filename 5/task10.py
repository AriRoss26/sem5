import argparse

def format_text_block(frame_height, frame_width, file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            # Читаем весь текст и заменяем переносы строк на пробелы, чтобы сделать сплошной текст
            text = f.read().replace('\n', ' ')
        result = []
        # Нарезаем текст жестко по ширине рамки (посимвольно, как показано в примере в задании)
        for i in range(0, len(text), frame_width):
            result.append(text[i : i + frame_width])
            # Если достигли максимальной высоты, прекращаем нарезку
            if len(result) >= frame_height:
                break   
        return "\n".join(result)
    except Exception as e:
        # В случае ошибки возвращаем текст исключения
        return f"[{type(e).__name__}] {str(e)}"
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--frame-height', type=int, required=True)
    parser.add_argument('--frame-width', type=int, required=True)
    parser.add_argument('filename')
    args = parser.parse_args()
    formatted_result = format_text_block(args.frame_height, args.frame_width, args.filename)
    print(formatted_result)

if __name__ == "__main__":
    main()