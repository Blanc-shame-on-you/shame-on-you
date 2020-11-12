import sys
import os
sys.path.append('/home/gpuadmin/shame-on-you/models/mask_detect/')
#from tensorflow_mask_detect import inference
from pytorch_infer import inference
from .convention import bitOperation
from .gan_genrator import generate_gan_img
import time
import cv2

#resullt 마스크 안쓴 사람 수 
#locations 마스크 안쓴사람의 얼굴 좌표 [[[xmin, ymin, xmax, ymax]]
'''
□마스크 디텍션
□세균맨 적용
□Cycle Gan 적용
    - 이미지 다시 키우기
    - 이미지 크롭 및 붙이기
□스트리밍 서비스 연결
'''
def detect(img_raw):
    start=time.time()
    #temp_img=img_raw.copy()
    result, locations =inference(img_raw)
    #img_raw에 cycle gan 적용 그리고 이미지 늘려서 거기다가 이미지 크롭
    print("detect time{}".format(start-time.time()))
    if result > 0:
        print('detected')
        return bitOperation(locations,img_raw)
    else:
        print('else')
        return img_raw
def mask_detection(img_raw):
    result, locations = inference(img_raw)
    return result > 0

def original(img_raw):
    start=time.time()
    result, locations =inference(img_raw)
    print("original time{}".format(start-time.time()))
    return img_raw 

def cycleGan(img_raw):
    start=time.time()
    width, height, channel = img_raw.shape

    gan_img = generate_gan_img(img_raw)
    print("cycleGan time{}".format(start-time.time()))
    return cv2.resize(gan_img, (height, width))

    
