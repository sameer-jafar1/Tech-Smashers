import cv2
import mediapipe as mp
import numpy as np
import json
import requests

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

# Gesture mapping
GESTURE_ACTIONS = {
    "swipe_left": "next_item",
    "swipe_right": "previous_item",
    "thumbs_up": "confirm_order",
    "fist": "select_item"
}

def detect_gesture(hand_landmarks):
    """Detects gestures based on hand landmarks"""
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    if thumb_tip.x < index_tip.x:  # Swipe Left
        return "swipe_left"
    elif thumb_tip.x > index_tip.x:  # Swipe Right
        return "swipe_right"
    elif thumb_tip.y < index_tip.y:  # Thumbs Up
        return "thumbs_up"
    elif thumb_tip.y > index_tip.y and index_tip.y > thumb_tip.y:  # Fist
        return "fist"
    return None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = detect_gesture(hand_landmarks)

            if gesture:
                action = GESTURE_ACTIONS.get(gesture)
                print(f"Detected Gesture: {gesture} → Action: {action}")
                
                # Send action to backend
                requests.post("http://127.0.0.1:5000/gesture", json={"action": action})

    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
