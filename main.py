'''
----------------------------------------  Main Class  ----------------------------------------
    Entry point of Gesture Controller
'''

import cv2
import mediapipe as mp 
import pyautogui
# import math
# from enum import IntEnum
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from google.protobuf.json_format import MessageToDict
# import screen_brightness_control as sbcontrol


from handRecog import HandRecog
from gest import Gest
from hlabel import HLabel
from controller import Controller
pyautogui.FAILSAFE = False


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands



class GestureController:
    """
    Handles camera, obtain landmarks from mediapipe, entry point
    for whole program.

    Attributes
    ----------
    gc_mode : int
        indicates weather gesture controller is running or not,
        1 if running, otherwise 0.
    cap : Object
        object obtained from cv2, for capturing video frame.
    CAM_HEIGHT : int
        highet in pixels of obtained frame from camera.
    CAM_WIDTH : int
        width in pixels of obtained frame from camera.
    hr_major : Object of 'HandRecog'
        object representing major hand.
    hr_minor : Object of 'HandRecog'
        object representing minor hand.
    dom_hand : bool
        True if right hand is domaniant hand, otherwise False.
        default True.
    """
    gc_mode = 0 
    cap = None
    CAM_HEIGHT = None
    CAM_WIDTH = None

    hr_major = None 
    hr_minor = None
    dom_hand = True # if true then major hand is domaniant hand

    def __init__(self):
        """Initilaizes attributes."""
        GestureController.gc_mode = 1 # running
        GestureController.cap = cv2.VideoCapture(0) #default capturing
        GestureController.CAM_HEIGHT = GestureController.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        GestureController.CAM_WIDTH = GestureController.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    
    def classify_hands(results):
        """
        sets 'hr_major', 'hr_minor' based on classification(left, right) of 
        hand obtained from mediapipe, uses 'dom_hand' to decide major and
        minor hand.
        """
        left, right = None,None
        try:
            handedness_dict = MessageToDict(results.multi_handedness[0])
            if handedness_dict['classification'][0]['label'] == 'Right':
                right = results.multi_hand_landmarks[0]
            else :
                left = results.multi_hand_landmarks[0]
        except:
            pass

        try:
            handedness_dict = MessageToDict(results.multi_handedness[1])
            if handedness_dict['classification'][0]['label'] == 'Right':
                right = results.multi_hand_landmarks[1]
            else :
                left = results.multi_hand_landmarks[1]
        except:
            pass
        
        if GestureController.dom_hand == True:
            GestureController.hr_major = right
            GestureController.hr_minor = left
        else :
            GestureController.hr_major = left
            GestureController.hr_minor = right

    def start(self):
        """
        Entry point of whole programm, caputres video frame and passes, obtains
        landmark from mediapipe and passes it to 'handmajor' and 'handminor' for
        controlling.
        """
        
        handmajor = HandRecog(HLabel.MAJOR) # 1
        handminor = HandRecog(HLabel.MINOR) # 0 for pinch like gesture

        with mp_hands.Hands(max_num_hands = 2,min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            while GestureController.cap.isOpened() and GestureController.gc_mode: # 1 frame per unit
                success, image = GestureController.cap.read() # True & image

                if not success:
                    print("Ignoring empty camera frame.")
                    continue
                
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB) # BGR -> RGB
                image.flags.writeable = False
                results = hands.process(image) # hands = mp.solutions.hands
                
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # RGB -> BGR

                if results.multi_hand_landmarks:                   
                    GestureController.classify_hands(results)
                    handmajor.update_hand_result(GestureController.hr_major)
                    handminor.update_hand_result(GestureController.hr_minor)

                    handmajor.set_finger_state()
                    handminor.set_finger_state()
                    gest_name = handminor.get_gesture()

                    if gest_name == Gest.PINCH_MINOR: #for pinch gesture
                        Controller.handle_controls(gest_name, handminor.hand_result)
                    else:
                        gest_name = handmajor.get_gesture()
                        Controller.handle_controls(gest_name, handmajor.hand_result)
                    
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                else:
                    Controller.prev_hand = None
                cv2.imshow('Gesture Controller', image)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
        GestureController.cap.release()
        cv2.destroyAllWindows()

# uncomment to run directly
gc1 = GestureController()
gc1.start()