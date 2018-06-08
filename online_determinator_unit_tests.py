import unittest, online_determinator, os, configparser


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

if __name__ == '__main__':
    unittest.main()
