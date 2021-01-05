from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import time
cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
time.sleep(2)


def decode(im):
    decodedObjects = pyzbar.decode(im)
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data, '\n')
    return decodedObjects


font = cv2.FONT_HERSHEY_SIMPLEX

while (cap.isOpened()):
    ret, frame = cap.read()
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    decodedObjects = decode(im)

    for decodedObject in decodedObjects:
        points = decodedObject.polygon

        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points;

        n = len(hull)

        for j in range(0, n):
            cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

        x = decodedObject.rect.left
        y = decodedObject.rect.top

        print(x, y)

        print('Type : ', decodedObject.type)
        print('Data : ', decodedObject.data, '\n')

        barCode = str(decodedObject.data)
        cv2.putText(frame, barCode, (x, y), font, 1, (0, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('s'):
        cv2.imwrite('Capture.png', frame)

cap.release()
cv2.destroyAllWindows()