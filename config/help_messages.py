from config.command import Commands


class HelpMessages:

    help_org = 'Привет! Краткий справочник взаимодействию с бото для организатора.\n' \
               'Принцип взаимодействия с ботом: ввод команды -> ввод необходимой информации по одному сообщению.\n' \
               'Команды:\nБлок организационных вопрос\n' \
               f'{Commands.start_active} - Начнет квест\n{Commands.get_leadboard} - Покажет текущий прогресс\n' \
               f'{Commands.get_members} - Получить участников мероприятия в формате username:team\n\n' \
               f'Блок рассылки\n{Commands.mailing}\n{Commands.team_mailing}\n{Commands.individual_mailing}\n\n' \
               f'Блок команд\n{Commands.add_team}\n{Commands.remove_team}\n{Commands.get_teams}\n\n' \
               f'Блок заданий\n{Commands.add_task}\n{Commands.remove_task}\n{Commands.get_tasks}\n\n' \
               f'Блок станций\n{Commands.add_station}\n{Commands.remove_station}\n{Commands.get_stations}' \
               f'Блок бана\n{Commands.ban_user}\n{Commands.ban_team}\n\n' \
               f'Блок импорта\n{Commands.import_tasks}\n{Commands.import_teams}\n{Commands.import_stations}'


    help_member = 'Привет! Рады видеть тебя на этом мероприятии и в области инфобеза. Надеюсь, тебе понравится!' \
                  '\n\nДоступные команды:' \
                  f'\n{Commands.get_station}\n{Commands.get_task}\n{Commands.push_key}\n{Commands.get_leadboard}' \
                  f'\n{Commands.detach_team}' \
                  f'\n\nЕсли что, команды всегда можно ввести текстом'


    help_new_user = 'Привет! Ты на мероприятии, посвященном CTF от пгути :)' \
                    '\nЧтобы присоединиться к команде, напиши\n' \
                    'Ввести токен команды'

    help_import = 'Правила импорта и создания заданий и станций в целом\n' \
                  'У каждой станции обязано быть задания.\n' \
                  'В начале создается задания, потом создается станция\n' \
                  'Соответственно, сначала необходимо заимпортировать задания, и после этого станции.' \
                  '\nИмпорт происходит из .csv файлов.\n' \
                  'Формат файлов: Файл:столбец1:...:стобецN' \
                  '\nКоманды:НазваниеКоманды\n' \
                  'Задания:НазваниеЗадания:Описание:Ответ\n' \
                  'Станции:НазваниеСтанции:Описание:uuidЗадания\n' \
                  f'uuidЗадание можно получить командой {Commands.get_tasks}\n' \
                  f'(на самом деле, на данный момент я не получила обратной связи по этому моменту, в целом можно' \
                  f'переделать и вводить НазваниеЗадания)'
