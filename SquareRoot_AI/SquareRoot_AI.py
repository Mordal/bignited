
import tensorflow as tf
from keras import layers
from multiprocessing import  Pipe, Process, Value
import numpy
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.ttk import *
from random import randrange
import datetime
import os

# to eliminate warnings when starting TF, the following flag is set
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class App(tk.Tk):
    is_on = False
    def __init__(self):
        super().__init__()
        self.title(' .. Square .. ')
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
        tk.Label(self, text='Enter a number: ',font=("Arial Bold",12)).grid(column=0, row=0, **padding)

        # Entry
        inputField = tk.Entry(self, textvariable=self.inputField_var)
        inputField.grid(column=1, row=0, **padding)
        inputField.focus()

        # Prediction label
        self.prediction_label = tk.Label(self, font=("Arial Bold",10))
        self.prediction_label.grid(column=0, row=1, columnspan=1, **padding)

        # True y label
        self.true_y_label = tk.Label(self, font=("Arial Bold",10))
        self.true_y_label.grid(column=0, row=2, columnspan=1, **padding)

        # Button
        self.button = tk.Button(self, text ="show current model", command = self.plotModel)
        self.button.grid(column=0, row=3, columnspan=1, **padding)

        # Save button
        self.saveButton = tk.Button(self, text="Save this model", command = self.saveModel)
        self.saveButton.grid(column=0, row=4, columnspan=1, **padding)

        # Toggle label
        self.toggle_label = tk.Label(self, font=("Arial Bold",10))
        self.toggle_label.grid(column=2, row=2, **padding)
        self.toggle_label.config(text = "Auto training is Off", fg = "grey")

        # Define Images
        self.on = tk.PhotoImage(file = "C:/repos/bignited/SquareRoot_AI/on.png")
        self.off = tk.PhotoImage(file = "C:/repos/bignited/SquareRoot_AI/off.png")
        
        # Toggle Button
        self.autoTrain_button = Button(self, image = self.off, command = self.switch)
        self.autoTrain_button.grid(column=2, row=3, **padding)

        # Debug Output
        self.debug_label = tk.Label(self, font=("Arial Bold",10))
        self.debug_label.grid(column=0, row=4, columnspan=3, **padding)

    def switch(self):
        # Toggle auto training On and Off   
        if self.is_on:
            self.autoTrain_button.config(image = self.off)
            self.toggle_label.config(text = "Auto training is Off", fg = "grey")
            self.is_on = False
            AutoTrain_Flag.value = 0
        else:
            self.autoTrain_button.config(image = self.on)
            self.toggle_label.config(text = "Auto training is On", fg = "green")
            self.is_on = True
            AutoTrain_Flag.value = 1

    def plotModel(self):
        # Graphic display
        plot_rec.send('Give me plot data please')
        plotting_data = plot_rec.recv()

        x_data_plot = numpy.array(plotting_data['x_data'])
        y_data_plot = numpy.array(plotting_data['predictions'])
        y_real_plot = numpy.array(plotting_data['square'])

        plt.plot(x_data_plot, y_data_plot, label='Prediction')
        plt.plot(x_data_plot, y_real_plot, label='Real square root')
        plt.legend()
        plt.show()

    def saveModel(self):
        saveModel_Flag.value = 1

    def getSquareRoot(self,input):
        input_send.send(input)
        prediction = round(prediction_rec.recv(),5)
        trueValue = round(y_true_rec.recv(),5)
        return prediction, trueValue

    def change(self, *args):
        input = self.validateInput(self.inputField_var.get())
        # empty (invalid) input returns emmediately
        if( input == ""): 
            self.prediction_label['text'] = "Error: enter a valid number!"
            self.true_y_label['text']= ""
            self.debug_label['text'] = ""
            return

        prediction,trueValue = self.getSquareRoot(input)
        
        self.prediction_label['text'] = "Model prediction: " + str(prediction)
        self.true_y_label['text'] = "Real square root: " + str(trueValue)
        self.debug_label['text'] = "Number of calculation iterations needed after prediction: " + str(calculationIterations.value)
    
    def validateInput(self, input):
        try:
            input = float(input)
            return input if input >=0 and input < 100000000 else ""
        except:
            return ""


class TensorFlowModel(Process):
    model = tf.keras.Sequential()
    fileName ='SquareModel'
    x_data = []
    y_data = []
    optimizer = 'adam'
    input_rec = None
    prediction_send = None
    y_true_send = None
    AutoTrain_Flag = None
    calculationIterations = None
    plot_send = None
    saveModel_Flag = None

    def run(self): # RUNNER
        self.initiateModel()
        START_TIME = datetime.datetime.now()

        while True:
            # Keep training the current data sets
            self.trainModel()

            # When receiving input
            if self.input_rec.poll() :
                prediction, y_true = self.predict(self.input_rec.recv())
                self.prediction_send.send(prediction)
                self.y_true_send.send(y_true)

            # When plot-data requested
            if self.plot_send.poll():
                self.plot_send.send(self.getPlotData())

            # When save flag received
            if self.saveModel_Flag.value == 1:
                self.saveModel_Flag.value = 0
                self.saveModel()

            # Auto Training = add a value every 5 seconds
            if self.AutoTrain_Flag.value == 1 and START_TIME+datetime.timedelta(seconds = 5) <  datetime.datetime.now():
                START_TIME = datetime.datetime.now()
                self.autoTrainModel()

    def initiateModel(self):
        # Build a new model
        self.model = tf.keras.Sequential() # Input_shape = 1, meaning I will give an input of 1 value
        self.model.add(layers.Dense(1, input_shape=(1,), activation='linear')) #first layer with density 1 for the single input
        self.model.add(layers.Dense(25, activation='elu')) #playing with the amount of layers and dimensions resulted in this amount
        self.model.add(layers.Dense(50, activation="elu"))      #trying to have a fast and high fitting regression
        self.model.add(layers.Dense(150, activation="elu")) 
        self.model.add(layers.Dense(1, activation='linear')) # Dense layer (output) of 1, meaning i will have 1 value as output
        
        try:
            self.loadModel()
        except:
            print("...No existing model to load")

        # Compile the model
        self.model.compile(optimizer=self.optimizer, loss= self.loss) #adam: after experimenting I concluded this optimizer fits best for fast fitting //adagrad will be used for finetuning
        print("..Building complete")

    def trainModel(self):
        if len(self.x_data) == 0: return #return if no values to train
        batch_size=1000 if len(self.x_data) > 1000 else len(self.x_data) # I will take batch_size = all values in my collection, with max= 1000
        history = self.model.fit(numpy.array(self.x_data),numpy.array(self.y_data), epochs=50, batch_size=batch_size , verbose=1) 
        current_loss_all = history.history['loss']
        current_loss = sum(current_loss_all) / len(current_loss_all)

        #switch between optimizers when specific loss value has been reached
        if current_loss < 1 and self.optimizer == 'adam':
            self.optimizer = 'adagrad'
            print("Optimizer changed to ADAGRAD", current_loss)
        elif current_loss > 1000 and self.optimizer == 'adagrad':
            self.optimizer = 'adam'
            print("Optimizer changed to ADAM", current_loss)

    def predict(self, input):
        prediction = float(self.model.predict(numpy.array([input])))
        real_y = float(self.calculate_Square(input,prediction))

        #add input and real square root to the database (if not yet present)
        if input not in self.x_data:
            self.x_data.append(input)
            self.y_data.append(real_y)
            self.x_data.sort()
            self.y_data.sort()

        return prediction, real_y

    # will pass a random integer (within range) to the model and evaluate the prediction
    def autoTrainModel(self):
        self.predict(randrange(1,100000))
        
    def getPlotData(self):
        self.plot_send.recv() # receive to empty the pipe
        return_x= []
        return_pred= []
        return_square= []

        if len(self.x_data) == 0:   #when no data: plot 200 points in range 1-100.000
            for x in range(1,100000,int(100000/200)):
                prediction, y_true = self.predict(x)
                return_x.append(x)
                return_pred.append(prediction)
                return_square.append(y_true)

        elif len(self.x_data) < 200:   #limit the plotting data to 200 points
            for x in self.x_data:
                prediction, y_true = self.predict(x)
                return_x.append(x)
                return_pred.append(prediction)
                return_square.append(y_true)

        else: #limit the plotting data to 200 points
            for x in range(0,max(self.x_data),int(max(self.x_data)/200)):
                prediction, y_true = self.predict(x)
                return_x.append(x)
                return_pred.append(prediction)
                return_square.append(y_true)

        data = {'x_data': return_x, 'predictions': return_pred, 'square': return_square}
        return data
        
    #this function works with tensors, and also returning a tensor 
    def loss(self, calculated_square, prediction):
        #  mae = mean_squared_error
        loss = tf.keras.losses.mse(calculated_square, prediction)
        # i'm making the loss x100 bigger to punish bigger mistakes harder. this results in faster fitting (MSE does basicly the same (and better))
        return tf.math.multiply(loss,100)
        
    def calculate_Square(self, input, prediction):
        iterations = 0
        while True:
            difference = prediction**2 - input
            if abs(difference) <= 0.00001:
                break
            try: # prediction of 0 handled
                prediction = (prediction + input / prediction) / 2
            except:
                prediction = prediction + input / (prediction + 0.000001) / 2
            iterations +=1
        self.calculationIterations.value = iterations
        return 0 if input == 0 else abs(prediction) #return 0 as real square root when input is 0

    def saveModel(self):
        self.model.save_weights(self.fileName)

    def loadModel(self):
        self.model.load_weights(self.fileName)
        self.optimizer = 'adagrad'
        print("...Existing model LOADED")


if __name__ == '__main__':
    # Value is a shared memory between de processes
    AutoTrain_Flag = Value('i',0) # 0=False 1=True
    calculationIterations = Value('i',0)
    saveModel_Flag = Value('i',0)
    
    # Pipes
    input_rec, input_send = Pipe(False)
    prediction_rec, prediction_send = Pipe(False)
    y_true_rec, y_true_send = Pipe(False)
    plot_rec, plot_send = Pipe(True) # 2-way pipe

    # Setting class + passing values and pipes
    print("Building model...")
    square_class = TensorFlowModel()
    square_class.y_true_send = y_true_send
    square_class.input_rec = input_rec
    square_class.AutoTrain_Flag = AutoTrain_Flag
    square_class.prediction_send = prediction_send
    square_class.calculationIterations = calculationIterations
    square_class.plot_send = plot_send
    square_class.saveModel_Flag = saveModel_Flag
    square_class.start()

    # starting frontend app
    app = App()
    app.mainloop()
    
    # terminate AI when closing the GUI
    square_class.terminate()
