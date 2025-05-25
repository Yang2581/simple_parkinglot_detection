import cv2
import pandas as pd
import numpy as np
import csv
import os
from parkinglot_info_reader import parkinglot_info_reader

area_list = []
tmp_area = []
CLK_count = 0

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK :  
        colorsBGR = (x, y)
        print(colorsBGR)
        
        # delacre golbel variables
        global CLK_count
        global tmp_area
        global area_list
        
        CLK_count = CLK_count + 1
        tmp_area.append((x,y))

        if CLK_count >= 4:
            area_list.append(tmp_area)
            CLK_count = 0
            tmp_area = []

            print("length of the area list: ", len(area_list))

        if len(area_list) > 0:
            # print('length of areas > 0')
            draw_polylines(area_list)
            
def draw_polylines(area_list):
    global img
    if len(area_list) < 1:
        cv2.imshow("RGB", img)
    else:
        for i in range(len(area_list)):
            cv2.polylines(img, [np.array(area_list[i],np.int32)], True, (0,0,255), 1)
            cv2.putText(img, str(i), area_list[i][0], cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 1)
            # print('draw polylines')
            cv2.imshow("RGB", img)

def save_csv_file(area_list, filename):
    # save the area information
    csv_file = open(filename+'.csv', 'w', encoding='utf-8')
    writer = csv.writer(csv_file)
    for area in area_list:
        writer.writerow(area)
    csv_file.close()
    print('csv file saved:\t', os.getcwd()+'/'+filename+'.csv')

def check_file_list(postfix = '.jpg'):
    filename_list = [name for name in os.listdir(os.getcwd())
                if name.endswith(postfix)]
    print('-------------------------------------')
    for i in range(len(filename_list)):
        print('[{}]'.format(i), '\t', filename_list[i])
    ret = input('Choose image file (enter the corresponding number): ')

    while eval(ret) < 0 or eval(ret) >= len(filename_list):
        ret = input('enter the valid number please!: ')
    ret = int(eval(ret))
    filename = filename_list[ret]
    return filename[:-4]

def load_image_file(file_name):
    global area_list
    area_list = []
    img=cv2.imread(file_name+'.jpg')
    img=cv2.resize(img,(1024, 768))
    return img

def load_parkinglot_info(file_name):
    global area_list
    area_list = parkinglot_info_reader(file_name)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)
filename = check_file_list()
img = load_image_file(filename)
new_img = img.copy()

while True:
    cv2.imshow("RGB", img)

    # get keyboard flag
    flag = cv2.waitKey(1)

    if flag == 8: # when backspace button clicked
        if len(area_list) < 1:
            print("No Elements in the area list !")
        else:
            area_list.pop()
            img = new_img.copy()
            print('pop an area information !')
            print("length of the area list: ", len(area_list))
            draw_polylines(area_list)

    if flag == ord('h'):
        print('------------- help list -------------')
        print('-esc:\t\t quit the program')
        print('-backspace:\t delete the last area')
        print('-c:\t\t change image file')
        print('-h:\t\t help')
        print('-s:\t\t save the area information to csv file')
        print('-l:\t\t load the area information from csv file')
        print('-------------------------------------')
    
    if flag == ord('c'):
        filename = check_file_list()
        img = load_image_file(filename)
        new_img = img.copy()
        cv2.imshow("RGB", img)

    if flag == ord('l'):
        filename = check_file_list('.csv')
        load_parkinglot_info(filename+'.csv')
        draw_polylines(area_list)

    if flag == ord('s'):
        save_csv_file(area_list, filename)
    
    if flag == 27:
        ret = input('save the csv file or not? (y) or (n): ')
        if ret == 'y':
            save_csv_file(area_list, filename)
            
            break
        else:
            print('quit the program directly')
            break

cv2.destroyAllWindows()