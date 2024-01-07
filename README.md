# TrafficLens: Real-time Surveillance and Speed Monitoring

## Overview
Project-FWOD is a comprehensive system developed as part of a Bachelor's degree in Computer Engineering. It leverages Computer Vision and Deep Learning techniques to detect and track vehicles, estimate their speed, and generate insightful reports and visualizations.

## System Description
The system utilizes the YOLOv4 object detection algorithm and the DeepSORT algorithm for multi-object tracking. It employs OpenCV, an open-source computer vision library, for video processing, and Polygon Testing to determine when a vehicle enters and leaves a predefined region of interest.

The speed of a vehicle is estimated by defining two regions of interest along a lane of the road. When a vehicle enters the first region, a timer starts, and when it exits the second region, the timer stops. The time difference, along with the distance between the two regions, is used to estimate the vehicle's speed.

All data, including vehicle IDs, vehicle type, and speed, is stored in an Excel file. If a vehicle's speed exceeds a preset limit, the system captures an image of the vehicle and generates a PDF report. The system also creates a scatter plot to provide valuable insights into traffic patterns and trends.

## Installation and Usage (Mac - CPU Only)
To use this project on a Mac (CPU only) or make it usable via GUI on Windows, follow these steps:

1. Make necessary changes to `gui.py`.
2. Create a new conda environment: `conda env create -n ENVNAME --file project_env.yml`.
3. Install the required packages: `pip install -r requirements.txt`.
4. Download the necessary files from the provided links.
5. Navigate to the `Four_Wheeler_Overspeeding_Detection/checkpoints/yolov4-416/variables` directory and place the `variables.data-00000-of-00001` file in it.
6. Navigate to the `Four_Wheeler_Overspeeding_Detection/data` directory and place the `yolov4.weights` file in it.
7. Navigate back to the main directory: `cd Four_Wheeler_Overspeeding_Detection`.
8. Run the GUI: `python3 gui.py`.
9. Add a video from the `Assets_video` folder. For speed estimation, the following videos have been mapped: `traffic_int1.mp4`, `traffic_int2.mp4`, `koteshwor.mp4`, `balkumari.mp4`, `satdobato.mp4`.

If you want to use your custom video, learn how to make the boxes required for the polygon testing. Use the GIMP app to make a square in the frame for the video. Refer to the code for making area in `main.py`.

## Acknowledgements
This project was inspired by and references the work done by theAIGuysCode.
