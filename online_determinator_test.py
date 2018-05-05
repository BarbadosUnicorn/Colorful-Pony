# Unit to test how ptogramm can: 1 - proccess 'color' arguments, 2 - convert it to 'Lab'

import unittest, online_determinator

class online_determinator_tests(unittest.TestCase):

    def test_color_retriever(self):
        self

    def test_RGBtoLab(self):
        self

if __name__ == '__main__':
    unittest.main()
# RGBtoLab must be devided in 2 pieses: 1 - function to process RGB color from 'color' input without shunting down server in case of wrong 'color'
# and 2 - color converter itelf. After that tests should be written.
