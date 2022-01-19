import zipfile

from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

# the rest is up to you!

import os
#os.mkdir('small_img')
local_zip = 'readonly/small_img.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('small_img')
zip_ref.close()


os.mkdir('images')
local_zip = 'readonly/images.zip'
zip_ref = zipfile.ZipFile(local_zip, 'r')
zip_ref.extractall('images')
zip_ref.close()

#list that contains the images names
pages_list=os.listdir('small_img')

Global_list=[]
for page_name in pages_list:
    local_list=[] 
    
    #local list = [ page_name , tesseract_text ] 
    
    local_list.append(page_name)
    img = Image.open('small_img/'+page_name)
    
    local_list.append(pytesseract.image_to_string(img).replace('-\n',''))

    Global_list.append(local_list)
    


def search(text,folder):
    for local_list in Global_list:
        if text in local_list[1]:
            print('Results found in file',local_list[0])
            
            try:
                img = Image.open(str(folder+local_list[0]))
                faces = (face_cascade.detectMultiScale(np.array(img),1.35,4)).tolist()
#                 storing the bounding boxes of all faces detected in each image of iteration
                faces_in_each = []
                
                for x,y,w,h in faces:
                    faces_in_each.append(img.crop((x,y,x+w,y+h)))
#                     modifying local data structure in each iteration to sotre PIL Image of each face
#                     display((img.crop((x,y,x+w,y+h))).resize((110,110)))
                
                contact_sheet = Image.new(img.mode, (550,110*int(np.ceil(len(faces_in_each)/5))))
#                 contact sheet modification to display each iteration's result
                x = 0
                y = 0

                for face in faces_in_each:
                    face.thumbnail((110,110))
#                     using HINT 4
                    contact_sheet.paste(face, (x, y))
                    
                    if x+110 == contact_sheet.width:
                        x=0
                        y=y+110
                    else:
                        x=x+110
                        
                display(contact_sheet)
            except:
                print('But there were no faces in that file!')
                
search("Christopher",'small_img/')


#list that contains the images names
pages_list=os.listdir('images')

Global_list=[]
for page_name in pages_list:
    local_list=[] 
    
    #local list = [ page_name , tesseract_text ] 
    
    local_list.append(page_name)
    img = Image.open('images/'+page_name)
    
    local_list.append(pytesseract.image_to_string(img).replace('-\n',''))

    Global_list.append(local_list)

search(text="Mark",folder='images/')
