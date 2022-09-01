import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [ 8, 12, 16, 20]

for tip in finger_tips:
    x,y = int(lm_index[tip].x*w), int(lm_index[tip].y*h)
    cv2.circle(img , (x,y), 15, (255, 0 ,0), cv2.FILLED)



def countFingers(image, hand_landmarks, handNo=0):
    
    if hand_landmarks:
        # Get all Landmarks of the FIRST Hand VISIBLE
        landmarks = hand_landmarks[handNo].landmark
        # print(landmarks)

        # Count Fingers        
        fingers = []

        for lm_index in tipIds:
                # Get Finger Tip and Bottom y Position Value
                finger_tip_y = landmarks[lm_index].y 
                finger_bottom_y = landmarks[lm_index - 2].y
                
                # Get Thumb Tip and Bottom y Position Value
                thumb_tip_x = landmarks[lm_index].x
                thumb_bottom_x = landmarks[lm_index - 2].x

                # Check if ANY FINGER is OPEN or CLOSED
                if lm_index[tip].x < lm_index[tip - 3].x:
                    cv2.circle(img, (x,y), 15, (0,255,0), cv2.FILLED)
                    finger_fold_status.append(True)
                else:
                    finger_fold_status.append(False)


        # print(fingers)
        totalFingers = fingers.count(1)

        # Display Text
        text = f'Fingers: {totalFingers}'

        cv2.putText(image, text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

# Define a function to 
def drawHandLanmarks(image, hand_landmarks):

    # Darw connections between landmark points
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)


while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detect the Hands Landmarks 
    results = hands.process(image)

    # Get landmark position from the processed result
    hand_landmarks = results.multi_hand_landmarks

    # Draw Landmarks
    drawHandLanmarks(image, hand_landmarks)

    # Get Hand Fingers Position        
    countFingers(image, hand_landmarks)

    cv2.imshow("Media Controller", image)

    # Quit the window on pressing Sapcebar key
    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()
