
import re
import tkinter as tk
from tkinter import PhotoImage
import time
import psutil
import os

start_time = time.perf_counter()
process = psutil.Process(os.getpid())
start_mem = process.memory_info().rss

def calculation(_input):
    operators = ["+", "-", "*", "/", "^", "√", "(", ")", "%", "π"]
    def split_and_identify(_input, operators):
        pattern = '(' + '|'.join(re.escape(item) for item in operators) + ')'
        parts = re.split(pattern, _input)
        return [part.strip() for part in parts if part.strip()]

    def calculate_square_root(S):
        if S < 0:
            raise ValueError("Cannot calculate square root of negative number")
        if S == 0:
            return 0.0
        guess = S / 2.0
        for _ in range(10):
            guess = 0.5 * (guess + S / guess)
        return guess

    input_splited = split_and_identify(_input, operators)


    for i in range(0, len(input_splited), 1):
        if input_splited[i] == "π":
            input_splited[i] = 3.141592653589793

    if input_splited[0] == "+" or input_splited[0] == "-":
        input_splited.insert(0, "0")

    for i in range(0, len(input_splited), 1):
        if input_splited[i] not in operators:
            input_splited[i] = float(input_splited[i])


    i = 0
    while i < len(input_splited)-1:

        if isinstance(input_splited[i], float) and input_splited[i+1] == "(" or isinstance(input_splited[i], float) and input_splited[i+1] == "√":
            input_splited.insert(i + 1, "*")
            i += 1
        elif input_splited[i] == ")" and isinstance(input_splited[i+1], float) or input_splited[i] == ")" and input_splited[i+1] == "(":
            input_splited.insert(i + 1, "*")
            i += 1

        else:
            i += 1
    i = 0
    while i < len(input_splited):
        if input_splited[i] == "(":
            x = i + 1
            depth = 1

            while x < len(input_splited) and depth > 0:
                if input_splited[x] == "(":
                    depth += 1
                elif input_splited[x] == ")":
                    depth -= 1
                if depth > 0:
                    x += 1

            if depth != 0: raise ValueError("Mismatched parentheses")

            inner_content = input_splited[i + 1: x]
            sub_expression_string = "".join(map(str, inner_content))
            sub_result = calculation(sub_expression_string)
            input_splited[i: x + 1] = [sub_result]

        else:
            i += 1


    for k in range(len(input_splited)):
        if input_splited[k] not in operators:
            try:
                input_splited[k] = float(input_splited[k])
            except (ValueError, TypeError):
                raise TypeError(f"Invalid token after recursion: {input_splited[k]} ({type(input_splited[k])})")


    i = 0
    while i < len(input_splited):

        op = input_splited[i]
        if op == "^" :

            sub_num = input_splited[i - 1] ** input_splited[i + 1]
            input_splited[i - 1:i + 2] = [sub_num]

        elif op == "√" :
            val = float(input_splited[i + 1])
            sub_num = calculate_square_root(val)
            input_splited[i:i + 2] = [sub_num]
        else:
            i += 1

    i = 1
    while i < len(input_splited):
        op = input_splited[i]
        if op == "*" :
            sub_num = input_splited[i-1] * input_splited[i+1]
            input_splited[i - 1:i + 2] = [sub_num]

        elif op == "/" :
            sub_num = input_splited[i-1] / input_splited[i+1]
            input_splited[i - 1:i + 2] = [sub_num]

        elif op == "%":
            sub_num = input_splited[i-1] / 100
            input_splited[i - 1:i + 1] = [sub_num]
            i -= 1

        else:
            i += 2


    item_reg = round(input_splited[0], 12)
    for i in range(0, len(input_splited), 1) :
        op = input_splited[i]

        if op == "+":
            number01 = input_splited[i + 1]
            item_reg += number01

        elif op == "-":
            number01 = input_splited[i + 1]
            item_reg -= number01
    return item_reg


#___________________________________________________________________________________________________________________________
#user_input = input("your calculation : ")
#result = calculation(user_input)
#print(result)
#___________________________________________________________________________________________________________________________

root = tk.Tk()
root.geometry("250x420")
root.resizable(0, 0)
root.configure(bg="white")
root.title("Calculator")

root.wm_iconphoto(True, tk.PhotoImage(file="calc_icon.png"))

frame = tk.Frame(root)
frame2 = tk.Frame(root)
frame3 = tk.Frame(root)
frame.configure(background="white")
frame2.configure(background="white")
frame3.configure(background="white")

def calc_output():
    entry_result.config(state="normal")
    entry_result.delete(0, tk.END)
    try:
        operation = entry.get()
        result2 = calculation(operation)
        entry_result.insert(0, str(result2))
    except ZeroDivisionError:
        entry_result.insert(0, "Division by Zero error.")
    except ValueError:
        entry_result.insert(0, "Syntax error.")
    except OverflowError:
        entry_result.insert(0, "Math error.")
    except TypeError:
        entry_result.insert(0, "Syntax error.")
    entry_result.config(state="readonly")

def erase():
    entry.delete(0, 'end')
    entry_result.config(state="normal")
    entry_result.delete(0, 'end')
    entry_result.config(state="readonly")

def erase_result():
    entry_result.config(state="normal")
    entry_result.delete(0, 'end')
    entry_result.config(state="readonly")

def validate_calculator_input(proposed_text):
    if proposed_text == "":
        return True
    pattern = r"^[0-9+\-*/^√().%π]*$"
    return bool(re.match(pattern, proposed_text))


vcmd = (root.register(validate_calculator_input), '%P')


entry_result = tk.Entry(frame2, width=20, font=("Arial", 18), relief="flat", justify="left")
entry_result.config(state="readonly")

label = tk.Label(frame, text="", bg="white")
button = tk.Button(frame3, text="=", width=3, height=1, font=("Arial", 15), relief="solid", bg="#31ce5f", command=lambda: calc_output())
entry = tk.Entry(frame2, width=20, font=("Arial", 15), relief="flat", validate="key", validatecommand=vcmd)


entry_result.bind("<Control-a>", lambda event: entry_result.selection_range(0, tk.END))
entry.bind("<Return>", lambda event: calc_output())
entry.bind("=", lambda event: calc_output())

def add_char(char):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + char)

#sorry for the mess that's my first project

button__ = tk.Button(frame3, text="ER", width=3, height=1, font=("Arial", 15), relief="solid", bg="orange",command=lambda: erase_result())
button__1 = tk.Button(frame3, text="C", width=3, height=1, font=("Arial", 15), relief="solid", bg="orange", command=lambda: erase())
button__2 = tk.Button(frame3, text="(", width=3, height=1, font=("Arial", 15), relief="solid", bg="orange",command=lambda: add_char("("))
button__3 = tk.Button(frame3, text=")", width=3, height=1, font=("Arial", 15), relief="solid", bg="orange",command=lambda: add_char(")"))
button__4 = tk.Button(frame3, text="π", width=3, font=("Arial", 15), relief="solid", bg="#7e7e7f", fg="white",command=lambda: add_char("π"))

button1 = tk.Button(frame3, text="1", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("1"))
button2 = tk.Button(frame3, text="2", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("2"))
button3 = tk.Button(frame3, text="3", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("3"))
button4 = tk.Button(frame3, text="4", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("4"))
button5 = tk.Button(frame3, text="5", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("5"))
button6 = tk.Button(frame3, text="6", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("6"))
button7 = tk.Button(frame3, text="7", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("7"))
button8 = tk.Button(frame3, text="8", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("8"))
button9 = tk.Button(frame3, text="9", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("9"))
button0 = tk.Button(frame3, text="0", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("0"))
button_ = tk.Button(frame3, text="/", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("/"))
button_1 = tk.Button(frame3, text="*", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("*"))
button_2 = tk.Button(frame3, text="-", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("-"))
button_3 = tk.Button(frame3, text="+", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("+"))
button_4 = tk.Button(frame3, text="^", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("^"))
button_5 = tk.Button(frame3, text=".", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("."))
button_6 = tk.Button(frame3, text="%", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("%"))
button_7 = tk.Button(frame3, text="√", width=3, height=1, font=("Arial", 15), relief="solid", bg="white",command=lambda: add_char("√"))

frame.pack(pady=0, padx=10)
frame2.pack(pady=50, padx=0)
frame3.pack(pady=10, padx=0)


button.grid(row=3, column=4, rowspan=2, sticky="nsew")
label.grid(row=0, column=0)
entry.grid(row=0, column=0)

entry_result.grid(row=1, column=0)

button__.grid(row=0, column=0)
button__1.grid(row=0, column=1)
button__2.grid(row=0, column=2)
button__3.grid(row=0, column=3)
button__4.grid(row=0, column=4)

button1.grid(row=3, column=0)
button2.grid(row=3, column=1)
button3.grid(row=3, column=2)
button4.grid(row=2, column=0)
button5.grid(row=2, column=1)
button6.grid(row=2, column=2)
button7.grid(row=1, column=0)
button8.grid(row=1, column=1)
button9.grid(row=1, column=2)
button0.grid(row=4, column=0)
button_.grid(row=1, column=3)
button_1.grid(row=2, column=3)
button_2.grid(row=3, column=3)
button_3.grid(row=4, column=3)
button_4.grid(row=1, column=4)
button_5.grid(row=4, column=1)
button_6.grid(row=4, column=2)
button_7.grid(row=2, column=4)


entry.focus_set()
root.mainloop()

end_time = time.perf_counter()
execution_time = end_time - start_time
end_mem = process.memory_info().rss

print(f"Execution Time: {execution_time:.4f} seconds")
print(f"Memory Consumed: {(end_mem - start_mem) / (1024 * 1024):.2f} MB")