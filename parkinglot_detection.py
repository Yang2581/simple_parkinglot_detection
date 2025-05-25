import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import time
from utils.parkinglot_info_reader import parkinglot_info_reader

model=YOLO('yolov8s.pt')


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK :  
        colorsBGR = [x, y]
        print(colorsBGR)

filename = '20230717105538'

area_list = parkinglot_info_reader(filename+'.csv')
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap=cv2.VideoCapture('parkingtest.mp4')

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame=cv2.resize(frame,(1024, 768))

    results=model.predict(frame)
    #   print(results)
    a=results[0].boxes.data
    px=pd.DataFrame(a.cpu()).astype("float")
    #    print(px)

    list9=[]

    for index,row in px.iterrows():
    #        print(row)

        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        if 'car' in c:
            cx=int(x1+x2)//2
            cy=int(y2 + (y1-y2)//5)

            for i in range(len(area_list)):
                cv2.polylines(frame, [np.array(area_list[i],np.int32)], True, (0,0,255), 1)
                cv2.putText(frame, str(i), area_list[i][0], cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1)
                # print('draw polylines')
                cv2.imshow("RGB", frame)

            for i in range(len(area_list)):
                results=cv2.pointPolygonTest(np.array(area_list[i],np.int32),((cx,cy)),False)
                if results>=0:
                    # cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
                    list9.append(c)
                    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,200,50),1)
                    cv2.polylines(frame, [np.array(area_list[i],np.int32)], True, (0,200,50), 1)
                    cv2.putText(frame, str(i)+':Occupied', area_list[i][0], cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,200,50), 1)

    cv2.imshow("RGB", frame)
    if cv2.waitKey(5)&0xFF==27:
            break

cap.release()
cv2.destroyAllWindows()
#stream.stop()
