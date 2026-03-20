import sqlite3
from tkinter.filedialog import askopenfilename

import numpy as np
import cv2
conn = sqlite3.connect('Textile.db')
with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM imgsave")
        rows = cursor.fetchall()
        for row in rows:
            filename = row[0]
uploaded_file =  filename
if uploaded_file is not None:
    # Read the uploaded image using OpenCV
    #image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
    image = cv2.imread(uploaded_file)
    img=image.copy()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    blur=cv2.blur(gray,(10,10))

    dst=cv2.fastNlMeansDenoising(blur,None,10,7,21)

    _,binary=cv2.threshold(dst,127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    kernel=np.ones((5,5),np.uint8)

    erosion=cv2.erode(binary,kernel,iterations=1)
    dilation=cv2.dilate(binary,kernel,iterations=1)

    if (dilation==0).sum()>1:
        contours,_=cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        for i in contours:
            if cv2.contourArea(i)<261121.0:
                cv2.drawContours(img,i,-1,(0,0,255),3)
            cv2.putText(img,"defective fabric",(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    else:
        cv2.putText(img, "Good fabric", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    cv2.imshow("fiber", image)

    cv2.imshow("fiber", blur)

    cv2.imshow("fiber", binary)

    cv2.imshow("fiber",erosion)

    cv2.imshow("fiber", dilation)

    cv2.imshow("fiber", img)
cv2.waitKey(0)
cv2.destroyAllWindows()