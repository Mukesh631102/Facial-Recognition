import cv2
import face_recognition

# Load the known face encodings and names
known_face_encodings = []
known_face_names = []

# Add known faces and their encodings
known_person1_image = face_recognition.load_image_file("C:\Users\pmuke\OneDrive\Desktop\New folder\modi.png")
known_person2_image = face_recognition.load_image_file("C:\Users\pmuke\OneDrive\Desktop\New folder\putin.jpeg")
known_person3_image = face_recognition.load_image_file("C:\Users\pmuke\OneDrive\Desktop\New folder\trump.jpeg")

# Encoding the faces
known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]
known_person2_encoding = face_recognition.face_encodings(known_person2_image)[0]
known_person3_encoding = face_recognition.face_encodings(known_person3_image)[0]

# Append encodings and names to the list
known_face_encodings.append(known_person1_encoding)
known_face_encodings.append(known_person2_encoding)
known_face_encodings.append(known_person3_encoding)

known_face_names.append("Modi")
known_face_names.append("Trump")
known_face_names.append("Putin")

# Initialize the video capture
video_capture = cv2.VideoCapture(0)

cv2.namedWindow("Video", cv2.WINDOW_NORMAL)

window_width = 640
window_height = 480
cv2.resizeWindow("Video", window_width, window_height)

is_fullscreen = False

while True:
    ret, frame = video_capture.read()

    # Detect faces and their encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    authentication_status = "Authentication Failed"  # Default status for unknown faces

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare the face encoding with known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"  # Default name for unmatched faces

        if True in matches:
            # If there's a match, get the name of the matched person
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            authentication_status = "Authentication Verified"  # Authentication successful

        # Draw a rectangle around the face and display the name or status
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, f"{name}: {authentication_status}", (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    # Show the video frame with authentication status
    cv2.imshow("Video", frame)

    # Check for key press to toggle fullscreen or quarter screen mode
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):  # Press 'q' to quit
        break
    elif key == ord('f'):  # Press 'f' for fullscreen
        if is_fullscreen:
            # If already in fullscreen, switch to quarter screen 
            cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Video", window_width, window_height)
            is_fullscreen = False
        else:
            # If in quarter screen, switch to fullscreen
            cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            is_fullscreen = True
    elif key == ord('e'):  # Press 'e' for quarter screen
        cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Video", window_width, window_height)
        is_fullscreen = False

video_capture.release()
cv2.destroyAllWindows()
