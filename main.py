# import statements
from DrumPiece import DrumPiece
import cv2
import numpy as np


def add_piece(x1, y1, x2, y2, key, name, drum_kit):
    '''
    :param x1: x coordinate of the top left corner of the box shape
    :param y1: y coordinate of the top left corner of the box shape
    :param x2: x coordinate of the bottom right corner of the box shape
    :param y2: y coordinate of the bottom right corner of the box shape
    :key: what key to press when user hits the piece
    :name: what is this piece of the drumkit called?
    :param drum_kit: the list in which each object of the class DrumPiece is stored
    :return: None

    This is a helper function for the build_kit function, so that objects can be created and further added into a list to keep a track of them
    '''
    new_piece = DrumPiece(x1, y1, x2, y2, key, name)
    drum_kit.append(new_piece)



def build_kit(drum_kit):
    '''
    This function is used to create a piece of the drumkit, while adding each piece into a list that is passed in as a parameter to this function
    '''
    add_piece(190, 330, 350, 490, 'v', 'Snare', drum_kit)
    add_piece(5, 100, 215, 240, 'n', 'Hi-Hat', drum_kit)
    add_piece(250, 30, 390, 120, 'f', 'Tom 1', drum_kit)
    add_piece(420, 30, 560, 120, 'h', 'Tom 2', drum_kit)
    add_piece(490, 250, 620, 330, 'u', 'Crash', drum_kit)



def main():


    # start video capture
    cap = cv2.VideoCapture(1)

    # list that stores every piece of the drumkit
    drum_kit = []
    # create drumkit pieces and add it to the list using the build_kit function
    build_kit(drum_kit)

    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # blurring the frame and converting BGR color definition to HSV
        blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        # placing each piece of the drum kit on the screen
        for piece in drum_kit:
            piece.place_piece(frame)


        # mask creation for red drum stick
        lower_red = np.array([130, 90, 100], dtype=np.uint8)
        upper_red = np.array([255, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_red, upper_red)


        # mask creation for blue drum stick
        lower_blue = np.array([100, 150, 0], dtype=np.uint8)
        upper_blue = np.array([130, 255, 255], dtype=np.uint8)
        mask_2 = cv2.inRange(hsv, lower_blue, upper_blue)


        # filtering kernel
        kernel = np.ones((3, 3), np.uint8)

        # filtering for red drum stick mask
        mask = cv2.dilate(mask, kernel, iterations=4) # dilation
        mask = cv2.GaussianBlur(mask, (5, 5), 100) # gaussian blur filtering

        # filtering for blue drum stick mask
        mask_2 = cv2.dilate(mask_2, kernel, iterations=4) # dilation
        mask_2 = cv2.GaussianBlur(mask_2, (5, 5), 100) # gaussian blur filtering

        # finding contours for red drum stick
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # finding contours for blue drum stick
        contours_2, _ = cv2.findContours(mask_2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


        # sorting the contours in ascending order
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True) # red contours
        contours_2 = sorted(contours_2, key=lambda x: cv2.contourArea(x), reverse=True) # white


        # red drum stick outline and actions
        for contour in contours:
            area = cv2.contourArea(contour)

            # this is so background noise contours that don't cover a lot of area are ignored
            if area > 1000:
                # find a rectangle bounding the contours and draw a circle at the start of the rectangle
                # this circle will be used to track the movement of the tip of the drum stick
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.circle(frame, (x, y), 20, (0, 255, 0), 2)
                cv2.drawContours(frame, contour, -1, (255, 0, 0), 1)

                for piece in drum_kit:
                    # if the drum stick hits the drum piece area, then play that particular piece
                    if x > piece.get_x1() - 30 and y > piece.get_y1() - 30 and x < piece.get_x2() + 20 and y < piece.get_y2():
                        piece.play_piece()

        # blue drumstick outline and actions
        for contour_b in contours_2:
            area = cv2.contourArea(contour_b)

            # this is so background noise contours that don't cover a lot of area are ignored
            if area > 1000:
                # finding a rectangle bounding the contours and drawing a circle at the start of the rectangle
                # this circle will be used to track the movement of the tip of the drum stick
                (x_b, y_b, w, h) = cv2.boundingRect(contour_b)
                cv2.circle(frame, (x_b, y_b), 20, (0, 0, 255), 2)
                cv2.drawContours(frame, contour_b, -1, (255, 0, 0), 1)

                for piece in drum_kit:
                    # if the drum stick hits the drum piece area, then play that particular piece
                    if x_b > piece.get_x1() and y_b > piece.get_y1() and x_b < piece.get_x2()  and y_b < piece.get_y2():
                        piece.play_piece()


        # resizing and showing the main window
        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Frame", 1400, 1000)
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()