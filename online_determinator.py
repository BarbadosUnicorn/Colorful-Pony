import pymysql
from flask import Flask, jsonify, request
app = Flask(__name__)


def color_retriever(color_input): # Making R, G and B variables from input string

    rgb = str(color_input)
    R16 = rgb[len(rgb) - 6:len(rgb) - 4]
    G16 = rgb[len(rgb) - 4:len(rgb) - 2]
    B16 = rgb[len(rgb) - 2:]

    color = {'R': R16, 'G': G16, 'B': B16}

    return color


def RGBtoLab(color):    # Converter from RGB to CIE Lab. Reference white used D65/2° standard illuminant

        # RGB to XYZ
        r = int(color['R'], 16) / 255
        g = int(color['G'], 16) / 255
        b = int(color['B'], 16) / 255

        if ( r > 0.04045 ):
            r = ( ( r + 0.055 ) / 1.055 ) ** 2.4
        else:
            r = r / 12.92

        if ( g > 0.04045 ):
            g = ( ( g + 0.055 ) / 1.055 ) ** 2.4
        else:
            g = g / 12.92

        if ( b > 0.04045 ):
            b = ( ( b + 0.055 ) / 1.055 ) ** 2.4
        else:
            b = b / 12.92

        X = r * 41.24 + g * 35.76 + b * 18.05
        Y = r * 21.26 + g * 71.52 + b * 7.22
        Z = r * 1.93 + g * 11.92 + b * 95.05

        # XYZ to CIE Lab
        X = X / 95.047
        Y = Y / 100
        Z = Z / 108.883

        if ( X > 0.008856 ):
            X = X ** ( 1/3 )
        else:
            X = ( 7.787 * X ) + ( 16 / 116 )

        if ( Y > 0.008856 ):
            Y = Y ** ( 1/3 )
        else:
            Y = ( 7.787 * Y ) + ( 16 / 116 )

        if ( Z > 0.008856 ):
            Z = Z ** ( 1/3 )
        else:
            Z = ( 7.787 * Z ) + ( 16 / 116 )

        L = ( 116 * Y ) - 16
        a = 500 * ( X - Y )
        b = 200 * ( Y - Z )
        # Any of L, a and b can be '+' or '-'

        return {'L': L, 'a': a, 'b': b}


@app.route('/api/get_pony_by_color')
def closest_color_online_determinator(): # Function to find closest color in database.

    color_input = request.args.get('color')
    color = color_retriever(color_input)

    try:
        int(str(color_input), 16)

    except:

        message =  {"status":"error","description":"Invalid color code."}
        resp = jsonify(message)
        resp.status_code = 403
        return resp
        pass

    color = RGBtoLab(color)

    db = pymysql.connect(host="127.0.0.1", port=3306, user="root", password="00000000",\
                                                                   database="pony_color_db", charset="utf8")
    cursor = db.cursor()

    query = """SELECT color.id, color.name, pony.name, body_part.name, color.RGB
               FROM pony_color
               INNER JOIN color     ON pony_color.color_id = color.id
               INNER JOIN pony      ON pony_color.pony_id  = pony.id
               INNER JOIN body_part ON pony_color.type_id  = body_part.id
               GROUP BY color.id, pony.id, body_part.id
               ORDER BY MIN((L - {L})*(L - {L})+(a - {a})*(a - {a})+(b - {b})*(b - {b})) LIMIT 1""".format(L = color['L'],\
                                                                                           a = color['a'], b = color['b'])

    cursor.execute(query)
    results = cursor.fetchall()

    db.close()

    response = '[ '

    for row in results:

        #color_id    = row[0]
        color_name  = row[1]
        name        = row[2]
        body_part   = row[3]
        color       = row[4]
        response = response[:-1] + '{"body_part":"%s","color":"%s","name":"%s","color_name":"%s"},' %(body_part,\
                                                                                        color, name, color_name)    # Concating objects to response

    response = response[:-1] + ']'    # JSON response is an array of objects

    return response

# Adress of fun: http://localhost:5000/api/get_pony_by_color?color=053550


'''
 if int(color_input, 16):
        color = color_retriever(color_input)
        color = RGBtoLab(color)
    
    else:
         message =  {"status":"error","description":"Invalid color code."}
        resp = jsonify(message)
        resp.status_code = 403
        return resp
        pass
'''
