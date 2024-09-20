class CSV_task:
    title = 'Задание'
    description = 'Описание'
    key = 'Ключ'


class CSV_team:
    name = 'Команды'


class CSV_station:
    title = 'Станция'
    description = 'Описание'
    key = 'Ключ'



def get_key_pairs(row: str):
    pairs = {}
    for key, value in row.items():
        columns = key.split(';')
        values = value.split(';')
        for column, value in zip(columns, values):
            pairs[column] = value

    return pairs