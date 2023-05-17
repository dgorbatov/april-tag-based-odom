import cv2
import numpy as np
import apriltag
import time

def runVideo(updateImage):
    cap = cv2.VideoCapture(0);
    cap.set(cv2.CAP_PROP_EXPOSURE,-1)

    detector = apriltag.Detector(options=apriltag.DetectorOptions(
        families='tag16h5',
        border=100, #Tag border size in pixels
        nthreads=4,
        quad_decimate=2.0, #detection of quads can be done on a lower-resolution image,
                        # improving speed at a cost of pose accuracy and a slight decrease in detection
                        # rate. Decoding the binary payload is still done at full resolution. Default is 1.0
        quad_blur=0.0, #What Gaussian blur should be applied to the segmented image (used for
                    # quad detection?) Parameter is the standard deviation in pixels. Very noisy
                    # images benefit from non-zero values (e.g. 0.8). Default is 0.0
        refine_edges=True, #True because it helps with pose estimation, and the downside of a minor performance decrease, edeges snap to strong gradients
        refine_decode=False,
        refine_pose=True,
        debug=False,
        quad_contours=True # Use new contour-based quad detection
    ));

    contrastMultiplier = 1.0;
    brightnessMultiplier = 1.0;

    while cv2.waitKey(1) == -1:
        ret, frame = cap.read()
        
        if ret:
            updateImage(frame);
            frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA);
            frame = cv2.convertScaleAbs(frame, contrastMultiplier, brightnessMultiplier);
            detections = detector.detect(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY));
            
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
                cv2.line(frame, ptA, ptB, (0, 0, 255), 2,)
                cv2.line(frame, ptB, ptC, (0, 0, 255), 2,)
                cv2.line(frame, ptC, ptD, (0, 0, 255), 2,)
                cv2.line(frame, ptD, ptA, (0, 0, 255), 2,)

                # draw the center (x, y)-coordinates of the AprilTag
                (cX, cY) = (int(r.center[0]), int(r.center[1]))
                cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)

                # draw the tag family on the image
                tagFamily = r.tag_family.decode("utf-8")
                cv2.putText(frame, tagFamily, (ptA[0], ptA[1] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
            cv2.imshow('Input', frame);
            
    cap.release()
    cv2.destroyAllWindows();