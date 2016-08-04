import requests, time, random, re, pickle
login = "login"
password = "password"
host = 'http://bunker.lunavod.ru/api/'
key_sub = re.compile("LIVESTREET_SECURITY_KEY = '\w*'")
sub = re.compile("\(\(\d*d\d+\)\)|\(\(\d*д\d+\)\)")
sub_dice = re.compile("d|д")

r=requests.post(host + 'login', data={"login": login, "password": password})
print(r.text)

page = requests.get("http://bunker.lunavod.ru/error", cookies=r.cookies).text
key_raw = re.search(key_sub, page).group()
my_key = key_raw[len("LIVESTREET_SECURITY_KEY = '"): -1]

try: # берём максимальный id из файла | taking max id from file
    input = open('dice_max_comm_id.pkl', 'rb')
    max_id = pickle.load(input)
    input.close()
except FileNotFoundError: # нет такого файла? Сделаем! | No such file? Create it!
    output = open('dice_max_comm_id.pkl', 'wb')
    pickle.dump(10, output)
    output.close()
    max_id = 0

while True:
    time.sleep(1)
    try:
        comments = requests.get(host + "comments/stream", cookies=r.cookies).json() #взяли список комментов | Taking comment id list
        if max_id < comments[0]:
            for i in comments: # бегаем по комментам
                if i <= max_id: break
                rep = ''
                cur = requests.get(host + 'comments/stream?id=%s' %i, cookies=r.cookies).json() # тиснули коммент | Taking comment
                cur_com = cur['text'].lower()
                res = re.findall(sub, cur_com) # посчитали количество бросков в комменте | Counting dice throwings
                for d in res:  # обрабатываем броски | Working with throwings
                    cur_d = d[2:-2]
                    sum = 0
                    try:
                        cur_d.index('d')
                        list_d = cur_d.split('d')
                    except ValueError:
                        list_d = cur_d.split('д')
                    if list_d[0] == '':
                        if list_d[1] > 0:
                            rep += '[ '
                            rep += str(random.randrange(int(list_d[1])) + 1) + " ]"
                    else:
                        for i in range(int(list_d[0])):
                            rep += '[ '
                            ra = random.randrange(int(list_d[1])) + 1
                            rep += str(ra) + " "
                            sum += ra
                        rep += "] = " + str(sum)
                    if len(res) > 1:
                        rep += "\n"
                if len(res) > 6: # если больше шести бросков - прячем | Hiding more than 6 throwings
                    reply = '<span class="spoiler"><span class="spoiler-title spoiler-close">Спойлер'\
                            +'</span><span class="spoiler-body">' + rep + '</span></span>'
                elif len(rep) > 76: # если длинна броска больше 76 символов - прячем | Hiding more than 76 symbols
                    reply = '<span class="spoiler"><span class="spoiler-title spoiler-close">Спойлер'\
                            +'</span><span class="spoiler-body">' + rep + '</span></span>'
                else: reply = rep
                # создали текст коммента | Creating comment text
                if len(reply) > 65000:
                    reply = """Вы кинули слишком много дайсов. Они не уместились в коммент.\nYou had htrown too much dice. They can`t fit in one comment."""
                    print(requests.post("http://bunker.lunavod.ru/blog/ajaxaddcomment/", data={'comment_text': reply,
                                                                                           'reply': cur['id'],
                                                                                           'cmt_target_id': cur['targetId'],
                                                                                           'security_ls_key': my_key},
                                                                                            cookies=r.cookies).content)
                elif len(reply) > 3:
                    print(reply)
                    print(requests.post("http://bunker.lunavod.ru/blog/ajaxaddcomment/", data={'comment_text': reply,
                                                                                           'reply': cur['id'],
                                                                                           'cmt_target_id': cur['targetId'],
                                                                                           'security_ls_key': my_key},
                                                                                            cookies=r.cookies).content)
        max_id = comments[0]
        output = open('dice_max_comm_id.pkl', 'wb') # запишем | Open file
        pickle.dump(max_id, output)     # максимальный id | Write max id in file
        output.close()                  # на всякий случай))) | Close file for extra safety)))
    except Exception as exc:
        print(exc)
        try:
            page = requests.get("http://bunker.lunavod.ru/error", cookies=r.cookies).text
            if page.find(my_key) > 0: # проверяем залогинен ли бот. Если security_ls_key == my_key - залогинен | Check if bot logged in (security_ls_key == my_key means logged)
                pass
            else: # если не залогинен - перелогиниваемся | Not logged - logging in
                r=requests.post(host + 'login', data={"login": login, "password": password})
                page = requests.get("http://bunker.lunavod.ru/error", cookies=r.cookies).text
                key_raw = re.search(key_sub, page).group()
                my_key = key_raw[len("LIVESTREET_SECURITY_KEY = '"): -1]
        except Exception as exc:
            print(exc)
            pass # если вдруг не получится залогиниться или спарсить страницу - попробуем начать сначала. | If failed - trying log in again


print(requests.get(host + 'exit', cookies=r.cookies).text)
