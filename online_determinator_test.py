import unittest, online_determinator

class online_determinator_tests(unittest.TestCase):

    def test_color_retriever_processing(self):

        self.assertEqual(online_determinator.color_retriever('123456'), {'R': '12', 'G': '34', 'B': '56'})


    def test_color_retriever_exceptions_NULL_color(self):

        self.assertRaises(ValueError, online_determinator.color_retriever, '')


    def test_color_retriever_exceptions_string_instead_of_color(self):

        self.assertRaises(ValueError, online_determinator.color_retriever, 'STRING')


    def test_color_retriever_exceptions_small_color(self):

        self.assertRaises(ValueError, online_determinator.color_retriever, '12345')


    def test_RGBtoLab_processing(self):
        self.assertEqual(online_determinator.RGBtoLab({'R': '12', 'G': '34', 'B': '56'}),\
                              {'L': 21.04306195157679, 'a': 1.0588301738765626, 'b': -24.104716268225335})


if __name__ == '__main__':
    unittest.main()
