# Smart Cap

The **Smart Cap** is an innovative wearable device that transforms a simple cap into a multifunctional assistant. By integrating Artificial Intelligence (AI), navigation technologies, and object recognition, this cap is designed to make daily tasks easier and hands-free.

## Features

- **Hands-Free Navigation**: Get real-time directions using Google Maps.
- **Object Recognition**: Identify objects in your surroundings with AI.
- **Voice Interaction**: Interact through voice commands for various tasks.
- **AI Chat Assistant**: Use Gemini AI to chat and find information on the go.
- **Weather Updates**: Receive real-time weather information.
- **Multimedia Support**: Play music and access other multimedia features.

## Components

### Hardware
- **Raspberry Pi 4 Model B+**: Core processing unit.
- **Pi Camera**: Captures images for object detection.
- **Mini Speakers and Microphone**: Enable voice interaction.
- **Power Bank**: Provides power for the setup.
- **Cap Structure**: Physical structure to house the components.

### Software
- **Gemini API**: Facilitates AI Chat Assistant.
- **Google Maps API**: Facilitates navigation features.
- **TensorFlow Lite**: Used for object recognition.

## How It Works

1. **Setup**: Install necessary Python packages and configure the Raspberry Pi with Raspberry Pi OS.
2. **Integration**: Combine Gemini AI, Google Maps API, and TensorFlow Lite for seamless operation.
3. **Functionality**: 
   - Use voice commands to interact with the assistant.
   - Navigate hands-free using real-time directions.
   - Identify objects with the Pi Camera and AI.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Jain131102/Smart-Cap.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Smart-Cap
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the setup script:
   ```bash
   bash setup.sh
   ```

## Usage

1. **Power on the Smart Cap**: Ensure the device is powered on and ready for use.
2. **Interact with the Assistant**: Use voice commands to interact with the assistant for various tasks.
3. **Access the Menu System**: Navigate through the menu for tasks like navigation, object recognition, and multimedia playback.

## Demo

[Watch the demo video](https://drive.google.com/drive/folders/1L7OMiA4udsOSYj4fNBuk2qjQIA-oRngw?usp=sharing)

## Future Scope

- Enhanced object detection for better accuracy.
- Offline map capabilities for travel and navigation.
- Integration with advanced AI technologies.

## References

- [Raspberry Pi](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
- [OpenCV](https://opencv.org/)
- [Google Maps Directions API](https://developers.google.com/maps/documentation/directions/start)
- [SpeechRecognition Library](https://pypi.org/project/SpeechRecognition/)
- [Google Text-to-Speech](https://cloud.google.com/text-to-speech)
- [PyTorch](https://pytorch.org/)
- [Pygame](https://www.pygame.org/news)

## License
This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

