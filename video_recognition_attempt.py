import numpy as np
import cv2
import mediapipe as mp
import serial

# Define the default position of the robotic hand in the 3D space
default_position = np.array([1, 0, 0])  # Replace with the actual default position

# Initialize serial communication with the Arduino
ser = serial.Serial('COM3', 9600)  # Replace with the actual serial port and baud rate

# Initialize the MediaPipe hand detection model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Define a function to calculate the angles for all five fingers
def calculate_angles(hand_landmarks):
    # Get the hand landmarks for each finger
    landmarks = hand_landmarks.landmark
    index_mcp = landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    index_pip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    index_dip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_DIP]
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_mcp = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    middle_pip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    middle_dip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
    middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_mcp = landmarks[mp_hands.HandLandmark.RING_FINGER_MCP]
    ring_pip = landmarks[mp_hands.HandLandmark.RING_FINGER_PIP]
    ring_dip = landmarks[mp_hands.HandLandmark.RING_FINGER_DIP]
    ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_mcp = landmarks[mp_hands.HandLandmark.PINKY_MCP]
    pinky_pip = landmarks[mp_hands.HandLandmark.PINKY_PIP]
    pinky_dip = landmarks[mp_hands.HandLandmark.PINKY_DIP]
    pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP]
    thumb_mcp = landmarks[mp_hands.HandLandmark.THUMB_CMC]
    thumb_ip = landmarks[mp_hands.HandLandmark.THUMB_IP]
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]

    # Calculate angles for the index finger
    index_proximal = np.array([index_pip.x - index_mcp.x, index_pip.y - index_mcp.y, index_pip.z - index_mcp.z])
    index_middle = np.array([index_dip.x - index_pip.x, index_dip.y - index_pip.y, index_dip.z - index_pip.z])
    index_distal = np.array([index_tip.x - index_dip.x, index_tip.y - index_dip.y, index_tip.z - index_dip.z])
    index_angles = [np.degrees(np.arccos(np.dot(index_proximal, default_position) / (np.linalg.norm(index_proximal) * np.linalg.norm(default_position)))),
                    np.degrees(np.arccos(np.dot(index_middle, default_position) / (np.linalg.norm(index_middle) * np.linalg.norm(default_position)))),
                    np.degrees(np.arccos(np.dot(index_distal, default_position) / (np.linalg.norm(index_distal) * np.linalg.norm(default_position))))]

    # Calculate angles for the middle finger
    middle_proximal = np.array([middle_pip.x - middle_mcp.x, middle_pip.y - middle_mcp.y, middle_pip.z - middle_mcp.z])
    middle_middle = np.array([middle_dip.x - middle_pip.x, middle_dip.y - middle_pip.y, middle_dip.z - middle_pip.z])
    middle_distal = np.array([middle_tip.x - middle_dip.x, middle_tip.y - middle_dip.y, middle_tip.z - middle_dip.z])
    middle_angles = [np.degrees(np.arccos(np.dot(middle_proximal, default_position) / (np.linalg.norm(middle_proximal) * np.linalg.norm(default_position)))),                     np.degrees(np.arccos(np.dot(middle_middle, default_position) / (np.linalg.norm(middle_middle) * np.linalg.norm(default_position)))),                     np.degrees(np.arccos(np.dot(middle_distal, default_position) / (np.linalg.norm(middle_distal) * np.linalg.norm(default_position))))]

    # Calculate angles for the ring finger
    ring_proximal = np.array([ring_pip.x - ring_mcp.x, ring_pip.y - ring_mcp.y, ring_pip.z - ring_mcp.z])
    ring_middle = np.array([ring_dip.x - ring_pip.x, ring_dip.y - ring_pip.y, ring_dip.z - ring_pip.z])
    ring_distal = np.array([ring_tip.x - ring_dip.x, ring_tip.y - ring_dip.y, ring_tip.z - ring_dip.z])
    ring_angles = [np.degrees(np.arccos(np.dot(ring_proximal, default_position) / (np.linalg.norm(ring_proximal) * np.linalg.norm(default_position)))),                   np.degrees(np.arccos(np.dot(ring_middle, default_position) / (np.linalg.norm(ring_middle) * np.linalg.norm(default_position)))),                   np.degrees(np.arccos(np.dot(ring_distal, default_position) / (np.linalg.norm(ring_distal) * np.linalg.norm(default_position))))]

    # Calculate angles for the pinky finger
    pinky_proximal = np.array([pinky_pip.x - pinky_mcp.x, pinky_pip.y - pinky_mcp.y, pinky_pip.z - pinky_mcp.z])
    pinky_middle = np.array([pinky_dip.x - pinky_pip.x, pinky_dip.y - pinky_pip.y, pinky_dip.z - pinky_pip.z])
    pinky_distal = np.array([pinky_tip.x - pinky_dip.x, pinky_tip.y - pinky_dip.y, pinky_tip.z - pinky_dip.z])
    pinky_angles = [np.degrees(np.arccos(np.dot(pinky_proximal, default_position) / (np.linalg.norm(pinky_proximal) * np.linalg.norm(default_position)))),                    np.degrees(np.arccos(np.dot(pinky_middle, default_position) / (np.linalg.norm(pinky_middle) * np.linalg.norm(default_position)))),                    np.degrees(np.arccos(np.dot(pinky_distal, default_position) / (np.linalg.norm(pinky_distal) * np.linalg.norm(default_position))))]

    # Calculate angles for the thumb
    thumb_proximal = np.array([thumb_ip.x - thumb_mcp.x, thumb_ip.y - thumb_mcp.y, thumb_ip.z - thumb_mcp.z])
    thumb_distal = np.array([thumb_tip.x - thumb_ip.x, thumb_tip.y - thumb_ip.y, thumb_tip.z - thumb_ip.z])
    thumb_angles = [np.degrees(np.arccos(np.dot(thumb_proximal, default_position) / (np.linalg.norm(thumb_proximal) * np.linalg.norm(default_position)))),
                    np.degrees(np.arccos(np.dot(thumb_distal, default_position) / (np.linalg.norm(thumb_distal) * np.linalg.norm(default_position))))]

    # Combine angles for all fingers
    angles = np.array([index_angles, middle_angles, ring_angles, pinky_angles, thumb_angles])

    return angles

# Start the video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect the hand landmarks
    result = hands.process(frame_rgb)

    # Draw the hand landmarks
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            angles = calculate_angles(hand_landmarks)
            # Send the angles to the Arduino
            ser.write(angles.tobytes())

    # Show the frame
    cv2.imshow('Hand Control', frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()

# Close the serial communication with the Arduino
ser.close()
 
