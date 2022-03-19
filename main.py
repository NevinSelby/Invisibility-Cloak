import cv2
import time
import numpy as np
import streamlit as st
from PIL import Image

st.header("Invisibility Cloak")
st.write("____________________________________________________________________________")
st.markdown("**BASIC WORKING OF THE WEBSITE**")
st.write("For this website to run, first you have to provide the color of the cloak which you want to use as your invisibility cloak.")
st.write("After this step, you have to provide a background image which will be used as reference for the invisibility cloak to work.")
st.write("After getting your background frame, your device camera will turn on again, and replace the area of cloak with the background in real time, and hence creating the effect of invisibility")
st.write("Hope you like it! :D")
st.write("____________________________________________________________________________")


def filter_mask(mask):
    open_kernel = np.ones((5,5),np.uint8)
    close_kernel = np.ones((7,7),np.uint8)
    dilation_kernel = np.ones((10, 10), np.uint8)
    close_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel)
    open_mask = cv2.morphologyEx(close_mask, cv2.MORPH_OPEN, open_kernel)
    dilation = cv2.dilate(open_mask, dilation_kernel, iterations= 1)
    return dilation

def startaction(color, background):
#     st.write("Testing inside startaction")
    videocapture = cv2.VideoCapture(0)

    red_low = [160,50,50]
    red_high = [180,255,255]

    blue_low = [110,50,50]
    blue_high = [130,255,255]

    green_low = [50, 100,100]
    green_high = [70, 255, 255]

    white_low = [0,0,200]
    white_high = [255,55,255]

    yellow_low = [25,50,50]
    yellow_high = [32,255,255]

    if color == 'Red':
        lower_bound = np.array(red_low)
        upper_bound = np.array(red_high)
    elif color == 'Blue':
        lower_bound = np.array(blue_low)
        upper_bound = np.array(blue_high)
    elif color == 'Green':
        lower_bound = np.array(green_low)
        upper_bound = np.array(green_high)
    elif color == 'White':
        lower_bound = np.array(white_low)
        upper_bound = np.array(white_high)
    elif color == 'Yellow':
        lower_bound = np.array(yellow_low)
        upper_bound = np.array(yellow_high)

    st.write("Click 'q' for exiting :)")

    while True:
        videocapture = cv2.VideoCapture(0)
        ret, frame = videocapture.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        mask = filter_mask(mask)
        
        cloak = cv2.bitwise_and(background, background, mask=mask)

        inverse_mask = cv2.bitwise_not(mask)  

        current_background = cv2.bitwise_and(frame, frame, mask=inverse_mask)

        combined = cv2.add(cloak, current_background)

        cv2.imshow("Final output", combined)

        if cv2.waitKey(1) == ord('q'):
            break

def main():
    # st.write("First select the color of the cloak you are using")
    flag = 0
    st.write("First, select the color of your cloak:")
    left_column, right_column = st.columns(2)
    with left_column:
        color = st.radio("", ['Red', 'Blue', 'Green', 'White', 'Yellow'])
    # st.write(color)

    st.write("____________________________________________________________________________")

    st.write("Now, let us click a background image for reference")
    if st.button("Click to take background"):
        # global background
        # background = takebg()
        videocapture = cv2.VideoCapture(0)
        _, background = videocapture.read()
        time.sleep(2)
        _, background = videocapture.read()
        videocapture.release()
        imageRGB = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(imageRGB)
        st.image(pil_img)
        flag = 1


        if flag == 1:
            st.write("Alright! we got the background..... Lesgooo")

        startaction(color, background)

main()

st.write("____________________________________________________________________________")
st.markdown("**(Note:** This website may feel laggy when testing the invisible cloak, since for each frame, there is a server lag. To experience the invisibility cloak without any lag, run main.py from my github : **)**")
st.write("")
