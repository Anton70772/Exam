import unittest
from tkinter import Tk, ttk, END
import math


def calc(key, calc_entry):
    if key == '=':
        try:
            expression = calc_entry.get()
            if 'log' in calc_entry.get():
                expression = expression.replace('log', 'math.log')
            result = eval(expression)
            calc_entry.insert(END, '=' + str(result))
            return result
        except ZeroDivisionError:
            calc_entry.insert(END, 'Ошибка! Деление на ноль!')
            return 'Ошибка! Деление на ноль!'
        except ValueError:
            calc_entry.insert(END, 'Ошибка!')
            return 'Ошибка!'
    elif key == '+':
        calc_entry.insert(END, '+')
    elif key == '-':
        calc_entry.insert(END, '-')
    elif key == '*':
        calc_entry.insert(END, '*')
    elif key == '/':
        calc_entry.insert(END, '/')
    elif key == 'C':
        calc_entry.delete(0, END)
    else:
        calc_entry.insert(END, key)


class TestCalculatorFunctions(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.calc_entry = ttk.Entry(self.root, width=33)
        self.calc_entry.grid(row=0, column=0, columnspan=5)

    def tearDown(self):
        self.root.destroy()

    def test_add(self):
        self.calc_entry.insert(END, '1+2')
        result = calc('=', self.calc_entry)
        self.assertEqual(result, 3)

    def test_subtract(self):
        self.calc_entry.insert(END, '10-5')
        result = calc('=', self.calc_entry)
        self.assertEqual(result, 5)

    def test_multiply(self):
        self.calc_entry.insert(END, '3*7')
        result = calc('=', self.calc_entry)
        self.assertEqual(result, 21)

    def test_divide(self):
        self.calc_entry.insert(END, '8/2')
        result = calc('=', self.calc_entry)
        self.assertEqual(result, 4)

        self.calc_entry.delete(0, END)
        self.calc_entry.insert(END, '10/0')
        result = calc('=', self.calc_entry)
        self.assertEqual(result, 'Ошибка! Деление на ноль!')


if __name__ == '__main__':
    unittest.main()
