import cv2
import numpy as np
import streamlit as st
import imutils
from PIL import ImageColor

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

st.title("WebCam Based Virtual Drawing System")
st.subheader("OpenCV application that can track an object’s movement, using which a user can draw on the screen by moving the object around — I call it Webcam Paint.")
st.header("Pick your Favorite Color & Brush Size")
color = st.beta_color_picker('Pick A Color', '#FF0000')
point_size= int(st.slider('Your Brush Size', 1, 30, 10))
RGB_COLOR = ImageColor.getcolor(color, "RGB")
RGB_COLOR = RGB_COLOR[::-1]
st.info("Color is: "+str(RGB_COLOR)+" & Ponter Size Is: "+str(point_size))
st.success("Design & Developed By Nilesh Verma")

def empty(a):
    pass
if st.button("Start"):

    video = cv2.VideoCapture(0)
    video.set(3,1000)      #3 is id for length 
    video.set(4,1000)      #4 is id for breadth  
    video.set(10,300)     #10 is id for brightness

    image_placeholder = st.empty()

    def getcontours(img):
        img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        
        lower = np.array([0,176,177])
        upper = np.array([179,255,255])
        
        mask = cv2.inRange(img_hsv,lower,upper)
        contour,heirarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        x ,y, w, h = 0,0,0,0
        for ctr in contour:
            peri = cv2.arcLength(ctr,True)

            approx = cv2.approxPolyDP(ctr,0.01*peri,True)
            if cv2.contourArea(ctr)>200:
                x, y, w, h = cv2.boundingRect(approx)
            
        return x+w,y

    def getpoint(img):
        allpoints=[]
        x,y = getcontours(img)
        cv2.circle(img,(x,y),5,(0,0,255),cv2.FILLED)
        if x!=0 and y!=0:
            allpoints.append([x,y])
        return allpoints

    def drawoncam(img,points):
        for pts in points:
            cv2.circle(img,(pts[0],pts[1]),point_size,RGB_COLOR,cv2.FILLED)

    allpoints = []
            
    while True:
        success , img_webcam = video.read()
        img_webcam = cv2.flip(img_webcam,1)
        img_webcam = imutils.resize(img_webcam, width=700)
        
        points = getpoint(img_webcam)
        if len(points)!=0:
            for pts in points:
                allpoints.append(pts)
        if len(allpoints)!=0:
            drawoncam(img_webcam,allpoints)
        
        image_placeholder.image(img_webcam,channels="BGR")
        
        if cv2.waitKey(1) & 0xFF==ord('q'):
            cv2.destroyAllWindows()
            break