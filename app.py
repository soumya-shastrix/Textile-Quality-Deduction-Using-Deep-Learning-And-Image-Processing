import os
import sqlite3
from tkinter.filedialog import askopenfilename
import matplotlib
import cv2
# //matplotlib.use('TkAgg')/
import cv2
import numpy as np
from flask import Flask, render_template, request
from matplotlib import pyplot as plt

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/contact")
def contact():
    return render_template("contact.html");

@app.route("/about")
def about():
    return render_template("about.html");


@app.route("/reg")
def reg():
    return render_template("register.html");
@app.route("/login1")
def login1():
    return render_template("login.html");
@app.route("/regsave1", methods=["POST", "GET"])
def regsave1():
    msg = "msg"
    print("bb")
    if request.method == "POST":

            Username1 = request.form["name"]
            email1 = request.form["email"]
            password1 = request.form["password"]
            cpassword1= request.form["confirm_password"]
            print("aa")
            if Username1 == "":
                msg = "Enter Username"
                return render_template("success.html", msg=msg)
            else:
                if email1 == "":
                    msg = "Enter Email"
                    return render_template("success.html", msg=msg)
                else:
                    if password1 == "":
                        msg = "Enter Password"
                        return render_template("success.html", msg=msg)
                    else:
                        if cpassword1 == "":
                            msg = "Enter Confirm Password"
                            return render_template("success.html", msg=msg)
                        else:
                                    with sqlite3.connect("Textile.db") as con:
                                        cur = con.cursor()
                                        cur.execute(
                                            "INSERT into register (name,email,password,confirm_password) values (?,?,?,?)",
                                            (Username1,email1,password1,cpassword1))
                                        con.commit()
                                        msg = "successfully Added"
                        return render_template("sucess.html", msg=msg)
@app.route("/lg", methods=["POST", "GET"])
def lg():
    msg = "msg"
    if request.method == "POST":
            un = request.form["un"]
            pw = request.form["pw"]
            if un=="":
                msg="Enter Username"
                return render_template('sucess.html',msg=msg)
            else:
                if pw=="":
                    msg = "Enter Password"
                    return render_template('sucess.html', msg=msg)
                else:

                    with sqlite3.connect("Textile.db") as con:
                            cur = con.cursor()
                            cur.execute("SELECT * FROM register where name=? and password=?",(un,pw))
                            rows = cur.fetchall()
                            for row in rows:
                                dbUser = row[0]
                                dbPass = row[2]
                                print(dbUser,dbPass)


                                if dbUser == un and dbPass==pw:
                                    return render_template('menu.html')
                                else:
                                    msg = "Try Again"
                                    return render_template('sucess.html', msg=msg)


@app.route("/capt", methods=["POST", "GET"])
def capt():
    import cv2

    # 1.creating a video object
    video = cv2.VideoCapture(0)
    # 2. Variable
    a = 0

    # 3. While loop
    while True:
        a = a + 1
        # 4.Create a frame object
        check, frame = video.read()
        # Converting to grayscale
        # gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # 5.show the frame!
        cv2.imshow("Capturing", frame)
        # 6.for playing
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    # 7. image saving
    showPic = cv2.imwrite("filename.jpg", frame)
    print(showPic)
    # 8. shutdown the camera
    video.release()
    cv2.destroyAllWindows
    return render_template("menu.html");

@app.route("/readimg", methods=["POST", "GET"])
def readimg():
    filename = askopenfilename(filetypes=[("images", "*.*")])
    img = cv2.imread(filename)
    conn = sqlite3.connect('Textile.db')
    cursor = conn.cursor()
    cursor.execute('delete from imgsave')
    cursor.execute('INSERT INTO imgsave(img ) VALUES(?)', (filename,))

    conn.commit()
    cv2.imshow("textile", img)  # I used cv2 to show image
    cv2.waitKey(0)
    return render_template("menu.html");

@app.route("/pre", methods=["POST", "GET"])
def pre():
    conn = sqlite3.connect('Textile.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM imgsave")
        rows = cursor.fetchall()
        for row in rows:
            filename = row[0]

    gray = cv2.imread(filename, 0)

    # Showing grayscale image
    cv2.imshow("Grayscale Image", gray)

    # waiting for key event
    cv2.waitKey(0)

    # destroying all windows
    cv2.destroyAllWindows()

    img = cv2.imread(filename)

    dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    cv2.imshow("Denoised", dst)

    # waiting for key event
    cv2.waitKey(0)

    plt.show()
    return render_template("menu.html");



@app.route("/seg", methods=["POST", "GET"])
def seg():
    conn = sqlite3.connect('Textile.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM imgsave")
        rows = cursor.fetchall()
        for row in rows:
            filename = row[0]
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, 0)
    plt.figure(figsize=(8, 8))
    plt.imshow(img, cmap="gray")
    plt.axis('off')
    plt.title("Original Image")
    plt.show()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.figure(figsize=(8, 8))
    plt.imshow(gray, cmap="gray")
    plt.axis('off')
    plt.title("GrayScale Image")
    plt.show()
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    plt.figure(figsize=(8, 8))
    plt.imshow(thresh, cmap="gray")
    plt.axis('off')
    plt.title("Threshold Image")
    plt.show()
    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=15)
    bg = cv2.dilate(closing, kernel, iterations=1)
    dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 0)
    ret, fg = cv2.threshold(dist_transform, 0.02 * dist_transform.max(), 255, 0)
    cv2.imshow('image', fg)
    plt.figure(figsize=(8, 8))
    plt.imshow(fg, cmap="gray")
    plt.axis('off')
    plt.title("Segmented Image")
    plt.show()
    return render_template("menu.html");

@app.route("/feat", methods=["POST", "GET"])
def feat():
    import sqlite3

    import cv2
    conn = sqlite3.connect('Textile.db')
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM imgsave")
        rows = cursor.fetchall()
        for row in rows:
            filename = row[0]
    img = cv2.imread(filename, 0)
    img = cv2.resize(img, (450, 300))

    def null(x):
        pass



        # get Trackbar position
    a = 80
    b = 120
        # Canny Edge detection
        # arguments: image, min_val, max_val
    canny = cv2.Canny(img, a, b)
        # display the images
    cv2.imshow('Canny', canny)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
    return render_template("menu.html");

@app.route("/defect", methods=["POST", "GET"])
def defect():
        os.system("python clf.py")
        os.system("python def.py")
        return render_template("menu.html");



if __name__ == '__main__':
    app.run()
