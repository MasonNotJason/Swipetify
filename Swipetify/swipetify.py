## hand tracking & display pulled from https://www.youtube.com/playlist?list=PLlLe2PpVuiVJEHO5UuLad4zd_iziE3b_o
import cv2              # for pulling and modifying camera data
import mediapipe as mp  # pre-trained general hand tracker
import pywinauto        # allows python script to interface with Spotify
from math import dist   # for distance calculations (neater than writing it all out by hand)
import warnings         # neuters the mediapipe UserWarning message. The console is clean again.
warnings.filterwarnings("ignore", category=UserWarning, module='google.protobuf.symbol_database')


HANDCOUNT = 1                       # number of hands on display. 1 recommended.
DISTANCE_MODIFIER = 3               # change this to modify elements that vary depending on distance from camera
SPOTIFY_TITLE = "Spotify Premium"   # change this to your Spotify window's title. Mine was "Spotify Premium," but yours might just be "Spotify"
CHECK_COUNT = 6                     # number of times pose must be made to allow cmd to trigger. Default is 8.
TESTCAM_ENABLE = False              # choose whether or not to enable the webcam display


capture = cv2.VideoCapture(0)                                                            # declares "capture" var as 0th detected webcam
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,90) ; capture.set(cv2.CAP_PROP_FRAME_WIDTH,160)    # sets camera capture's height ; width

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

Hand = mp_hands.Hands(max_num_hands=HANDCOUNT)

# Hooking into Spotify
try:
    app = pywinauto.Application().connect(title=SPOTIFY_TITLE)
    print('Spotify found')
except pywinauto.findwindows.ElementNotFoundError:
    app = pywinauto.Application().connect(best_match="Chrome_Widget_Win0")
    print('lesser spotify found')
finally:
    sp = app["Chrome_Widget_Win0"]
if SPOTIFY_TITLE not in str(app.windows()):
    print('failed to find Spotify')

# Hand detection & bulk logic
cmdpose_made = False ; cmdpose_counter = int(0) ; not_cmdpose_counter = int(0) ; indexPath = []
while True:
    success,frame = capture.read()          # boolean if frame received, frame image data
    if success:                             # if the frame was received
        RGB_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        
        result_hand = Hand.process(RGB_frame)   # this ONE line processes the frame & tracks the hand's segments. Pretty cool.
        if TESTCAM_ENABLE:
            if result_hand.multi_hand_landmarks:
                for hand_landmarks in result_hand.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)

        try:    # to detect & track the pose...
            # this image is VERY helpful for doing this: https://www.researchgate.net/profile/Dane-Brown-2/publication/362871842/figure/fig1/AS:11431281084350163@1663153181104/MediaPipe-Hands-21-landmarks-13.ppm
            indexTip = result_hand.multi_hand_landmarks[0].landmark[8]
            middleTip = result_hand.multi_hand_landmarks[0].landmark[12]
            middleLower = result_hand.multi_hand_landmarks[0].landmark[10]
            ringTip = result_hand.multi_hand_landmarks[0].landmark[16]
            wrist = result_hand.multi_hand_landmarks[0].landmark[0]

            # logic for pose detection: ensure small dist between index & middle ; ring & wrist. Ensure that index & ring are far apart.
            if (dist([indexTip.x,indexTip.y],[middleTip.x,middleTip.y]) < .08*DISTANCE_MODIFIER ) and ((dist([ringTip.x,ringTip.y],[wrist.x,wrist.y])+.1) < dist([indexTip.x,indexTip.y],[wrist.x,wrist.y]) ):
                cmdpose_made = True ; cmdpose_counter += 1
                indexPath.append([indexTip.x,indexTip.y])
            else:
                cmdpose_made = False ; not_cmdpose_counter+=1
                if not_cmdpose_counter >= 10: cmdpose_made = False ; cmdpose_counter = int(0) ; not_cmdpose_counter = int(0) ; indexPath = []
        except: # if the detection failed...
            cmdpose_made = False ; not_cmdpose_counter+=1
            if not_cmdpose_counter >= 10: cmdpose_made = False ; cmdpose_counter = int(0) ; not_cmdpose_counter = int(0) ; indexPath = []

        if (cmdpose_made == False) and (cmdpose_counter >= CHECK_COUNT):
            delta_x = indexPath[0][0] - indexPath[-1][0] ; delta_y = indexPath[0][1] - indexPath[-1][1]
            delta_x = delta_x*(2/3)
            
            indexPathDirs = []
            for n in range(len(indexPath)):
                try:
                    indexPathDirs.append(indexPath[n][0] - indexPath[n+1][0])
                except: pass
            indexPathHeading = float(0)
            for dir in indexPathDirs:
                indexPathHeading+=dir
            indexPathHeading = indexPathHeading/len(indexPath)
            print(indexPathHeading)


            # Pause/Play
            if abs(delta_x) < abs(delta_y):
                if( delta_y != abs(delta_y)) and ((middleTip.y-middleLower.y - abs(middleTip.y-middleLower.y)) == 0):
                    print('Pause/Play!',delta_x,delta_y)
                    sp.send_keystrokes(' ',with_spaces=True)
                    cmdpose_made = False ; cmdpose_counter = int(0) ; not_cmdpose_counter = int(0) ; indexPath = []

            # Skip / Unskip
            if abs(delta_x) > abs(delta_y):
                if(delta_x == abs(delta_x)):
                    print('Skip!',delta_x,delta_y)
                    sp.send_keystrokes('^{RIGHT}')
                    cmdpose_made = False ; cmdpose_counter = int(0) ; not_cmdpose_counter = int(0) ; indexPath = []
                else:
                    print('Unskip!',delta_x,delta_y)
                    sp.send_keystrokes('^{LEFT}')
                    cmdpose_made = False ; cmdpose_counter = int(0) ; not_cmdpose_counter = int(0) ; indexPath = []

        if TESTCAM_ENABLE: cv2.imshow("omg it's me",frame)
        cv2.waitKey(1)                      # waits for a count of 1 before looping again
