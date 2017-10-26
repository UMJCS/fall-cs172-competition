import cv2
from cv2 import VideoWriter,VideoWriter_fourcc,imread,resize
import os
img_root= os.getcwd()+"\\..\\..\\video\\frames\\"
video_root=os.getcwd()+'\\..\\..\\video\\video.avi'
print(img_root)

#Edit each frame's appearing time!
fps=10
fourcc=VideoWriter_fourcc(*"MJPG")
videoWriter=cv2.VideoWriter(video_root,fourcc,fps,(1601,901))

for i in range(1,156):
    print(img_root+str(i)+'.jpg')
    frame = cv2.imread(img_root+str(i)+'.jpg')
    videoWriter.write(frame)
videoWriter.release()
