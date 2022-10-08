
from datetime import datetime
from multiprocessing import Array, Process, Value
import tkinter as tk
from tkinter.ttk import *


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title(' .. Fibonacci .. ')
        self.geometry("850x200")

        self.inputField_var = tk.StringVar()
        self.inputField_var.trace('w', self.change)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.create_widgets()

    def create_widgets(self):

        padding = {'padx': 5, 'pady': 5}
        # Main label
        tk.Label(self, text='Enter a number to start:',font=("Arial Bold",12)).grid(column=0, row=0, **padding)

        # Entry
        inputField = tk.Entry(self, textvariable=self.inputField_var)
        inputField.grid(column=1, row=0, **padding)
        inputField.focus()

        # Output label
        self.output_label = tk.Label(self, font=("Arial Bold",12))
        self.output_label.grid(column=0, row=1, columnspan=3, **padding)

        # Output reeks
        self.output_reeks = tk.Label(self, font=("Arial Bold",10))
        self.output_reeks.grid(column=0, row=2, columnspan=3, **padding)

        # Debug Output
        self.debug_label = tk.Label(self, font=("Arial Bold",9))
        self.debug_label.grid(column=0, row=4, columnspan=3, **padding)
        

    def change(self, *args):
        START_TIME = datetime.now().microsecond
        input = self.validateInput(self.inputField_var.get())

        #c_ulonglong has a limit of 18446744073709551615, 99194853094755497 returns as 10th number 12200160415121800000: bigest number i can store in a shared memory of integers.
        try:
            if input > 99194853094755497:
                input = 99194853094755497
                self.output_label['text'] = 'c_ulonglong limit has been reached'
        except:
            pass

        # empty (invalid) input, or same input as before returns emmediately
        if( input == "" or input_value.value == input): #or int(input_value[0]) == input
            END_TIME = datetime.now().microsecond
            self.debug_label['text']= "Response was given in " + str(END_TIME-START_TIME) + ' Microseconds'
            return
        
        readyFlag.value = 0

        #setting this value triggers the response process-thread
        input_value.value = input

        ##waiting for ready flag
        while readyFlag.value == 0:
            pass
       
        self.output_reeks['text'] = response_reeks[:]

        END_TIME = datetime.now().microsecond
        self.debug_label['text']= "Response was given in " + str(END_TIME-START_TIME) + ' Microseconds'

    def validateInput(self, input):
        try:
            input_int = int(round(float(input)))
            self.output_label['text'] = "Input: " + str(input_int)
            return input_int
        except:
            self.output_label['text'] = "Error: enter a valid number!"
        return ""

class Fibonacci():

    def calculate_reeks(fibonacci_reeks,fibonacci_inbetween_reeks):
        fibonacci_reeks[0]= 0
        fibonacci_reeks[1]= 1
        fibonacci_inbetween_reeks[0] = 0
        i = 2
        while True:
            previousNumber1 = fibonacci_reeks[i-2]
            previousNumber2 = fibonacci_reeks[i-1]
            nextNumber = previousNumber1 + previousNumber2

            #when all positions in the fibonacci_reeks array have been filled, stop this process.
            try:
                fibonacci_reeks[i]= nextNumber
            except:
                print(i, 'numbers have been calculated')
                break

            #calculating inbetween numbers for faster index localisation
            inbetweenNumber = previousNumber2 + ((nextNumber - previousNumber2)/2)
            fibonacci_inbetween_reeks[i-1] = inbetweenNumber 
            i +=1

    def predict_reeks(predicted_reeks_Up, Start_Predict_Flag, input_value, fibonacci_inbetween_reeks, fibonacci_reeks,
        predicted_inbetween_Up, predicted_reeks_Down, predicted_inbetween_Down):

        while True:

            #waiting for starting flag from the response process
            while Start_Predict_Flag.value == 0 :
                pass

            current_input = input_value.value
            next_input_up = current_input * 10
            next_input_down = current_input / 10
            
            if next_input_up <= 99194853094755497:

                # Predict UP
                for i in range(len(fibonacci_inbetween_reeks)):
                    if fibonacci_inbetween_reeks[i] >= next_input_up:
                        try:
                            predicted_reeks_Up[:] = fibonacci_reeks[i:i+14]
                            predicted_inbetween_Up[:] = fibonacci_inbetween_reeks[i:i+14]
                        except:
                            pass
                        break
            
            # Predict DOWN
            for i in range(len(fibonacci_inbetween_reeks)):
                if fibonacci_inbetween_reeks[i] >= next_input_down:
                    try:
                        predicted_reeks_Down[:] = fibonacci_reeks[i:i+14]
                        predicted_inbetween_Down[:] = fibonacci_inbetween_reeks[i:i+14]
                    except:
                        pass
                    break

            Start_Predict_Flag.value = 0

    def get_response_reeks(input_value, response_reeks, fibonacci_inbetween_reeks, fibonacci_reeks, readyFlag, Start_Predict_Flag, 
        predicted_reeks_Up, predicted_inbetween_Up,predicted_reeks_Down, predicted_inbetween_Down):
        value = 0
        while True:
            #waiting for input value to change   
            while input_value.value == value:
                pass
          
            input_value_lock = input_value.value

            #using the predicted arrays if possible (if len of input changes 1 or -1, I can use them)
            match (len(str(input_value_lock)) - len(str(value))):
                case 1:
                    for i in range(len(predicted_inbetween_Up)):
                        if predicted_inbetween_Up[i] >= input_value_lock:
                            try:
                                response_reeks[:] = predicted_reeks_Up[i+1:i+11]
                            except:
                                    pass
                            readyFlag.value = 1
                            break

                case -1:
                    for i in range(len(predicted_inbetween_Down)):
                        if predicted_inbetween_Down[i] >= input_value_lock:
                            try:
                                response_reeks[:] = predicted_reeks_Down[i+1:i+11]
                            except:
                                pass
                            readyFlag.value = 1
                            break

                case _:
                    for i in range(len(fibonacci_inbetween_reeks)):
                        if fibonacci_inbetween_reeks[i] >= input_value_lock:
                            try:
                                response_reeks[:] = fibonacci_reeks[i+1:i+11]
                            except:
                                pass
                            readyFlag.value = 1
                            break
                
            value = input_value_lock
            Start_Predict_Flag.value = 1

    
if __name__ == '__main__':

    # Initiating my global variables to be used through the processes  

    # SMALL numbers  
    fibonacci_reeks = Array('Q', 94)
    fibonacci_inbetween_reeks = Array('d', 94)

    predicted_reeks_Up = Array('Q', 14)
    predicted_inbetween_Up = Array('d', 14)
    predicted_reeks_Down = Array('Q', 14)
    predicted_inbetween_Down = Array('d', 14)

    response_reeks = Array('Q', 10)
    input_value =  Value('Q',0)

    readyFlag = Value('i',0) # 0=False 1=True
    Start_Predict_Flag = Value('i',0) # 0=False 1=True


    #running workers in different processes
    t1 = Process(target=Fibonacci.calculate_reeks, args=(fibonacci_reeks,fibonacci_inbetween_reeks))
    t1.start()
    t2 = Process(target=Fibonacci.get_response_reeks, args=(input_value, response_reeks,fibonacci_inbetween_reeks,fibonacci_reeks,readyFlag,Start_Predict_Flag, predicted_reeks_Up, 
        predicted_inbetween_Up,predicted_reeks_Down, predicted_inbetween_Down))
    t2.start()
    t3 = Process(target=Fibonacci.predict_reeks, args=(predicted_reeks_Up, Start_Predict_Flag, input_value, fibonacci_inbetween_reeks, fibonacci_reeks, predicted_inbetween_Up,
         predicted_reeks_Down,predicted_inbetween_Down))
    t3.start()

    #starting frontend app
    app = App()
    app.mainloop()
    
    # CLOSE
    t1.terminate()
    t2.terminate()
    t3.terminate()
