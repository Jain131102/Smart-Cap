#!/bin/bash

# Object Detection
# Clone the TensorFlow examples Git repository
git clone https://github.com/tensorflow/examples --depth 1

# Create virtual environment
python3 -m pip install virtualenv

# Check Python version
python3 --version
sudo apt update && sudo apt install -y software-properties-common \
&& sudo add-apt-repository -y ppa:deadsnakes/ppa \
&& sudo apt update && sudo apt install -y python3.7 python3.7-distutils python3-pip

# Navigate to the examples directory
cd examples

# Create a Python 3.7 virtual environment
python3.7 -m venv tf

# List the files and directories (Optional)
ls

# Activate the virtual environment
source tf/bin/activate

# Navigate to the Raspberry Pi object detection example directory
cd lite/examples/object_detection/raspberry_pi

# Run the setup script to install dependencies and download the TFLite models
sh setup.sh

# Note: The setup script installs the TensorFlow Lite runtime (tflite_runtime) instead of the full TensorFlow package.

# Upgrade tflite-support after setup.sh finishes
python -m pip install --upgrade tflite-support==0.4.3
#!/bin/bash

# Overwrite detect.py with the desired content
cat <<EOF > detect.py
import subprocess
import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils

def capture_image(filename="test_image.jpg"):
"""
Capture an image using libcamera-still and save it to a file.
Args:
filename (str): Name of the file to save the image.
"""
try:
# Use espeak to announce the start of the image capture process
subprocess.run(["espeak", "Clicking picture"], check=True)

# Capture image using libcamera-still without preview
subprocess.run(["sudo", "libcamera-still", "-o", filename], check=True)

# Use espeak to announce completion of image capture
subprocess.run(["espeak", "Picture clicked"], check=True)

print(f"Image captured and saved as {filename}")

except subprocess.CalledProcessError as e:
print("Failed to capture image:", e)


def rotate_image(image_path, output_path, rotations=2):
"""
Rotate the image 90 degrees to the right a specified number of times and save it.
Args:
image_path (str): Path to the image file to rotate.
output_path (str): Path to save the rotated image.
rotations (int): The number of 90-degree clockwise rotations to apply.
"""
# Load the image from file
image = cv2.imread(image_path)

# Apply rotations
rotations = rotations % 4
for _ in range(rotations):
image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

# Save the rotated image
cv2.imwrite(output_path, image)
print(f"Rotated image saved as {output_path}")
return output_path


def detect_and_announce_objects(image_path, model="efficientdet_lite0.tflite"):
"""
Detect objects in an image and announce the detected objects with voice.
Args:
image_path (str): Path to the image file.
model (str): Path to the TFLite object detection model.
"""
# Load the rotated image
image = cv2.imread(image_path)

# Initialize the object detection model
base_options = core.BaseOptions(
file_name=model, use_coral=False, num_threads=4)
detection_options = processor.DetectionOptions(
max_results=3, score_threshold=0.3)
options = vision.ObjectDetectorOptions(
base_options=base_options, detection_options=detection_options)
detector = vision.ObjectDetector.create_from_options(options)

# Convert the image from BGR to RGB as required by the TFLite model
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Create a TensorImage object from the RGB image
input_tensor = vision.TensorImage.create_from_array(rgb_image)

# Run object detection estimation using the model
detection_result = detector.detect(input_tensor)

# Collect detected object names
detected_objects = [detection.categories[0].category_name
for detection in detection_result.detections]

# Announce detected objects
if detected_objects:
announcement = "Detected objects are: " + ", ".join(detected_objects)
else:
announcement = "No objects detected."

# Use espeak to announce detected objects
subprocess.run(["espeak", announcement], check=True)
print(announcement)


# Main function to capture, rotate, detect, and announce
def main():
image_path = "captured_image.jpg"
rotated_image_path = "rotated_image.jpg"

# Step 1: Capture the image
capture_image(filename=image_path)

# Step 2: Rotate the image
rotated_image_path = rotate_image(image_path, rotated_image_path, rotations=2)

# Step 3: Detect and announce objects in the rotated image
detect_and_announce_objects(rotated_image_path)

# Exit the program
print("Finished object detection and announcement. Exiting.")


if __name__ == '__main__':
main()
EOF

#echo "detect.py has been updated."


# Deactivate the virtual environment (optional)
# deactivate
