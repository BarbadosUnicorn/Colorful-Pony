import unittest, online_determinator, os, configparser, pymysql


def select(column_name, table_name, key_dict):
    key = list(key_dict.keys())[0]
    value = key_dict[key]
    query = """SELECT {COLUMN}
               FROM {TABLE}
               WHERE {KEY} = '{VALUE}' """.format(COLUMN = column_name, TABLE = table_name,\
                                                          KEY = key, VALUE = value)
    online_determinator.cursor.execute(query)
    return online_determinator.cursor.fetchall()[0][0]


def delete(table_name, key_dict):
    key = list(key_dict.keys())[0]
    value = key_dict[key]
    query = """DELETE FROM {TABLE} 
               WHERE {KEY} = '{VALUE}' """.format(TABLE = table_name, KEY = key, VALUE = value)

    online_determinator.cursor.execute(query)
    online_determinator.db.commit()


pony_dict_1 = dict(name='pony_1')
pony_dict_2 = dict(name='pony_2')

class online_determinator_unit_tests(unittest.TestCase):

    # color_retriever_tests

    def test_color_retriever_processing(self):
        self.assertEqual(online_determinator.color_retriever('123456'), {'R': '12', 'G': '34', 'B': '56'})

    def test_color_retriever_exceptions_NULL_color(self):
        self.assertRaises(ValueError, online_determinator.color_retriever, '')

    def test_color_retriever_exceptions_string_instead_of_color(self):
        self.assertRaises(ValueError, online_determinator.color_retriever, 'STRING')

    def test_color_retriever_exceptions_small_color(self):
        self.assertRaises(ValueError, online_determinator.color_retriever, '12345')

    # RGBtoLab_tests

    def test_RGBtoLab_processing(self):
        self.assertEqual(online_determinator.RGBtoLab({'R': '12', 'G': '34', 'B': '56'}),\
                              {'L': 21.04306195157679, 'a': 1.0588301738765626, 'b': -24.104716268225335})

    # config_tests

    def test_get_setting(self):
        self.assertEqual(online_determinator.get_setting("settings.ini", 'Settings', 'URL'), 'http://localhost:5000')

    def test_get_setting_wrong_path(self):
        self.assertEqual(online_determinator.get_setting("settings404.ini", 'Settings', "db_password"), 'DB_password_value')
        os.remove("settings404.ini")

    def test_get_setting_Null_path(self):
        self.assertRaises(FileNotFoundError, online_determinator.get_setting, '', "db_password", "DB_password_value")

    def test_get_setting_wrong_section(self):
        self.assertRaises(configparser.NoSectionError, online_determinator.get_setting, "settings.ini", 'Settings404', 'setting404')

    def test_get_setting_wrong_option(self):
        self.assertRaises(configparser.NoOptionError, online_determinator.get_setting, "settings.ini",  'Settings', "db_password404")

    def test_get_setting_Null_option(self):
        self.assertRaises(TypeError, online_determinator.get_setting, "settings.ini",  'Settings')

    # Insert/replace - _machine's tests

    def test_insert_machine_right_data(self):
        self.assertEqual(online_determinator.insert_machine('pony', pony_dict_1, 'id'), select('id', 'pony', pony_dict_1))
        delete('pony', pony_dict_1)

    def test_insert_machine_wrong_table(self):
        print(ValueError.__class__)
        print(ValueError.__dict__)
        print(FileNotFoundError.__class__)
        print(FileNotFoundError.__dict__)
        print(configparser.NoOptionError.__class__)
        print(configparser.NoOptionError.__dict__)
        print(pymysql.err.ProgrammingError.__class__)
        print(pymysql.err.ProgrammingError.__dict__)
        self.assertRaises(pymysql.err.ProgrammingError, online_determinator.insert_machine('not_pony', pony_dict_1, 'id'))











    def test_replace_machine_right_data(self):
        online_determinator.insert_machine('pony', pony_dict_1, 'id')
        online_determinator.replace_machine('pony', pony_dict_2, pony_dict_1)

        if select('id', 'pony', pony_dict_2) is not None:
            contain = True
        else:
            contain = False

        self.assertEqual(contain, True)
        delete('pony', pony_dict_2)



if __name__ == '__main__':
    unittest.main()
