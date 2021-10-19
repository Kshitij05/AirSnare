import cv2
import pyautogui

class DrumPiece:
    '''
    Class to represent a blueprint for each of the piece  of the drumkit
    '''


    def __init__(self, x1, y1, x2, y2, key, name):
        '''
        Constructor for the drum piece
        :param x1: x coordinate of the top left corner of the box shape
        :param y1: y coordinate of the top left corner of the box shape
        :param x2: x coordinate of the bottom right corner of the box shape
        :param y2: y coordinate of the bottom right corner of the box shape
        :key: what key to press when user hits the piece
        :name: what is this piece of the drumkit called?
        '''
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._key = key
        self._name = name


        # Coordinates for the text that would be placed inside  the box
        self._text_x = int(((self._x1 + self._x2)/2) - 50)
        self._text_y = int(((self._y1 + self._y2)/2) + 10)


    def get_x1(self):
        return self._x1

    def get_y1(self):
        return self._y1

    def get_x2(self):
        return self._x2

    def get_y2(self):
        return self._y2

    def get_key(self):
        return self._key

    def get_name(self):
        return self._name

    def set_x1(self, x1_new):
        self._x1 = x1_new

    def set_y1(self, y1_new):
        self._y1 = y1_new

    def set_x2(self, x2_new):
        self._x2 = x2_new

    def set_y2(self, y2_new):
        self._y2 = y2_new

    def set_key(self, new_key):
        self._key = new_key

    def set_name(self, new_name):
        self._name = new_name

    def place_piece(self, frame):
        '''
        :param frame: where to place the drum set i.e. what frame of the opencv window
        :return: None; draws the area that would serve as the corresponding drum piece
        '''
        cv2.rectangle(frame, (self._x1, self._y1), (self._x2, self._y2), (0, 255, 0), 3)
        cv2.putText(frame, self._name, (self._text_x, self._text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    def play_piece(self):
        '''
        :return: None; plays the drum piece based on the specified key input
        '''
        pyautogui.press(self._key)
