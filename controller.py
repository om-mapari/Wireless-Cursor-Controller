# import libraries


import pyautogui
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
    prev_hand : tuple
        stores (x, y) coordinates of hand in previous frame.
    
    """

    tx_old = 0
    ty_old = 0
    flag = False
    grabflag = False
    prev_hand = None
    
    

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

        # After this line is executed, sx will contain the width of the computer screen and sy will contain the height of the computer screen. ------ screen size
        sx,sy = pyautogui.size() 


        #this function position() returns the current position of the mouse on the screen in x and y coordinates.    ------ old coordinate of mouse
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

        if distsq <= 25: # 5
            ratio = 0
        elif distsq <= 900: # 30
            ratio = 0.07 * (distsq ** (1/2))
        else:
            ratio = 2.1
        x , y = x_old + delta_x*ratio , y_old + delta_y*ratio
        return (x,y)

    

    def handle_controls(gesture, hand_result):  
        """Impliments all gesture functionality.""" 

        #initializing two variables "x" and "y" to None. 
        x,y = None,None

        #reset previous gesture
        #If the gesture is not "PALM", then "x" and "y" are assigned the position of the hand.
        if gesture != Gest.PALM :
            x,y = Controller.get_position(hand_result)
        
        # if gesture is not "FIST" then set grabflag= False
        if gesture != Gest.FIST and Controller.grabflag:
            Controller.grabflag = False
            pyautogui.mouseUp(button = "left")

        #current gesture
        # v - gesture
        if gesture == Gest.V_GEST:
            Controller.flag = True
            pyautogui.moveTo(x, y, duration = 0.1)

        # fist -gesture
        elif gesture == Gest.FIST:
            if not Controller.grabflag : 
                Controller.grabflag = True
                pyautogui.mouseDown(button = "left")
            pyautogui.moveTo(x, y, duration = 0.1)

        # mid -gesture
        elif gesture == Gest.MID and Controller.flag:
            pyautogui.click()
            Controller.flag = False

        # index -gesture
        elif gesture == Gest.INDEX and Controller.flag:
            pyautogui.click(button='right')
            Controller.flag = False



        