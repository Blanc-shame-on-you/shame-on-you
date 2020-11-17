import sqlite3
import numpy as np
import io
import cv2

def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

def setting():
    # Converts np.array to TEXT when inserting
    sqlite3.register_adapter(np.ndarray, adapt_array)

    # Converts TEXT to np.array when selecting
    sqlite3.register_converter("array", convert_array)

    x = np.arange(12).reshape(2,6)

    con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
    #cur.execute("create table test (arr array)")
    return cur

def crop_and_save(image,location,cur):
    xmin, ymin, xmax, ymax=location
    croped_image=image[ymin:ymax,xmin:xmax  ,::-1]
    cur.execute("insert into people (arr) values (?)", (croped_image, ))

'''def test_save(image,cur):
    cur.execute("insert into people (arr) values (?)", (image, ))'''

def load(cur):
    cur.execute("select arr from people")
    data = cur.fetchone()[0]
    return data

'''cursor=setting()
img=cv2.imread('C:/Users/Lee/Pictures/gan_1.jpg')
test_save(img,cursor)
cv2.imshow("test",load(cursor))'''