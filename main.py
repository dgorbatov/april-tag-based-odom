import cv2
import numpy as np
import apriltag
import time

cap = cv2.VideoCapture(0);

detector = apriltag.Detector(options=apriltag.DetectorOptions(
    families='tag16h5',
    border=1,
    nthreads=1,
    quad_decimate=2.0,
    quad_blur=1.0,
    refine_edges=True,
    refine_decode=False,
    refine_pose=False,
    debug=True,
    quad_contours=True
));


while cv2.waitKey(1) == -1:
    ret, frame = cap.read()
    
    if ret:
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA);
        detections = detector.detect(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY));
        print(detections);
        
        # loop over the AprilTag detection results
        for r in detections:
            # extract the bounding box (x, y)-coordinates for the AprilTag
            # and convert each of the (x, y)-coordinate pairs to integers
            (ptA, ptB, ptC, ptD) = r.corners
            ptB = (int(ptB[0]), int(ptB[1]))
            ptC = (int(ptC[0]), int(ptC[1]))
            ptD = (int(ptD[0]), int(ptD[1]))
            ptA = (int(ptA[0]), int(ptA[1]))

            # draw the bounding box of the AprilTag detection
            cv2.line(frame, ptA, ptB, (255, 255, 0), 2,)
            cv2.line(frame, ptB, ptC, (255, 255, 0), 2,)
            cv2.line(frame, ptC, ptD, (255, 255, 0), 2,)
            cv2.line(frame, ptD, ptA, (255, 255, 0), 2,)

            # draw the center (x, y)-coordinates of the AprilTag
            (cX, cY) = (int(r.center[0]), int(r.center[1]))
            cv2.circle(frame, (cX, cY), 5, (255, 255, 0), -1)

            # draw the tag family on the image
            tagFamily = r.tag_family.decode("utf-8")
            cv2.putText(frame, tagFamily, (ptA[0], ptA[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            print("[INFO] tag family: {}".format(tagFamily))
 
        cv2.imshow('Input', frame);
        
cap.release()
cv2.destroyAllWindows();