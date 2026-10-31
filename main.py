import argparse
from module_sort import polyphase_sort


def parse_args() -> argparse.Namespace:
    """
    Разбирает аргументы командной строки.

    Returns:
        Объект Namespace с полями: source, output, reverse, key, type.
    """
    parser = argparse.ArgumentParser(
        description="Многофазная (фибоначчиева) внешняя сортировка txt/csv файлов.")
    parser.add_argument("-s", "--source",
                        help="исходный файл (txt или csv)")
    parser.add_argument("-o", "--output",
                        help="выходной файл")
    parser.add_argument("-r", "--reverse", action="store_true",
                        help="сортировать по невозрастанию")
    parser.add_argument("-k", "--key",
                        help="номер или имя столбца csv для сортировки")
    parser.add_argument("-t", "--type",
                        help="тип данных в файле (i - integer, f - float, s - string)")
    return parser.parse_args()


if __name__ == "__main__":
    """
    Точка входа программы: разбирает аргументы и запускает сортировку.
    """
    args = parse_args()

    file_path = [args.source]
    output_file = args.output
    if output_file is None:
        output_file = ""
    reverse = args.reverse
    key = args.key
    type_data = args.type

    polyphase_sort(file_path, output_file,  reverse, key, type_data)
