import pyautogui
# import screen_brightness_control as sbcontrol
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from gest import Gest


# Executes commands according to detected gestures
class Controller:
    """
    Executes commands according to detected gestures.

    Attributes
    ----------
    tx_old : int
        previous mouse location x coordinate
    ty_old : int
        previous mouse location y coordinate
    flag : bool
        true if V gesture is detected
    grabflag : bool
        true if FIST gesture is detected

    """

    tx_old = 0
    ty_old = 0
    trial = True
    flag = False
    grabflag = False

    framecount = 0
    prev_hand = None


    # Locate Hand to get Cursor Position
    # Stabilize cursor by Dampening
    def get_position(hand_result):
        """
        returns coordinates of current hand position.

        Locates hand to get cursor position also stabilize cursor by 
        dampening jerky motion of hand.

        Returns
        -------
        tuple(float, float)
        """
        point = 9
        position = [hand_result.landmark[point].x ,hand_result.landmark[point].y]
        sx,sy = pyautogui.size()
        x_old,y_old = pyautogui.position()
        x = int(position[0]*sx)
        y = int(position[1]*sy)
        if Controller.prev_hand is None:
            Controller.prev_hand = x,y
        delta_x = x - Controller.prev_hand[0]
        delta_y = y - Controller.prev_hand[1]

        distsq = delta_x**2 + delta_y**2
        ratio = 1
        Controller.prev_hand = [x,y]

        if distsq <= 25:
            ratio = 0
        elif distsq <= 900:
            ratio = 0.07 * (distsq ** (1/2))
        else:
            ratio = 2.1
        x , y = x_old + delta_x*ratio , y_old + delta_y*ratio
        return (x,y)


    def handle_controls(gesture, hand_result):  
        """Impliments all gesture functionality."""      
        x,y = None,None
        if gesture != Gest.PALM :
            x,y = Controller.get_position(hand_result)
        
        # flag reset
        if gesture != Gest.FIST and Controller.grabflag:
            Controller.grabflag = False
            pyautogui.mouseUp(button = "left")


        if gesture == Gest.V_GEST: # V shape
            Controller.flag = True
            pyautogui.moveTo(x, y, duration = 0.1)


        elif gesture == Gest.MID and Controller.flag: # left click
            pyautogui.click()
            Controller.flag = False

        elif gesture == Gest.INDEX and Controller.flag: # right click
            pyautogui.click(button='right')
            Controller.flag = False