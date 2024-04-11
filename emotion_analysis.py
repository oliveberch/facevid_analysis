# Install required packages - deepface

# Clone the deepface repository https://github.com/serengil/deepface.git

# Import necessary libraries
import cv2
from deepface import DeepFace
from collections import Counter

# Function to calculate the overall dominant emotion
def calculate_overall_emotion(emotions_list):
    """
    Calculate the overall dominant emotion based on a list of emotion predictions.

    Parameters:
    emotions_list (list): List of dictionaries containing emotion predictions for each frame.

    Returns:
    str: The overall dominant emotion.
    """
    overall_emotion_count = Counter()

    # Count the occurrences of each emotion across all frames
    for result in emotions_list:
        for emotion, confidence in result['emotion'].items():
            overall_emotion_count[emotion] += confidence
    
    # Find the emotion with the highest total confidence
    overall_emotion = overall_emotion_count.most_common(1)[0][0]
    
    return overall_emotion

# Load the pre-trained emotion detection model
DeepFace.build_model("Emotion")

# OpenCV video capture
video_path = "/content/MicrosoftTeams-video.mp4"
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Unable to open video")
    exit()

# List to store results for all frames
all_results = []

# Main loop to process each frame in the video
while cap.isOpened():
    # Read a frame from the video
    ret, frame = cap.read()

    if not ret:
        # Break the loop if there are no more frames
        break

    # Try to detect emotions in the frame
    try:
        # Analyze the emotions in the frame
        results = DeepFace.analyze(frame, actions=['emotion'])
        
        # Extend the list of results with the new analysis
        all_results.extend(results)
        
        # For visualization:
        # You may want to draw the detected emotions on the frame
        # For simplicity, we're just printing the results

    except Exception as e:
        # Skip frame if there's an error
        # print("Error:", e)
        continue

# Calculate the overall dominant emotion based on all frames
overall_emotion = calculate_overall_emotion(all_results)
print("Overall Dominant Emotion:", overall_emotion)

# Release the video capture object
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
