import numpy as np
from autopy import mouse as ms
import autopy
import os


# -2 = covered
# -1 = bomb (bomb or flag)
# 0 = uncovered empty
# 1 - 8, just numbers
options = [-2,-1,0,1,2,3,4,5,6,7,8]

# given
# array of nine with centre number + empty neighbour
# 1) completed -- if centre square == number of bombs
# 2) everything is flaggable -- if centre square = number of bombs + empties
# 3) unclickable

testArray = np.array([  [-2, -2, -1],
                        [ 3,  4, -1],
                        [ 6,  7,  8] ])

def histo(array):
  for i in array.flatten():
    print i

class mineSweepNine:
  histo = { -2:0, 
            -1:0 }
  def __init__(self, nine):
    self.array = nine.flatten()
    self.centre = self.array[4]
    for i in range(4) + range(5,9):
      j = self.array[i]
      if j in self.histo:
        self.histo[j] += 1
    self.leftClick = self.centre == self.histo[-1]
    self.rightClick = self.centre == self.histo[-1] + self.histo[-2]

a = mineSweepNine(testArray)
print a.leftClick, a.rightClick