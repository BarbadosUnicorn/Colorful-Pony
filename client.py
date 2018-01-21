import requests

host = 'http://localhost:5000/api/get_pony_by_color?color={}'

while True:
    try:
        print('Enter color of pony in HEX format with "#" symbol:')
        color = input()
        if color == 'exit': break
        color = str(color).rstrip()
        color = color[len(color)-6:]
        int(color, 16)

        response = requests.get(host.format(color)).json()

        for row in response:
            print('Closest color belong to %s of %s. It`s %s (%s). \n' %(row['body_part'],  row['name'], \
                                                                      row['color_name'], row['color']))
    except Exception as exc:
        print('')
        pass
