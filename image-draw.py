import math
import os, sys
from PIL import Image
import mcpi.minecraft as minecraft
mc = minecraft.Minecraft.create()

# single hex digits to decimal numbers
hexConv = {
    '0': 0,  '1': 1,  '2': 2,  '3': 3,
    '4': 4,  '5': 5,  '6': 6,  '7': 7,
    '8': 8,  '9': 9,  'a': 10, 'b': 11,
    'c': 12, 'd': 13, 'e': 14, 'f': 15
}


# converts a hex string to a decimal int
def hexToDec(hexNum):
    decNum = 0
    for digit in range(0, len(hexNum)):
        decNum += hexConv[hexNum[digit]] * math.pow(16, (len(hexNum)-digit-1))
    return int(decNum)

# converts a decimal int to an array of RGB values
def decToRGB(decNum):
     return [int(math.floor(decNum / 65536)),
             int(math.floor(decNum / 256) % 256),
             decNum % 256]

# gets a value to see how close two colors are
def RGBCompare(RGB1, RGB2):
    red = abs(RGB1[0] - RGB2[0])
    green = abs(RGB1[1] - RGB2[1])
    blue = abs(RGB1[2] - RGB2[2])
    return red + green + blue
    # might add weight multipliers to colors to get better color matching

def getClosest(RGBNum):
    compVal = 1000 # max value; should get replaced
    currentIndex = 0
    closestIndex = 0
    for block in blockList:
        currentCompVal = RGBCompare(RGBNum, block[0])
        if (currentCompVal < compVal):
            compVal = currentCompVal
            closestIndex = currentIndex
        currentIndex += 1
    return closestIndex

# create an array of block ids
blockList = []
blockFile = open("colors-to-block-id.txt")
for line in blockFile:
    blockList.append(line[0:-1].split(":"))

# convert that array's hex strings to rgb arrays
for block in blockList:
    block[0] = decToRGB(hexToDec(block[0]))

im = Image.open(sys.argv[1])
width, height = im.size
rgb_im = im.convert('RGB')
pix = rgb_im.load()
for x in range(0, width):
    for y in range(0, height):
        colorIndex = getClosest(pix[x,y])
        if (len(blockList[colorIndex]) == 2):
            mc.setBlock(x, height-y, 0, float(blockList[colorIndex][1]))
        elif (len(blockList[colorIndex]) == 3):
            mc.setBlock(x, height-y, 0, float(blockList[colorIndex][1]), float(blockList[colorIndex][2]))

print "done"
