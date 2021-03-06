import face_recognition
import cv2
import socket
import time
import struct
import numpy as np
import serial
port = "/dev/ttyUSB1"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#udp_ip ="192.168.1.5"
udp_ip ="169.254.164.111"
#udp_ip =  "192.168.1.4"
#udp_ip =  '192.168.1.5'
server_address = (udp_ip, 51002)
serialFromArduino =serial.Serial(port,9600)
serialFromArduino.flushInput()
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
print("[INFO] sampling THREADED frames from webcam...")
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
hsutsaiming_image = face_recognition.load_image_file("hsutsaiming.jpg")
hsutsaiming_face_encoding = face_recognition.face_encodings(hsutsaiming_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
isDetection=0

#read adu data!!


while True:
    #input = serialFromArduino.read()
    #serialFromArduino.flushInput()     
    serialFromArduino.flushInput()
    t1 = time.time()
    while not serialFromArduino.readable():
        if time.time()- t1>=1:
            break
        pass
    input = serialFromArduino.read()
    data = str(input)
    print data

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces([hsutsaiming_face_encoding],face_encoding)
            name = "Unknown"   

            if match[0]:
                name ="hsutsaiming"
                isDetection=1
            else :
                isDetection=0

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    

    for (top, right, bottom, left), name in zip(face_locations, face_names):
             # Scale back up face locations since the frame we detected in was scaled to 1/4 size
              top *= 4
              right *= 4
              bottom *= 4
              left *= 4

        # Draw a box around the face
              cv2.rectangle(frame, (left, top), (right, bottom), (128,255,0),3)
        
              cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_DUPLEX, 1.0, (128,255,0),3)
			   
    # Display the resulting image
            
    cv2.imshow('Video', frame)
    if isDetection==1:
       data1='F'
       t1 = time.time()
       #print t1
       client_socket.sendto(data1, server_address)
       
       #print isDetection
       #print data1
    else :
        t1 = time.time()
        #print t1 
        client_socket.sendto(data , server_address)
        #print isDetection  
        #print data
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release handle to the webcam

video_capture.release()
client_socket.close()
cv2.destroyAllWindows()

