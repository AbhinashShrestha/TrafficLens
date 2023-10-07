# Project-FWOD

A project i created for my Minor Project in Bachelor in Computer Engineering
ABSTRACT
This is a Computer Vision and Deep Learning System which detects vehicles, tracks them, assigns them ids, estimates their speed and generates a pdf report and creates a scatter plot. The system employs the YOLOv4 object detection algorithm and the DeepSORT algorithm for multi-object tracking. The system uses OpenCV, an open-source computer vision library, to load and modify video footage, and Polygon Testing which is used to determine when a vehicle enters and leaves a predefined region of interest. To estimate the speed of a vehicle, the system uses the unique IDs of each vehicle detected and tracked by YOLOv4 and DeepSORT respectively in the video stream after which it defines two regions of interest along a lane of the road. When a vehicle enters the first region, a timer starts, and when it exits the second region, the timer stops. The time difference, along with the distance between the two regions, is used to estimate the vehicle's speed. All data, including vehicle IDs, vehicle type, and speed, is stored in an Excel file. If a vehicle's speed exceeds a preset limit, the system captures an image of the vehicle and generates a PDF report which contains the Vehicle type, Speed, Vehicle Id and the image of the vehicle. Additionally, the system creates a scatter plot which provides valuable insights into traffic patterns and trends that helps visualize and analyze the traffic flow.





how to use the project on mac (cpu only) 
to make this usable via gui on windows . 
make needed changes to gui.py

conda env create -n ENVNAME --file project_env.yml
pip install -r requirements.txt

Download the files from the links 

https://anonfiles.com/XbH3I0ofzc/yolov4_weights(doesnt exist)
https://anonfiles.com/v5GdIco5zc/variables_data_00000_of_00001






Then go to the folder Four_Wheeler_Overspeeding_Detection/checkpoints/yolov4-416/variables






Then place the file "variables.data-00000-of-00001" in the folder such that the location of the file is Four_Wheeler_Overspeeding_Detection/checkpoints/yolov4-416/variables/variables.data-00000-of-00001





Come back to main folder and go to the folder Four_Wheeler_Overspeeding_Detection/data







And place the file "yolov4.weights" in the folder such that data/yolov4.weights

now
cd Four_Wheeler_Overspeeding_Detection


python3 gui.py
add a video from the Assets_video folder
for speed estimation only the below videos have been mapped.
traffic_int1.mp4
traffic_int2.mp4
koteshwor.mp4
balkumari.mp4
satdobato.mp4





#if you want to use your custom video then learn how to make the boxes required for the polygon testing. 
go to the gimp app. 
use it to make a a square in the frame for the video. look at the code for making area in main.py.



reference and thanks to
https://github.com/theAIGuysCode/yolov4-deepsort.
