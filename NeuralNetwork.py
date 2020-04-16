import numpy as np
import math


# There will be one hidden layer in the neural network.


class NeuralNetwork:
    def __init__(self, layers=[1, 1, 1]):
        self.layers = layers

        # output of each neuron
        self.NeuronOutput = [[] for i in range(len(layers))]
        for i in range(len(layers)):
            for j in range(layers[i]):
                self.NeuronOutput[i].append(0)

        # bias of each neuron
        self.NeuronBias = [[] for i in range(len(layers))]
        for i in range(len(layers)):
            for j in range(layers[i]):
                self.NeuronBias[i].append(np.random.uniform(-0.5, 0.5))

        # weights of each neuron
        self.weights = [np.random.uniform(-0.5, 0.5, (layers[i], layers[i + 1])) for i in range(len(layers) - 1)]

    # Activation function for the NN, using sigmoid here
    def activate(self, value):
        return 1 / (1 + math.exp(-value))

    # Get output of the network given input vector
    def feed_forward(self, inputs):
        # input inputs
        self.NeuronOutput[0] = [math.tanh(inputs[i] + self.NeuronBias[0][i]) for i in range(len(self.NeuronOutput[0]))]
        for i in range(len(self.NeuronOutput[1:])):
            for j in range(len(self.NeuronOutput[i + 1])):
                value = 0
                for k in range(len(self.NeuronOutput[i])):
                    value += self.NeuronOutput[i][k] * self.weights[i][k, j]
                self.NeuronOutput[i + 1][j] = math.tanh(value + self.NeuronBias[i + 1][j])
        return self.NeuronOutput[-1]

    # randomly mutate weights and biases according to a given rate
    def mutate(self, rate=0.05):
        for i in range(len(self.NeuronBias)):
            for j in range(len(self.NeuronBias[i])):
                if np.random.rand() < rate:
                    self.NeuronBias[i][j] = np.random.uniform(-0.5, 0.5)
        for i in range(len(self.weights)):
            randomweights = np.random.uniform(-0.5, 0.5, self.weights[i].shape)
            k = np.random.rand(*self.weights[i].shape) < rate
            self.weights[i][k] = randomweights[k]

    # duplicate a given NN
    def duplicate(self):
        Child = NeuralNetwork(self.layers)
        Child.NeuronBias = self.NeuronBias
        Child.weights = self.weights
        return Child

