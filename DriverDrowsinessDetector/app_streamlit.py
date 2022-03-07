from src.modules.Face import Face
import streamlit as st
import cv2
from pygame import mixer

mixer.init()
sound = mixer.Sound('src/utils/alarm.wav')
test_im = cv2.imread('/Users/kimfriedel/code/Pr4t3/DriverDrowsinessDetector/DriverDrowsinessDetector/1318.jpg')

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
cache_len = 10
eye_cache = [0] * cache_len
yawn_cache = [0] * cache_len
tilt_cache = [0] * cache_len
danger_score = 0

st.title("Driver Drowsiness Detector App")
run = st.radio('Webcam:', ('On', 'Off'))

eye_button = st.checkbox("Toggle eyes")
yawn_button = st.checkbox("Toggle yawn")
tilt_button = st.checkbox("Toggle tilt")

FRAME_WINDOW = st.image([])
cam = cv2.VideoCapture(0)

while run:
    danger_score = sum(eye_cache) + sum(tilt_cache)
    open_eye_label = 'Eyes Open'
    yawn_label = 'Not Yawning'
    tilt_label = 'Not Tilting'
    _, frame = cam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    height, width = frame.shape[:2]

    face = Face(frame)

    #TODO toggle to turn off rectangle around face
    if yawn_button:
        face.draw_rectangle()

    if eye_button:
        face.left_eye.draw_rectangle()
        face.right_eye.draw_rectangle()

    if tilt_button:
        face.tilt.draw_connections(0.4)

    if not face.left_eye.open and not face.right_eye.open:
        open_eye_label = 'Eyes Closed'
        del eye_cache[0]
        eye_cache.append(1)
    else:
        del eye_cache[0]
        eye_cache.append(0)


    cv2.putText(frame, open_eye_label, (10,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)

    if face.yawn:
        yawn_label = 'Yawning'
        del yawn_cache[0]
        yawn_cache.append(1)
    else:
        del yawn_cache[0]
        yawn_cache.append(0)


    cv2.putText(frame, yawn_label, (10,height-40), font, 1,(255,255,255),1,cv2.LINE_AA)

    if face.tilt.tilt:
        tilt_label = 'Tilting'
        del tilt_cache[0]
        tilt_cache.append(1)
    else:
        del tilt_cache[0]
        tilt_cache.append(0)


    if sum(eye_cache)/cache_len >= 0.8:
        sound.play()
        cv2.putText(frame, f'ALARM! Score: {danger_score}', (10,height-80), font, 1,(255,0,0),1,cv2.LINE_AA)

    if sum(tilt_cache)/cache_len >= 0.8:
        sound.play()
        cv2.putText(frame, f'ALARM! Score: {danger_score}', (10,height-80), font, 1,(255,0,0),1,cv2.LINE_AA)

    cv2.putText(frame, tilt_label, (10,height-60), font, 1,(255,255,255),1,cv2.LINE_AA)


    FRAME_WINDOW.image(frame)

    print(tilt_cache)
    #cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

else:
    st.write("Stopped")

# cv2.destroyAllWindows()
