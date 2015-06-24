import pymysql
import time
import sys
from os import listdir
import cv2

import threading
import numpy as np

start = time.time()
FRAMEMAX = 800
myDirectory = "/Users/Neo/Documents/Programming/Python3/Image/"


class thread1(threading.Thread):

    def __init__(self,filename):
        super(thread1,self).__init__()
        self.filename=filename

    def run(self):
        playVideo(self.filename)

class thread2(threading.Thread):
    def __init__(self,filename):
        super(thread2,self).__init__()
        self.filename=filename

    def run(self):
        videoAnasis(self.filename)

def readfile(myDirectory):
    allFileName = listdir(myDirectory)
    allFileName.sort()
    return allFileName[len(allFileName)-2]


def writeintodb(data):


    MWE = data[0]
    MEW = data[1]
    CNS = data[2]
    CSN = data[3]
    time = data[4]
    

    try:
        conn = pymysql.connect(host="172.17.108.132",port=3306,user='root',passwd='526840',db='smarttraffic')

        cur = conn.cursor()

        cur.execute("INSERT INTO traffic(time,Magnolia_WE,Magnolia_EW,College_NS,College_SN) VALUES (%s,%s,%s,%s,%s)"
,(time,MWE,MEW,CNS,CSN))

        conn.commit()

        cur.close()
        conn.close()
        return True
    except:
        print("Unexpected error:", sys.exc_info()[0])

        return False    


def playVideo(filename):
    frameNum = 0
    cap = cv2.VideoCapture('./Image/'+filename)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('output.avi',fourcc,20.0,(1280,720))


    while (1):
        frameNum += 1
        ret, frame = cap.read()

        fgmask = fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        rawdata = cv2.cvtColor(fgmask,cv2.COLOR_GRAY2BGR) # gray values

        # out.write(frame)

        cv2.imshow('frame',fgmask)
        k = cv2.waitKey(1) & 0xff
        if k == 1:
            break
        if frameNum > FRAMEMAX:
            break
    cap.release()
    cv2.destroyAllWindows()

def videoAnasis(filename, filenamePrefix):
    cap = cv2.VideoCapture('./Image/'+filename)
    VIDEO_WIDTH = 1280
    VIDEO_HEIGHT = 720
    NUMOFPIXELS = VIDEO_WIDTH * VIDEO_HEIGHT


    fgbg = cv2.createBackgroundSubtractorMOG2()
    frameNum = 0
    EMag_E_totalWhite = 0 # car in E Magnolia Ave, going eastboundf
    EMag_E_pixel_count = 0.1 # count totally how many pixels in this area
    EMag_W_totalWhite = 0
    EMag_W_pixel_count = 0.1
    SCol_S_totalWhite = 0 # car in S College Str, going southbound
    SCol_S_pixel_count = 0.1
    SCol_N_totalWhite = 0
    SCol_N_pixel_count = 0.1

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

    while(1):
        frameNum += 1

        ret, frame = cap.read()
        if frameNum%50==0:

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
            step1=5
            step2=5
            # print(time.time()-start)

            for i in range(0,VIDEO_HEIGHT,step1):
                for j in range(0,VIDEO_WIDTH,step2):
                    tmp = 0
                    if rawdata[i][j][0] > 120:
                        tmp = 1

                    if i - 0.63 * j >= 328.63: # j is x, i is y
                        SCol_N_pixel_count += 1
                        SCol_N_totalWhite += tmp
                    elif i + 0.88 * j >= 1476.08:
                        # if i<2000:
                        EMag_E_pixel_count += 1
                        EMag_E_totalWhite += tmp
                    #elif i + 0.56 * j >= 942.28:
                    elif i + 0.56 * j >= 1142.28:
                        EMag_W_pixel_count += 1
                        EMag_W_totalWhite += tmp
                    else:
                        SCol_S_pixel_count += 1
                        SCol_S_totalWhite += tmp

            # cv2.imshow('frame',rawdata)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
             break
        if frameNum > FRAMEMAX:
             break

    cap.release()
    cv2.destroyAllWindows()

    ratio_Emag_E=float(EMag_E_totalWhite)/EMag_E_pixel_count
    ratio_Emag_W=float(EMag_W_totalWhite)/EMag_W_pixel_count
    ratio_SCOl_N=float(SCol_N_totalWhite)/SCol_N_pixel_count
    ratio_SCOl_S=float(SCol_S_totalWhite)/SCol_S_pixel_count

    condition=[0,0,0,0,int(filenamePrefix)]
    traffic=[ratio_Emag_E,ratio_Emag_W,ratio_SCOl_S,ratio_SCOl_N]
    threshold=[0.05,0.1,0.3,0.5]
    for i in range(4):
        if traffic[i]<=threshold[0]:
            condition[i]=1
        elif traffic[i]<=threshold[1]:
            condition[i]=2
        elif traffic[i]<=threshold[2]:
            condition[i]=3
        elif traffic[i]<=threshold[3]:
            condition[i]=4
        else:
            condition[i]=5

    # print(time.time()-start)
    #
    # print(EMag_E_totalWhite)
    # print(EMag_W_totalWhite)
    # print(SCol_N_totalWhite)
    # print(SCol_S_totalWhite)
    # print('--------------------')
    # print(EMag_E_pixel_count)
    # print(EMag_W_pixel_count)
    # print(SCol_N_pixel_count)
    # print(SCol_S_pixel_count)
    # print('----------------------')
    print(ratio_Emag_E)
    print(ratio_Emag_W)
    print(ratio_SCOl_N)
    print(ratio_SCOl_S)
    #
    # print(frameNum)
    # print(time.time()-start)
    return condition








# thread1(file).start()
# thread2(file).start()


while(1):
    file = readfile(myDirectory)
    newfilePrefix = file[0:10]
    newfile = newfilePrefix + "-1" +".mp4"
    # playVideo(file)
    road_condition = videoAnasis(file,newfilePrefix)
    writeintodb(road_condition)
    print(road_condition)