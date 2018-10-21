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
pony_dict_wrong = dict(second_name='pony_2')
pony_dict_wrong_value = dict(name='pony_3')

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

    # Insert_machine's tests

    def test_insert_machine_right_data(self):
        self.assertEqual(online_determinator.insert_machine('pony', pony_dict_1, 'id'), select('id', 'pony', pony_dict_1))
        delete('pony', pony_dict_1)

    def test_insert_machine_wrong_table(self):
        with self.assertRaises(Exception) as context:
            online_determinator.insert_machine('not_pony', pony_dict_1, 'id')
        self.assertTrue("Table 'pony_color_db.not_pony' doesn't exist" in str(context.exception))

    def test_insert_machine_wrong_column(self):
        with self.assertRaises(Exception) as context:
            online_determinator.insert_machine('pony', pony_dict_wrong, 'id')
        self.assertTrue("Unknown column 'second_name' in 'field list'" in str(context.exception))

    def test_insert_machine_wrong_output_column(self):
        with self.assertRaises(Exception) as context:
            online_determinator.insert_machine('pony', pony_dict_1, 'id_number')
        self.assertTrue("Unknown column 'id_number' in 'field list'" in str(context.exception))
        delete('pony', pony_dict_1)

    # Replace_machine's tests

    def test_replace_machine_right_data(self):
        online_determinator.insert_machine('pony', pony_dict_1, 'id')
        online_determinator.replace_machine('pony', pony_dict_2, pony_dict_1)

        if select('id', 'pony', pony_dict_2) is not None:
            contain = True
        else:
            contain = False

        self.assertEqual(contain, True)
        delete('pony', pony_dict_2)

    def test_replace_machine_wrong_tabe(self):
        online_determinator.insert_machine('pony', pony_dict_1, 'id')
        with self.assertRaises(Exception) as context:
            online_determinator.replace_machine('not_pony', pony_dict_2, pony_dict_1)
        self.assertTrue("Table 'pony_color_db.not_pony' doesn't exist" in str(context.exception))
        delete('pony', pony_dict_1)

    def test_replace_machine_wrong_new_data_column(self):
        online_determinator.insert_machine('pony', pony_dict_1, 'id')
        with self.assertRaises(Exception) as context:
            online_determinator.replace_machine('pony', pony_dict_wrong, pony_dict_1)
        self.assertTrue("Unknown column 'second_name' in 'field list'" in str(context.exception))
        delete('pony', pony_dict_1)

    def test_replace_machine_wrong_key_column(self):
        online_determinator.insert_machine('pony', pony_dict_1, 'id')
        with self.assertRaises(Exception) as context:
            online_determinator.replace_machine('pony', pony_dict_2, pony_dict_wrong)
        self.assertTrue("Unknown column 'second_name' in 'where clause'" in str(context.exception))
        delete('pony', pony_dict_1)

    def test_replace_machine_wrong_key_value(self):
        id = online_determinator.insert_machine('pony', pony_dict_1, 'id')
        online_determinator.replace_machine('pony', pony_dict_2, pony_dict_wrong_value)
        self.assertEqual(id, select('id', 'pony', pony_dict_1 ))
        delete('pony', pony_dict_1)

    # Role_finder's tests

    def test_role_finder_right_data(self):
        print()

if __name__ == '__main__':
    unittest.main()
