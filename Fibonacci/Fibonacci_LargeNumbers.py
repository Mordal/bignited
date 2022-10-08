
from datetime import datetime
from multiprocessing import  Pipe, Process, Value
import time
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
        
        # self.inputField_var.set(0)

    def change(self, *args):
        START_TIME = datetime.now().microsecond
        input = self.validateInput(self.inputField_var.get())

        # empty (invalid) input returns emmediately
        if( input == ""): 
            END_TIME = datetime.now().microsecond
            self.debug_label['text']= "Response was given in " + str(END_TIME-START_TIME) + ' Microseconds'
            return

        Start_Flag.value = 1
        #setting this value triggers the response process-thread
        input_send.send(input)

        self.output_reeks['text'] = output_rec.recv()

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

    def calculate_reeks(fibonacciReeks_send,fibonacciReeks_inbetween_send, Start_Flag):
        fibonacci_reeks = [0,1]
        fibonacci_inbetween_reeks = [0]

        i = 2
        while i < 1000:
            previousNumber1 = fibonacci_reeks[i-2]
            previousNumber2 = fibonacci_reeks[i-1]
            nextNumber = previousNumber1 + previousNumber2

            fibonacci_reeks.append(nextNumber)

            #calculating inbetween numbers for faster index localisation
            inbetweenNumber = previousNumber2 + ((nextNumber - previousNumber2)/2)
            fibonacci_inbetween_reeks.append(inbetweenNumber)
            i +=1

            # Flag to only send fibonacci when requested
            if Start_Flag.value == 1:
                fibonacciReeks_send.send(fibonacci_reeks)
                fibonacciReeks_inbetween_send.send(fibonacci_inbetween_reeks)
                Start_Flag.value = 0

        if not fibonacciReeks_send.poll():
            fibonacciReeks_send.send(fibonacci_reeks)
            fibonacciReeks_inbetween_send.send(fibonacci_inbetween_reeks)


    def predict_reeks(inputPrediction_rec, predictUP_send, predictUP_inbetween_send, 
        predictDOWN_send, predictDOWN_inbetween_send, fibonacciReeks2_rec, fibonacciReeks2_inbetween_rec):
        while True:

            #this waits for a message from the Pipe()
            current_input = inputPrediction_rec.recv()
            fibonacci_reeks = fibonacciReeks2_rec.recv()
            fibonacci_inbetween_reeks = fibonacciReeks2_inbetween_rec.recv()

            next_input_up = current_input * 10
            next_input_down = current_input / 10
            
            # Predict UP
            i=0
            for i in range(len(fibonacci_inbetween_reeks)-14):
                if fibonacci_inbetween_reeks[i] >= next_input_up:
                    predictUP_send.send(fibonacci_reeks[i:i+14])
                    predictUP_inbetween_send.send(fibonacci_inbetween_reeks[i:i+14])
                    break
            if i == len(fibonacci_inbetween_reeks)-15:
                print('sending highest possible')
                predictUP_send.send(fibonacci_reeks[i+4:i+14])
                predictUP_inbetween_send.send(fibonacci_inbetween_reeks[i+4:i+14])

            # Predict DOWN
            for i in range(len(fibonacci_inbetween_reeks)-14):
                if fibonacci_inbetween_reeks[i] >= next_input_down:
                    predictDOWN_send.send(fibonacci_reeks[i:i+14])
                    predictDOWN_inbetween_send.send(fibonacci_inbetween_reeks[i:i+14])
                    break
            if i == len(fibonacci_inbetween_reeks)-15:
                print('sending highest possible')
                predictDOWN_send.send(fibonacci_reeks[i+4:i+14])
                predictDOWN_inbetween_send.send(fibonacci_inbetween_reeks[i+4:i+14])

    def get_response_reeks(fibonacciReeks_rec, fibonacciReeks_inbetween_rec, input_rec, output_send, 
            inputPrediction_send, predictUP_rec, predictUP_inbetween_rec, predictDOWN_rec, predictDOWN_inbetween_rec, 
            fibonacciReeks2_send, fibonacciReeks2_inbetween_send, Predict_Flag):

        fibonacci_reeks = []
        fibonacci_inbetween_reeks = []
        response_reeks = []
        predicted_reeks_Up = []
        predicted_inbetween_Up = []
        predicted_reeks_Down = []
        predicted_inbetween_Down = []
        value = 0
        input_value = 0

        while True:
            if Predict_Flag.value == 1 :
                predicted_reeks_Up = predictUP_rec.recv()
                predicted_inbetween_Up = predictUP_inbetween_rec.recv()
                predicted_reeks_Down = predictDOWN_rec.recv()
                predicted_inbetween_Down = predictDOWN_inbetween_rec.recv()

            # waiting for input
            input_value = input_rec.recv()

            # when the calculation thread has finished, no more data to receive
            if fibonacciReeks_rec.poll() :
                fibonacci_reeks = fibonacciReeks_rec.recv()
                fibonacci_inbetween_reeks = fibonacciReeks_inbetween_rec.recv()
 
            #using the predicted arrays if possible (if len() of input changes 1 or -1, I can use them)
            match (len(str(input_value)) - len(str(value))):
                # case 1:
                #     if len(predicted_inbetween_Up)== 10:
                #         response_reeks = predicted_reeks_Up
                #     else:
                #         for i in range(len(predicted_inbetween_Up)):
                #             if predicted_inbetween_Up[i] >= input_value:
                #                 response_reeks = predicted_reeks_Up[i+1:i+11] 
                #                 break

                # case -1:
                #     if len(predicted_inbetween_Up)== 10:
                #         response_reeks = predicted_reeks_Down
                #     for i in range(len(predicted_inbetween_Down)):
                #         if predicted_inbetween_Down[i] >= input_value:
                #             response_reeks = predicted_reeks_Down[i+1:i+11]
                #             break

                case _:
                    i=0
                    for i in range(len(fibonacci_inbetween_reeks)-10):
                        if fibonacci_inbetween_reeks[i] >= input_value:
                            response_reeks = fibonacci_reeks[i+1:i+11]
                            break
                    if i == len(fibonacci_inbetween_reeks)-11: #when reached the end
                        response_reeks = fibonacci_reeks[i:i+10]

            output_send.send(response_reeks)
            value = input_value
            Predict_Flag.value = 1 #activate prediction

            #sending a GO to the prediction process
            inputPrediction_send.send(input_value)
            fibonacciReeks2_send.send(fibonacci_reeks)
            fibonacciReeks2_inbetween_send.send(fibonacci_inbetween_reeks)
                

if __name__ == '__main__':

    # Initiating my global variables to be used through the processes  
    fibonacciReeks_rec, fibonacciReeks_send = Pipe()
    fibonacciReeks_inbetween_rec, fibonacciReeks_inbetween_send = Pipe(False)
    fibonacciReeks2_rec, fibonacciReeks2_send = Pipe(False)
    fibonacciReeks2_inbetween_rec, fibonacciReeks2_inbetween_send = Pipe(False)
    
    input_rec, input_send = Pipe(False)
    output_rec, output_send = Pipe(False)

    inputPrediction_rec, inputPrediction_send = Pipe(False)
    predictUP_rec, predictUP_send = Pipe(False)
    predictUP_inbetween_rec, predictUP_inbetween_send = Pipe(False)
    predictDOWN_rec, predictDOWN_send = Pipe(False)
    predictDOWN_inbetween_rec, predictDOWN_inbetween_send = Pipe(False)

    #value is a shared memory between de processes, it has limitations unlike the built-in variables of Python
    Start_Flag = Value('i',0) # 0=False 1=True
    Predict_Flag = Value('i',0) # 0=False 1=True

    #running workers in different processes
    t1 = Process(target=Fibonacci.calculate_reeks, args=(fibonacciReeks_send,fibonacciReeks_inbetween_send, Start_Flag))
    t1.start()
    time.sleep(1) #give time to start up this process
    
    t2 = Process(target=Fibonacci.get_response_reeks, args=(fibonacciReeks_rec, fibonacciReeks_inbetween_rec, input_rec, output_send, 
        inputPrediction_send, predictUP_rec, predictUP_inbetween_rec, predictDOWN_rec, predictDOWN_inbetween_rec, 
        fibonacciReeks2_send, fibonacciReeks2_inbetween_send, Predict_Flag))
    t2.start()
    
    t3 = Process(target=Fibonacci.predict_reeks, args=(inputPrediction_rec, predictUP_send, predictUP_inbetween_send, 
        predictDOWN_send, predictDOWN_inbetween_send, fibonacciReeks2_rec, fibonacciReeks2_inbetween_rec ))
    t3.start()
    
    #starting frontend app
    app = App()
    app.mainloop()
    
    # CLOSE
    t1.terminate()
    t2.terminate()
    t3.terminate()

