'''
MIT License

Copyright (c) 2019 Oleksii Savchenko

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os
import cv2
from vidstab import VidStab, layer_overlay, download_ostrich_video

# Download test video to stabilize
if not os.path.isfile("./in/takeoff_720.mp4"):
    download_ostrich_video("./in/takeoff_720.mp4")

# Initialize object tracker, stabilizer, and video reader
object_tracker = cv2.TrackerCSRT_create()
stabilizer = VidStab()
vidcap = cv2.VideoCapture("./in/takeoff_720.mp4")

# Initialize bounding box for drawing rectangle around tracked object
object_bounding_box = None

while True:
    grabbed_frame, frame = vidcap.read()

    # Pass frame to stabilizer even if frame is None
    stabilized_frame = stabilizer.stabilize_frame(input_frame=frame, border_size=30)

    # If stabilized_frame is None then there are no frames left to process
    if stabilized_frame is None:
        break

    # Draw rectangle around tracked object if tracking has started
    if object_bounding_box is not None:
        success, object_bounding_box = object_tracker.update(stabilized_frame)

        if success:
            (x, y, w, h) = [int(v) for v in object_bounding_box]
            cv2.rectangle(stabilized_frame, (x, y), (x + w, y + h),
                          (0, 255, 0), 1)

    # Display stabilized output
    cv2.imshow('Frame', stabilized_frame)

    key = cv2.waitKey(5)

    # Select ROI for tracking and begin object tracking
    # Non-zero frame indicates stabilization process is warmed up
    if stabilized_frame.sum() > 0 and object_bounding_box is None:
        object_bounding_box = cv2.selectROI("Frame",
                                            stabilized_frame,
                                            fromCenter=False,
                                            showCrosshair=False)
        object_tracker.init(stabilized_frame, object_bounding_box)
    elif key == 27:
        break

vidcap.release()
cv2.destroyAllWindows()
