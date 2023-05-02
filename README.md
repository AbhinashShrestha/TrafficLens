# Project-FWOD

how to use the project 

conda env create -n ENVNAME --file project_env.yml

Download the files from the links 

https://anonfiles.com/XbH3I0ofzc/yolov4_weights
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




