#!/usr/bin/python2.7

"""network_master.py
~~~~~~~~~~~~~~

Uses multiple network_slaves to train the neural network.

It works by making remote procedure calls to its slaves with the current neural 
network parameters, and then uses the updates from the slaves to update the 
networks parameters.

The master connects to multiple slave servers to distribute the 
work of training the network.

"""

import socket
import symmetricjsonrpc
import cPickle
import base64
import json
import numpy as np

import network_slave

slave_port = 4712
epochs = 30
rounds_done = 0

class NetworkRPCClient(symmetricjsonrpc.RPCClient):
    class Request(symmetricjsonrpc.RPCClient.Request):
        def dispatch_request(self, subject):
            
            # Handle callbacks from the server
            #print "dispatch_request(%s)" % (repr(subject),)
            assert subject['method'] == "updates"
            params = subject['params']
            print('received')
            #add received deltas
            delt_weights = [np.array(w) for w in params["delt_weights"]]
            delt_biases = [np.array(w) for w in params['delt_biases']]
            new_weights = np.add(net.weights, delt_weights)
            new_biases = np.add(net.biases, delt_biases)
            print('calculated new params. rounds_done: ' + str(rounds_done))
            if(rounds_done < epochs):
                print('doing more training.')
                self.parent.request('train', params = net.stringify(), wait_for_response = False)
            
            return "accepted updates"

#Make starting network
net = network_slave.Network([784,30,10], cost=network_slave.CrossEntropyCost)
net.large_weight_initializer()

if __name__ == '__main__':
    slave_ips = []
    with open('/home/ubuntu/hosts') as hosts:
        #First line is host group
        #Second line is IP of master
        #All remaining lines are slave nodes
        hosts.readline()
        hosts.readline()
        for line in hosts:
            #Get the IP from each line for slave nodes
            slave_ips.append(line.split(' ')[0])

    slave_clients = []
    for slave_ip in slave_ips:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print((slave_ip, slave_port))
        s.connect((slave_ip, slave_port))
        client = NetworkRPCClient(s)
        slave_clients.append(client)

    print('Beginning to send training requests to slaves')
    for slave_client in slave_clients:
        """
        print('This might take awhile')
        res = slave_client.request('train', params=net.stringify(), wait_for_response = True)
        print('res: ' + repr(res) + ' and: ' + str(type(res)))
        """
        res = slave_client.request('train', params=net.stringify(), wait_for_response=False)
        #print('res: ' + repr(res))

    """
    print('Shutting down clients')
    #Now that we've finished training, shutdown all clients
    for slave_client in slave_clients:
        slave_client.notify('shutdown')
        slave_client.shutdown()
    """
    

