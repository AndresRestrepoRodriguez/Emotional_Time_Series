# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 15:56:24 2023

@author: USER
"""

import pickle

file = open("E:\\Maestria\\Tesis\\datos\\records\\id_0\\lesson_1\\id_0.pickle",'rb')

object_file = pickle.load(file)
data = []

ENG_POS = 1
EXC_POS = 3
STR_POS = 6
REL_POS = 8
INT_POS = 10
FOC_POS = 12

pos_emotions = [ENG_POS, EXC_POS, STR_POS, REL_POS, INT_POS, FOC_POS]

data_temp = []
for i in object_file:
    record_data = i['data']
    record_time = i['time']
    data_temp.append(record_time)
    for j in pos_emotions:
        data_temp.append(record_data[j])
    data.append(data_temp)
    data_temp = list()