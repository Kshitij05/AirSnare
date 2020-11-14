# import statements
import cv2
import numpy as np
import pyautogui
import keyboard

# start video capture
cap = cv2.VideoCapture(0)

# Note: Use blue colour as the left drumstick, and the red colour as  the right drumstick

# The following are the area coordinates for drum kit pieces

# snare and snare text coordinates
snare_x1 = 190
snare_y1  = 330
snare_x2 = 350
snare_y2 = 490

snare_text_x = ((snare_x1 + snare_x2)/2) - 40
snare_text_x = int(snare_text_x)
snare_text_y = ((snare_y1 + snare_y2)/2) + 10
snare_text_y = int(snare_text_y)

# hi-hat and hi-hat text coordinates
hi_hat_x1 = 5
hi_hat_y1 = 100
hi_hat_x2 = 215
hi_hat_y2 = 240

hi_hat_text_x = ((hi_hat_x1 + hi_hat_x2)/2) - 50
hi_hat_text_x = int(hi_hat_text_x)
hi_hat_text_y = ((hi_hat_y1 + hi_hat_y2)/2) + 10
hi_hat_text_y = int(hi_hat_text_y)

# tom 1 and tom 1 text coordinates
tom1_x1 = 250
tom1_y1 = 30
tom1_x2 = 390
tom1_y2 = 120

tom1_text_x = ((tom1_x1 + tom1_x2)/2) - 50
tom1_text_x = int(tom1_text_x)
tom1_text_y = ((tom1_y1 + tom1_y2)/2) + 10
tom1_text_y = int(tom1_text_y)

# tom 2 and tom 2 text coordinates
tom2_x1 = 420
tom2_y1 = 30
tom2_x2 = 560
tom2_y2 = 120

tom2_text_x = ((tom2_x1 + tom2_x2)/2) - 50
tom2_text_x = int(tom2_text_x)
tom2_text_y = ((tom2_y1 + tom2_y2)/2) + 10
tom2_text_y = int(tom2_text_y)

# crash and crash text coordinates
crash_x1 = 490
crash_y1 = 250
crash_x2 = 620
crash_y2 = 330

crash_text_x = ((crash_x1 + crash_x2)/2) - 50
crash_text_x = int(crash_text_x)
crash_text_y = ((crash_y1 + crash_y2)/2) + 10
crash_text_y = int(crash_text_y)





while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)


    # mask creation for red objects
    lower_red = np.array([130, 90, 100], dtype=np.uint8)
    upper_red = np.array([255, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_red, upper_red)


    # mask creation for blue objects
    lower_blue = np.array([100, 150, 0], dtype=np.uint8)
    upper_blue = np.array([130, 255, 255], dtype=np.uint8)
    mask_2 = cv2.inRange(hsv, lower_blue, upper_blue)


    # filtering kernel
    kernel = np.ones((3, 3), np.uint8)

    # filtering for red mask
    mask = cv2.dilate(mask, kernel, iterations=4) # dilation
    mask = cv2.GaussianBlur(mask, (5, 5), 100) # gaussian blur filtering

    # filtering for blue mask
    mask_2 = cv2.dilate(mask_2, kernel, iterations=4) # dilation
    mask_2 = cv2.GaussianBlur(mask_2, (5, 5), 100) # gaussian blur filtering

    # finding contours for red objects
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # finding contours for blue objects
    contours_2, _ = cv2.findContours(mask_2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


    # sorting the contours in ascending order
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True) # red contours
    contours_2 = sorted(contours_2, key=lambda x: cv2.contourArea(x), reverse=True) # white

    '''
    Drum Kit Starts 
    '''

    # snare drum
    cv2.rectangle(frame, (snare_x1, snare_y1), (snare_x2, snare_y2), (0, 255, 0), 3)
    cv2.putText(frame, "Snare", (snare_text_x, snare_text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)


    # hi-hat
    cv2.rectangle(frame, (hi_hat_x1, hi_hat_y1), (hi_hat_x2, hi_hat_y2), (0, 255, 0), 3)
    cv2.putText(frame, "Hi-Hat", (hi_hat_text_x, hi_hat_text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # tom 1
    cv2.rectangle(frame, (tom1_x1, tom1_y1), (tom1_x2, tom1_y2), (0, 255, 0), 3)
    cv2.putText(frame, "Tom 1", (tom1_text_x, tom1_text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # tom 2
    cv2.rectangle(frame, (tom2_x1, tom2_y1), (tom2_x2, tom2_y2), (0, 255, 0), 3)
    cv2.putText(frame, "Tom 2", (tom2_text_x, tom2_text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)



    # crash
    cv2.rectangle(frame, (crash_x1, crash_y1), (crash_x2, crash_y2), (0, 255, 0), 3)
    cv2.putText(frame, "Crash", (crash_text_x, crash_text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)




    '''
    Drum Kit Ends
    '''

    # bass drum on spacebar hit
    if keyboard.is_pressed('space'):
        pyautogui.press('b')



    # red drumstick/right drumstick outline and actions
    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 1000:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.circle(frame, (x, y), 20, (0, 255, 0), 2)
            cv2.drawContours(frame, contour, -1, (255, 0, 0), 1)


            # right hand drum stick snare
            # Corrections are for increased sensitivity
            if x > snare_x1-30 and y > snare_y1-30 and x < snare_x2+20 and y < snare_y2:
                pyautogui.press('v')

            # right hand drum stick high hat closed
            # I will add some correction here as well
            if x > hi_hat_x1 and y > hi_hat_y1+20 and x < hi_hat_x2+20 and y < hi_hat_y2:
                pyautogui.press('n')

            # tom 1
            if x > tom1_x1 and y > tom1_y1 and x < tom1_x2 and y < tom1_y2:
                pyautogui.press('g')

            # tom 2
            if x > tom2_x1 and y > tom2_y1 and x < tom2_x2 and y < tom2_y2:
                pyautogui.press('h')


            # crash
            if x > crash_x1 and y > crash_y1 and x < crash_x2 and y < crash_y2:
                pyautogui.press('u')


    # blue drumstick/left drumstick outline and actions
    for contour_b in contours_2:
        area = cv2.contourArea(contour_b)

        if area > 1000:
            (x_b, y_b, w, h) = cv2.boundingRect(contour_b)
            cv2.circle(frame, (x_b, y_b), 20, (0, 0, 255), 2)
            cv2.drawContours(frame, contour_b, -1, (255, 0, 0), 1)


            # snare and snare corrections for increased sensitivity
            if x_b > snare_x1-60 and y_b > snare_y1-45 and x_b < snare_x2+20 and y_b < snare_y2:
                #keyboard.press_and_release('c')
                pyautogui.press('c')


            # hi-hat and hi-hat corrections for increased sensitivity
            if x_b > hi_hat_x1 and y_b > hi_hat_y1+20 and x_b < hi_hat_x2+20 and y_b < hi_hat_y2:
                pyautogui.press('x')


            # tom 1
            if x_b > tom1_x1 and y_b > tom1_y1 and x_b < tom1_x2 and y_b < tom1_y2:
                pyautogui.press('f')

            # tom 2
            if x_b > tom2_x1  and y_b > tom2_y1 and x_b < tom2_x2 and y_b < tom2_y2:
                pyautogui.press('g')


            # crash
            if x_b > crash_x1 and y_b > crash_y1 and x_b < crash_x2 and y_b < crash_y2:
                pyautogui.press('e')




    # red mask window for reference
    cv2.imshow("Mask", mask)

    # resizing and showing the main window
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Frame", 1400, 1000)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()
