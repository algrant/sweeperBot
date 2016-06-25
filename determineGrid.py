import numpy as np
from autopy import mouse as ms
import autopy
from PIL import Image
import imagehash
import os
import time
def histo(array):
  for i in array.flatten():
    print i

class mineSweepNine:
  
  def __init__(self, nine):
    self.histo = { -2:0, 
            -1:0 }
    self.array = nine.flatten()
    self.centre = self.array[4]
    for i in range(4) + range(5,9):
      j = self.array[i]
      if j in self.histo:
        self.histo[j] += 1
    self.leftClick = self.centre > 0 and self.histo[-1] > 0 and self.centre == self.histo[-2]
    self.rightClick = self.centre > 0 and self.histo[-1] > 0 and self.centre == self.histo[-1] + self.histo[-2]

def getScreenshot():
  os.system("screencapture funscreen.png")
  return [Image.open('funscreen.png'), apOpen('funscreen.png')]


apOpen = autopy.bitmap.Bitmap.open

numbers = [apOpen("unknown.png")] + [ apOpen("n%i.png"%i) for i in range(7)]
numbersImages = [Image.open("unknown.png")] + [ Image.open("n%i.png"%i) for i in range(7)]
numbersAsString = [apOpen("unknown.png").to_string()] + [ apOpen("n%i.png"%i).to_string() for i in range(7)]
hashedNumbers = [imagehash.average_hash(im) for im in numbersImages]
arrayNumbers = [np.sum(np.array(im).flatten()) for im in numbersImages]

# screen = apOpen('funscreen.png')
# imScreen = Image.open('funscreen.png')
changedSomething = True
qq = 0
while changedSomething and qq != 50:
  qq +=1
  changedSomething = False

  imScreen, screen = getScreenshot()
  screen.save('new_screenshot.png')

  


  offset = screen.find_bitmap(numbers[2])
  offset = offset[0]%64,offset[1]%64

  ranges = [(screen.width-offset[0])/64, (screen.height-offset[1])/64]
  minIndex = [ranges[0], ranges[1]]
  maxIndex = [0,0]
  fullArray = np.zeros(ranges)
  fullArray.fill(-2)

  print fullArray
  for i in range(ranges[0]-1):
    for j in range(ranges[1]-1):
      x = i*64 + offset[0] - 1
      y = j*64 + offset[1] - 1

      im = imScreen.crop((x,y, x+60, y+60))
      ar = np.sum(np.array(im).flatten())
      hashed = imagehash.average_hash(im)

      if ar in arrayNumbers:
        indices = [(x + 1 - offset[0])/64,(y+1-offset[1])/64]
        if indices[0] < minIndex[0]:
          minIndex[0] = indices[0]
        if indices[1] < minIndex[1]:
          minIndex[1] = indices[1]
        if indices[0] > maxIndex[0]:
          maxIndex[0] = indices[0]
        if indices[1] > maxIndex[1]:
          maxIndex[1] = indices[1]
        # im.save("test_%i_%i.png"%(x,y))
        
        fullArray[indices[0],indices[1]] = arrayNumbers.index(ar) - 1
        print indices, arrayNumbers.index(ar) - 1

  # imagehash.average_hash(meinsweeper)
  print minIndex, maxIndex
  usefulArray = fullArray[minIndex[0]:maxIndex[0],minIndex[1]:maxIndex[1]]
  print usefulArray.shape
  for x in range(1, usefulArray.shape[0]-1):
    for y in range(1, usefulArray.shape[1]-1):
      
      mn = mineSweepNine(usefulArray[x-1:x+2,y-1:y+2]) 
      if mn.leftClick or mn.rightClick:
        changedSomething = True
        p = [offset[0] + (minIndex[0]+x)*64, offset[1] + (minIndex[1]+y)*64]
        print mn.array
        ms.smooth_move(p[0]/2+20,p[1]/2+20)
        if mn.leftClick:
          ms.click(ms.LEFT_BUTTON)
          ms.click(ms.LEFT_BUTTON)
        else:
          ms.click(ms.RIGHT_BUTTON)
  time.sleep(0.5)