from tkinter import Tk, END, messagebox, ttk, W, E, StringVar
import math

def convert_length(value, from_unit, to_unit):
    try:
        value = float(value)
    except ValueError:
        return "Ошибка: невозможно преобразовать в число"

    area_units = {"см²", "м²", "дм²"}
    if from_unit in area_units or to_unit in area_units:
        area_units_dict = {"см²": 1, "м²": 10000, "дм²": 100}
        if from_unit in area_units and to_unit in area_units:
            return value * (area_units_dict[from_unit] / area_units_dict[to_unit])
        else:
            return "Ошибка: невозможно выполнить конвертацию между длиной и площадью"

    length_units_dict = {"см": 1, "м": 100, "дм": 10}
    if from_unit in length_units_dict and to_unit in length_units_dict:
        return value * (length_units_dict[from_unit] / length_units_dict[to_unit])
    else:
        return "Ошибка: невозможно выполнить конвертацию"


def show_convert_dialog():
    convert_window = Tk()
    convert_window.title("Конвертация")
    convert_window.geometry("300x220")

    ttk.Label(convert_window, text="Значение:").grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(convert_window, text="Из:").grid(row=1, column=0, padx=10, pady=10)
    ttk.Label(convert_window, text="В:").grid(row=2, column=0, padx=10, pady=10)

    value_entry = ttk.Entry(convert_window, width=20)
    value_entry.grid(row=0, column=1, padx=10, pady=10)

    from_unit_var = StringVar()
    from_unit_combobox = ttk.Combobox(convert_window, textvariable=from_unit_var, values=["см", "м", "дм", "см²", "м²", "дм²"])
    from_unit_combobox.grid(row=1, column=1, padx=10, pady=10)

    to_unit_var = StringVar()
    to_unit_combobox = ttk.Combobox(convert_window, textvariable=to_unit_var)
    to_unit_combobox.grid(row=2, column=1, padx=10, pady=10)

    def update_to_units(*args):
        from_unit = from_unit_combobox.get()
        if from_unit.endswith("²"):
            to_unit_combobox.config(values=["см²", "м²", "дм²"])
        else:
            to_unit_combobox.config(values=["см", "м", "дм"])

    from_unit_combobox.bind("<<ComboboxSelected>>", update_to_units)

    def perform_conversion():
        try:
            value = value_entry.get().strip()
            from_unit = from_unit_combobox.get()
            to_unit = to_unit_combobox.get()

            valid_units = {"см", "м", "дм", "см²", "м²", "дм²"}
            if from_unit.lower() not in valid_units or to_unit.lower() not in valid_units:
                messagebox.showerror("Ошибка", "Неправильно выбраны единицы измерения.")
                return

            value = float(value)
            if from_unit.endswith("²") and not to_unit.endswith("²"):
                messagebox.showerror("Ошибка", "Нельзя конвертировать площадь в длину.")
                return
            elif not from_unit.endswith("²") and to_unit.endswith("²"):
                messagebox.showerror("Ошибка", "Нельзя конвертировать длину в площадь.")
                return

            result = convert_length(value, from_unit, to_unit)
            calc_entry.delete(0, END)
            calc_entry.insert(END, result)
            convert_window.destroy()
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите числовое значение для конвертации.")

    convert_button = ttk.Button(convert_window, text="Конвертировать", command=perform_conversion)
    convert_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    convert_window.mainloop()

root = Tk()
root.title('Инженерный калькулятор')
root.resizable(width=False, height=False)

btn_list = [
    'cos', 'sin', 'log', 'ln', 'n!',
    'e', 'π', '√', '+', '*',
    '7', '8', '9', '-', '÷',
    '4', '5', '6', 'xⁿ', '%',
    '1', '2', '3', '(', ')',
    '0', '.', '=', 'C', 'Exit',
    'Конвертация'
]

calc_entry = ttk.Entry(root, width=33)
calc_entry.grid(row=0, column=0, columnspan=5, sticky=W + E)

ttk.Style().configure("TButton", padding=(0, 5, 0, 5),
                      font='serif 10')

r = 1
c = 0
for btn in btn_list:
    rel = ''
    cmd = lambda x=btn: calc(x)

    ttk.Button(root, text=btn, command=cmd, width=15).grid(row=r, column=c)
    c += 1
    if c > 4:
        c = 0
        r += 1


def calc(key):
    if key == '=':
        try:
            expression = calc_entry.get()
            if 'log' in calc_entry.get():
                expression = expression.replace('log', 'math.log')
            result = eval(expression)
            calc_entry.insert(END, '=' + str(result))
        except ZeroDivisionError:
            calc_entry.insert(END, 'Ошибка! Деление на ноль!')
            messagebox.showerror('Ошибка', 'Деление на ноль!')
        except ValueError:
            calc_entry.insert(END, 'Ошибка!')
            messagebox.showerror('Ошибка! Проверьте введенные данные.')
    elif key == 'cos':
        calc_entry.insert(END, "=" + str(math.cos(int(calc_entry.get()))))
    elif key == 'sin':
        calc_entry.insert(END, "=" + str(math.sin(int(calc_entry.get()))))
    elif key == 'log':
        calc_entry.insert(END, 'log(a, b)')
    elif key == 'ln':
        calc_entry.insert(END, "=" + str(math.log(int(calc_entry.get()))))
    elif key == 'n!':
        calc_entry.insert(END, "=" + str(math.factorial(int(calc_entry.get()))))
    elif key == 'e':
        calc_entry.insert(END, math.e)
    elif key == 'π':
        calc_entry.insert(END, math.pi)
    elif key == '√':
        calc_entry.insert(END, '=' + str(math.sqrt(int(calc_entry.get()))))
    elif key == '÷':
        if calc_entry.get() == '':
            calc_entry.insert(END, 'Ошибка! Нельзя делить на пустое значение!')
            messagebox.showerror('Ошибка', 'Нельзя делить на пустое значение!')
        else:
            calc_entry.insert(END, '/')
    elif key == 'xⁿ':
        calc_entry.insert(END, '**')
    elif key == '(':
        calc_entry.insert(END, '(')
    elif key == ')':
        calc_entry.insert(END, ')')
    elif key == 'C':
        calc_entry.delete(0, END)
    elif key == 'Exit':
        root.after(1, root.destroy)
    elif key == 'Конвертация':
        show_convert_dialog()
    else:
        calc_entry.insert(END, key)

root.mainloop()
