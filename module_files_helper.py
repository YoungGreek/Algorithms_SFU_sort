SUPPORTED_FORMATS = ('.csv', '.txt')


def check_format(file_format) -> str:
    """
    Проверяет формат файла.

    Args:
        file_format: формат файла (расширение имени файла)

    Returns:
        Строка 'csv' или 'txt'.

    Raises:
        ValueError: если формат файла не поддерживается.
    """

    extension = file_format

    if file_format[0] != ".":
        extension = "." + file_format

    if extension not in SUPPORTED_FORMATS:

        raise ValueError(
            f'Неподдерживаемый формат файла {file_path}: '
            f'ожидается один из {", ".join(SUPPORTED_FORMATS)}'
        )

    return extension.lstrip('.')


def parse_value(value: str, type_data: str):
    """
    Преобразует строку в значение нужного типа.

    Args:
        value: строка из файла.
        type_data: 'i' (целые), 'f' (float), 's' (строки).

    Returns:
        Значение соответствующего типа.
    """
    if type_data == 'i':
        return int(value)
    if type_data == 'f':
        return float(value)
    return value


def get_file_data_txt(src: list, type_data: str) -> list:
    """
    Читает построчный txt-файл и возвращает список разобранных значений.

    Args:
        src: список с путём к файлу.
        type_data: тип записей — 'i' (целые), 'f' (float), 's' (строки).

    Returns:
        Список значений заданного типа; для пустого файла — пустой список.
    """
    with open(src[0], 'r', encoding="utf-8") as file:
        lines = file.readlines()

    result = []

    for line in lines:

        stripped = line.strip()
        if not stripped:
            continue

        result.append(parse_value(stripped, type_data))

    return result


def write_result_to_file_txt(result: list, src: list) -> None:
    """
    Записывает элементы построчно в файл, перезаписывая содержимое.

    Args:
        result: список элементов для записи.
        src: список с путём к файлу.
    """
    with open(src[0], 'w', encoding="utf-8") as file:
        for item in result:
            file.write(str(item) + "\n")


def get_file_data_csv(src: list, key: str, type_data: str):
    """
    Читает csv и возвращает данные колонки key вместе со структурой файла.

    Номер колонки n определяется по заголовку: заголовок разбивается по запятой, ищется позиция колонки с именем key.

    Args:
        src: список с путём к файлу.
        key: имя колонки, по которой сортируем.
        type_data: тип значений колонки — 'i', 'f' или 's'.

    Returns:
        Кортеж (data, names, rows): данные колонки, имена колонок, исходные строки.

    Raises:
        ValueError: если колонки key нет в заголовке.
    """
    with open(src[0], 'r', encoding="utf-8") as file:
        lines = file.readlines()

    names = lines[0].strip().split(',')
    if key not in names:
        raise ValueError(f'Колонка {key} не найдена в заголовке файла {src[0]}')

    n = names.index(key)

    data = []
    rows = []
    for line in lines[1:]:

        stripped = line.strip()
        if not stripped:
            continue

        fields = stripped.split(',')

        rows.append(fields)
        data.append(parse_value(fields[n], type_data))

    return data, names, rows


def write_result_to_file_csv(file_path: list, names: list, rows: list) -> None:
    """Записывает csv: заголовок и строки отсортированные по колонке.

    Args:
        file_path: путь к файлу результата.
        names: имена колонок из заголовка.
        rows: строки.
    """
    with open(file_path[0], 'w', encoding="utf-8", newline="") as file:

        file.write(','.join(names) + "\n")

        for fields in rows:
            file.write(','.join(fields) + "\n")
