#file for storing a clean mutable mlp
import numpy as np
import matplotlib.pyplot as plt

def nonlin(x, derive = False):
    if derive == True:
        return (x *(1 - x))
    else:
        return 1 /(1+(np.exp(-x)))

def SSE(network, actual):
    error = 0
    for i in range(0,len(network),1):
        error += ((actual[i] - network[i])**2)
    bigerror = (np.sum(error))*0.5
    return bigerror

def think(inputs, synapse, noise = False, with_bias = False): #paper did not say they used a bias term
    if with_bias == True:
        bias= -1
    else:
        bias = 0
    if noise == False:
        return nonlin((np.dot(inputs,synapse)+ bias))
    else:
        nois = np.random.uniform(low=-1.0,high=1.0,size=(len(np.dot(inputs,synapse))))
        return nonlin((np.dot(inputs,synapse)+ bias + nois))

def think_astro(inputs, synapse,with_bias=False):
    if with_bias == True:
        bias= -1.0
    else:
        bias = 0.0
    return (np.dot(inputs,synapse)+ bias)

def Flatt(inputlist):
    output_list = []
    for row in inputlist:
            output_list.append(row)
    return output_list

def Error(networkoutput, actual): #actual is 0-9, network is (1,10)

    represent = actual #done this way for easy adjustment
    network_error = actual - networkoutput

    return network_error

input_x = [ [0,0],
            [1,0],
            [0,1],
            [1,1]
]


output_y = [[0,0],[1,1],[1,1],[0,0]]


#network parameters
hidden_layer_count = 1 #needs at least 1 hidden unit
hidden_units = 20 #all hidden layers have the same amount
output_units = len(output_y[0])
total_layer_count = hidden_layer_count + 2
epoch_count = 50
l_rate = 0.1


syn_list = []
syn01 = 2*np.random.random(((len(input_x[0])),hidden_units)) -1
syn_list.append(syn01)

for layer in range(0,hidden_layer_count-1):

    syn_hid = 2*np.random.random((hidden_units,hidden_units)) -1
    syn_list.append(syn_hid)


synoutput = 2* np.random.random((hidden_units,output_units))-1  # 2* -1 to center random values around 0
syn_list.append(synoutput)


print('beginning testing, Epoch = 0/'+str(epoch_count))
SSE_Plot = []
for i in range(epoch_count):
    epoch_error = np.zeros(output_units)
    epoch_error = epoch_error.reshape(1,output_units)
    sse_perepoch = 0


    for train_unit_count in range(0, int(len(input_x))-1):

        current_sse = 0

  
        train_unit = input_x[train_unit_count]
        train_unit = np.asarray(train_unit)
        layer_list = []

        new_unit = Flatt(train_unit)
        new_unit = np.asarray(new_unit)
    

        layer_list.append(new_unit.T)

        for lay in range(1,total_layer_count):
            prev_layer = layer_list[lay-1]
            layer = think(prev_layer,syn_list[lay-1])
            layer_list.append(layer)

        net_error = Error(layer_list[-1],output_y[train_unit_count])

        epoch_error += net_error

        current_sse = SSE(layer_list[-1],output_y[train_unit_count])
        sse_perepoch += current_sse
  
        final_delta = net_error * nonlin(layer_list[-1], derive= True)
        delta_list = []
        delta_list.append(np.asarray(final_delta)) #delta is backwards should be 6 total deltas (for every layer except input)

        ######back prop

        synapse_count = len(syn_list)-1
        
        start_synapse_count = len(syn_list)-1
        while synapse_count > 0:

            incoming_delta = delta_list[start_synapse_count - synapse_count]

            syp_inq = syn_list[synapse_count] 

            new_layer_error = incoming_delta.dot(syp_inq.T)

            next_delta = new_layer_error * nonlin(layer_list[synapse_count],derive= True)

            syn_adj = np.dot(layer_list[synapse_count].reshape(len(layer_list[synapse_count]),1),incoming_delta.reshape(len(incoming_delta),1).T)

            syn_list[synapse_count] += syn_adj * l_rate

            delta_list.append(np.asarray(next_delta))

            synapse_count -= 1

    SSE_Plot.append(sse_perepoch / train_unit_count)
    if i%100 == 0:
        print('current Epoch:',i)
        print('average_sse', sse_perepoch / train_unit_count)

##plotfitness over time
plt.plot(SSE_Plot)
plt.show()

#validation - single trial
trial_num = 0
trial_output = output_y[trial_num]
print('target', trial_output)

#run value back through network
train_unit = input_x[trial_num]
train_unit = np.asarray(train_unit)
layer_list = []

new_unit = Flatt(train_unit)
new_unit = np.asarray(new_unit)


layer_list.append(new_unit.T)

for lay in range(1,total_layer_count):
    prev_layer = layer_list[lay-1]
    layer = think(prev_layer,syn_list[lay-1])
    layer_list.append(layer)

network_output = layer_list[-1]
print('actual',network_output)

