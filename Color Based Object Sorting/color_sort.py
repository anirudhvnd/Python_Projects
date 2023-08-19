import cv2
from PIL import Image
from gpiozero import AngularServo
from time import sleep
from util import get_limits

pushser = AngularServo(18, min_pulse_width=0.0007, max_pulse_width=0.0024)
slideser = AngularServo(17, min_pulse_width=0.0007, max_pulse_width=0.0024)
sleep(1)
slideser.angle=0
pushser.angle=25
sleep(1)

count=0

red = [0,0,255]
blue = [0,255,0]
yellow = [0,255,255]
cap = cv2.VideoCapture(0)
while count!=18:
    pushser.angle=-15
    ret, frame = cap.read()
    count+=1
    if count%6!=0:
        continue

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimitb, upperLimitb = get_limits(color=blue)
    lowerLimitr, upperLimitr = get_limits(color=red)
    lowerLimity, upperLimity = get_limits(color=yellow)

    maskb = cv2.inRange(hsvImage, lowerLimitb, upperLimitb)
    maskr = cv2.inRange(hsvImage, lowerLimitr, upperLimitr)
    masky = cv2.inRange(hsvImage, lowerLimity, upperLimity)

    maskb_ = Image.fromarray(maskb)
    maskr_ = Image.fromarray(maskr)
    masky_ = Image.fromarray(masky)

    bboxb = maskb_.getbbox()
    bboxr = maskr_.getbbox()
    bboxy = masky_.getbbox()
    
    b=0
    r=0
    y=0

    if bboxb is not None:
        x1, y1, x2, y2 = bboxb

        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        frame=cv2.putText(frame,'Blue',(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        b=1
    
    if bboxr is not None:
        x1, y1, x2, y2 = bboxr

        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        frame=cv2.putText(frame,'Red',(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)
        r=1
        
    if bboxy is not None:
        x1, y1, x2, y2 = bboxy

        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        frame=cv2.putText(frame,'Yellow',(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        y=1
        

    cv2.imshow('frame', frame)
    if b==1:
        slideser.angle=45
        sleep(0.5)
        pushser.angle=-80
        sleep(0.5)
        pushser.angle=25
        sleep(1)
        slideser.angle=0
        b=0
        
    if r==1:
        sleep(0.5)
        pushser.angle=-80
        sleep(0.5)
        pushser.angle=25
        sleep(1)
        r=0
        
    if y==1:
        slideser.angle=-45
        sleep(0.5)
        pushser.angle=-80
        sleep(0.5)
        pushser.angle=25
        sleep(1)
        slideser.angle=0
        y=0
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    sleep(1.5)
    count=0
    
pushser.angle=25

cap.release()

cv2.destroyAllWindows()
