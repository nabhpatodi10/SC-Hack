import cv2
import numpy as np
import time
from mtcnn.mtcnn import MTCNN
from keras_facenet import FaceNet
from numpy.linalg import norm

def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

# Initialize the MTCNN face detector
detector = MTCNN()

# Load the FaceNet model via keras_facenet
embedder = FaceNet()

# Load the reference image and convert to RGB
ref_img = cv2.imread("Images/reference.jpg")
if ref_img is None:
    print("Reference image not found!")
    exit()
ref_img_rgb = cv2.cvtColor(ref_img, cv2.COLOR_BGR2RGB)

# Detect face(s) in the reference image
faces = detector.detect_faces(ref_img_rgb)
if len(faces) == 0:
    print("No face detected in reference image.")
    exit()

# Use the first detected face from the reference image
x, y, w, h = faces[0]['box']
x, y = max(0, x), max(0, y)
ref_face = ref_img_rgb[y:y+h, x:x+w]

# Resize to the expected FaceNet input size (typically 160x160)
ref_face_resized = cv2.resize(ref_face, (160, 160))
ref_face_array = np.expand_dims(ref_face_resized, axis=0)

# Compute the reference embedding
ref_embedding = embedder.embeddings(ref_face_array)[0]

# Define a cosine similarity threshold for identification
threshold = 0.5  # Adjust based on your testing

# Start video capture
cap = cv2.VideoCapture(0)
frame_count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    # Convert the frame to RGB for MTCNN processing
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect faces in the current frame
    detections = detector.detect_faces(frame_rgb)
    for detection in detections:
        x, y, w, h = detection['box']
        # Ensure positive coordinates
        x, y = max(0, x), max(0, y)
        # Draw a rectangle on the original frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Extract the face ROI and resize to (160, 160)
        face_roi = frame_rgb[y:y+h, x:x+w]
        try:
            face_resized = cv2.resize(face_roi, (160, 160))
        except Exception as e:
            continue
        
        face_array = np.expand_dims(face_resized, axis=0)
        # Compute the embedding for the detected face
        embedding = embedder.embeddings(face_array)[0]
        # Compare the embedding with the reference using cosine similarity
        sim = cosine_similarity(ref_embedding, embedding)
        label = "Reference" if sim > threshold else "Unknown"
        
        cv2.putText(frame, f"{label}: {sim:.2f}", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Calculate and display FPS
    elapsed = time.time() - start_time
    fps = frame_count / elapsed
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
    cv2.imshow("MTCNN + keras_facenet", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()