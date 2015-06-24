import numpy as np
import cv2

cap = cv2.VideoCapture('./Image/capture.mp4')
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
NUMOFPIXELS = VIDEO_WIDTH * VIDEO_HEIGHT
# whiteNum = {} # number of white points
# for n in range(NUMOFPIXELS):
#     whiteNum[n] = 0

fgbg = cv2.createBackgroundSubtractorMOG2()
frameNum = 0
EMag_E_totalWhite = 0 # car in E Magnolia Ave, going eastbound
EMag_E_pixel_count = 0 # count totally how many pixels in this area
EMag_W_totalWhite = 0
EMag_W_pixel_count = 0
SCol_S_totalWhite = 0 # car in S College Str, going southbound
SCol_S_pixel_count = 0
SCol_N_totalWhite = 0
SCol_N_pixel_count = 0

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

while(1):
    frameNum += 1
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    rawdata = cv2.cvtColor(fgmask,cv2.COLOR_GRAY2BGR) # gray values
    # for i in range(VIDEO_HEIGHT):
    #     for j in range(VIDEO_WIDTH):
    #         tmp = 0
    #         if rawdata[i][j][0] > 120:
    #             tmp = 1
    #
    #         whiteNum[i + j * VIDEO_WIDTH] = tmp
    #totalWhite[frameNum] = sum(whiteNum.values())
    #print(totalWhite)
    # for i in range(VIDEO_HEIGHT):
    #     for j in range(VIDEO_WIDTH):
    #         tmp = 0
    #         if rawdata[i][j][0] > 120:
    #             tmp = 1
    #
    #         if i - 0.63 * j >= 328.63: # j is x, i is y
    #             SCol_N_pixel_count += 1
    #             SCol_N_totalWhite += tmp
    #         elif i + 0.88 * j >= 1476.08:
    #             EMag_E_pixel_count += 1
    #             EMag_E_totalWhite += tmp
    #         elif i + 0.56 * j >= 942.28:
    #             EMag_W_pixel_count += 1
    #             EMag_W_totalWhite += tmp
    #         else:
    #             SCol_S_pixel_count += 1
    #             SCol_S_totalWhite += tmp





    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(1) & 0xff
    if k == 1:
        break
    if frameNum > 200:
        break

cap.release()
cv2.destroyAllWindows()

print(EMag_E_totalWhite)
print(EMag_W_totalWhite)
print(SCol_N_totalWhite)
print(SCol_S_totalWhite)
