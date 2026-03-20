import sqlite3
from tkinter.filedialog import askopenfilename

import cv2

filename = askopenfilename(filetypes=[("images", "*.*")])
img = cv2.imread(filename)
conn = sqlite3.connect('Textile.db')
cursor = conn.cursor()
cursor.execute('delete from imgsave')
cursor.execute('INSERT INTO imgsave(img ) VALUES(?)', (filename,))

conn.commit()
cv2.imshow("textile", img)  # I used cv2 to show image
cv2.waitKey(0)