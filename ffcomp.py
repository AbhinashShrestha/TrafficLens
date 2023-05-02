# multiple video processing code
# import os
# import subprocess
# # Provide the path to the folder you want to count files in
# folder_path = "../Assets_videos"

# # Get the list of all files in the folder
# files = os.listdir(folder_path)

# # Filter the list of files to only include files with the .mp4 extension
# mp4_files = [file for file in files if file.endswith('.mp4')]

# # Count the number of .mp4 files in the folder
# number_of_mp4_files = len(mp4_files)

# # Print the result
# print("Number of .mp4 files in the folder:", number_of_mp4_files)
# def video_processing(i):
#     # Set the input and output file paths
#     input_file = f'../Assets_videos/traffic_{i}.mp4'
#     print(input_file)
#     base_name = os.path.splitext(os.path.basename(input_file))[0]
#     output_file = f'../Assets_videos/{base_name}_processed.avi'

#     # Set the codec and quality level
#     codec = 'libx264'  # try a different codec
#     quality = 35  # try a different quality level

#     # Set the frame rate and resolution
#     fps = 10
#     resolution = '1280x720'  # try a higher resolution

#     # Build the FFmpeg command
#     command = ['ffmpeg', '-y', '-i', input_file, '-c:v', codec, '-crf', str(quality), '-b:v', '200K', '-r', str(fps), '-s', resolution, output_file]

#     # Run the command
#     subprocess.run(command)
# for i in range(number_of_mp4_files):
#     print(f'{i+1} video is being processed')
#     video_processing(i+1)

# single video processing code
import os
import subprocess
import json

# Set the input and output file paths
with open('database_proxy.json') as f:
    data = json.load(f)
current_file = data['filename']
#video 
video_folder = "Assets_videos"
input_file = os.path.join(video_folder, current_file)
# input_file = 'Assets_videos/traffic_13.mp4'
base_name = os.path.splitext(os.path.basename(input_file))[0]
output_file = f'Assets_videos/{base_name}_processed.mp4'
processed_output = os.path.splitext(os.path.basename(output_file))[0] + '.mp4'  # Add the extension

# Set the codec and quality level
codec = 'libx264'  # try a different codec
quality = 30  # try a different quality level

# Set the frame rate and resolution
fps = 24
resolution = '1280x720'  # try a higher resolution

# Build the FFmpeg command
command = ['ffmpeg', '-y', '-i', input_file, '-c:v', codec, '-crf', str(quality), '-b:v', '300K', '-r', str(fps), '-s', resolution, output_file]

# Run the command
subprocess.run(command)
# Write base_name_output back to JSON file
data['processed_filename'] = processed_output
with open('database_proxy.json', 'w') as f:
    json.dump(data, f)