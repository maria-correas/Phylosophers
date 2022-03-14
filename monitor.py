#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 10:28:51 2022

@author: mat
"""

from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Value
from multiprocessing import current_process
import time, random

K=10
NR = 10
NW = 2

class Table():
    def __init__(self, n_phil, manager):
        self.phil  =manager.list( [False]*n_phil)  # lista de booleanos uqe dice si un filosofo esta comiendo o no (false es no)
        self.eating = Value('i', 0)  #valor que dice cuantos filososfos estan comiento en este momento 
        self.mutex = Lock() #esto no sabemos si hay que ponerlo 
        self.freefork = Condition(self.mutex)
        self.actual = None



    def set_current_phil(self,i):
         self.actual = i
       
    def vecinos_libres(self):
        i= self.actual
        return (not self.phil[(i-1)%len(self.phil)]) and (not self.phil[(i+1)%len(self.phil)])

    def wants_eat(self,i):
        self.mutex.acquire()   #ponemos el mutex porque estamos modificando la lista de filosofos que es una variable comun (Pablo)
        self.freefork.wait_for(self.vecinos_libres)
        self.phil[i] = True #esta comiendo el filosofo
        self.eating.value += 1 #aumentamos el numero de filosofos que estan comiendo 
        self.mutex.release()
  
    def wants_think(self,i):
        self.mutex.acquire()
        self.phil[i] = False #esta pensando el filosofo
        self.eating.value -= 1 #disminuimos el numero de filosofos que estan comiendo 
        self.freefork.notify() #decimos que los tenedores estan libres 
        self.mutex.release()
      

   
