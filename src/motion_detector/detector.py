import cv2

# Initialize the camera
cap = cv2.VideoCapture(0)

# Create the background subtractor object
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    
    # Apply background subtraction
    fgmask = fgbg.apply(frame)
    
    # Threshold the image
    th = 2
    imask = fgmask > th
    
    # Count the number of non-zero pixels in the image
    nz = cv2.countNonZero(imask)
    
    # If there are more than 500 non-zero pixels, motion is detected
    if nz > 500:
        # Save the current frame as an image
        cv2.imwrite('motion_detected.jpg', frame)
        
    # Display the original and processed frames
    cv2.imshow('Frame', frame)
    cv2.imshow('FG Mask', fgmask)
    
    # Exit if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
