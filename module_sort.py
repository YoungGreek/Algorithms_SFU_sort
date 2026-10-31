from module_files_helper import *

N_SEQUENCES = 3   # Всего последовательностей: f1, f2 — входные, f3 — выходная
N_INPUTS = N_SEQUENCES - 1


def polyphase_sort(src: list, output: str, reverse: bool, key: str, type_data: str) -> None:
    """
    Функция - диспетчер, принимает данные из файла, передает в обработку, передает на вывод.

    Args:
        src: список с путём к исходному файлу.
        output: строка с путём к файлу результата.
        reverse: False — по неубыванию, True — по невозрастанию.
        key: имя колонки для csv (игнорируется для txt).
        type_data: тип записей — 'i', 'f' или 's'.

    Raises:
        ValueError: если формат файла не поддерживается или колонка
            key не найдена в заголовке csv.
    """

    file_format = get_format(src[0])

    names, rows, n = None, None, None
    if file_format == 'txt':
        data = get_file_data_txt(src, type_data)
    else:
        data, names, rows = get_file_data_csv(src, key, type_data)
        data = [(value, idx) for idx, value in enumerate(data)]

    result = []

    if len(data) > 0:

        inputs, a, d, level = distribute(data, reverse)

        while level > 0:
            inputs, a, d = merge_pass(inputs, a, d, reverse)
            level -= 1

        result = inputs[0][0]

    if output == "":
        output_file = src
    else:
        output_file = [output]

    if file_format == 'txt':
        write_result_to_file_txt(result, output_file)
    else:
        sorted_rows = [rows[idx] for _, idx in result]
        write_result_to_file_csv(output_file, names, sorted_rows)


def distribute(sequence: list, reverse: bool = False):
    """
    Распределяет серии по входным последовательностям..

    Args:
        sequence: исходная последовательность элементов.
        reverse: направление сортировки.

    Returns:
        Кортеж (inputs, a, d, level).
    """
    series = split_series(sequence, reverse)  # Массив серий из исходной последовательности
    inputs = [[] for _ in range(N_INPUTS)]  # Начальное заполнение последовательностей

    a = [1] * N_INPUTS + [0]  # Идеальное число серий в i-ой последовательности
    d = [1] * N_INPUTS + [0]  # Число пустых серий в i-ой последовательности

    level = 1
    for one_series in series:
        j, level = select(a, d, level)
        inputs[j].append(one_series)

    return inputs, a, d, level


def in_order(prev_item, cur_item, reverse: bool = False) -> bool:
    """
    Проверяет, упорядочены ли два элемента в заданном направлении.

    Args:
        prev_item: предыдущий элемент серии.
        cur_item: текущий элемент.
        reverse: направление сортировки.

    Returns:
        True, если серия продолжается, иначе False.
    """
    if reverse:
        return prev_item >= cur_item
    return prev_item <= cur_item


def split_series(items: list, reverse: bool = False) -> list:
    """
    Разбивает последовательность на упорядоченные серии.

    Args:
        items: исходная последовательность элементов.
        reverse: направление сортировки.

    Returns:
        Список серий — списков элементов.
    """
    series = []
    current = []
    for item in items:

        if current and not in_order(current[-1], item, reverse):  # Сравнение с учётом направления
            series.append(current)
            current = []

        current.append(item)

    if current:
        series.append(current)

    return series


def select(a: list, d: list, level: int):
    """
    Выбирает входную последовательность для следующей серии.

    Args:
        a: идеальные числа серий по последовательностям.
        d: числа пустых серий по последовательностям.
        level: текущий уровень чисел Фибоначчи.

    Returns:
        Кортеж (j, level): номер выбранной последовательности и уровень.
    """
    j = 0

    if d[j] < d[j + 1]:
        j += 1

    elif d[j] == 0:

        level += 1  # Уровень исчерпан — вычисляем следующий уровень чисел Фибоначчи

        a0 = a[0]
        for i in range(N_INPUTS):
            d[i] = a0 + a[i + 1] - a[i]
            a[i] = a0 + a[i + 1]

        j = 0

    d[j] -= 1

    return j, level


def merge_series(active, reverse: bool = False) -> list:
    """
    Сливает несколько упорядоченных серий в одну.

    Args:
        active: список сливаемых серий.
        reverse: направление сортировки.

    Returns:
        Одна объединённая серия.
    """
    merged = []
    pos = [0] * len(active)
    while True:
        best = -1
        for idx in range(len(active)):
            if pos[idx] < len(active[idx]):
                if best == -1:
                    best = idx
                else:
                    cur, best_val = active[idx][pos[idx]], active[best][pos[best]]

                    if (cur > best_val) if reverse else (cur < best_val):
                        best = idx

        if best == -1:
            return merged

        merged.append(active[best][pos[best]])
        pos[best] += 1


def merge_pass(inputs, a, d, reverse: bool = False):
    """
    Выполняет один проход слияния и поворачивает роли последовательностей
    (входная с меньшим количество серий становится выходной и т.д.).

    Args:
        inputs: последовательности с сериями.
        a: идеальные числа серий по последовательностям.
        d: числа пустых серий по последовательностям.
        reverse: направление сортировки.

    Returns:
        Кортеж (inputs, a, d) после прохода и смены ролей последовательностей.
    """
    out = []
    min_fib_num = a[N_INPUTS - 1]  # Определяем количество сливаемых серий
    for _ in range(min_fib_num):
        active = []
        for i in range(N_INPUTS):
            if d[i] > 0:
                d[i] -= 1  # Пустая серия пропускается без чтения
            else:
                active.append(inputs[i].pop(0))
        if not active:
            d[N_INPUTS] += 1
        else:
            out.append(merge_series(active, reverse))

    # Поворот карты индексов
    inputs = [out, inputs[0], inputs[1]]
    a = [min_fib_num, a[0] - min_fib_num, a[1] - min_fib_num]
    d = [d[N_INPUTS], d[0], d[1]]

    return inputs, a, d
