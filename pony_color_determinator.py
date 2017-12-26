import csv

def pony_color_determinator(file_obj):    # Чтение csv через csv.DictReader

    reader = csv.DictReader(file_obj, delimiter=',')    # Превращаем строки в словари
    # Сделали список словарей reader. Обращаться к нему откуда либо извне этой функции - безсмысленно. Надо запомнить.

    print('Enter body color of pony in HEX format without "#" symbol:')
    color = input()    # Вводим цвет
    response = 'Didn`t found ponys with this body color'

    for line in reader:
        if line["body_color"] == color:
            response = 'It`s %s!' %line['pony_name']

    print(response)





if __name__ == "__main__":
    with open("C:/Users/Nikita/PycharmProjects/ColorfulPony/pony_color_database.csv") as f_obj:
        pony_color_determinator(f_obj)    # Вызываем функцию

    f_obj.closed
