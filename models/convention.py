import os
import cv2 
import numpy 

def bitOperation(directions, mainImg):
    addImage = cv2.imread('./virus.png')
    
    addImggray = cv2.cvtColor(addImg, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(addImggray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    addImg_fg = cv2.bitwise_and(mainImg, addImg, mask=mask)

    rows, cols = addImg.shape[:2]
    for vpos,hpos in directions:
        roi = mainImg[vpos:rows+vpos, hpos:cols+hpos]
        #roi = mainImg[vpos:rows+vpos, hpos:cols+hpos]
        
        mainImg_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        #mainImg_bg = cv2.bitwise_and(roi,roi, mask=mask_inv)

        dst = cv2.add(mainImg_bg, addImg_fg)
        mainImg[vpos:rows+vpos, hpos:cols+hpos] = dst
        #mainImg[vpos:rows+vpos, hpos:cols+hpos].copyTo(addImg_fg)

    ret, result = cv2.imencode('.jpg', mainImg)
    result = result.tobytes()
    return result