import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkinter.filedialog import askopenfilename
from tkinter import *
import subprocess as sp
import csv
from datetime import date, datetime
import time

root = tk.Tk()

###########################################################################################
# Frames declaration
###########################################################################################


frame1 = tk.Frame(master=root, width=150, height=400, bg="green")
frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

frame2 = tk.Frame(master=root, width=400,  height=400, bg="white")
frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

frame3 = tk.Frame(master=root, width=150,  height=400, bg="orange")
frame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)


###########################################################################################
# Radiobuttons creation and rules definition (functions call)
###########################################################################################


weight = IntVar()
height = IntVar()
Label(frame1, text='Weight option?', bg="green").place(x=30, y=150)
r1 = Radiobutton(frame1, text='Stones and Pounds', value=1, command=lambda: weight_disable_r1(), variable=weight, bg="green").place(x=10, y=180)
r2 = Radiobutton(frame1, text='KGs                           ',value=2,  command=lambda: weight_disable_r2(), variable=weight, bg="green").place(x=10, y=200)

Label(frame3, text='Height option?', bg="orange").place(x=30, y=150)
Radiobutton(frame3, text='Feet and Inches', value=1, command=lambda: height_disable_r1(), variable=height, bg="orange").place(x=10, y=180)
Radiobutton(frame3, text='CM                           ',value=2, command=lambda: height_disable_r2(), variable=height, bg="orange").place(x=10, y=200)


###########################################################################################
# Radiobuttons enable/disable functions
###########################################################################################


def weight_disable_r1():
    KGs.config(state='disabled')
    Stones.config(state='normal')
    Pounds.config(state='normal')

def weight_disable_r2():

    KGs.config(state='normal')
    Stones.config(state='disabled')
    Pounds.config(state='disabled')

def height_disable_r1():
    CM.config(state='disabled')
    Feet.config(state='normal')
    Inches.config(state='normal')

def height_disable_r2():

    CM.config(state='normal')
    Feet.config(state='disabled')
    Inches.config(state='disabled')


###########################################################################################
# Conversion functions 
###########################################################################################


centimeters = StringVar()
feet = StringVar()
inches = StringVar()
kilograms = StringVar()
stones = StringVar()
pounds = StringVar()


###########################################################################################
# Conversion functions
###########################################################################################


def master():
    label9.configure(text="0")
    label10.configure(text="-------------")
    error.configure(text="")
    name = name_entry.get()
    if name == '':
        error.configure(text="Inform your name")
    else:
        try:
            height_selected = height.get()
            global height_final_in_meters
            global weight_final
            if (height_selected == 1):
                height_final_in_meters = cm_to_meter(height_imperial_to_metric())
            elif (height_selected == 2):
                height_final_in_meters = cm_to_meter(getint(CM.get()))
                height_metric_to_imperial()
            else:
                raise NameError

            weight_selected = weight.get()
            if (weight_selected == 1):
                weight_final = weight_imperial_to_metric()
            elif (weight_selected == 2):
                weight_final = getdouble(KGs.get())
                weight_metric_to_imperial()
            else:
                raise NameError

            # height_final_in_meters = cm_to_meter(height_final)
            bmi = weight_final / (height_final_in_meters * height_final_in_meters)
            bmi = round(bmi, 2)
            # Date and time
            today_date = date.today()
            data_text = '{}/{}/{}'.format(today_date.day, today_date.month,
                                          today_date.year)
            time_now = time.strftime('%H:%M:%S')

        except ValueError as err:
            error.configure(text="Enter valid values")
            print(err)
        except ZeroDivisionError as err:
            error.configure(text="Zero Division Error")
            print(err)
        except NameError:
            error.configure(text="Select Weight and height options")
        else:
            if bmi < 18.5:
                label9.configure(text=str(bmi))
                label10.configure(text="Underweight")
            elif bmi >= 18.5 and bmi < 25:
                label9.configure(text=str(bmi))
                label10.configure(text="Normal (healthy weight)")

            elif bmi >= 25 and bmi < 30:
                label9.configure(text=str(bmi))
                label10.configure(text="Overweight")

            elif bmi >= 30:
                label9.configure(text=str(bmi))
                label10.configure(text="Obese")
            else:
                pass
            fields = ['Name: ' + name, ' Weight: ' + str(weight_final), ' height: ' + str(height_final_in_meters),
                      ' Date: ' + data_text, ' Hour: ' + time_now]
            with open('python_course.csv', 'a') as python_file:
                writer = csv.writer(python_file, delimiter=',', lineterminator='\n')
                writer.writerow(fields)


def cm_to_meter(cm):
    return float(cm/100)

def weight_imperial_to_metric():
    st = getdouble(Stones.get())
    lb = getdouble(Pounds.get())
    st = st + (lb / 14)
    kg = st * 6.35029318
    kilograms.set(str(kg))
    return round(kg, 2)

def weight_metric_to_imperial():
    kg = getdouble(KGs.get())
    st = int(kg / 6.35029318)
    lb = (kg / 6.35029318) - st
    lb = lb * 14
    stones.set(str(round(st, 2)))
    pounds.set(str(round(lb, 2)))

def height_imperial_to_metric():
    ft = getdouble(Feet.get())
    ih = getdouble(Inches.get())
    cm = (ft * 30.48) + (ih * 2.54)
    centimeters.set(str(round(cm, 2)))
    return round(cm, 2)

def height_metric_to_imperial():
    cm = getint(CM.get())
    tt = cm / 2.54
    ft = int(tt / 12)
    ih = tt - (12 * ft)
    feet.set(str(round(ft, 2)))
    inches.set(str(round(ih, 2)))


###########################################################################################
# Title
###########################################################################################


label1 = Label(frame2, text="Body Mass Index Calculator", font=("Arial", 19), bg="white", fg="green")
label1.place(x=50, y=12)


###########################################################################################
# Weight fields declaration
###########################################################################################


name = Label(frame2, text="Inform your name:", font=("Arial", 11), bg="white")
name.place(x=60, y=75)
name_entry = Entry(frame2, width=20, )
name_entry.place(x=190, y=75)

label2 = Label(frame2, text="Stones:", font=("Arial", 11), bg="white")
label2.place(x=15, y=145)
Stones = Entry(frame2, width=7, state='disabled', textvariable=stones)
Stones.place(x=70, y=145)

label3 = Label(frame2, text="Pounds:", font=("Arial", 11), bg="white")
label3.place(x=120, y=145)
Pounds = Entry(frame2, width=7, state='disabled', textvariable=pounds)
Pounds.place(x=180, y=145)

label4 = Label(frame2, text="      or       KGs", font=("Arial", 11), bg="white")
label4.place(x=220, y=145)
KGs = Entry(frame2, width=7, state='disabled', textvariable=kilograms)
KGs.place(x=320, y=145)


###########################################################################################
# Weight fields declaration
###########################################################################################


label5 = Label(frame2, text="Feet:", font=("Arial", 11), bg="white")
label5.place(x=15, y=195)
Feet = Entry(frame2, width=7, state='disabled', textvariable=feet)
Feet.place(x=70, y=195)

label6 = Label(frame2, text="Inches:", font=("Arial", 11), bg="white")
label6.place(x=120, y=195)
Inches = Entry(frame2, width=7, state='disabled',textvariable=inches)
Inches.place(x=180, y=195)

label7 = Label(frame2, text="      or       CM", font=("Arial", 11), bg="white")
label7.place(x=220, y=195)
CM = Entry(frame2, width=7, state='disabled', textvariable=centimeters)
CM.place(x=320, y=195)

calculate_button = Button(frame2, text="Calculate your BMI now", font=("Arial", 11), command=master, bg="green", fg="white")
calculate_button.place(x=125, y=235)

error = Label(frame2, text=" ", font=("Arial", 11), bg="white", fg="orange")
error.place(x=165, y=275)

label8 = Label(frame2, text="BMI  =", font=("Arial", 11), bg="white")
label8.place(x=100, y=310)

label9 = Label(frame2, text="0", font=("Arial", 11), bg="white")
label9.place(x=150, y=310)

label10 = Label(frame2, text="-------------", font=("Arial", 11), bg="white")
label10.place(x=205, y=310)



def open_file():
    programname = "Notepad.exe"
    filename = "python_course.csv"
    sp.Popen([programname, filename])

csv_button = Button(frame2, text="Open CSV", font=("Arial", 11), bg="green", fg="white", command = lambda:open_file())
csv_button.place(x=165, y=350)

root.mainloop()