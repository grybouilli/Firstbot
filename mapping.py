import matplotlib.pyplot as plt
import cv2 as cv

import numpy as np
####
pos_array_x = []
pos_array_y = []

def mapping():
  print("starting pyplot")
  plt.figure()
  plt.plot(pos_array_x, pos_array_y)
  plt.show()
  print("ending pyplot")

def read_pos_from_file():
  file = open("positions.txt", "r")
  content = file.read()
  array_str = content.splitlines( )
  for string in array_str:
    pos_array_x.append(float(string.split(',')[0]))
    pos_array_y.append(float(string.split(',')[1]))

  file.close()

read_pos_from_file()
mapping()