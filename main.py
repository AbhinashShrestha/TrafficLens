import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from absl import app, flags
from absl.flags import FLAGS
import core.utils as utils
from core import *
# from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
from core.config import cfg
# from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tensorflow.compat.v1 import ConfigProto
# from tensorflow import ConfigProto,InteractiveSession
from tensorflow.compat.v1 import InteractiveSession
# deep sort imports
from deep_sort import preprocessing, nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
# flags.DEFINE_string('framework', 'tf', '(tf, tflite, trt')
flags.DEFINE_string('weights', './checkpoints/yolov4-416','path to weights file')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
flags.DEFINE_string('output_format', 'mp4v', 'codec used in VideoWriter when saving video to file')
flags.DEFINE_float('iou', 0.45, 'iou threshold')
flags.DEFINE_float('score', 0.50, 'score threshold')
flags.DEFINE_boolean('dont_show', False, 'dont show video output')
flags.DEFINE_boolean('count', False, 'count objects being tracked on screen')
import uuid
import json

with open('database_proxy.json') as f:
    data = json.load(f)

current_file = data['processed_filename']
#video 
video_folder = "Assets_videos" # Only those videos in this folder will work 
video_src = os.path.join(video_folder, current_file)
base_name = os.path.splitext(os.path.basename(video_src))[0]
unique_filename = 'Result_of_' + base_name + '_' + str(uuid.uuid4().hex)
output = f"outputs/{unique_filename}.mp4"
data['output_video_path'] = output
# Open the database_proxy.json file for writing and dump the updated dictionary back to the file
with open('database_proxy.json', 'w') as f:
    json.dump(data, f)
match base_name:
    case 'traffic_int1_processed': #has 524 frames about 13min
        region_of_interest_A1 = np.array([(6,600),(67,540),(633,540),(633,600)]) #A1
        region_of_interest_A1 = region_of_interest_A1.astype(np.int32) # convert to integer format
        region_of_interest_A2= np.array([(150,490),(230,437),(650,437),(650,490)]) #A2
        region_of_interest_A2 = region_of_interest_A2.astype(np.int32) # convert to integer format
        region_of_interest_B1= np.array([(660,380),(660,360),(922,360),(980,380)]) #B1
        region_of_interest_B1 = region_of_interest_B1.astype(np.int32) 
        region_of_interest_B2 = np.array([(710,520),(700,470),(1100,470),(1200,520)])# B2
        region_of_interest_B2 = region_of_interest_B2.astype(np.int32)
        gap_meter_A = 250
        gap_meter_B = 350

    case 'sankhamul_processed': #has 3206 frames
        #shankhamul
        region_of_interest_A1 = np.array([(245,440),(305,385),(595,385),(570,440)]) #A1
        region_of_interest_A1 = region_of_interest_A1.astype(np.int32) # convert to integer format
        region_of_interest_A2= np.array([(490,230),(525,200),(700,200),(678,230)]) #A2
        region_of_interest_A2 = region_of_interest_A2.astype(np.int32) # convert to integer format
        region_of_interest_B1= np.array([(675,245),(695,210),(900,210),(895,245)]) #B1
        region_of_interest_B1 = region_of_interest_B1.astype(np.int32) 
        region_of_interest_B2 = np.array([(553,525),(575,475),(930,475),(950,525)])# B2
        region_of_interest_B2 = region_of_interest_B2.astype(np.int32) 
        gap_meter_A = 360
        gap_meter_B = 350

    case 'balkumari_processed': #has 5065 frames
        #balkumari       
        region_of_interest_A1 = np.array([(3,390),(60,340),(570,340),(560,390)]) #A1
        region_of_interest_A1 = region_of_interest_A1.astype(np.int32) # convert to integer format
        region_of_interest_A2= np.array([(270,160),(320,120),(620,120),(605,160)]) #A2
        region_of_interest_A2 = region_of_interest_A2.astype(np.int32) # convert to integer format
        region_of_interest_B1= np.array([(635,200),(640,165),(1005,165),(1025,200)]) #B1
        region_of_interest_B1 = region_of_interest_B1.astype(np.int32) 
        region_of_interest_B2 = np.array([(610,380),(620,340),(1170,340),(1200,380)])# B2
        region_of_interest_B2 = region_of_interest_B2.astype(np.int32)
        gap_meter_A = 460
        gap_meter_B = 370
    
    case 'koteshwor_processed':
        region_of_interest_A1 = np.array([(60,390),(115,340),(580,340),(570,390)]) #A1
        region_of_interest_A1 = region_of_interest_A1.astype(np.int32) # convert to integer format
        region_of_interest_A2= np.array([(270,160),(320,120),(618,120),(605,160)]) #A2
        region_of_interest_A2 = region_of_interest_A2.astype(np.int32) # convert to integer format
        region_of_interest_B1= np.array([(635,200),(640,165),(1000,165),(1025,200)]) #B1
        region_of_interest_B1 = region_of_interest_B1.astype(np.int32) 
        region_of_interest_B2 = np.array([(615,380),(620,340),(1165,340),(1195,380)])# B2
        region_of_interest_B2 = region_of_interest_B2.astype(np.int32)
        gap_meter_A = 470
        gap_meter_B = 370
    
    case 'satdobato_processed': #has 723 frames
        region_of_interest_A1 = np.array([(25,260),(75,230),(405,230),(385,260)]) #A1
        region_of_interest_A1 = region_of_interest_A1.astype(np.int32) # convert to integer format
        region_of_interest_A2= np.array([(320,70),(340,50),(515,50),(505,70)]) #A2
        region_of_interest_A2 = region_of_interest_A2.astype(np.int32) # convert to integer format
        region_of_interest_B1= np.array([(448,175),(480,145),(1035,145),(1085,175)]) #B1
        region_of_interest_B1 = region_of_interest_B1.astype(np.int32) 
        region_of_interest_B2 = np.array([(355,348),(365,315),(1230,315),(1260,348)])# B2
        region_of_interest_B2 = region_of_interest_B2.astype(np.int32)
        gap_meter_A = 360
        gap_meter_B = 390
        
    case 'traffic_int2_processed': #723 frames and 15 minutes
        region_of_interest_A1 = np.array([(750,448),(750,400),(1202,400),(1292,440)]) #A1
        region_of_interest_A1 = region_of_interest_A1.astype(np.int32) # convert to integer format
        region_of_interest_A2= np.array([(715,333),(700,303),(973,303),(1051,333)]) #A2
        region_of_interest_A2 = region_of_interest_A2.astype(np.int32) # convert to integer format
        region_of_interest_B1= np.array([(279,384),(331,360),(700,362),(693,384)]) #B1
        region_of_interest_B1 = region_of_interest_B1.astype(np.int32) 
        region_of_interest_B2 = np.array([(115,477),(125,445),(687,445),(678,477)])# B2
        region_of_interest_B2 = region_of_interest_B2.astype(np.int32) 
        gap_meter_A = 480
        gap_meter_B = 380
    
WIDTH = 1280 #WIDTH OF VIDEO FRAME
HEIGHT = 720 #HEIGHT OF VIDEO FRAME
speedLimit = 50 #SPEEDLIMIT
def blackout(image):
    xBlack = 350
    yBlack = 350
    triangle_cnt = np.array( [[0,0], [xBlack,0], [0,yBlack]] )
    triangle_cnt2 = np.array( [[WIDTH,0], [WIDTH-xBlack,0], [WIDTH,yBlack]] )
    cv2.drawContours(image, [triangle_cnt], 0, (0,0,0), -1)
    cv2.drawContours(image, [triangle_cnt2], 0, (0,0,0), -1)

    return image

# Initialize dictionary to store saved images and IDs
saved_objects = {}
vehicle_info ={}
directory_path = f"overspeeding_vehicles_{base_name}"
# check if directory exists
if not os.path.exists(directory_path):
    # create directory
    os.mkdir(directory_path)
    
def save_detected_objects(frame,carid,class_name,box):
    x, y, width, height = box
    # path = f"overspeeding_vehicles_{base_name}"
    # crop detection from image (take an additional 5 pixels around all edges)
    cropped_img = frame[int(y)-5:int(height)+5, int(x)-5:int(width)+5]
    # construct image name and join it to path for saving crop properly
    img_name = class_name + '_' + str(carid) + '.png'
    img_path = os.path.join(directory_path, img_name)
    # save image
    cv2.imwrite(img_path, cropped_img)

def main(_argv):
    # Definition of the parameters
    max_cosine_distance = 0.4#
    nn_budget = None
    nms_max_overlap = 1.0

    # initialize deep sort
    model_filename = 'deep_sort_model/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename, batch_size=1)
    # calculate cosine distance metric
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    # initialize tracker
    tracker = Tracker(metric)

    # load configuration for object detector
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)
    input_size = FLAGS.size
    video_path = video_src

  
    saved_model_loaded = tf.saved_model.load(FLAGS.weights, tags=[tag_constants.SERVING])
    infer = saved_model_loaded.signatures['serving_default']

    # begin video capture
    try:
        vid = cv2.VideoCapture(int(video_path))
    except:
        vid = cv2.VideoCapture(video_path)

    out = None

    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
    out = cv2.VideoWriter(output, codec, fps, (width, height))


    frame_num = 0
    vehicle_in_roi_A= {}
    vehicle_run_time_A = {}
    vehicle_in_roi_B= {}
    vehicle_run_time_B = {}
   
    
    # while video is running
    while True:
        return_value, frame = vid.read()
        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        else:
            print('Video has ended or failed, try a different video format!')
            break
        
        frame = blackout(frame)

        frame_num = frame_num + 1
        print('Frame #: ', frame_num)
        
        
        image_data = cv2.resize(frame, (input_size , input_size))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)

        batch_data = tf.constant(image_data)
        pred_bbox = infer(batch_data)
        for key, value in pred_bbox.items():
            boxes = value[:, :, 0:4]
            pred_conf = value[:, :, 4:]
            
            
        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=FLAGS.iou,
            score_threshold=FLAGS.score
        )

        # convert data to numpy arrays and slice out unused elements
        num_objects = valid_detections.numpy()[0]
        bboxes = boxes.numpy()[0]
        bboxes = bboxes[0:int(num_objects)]
        scores = scores.numpy()[0]
        scores = scores[0:int(num_objects)]
        classes = classes.numpy()[0]
        classes = classes[0:int(num_objects)]

        # format bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, width, height
        original_h, original_w, _ = frame.shape
        bboxes = utils.format_boxes(bboxes, original_h, original_w)

        # store all predictions in one parameter for simplicity when calling functions
        pred_bbox = [bboxes, scores, classes, num_objects]

        # read in all class names from config
        class_names = utils.read_class_names(cfg.YOLO.CLASSES)

        # by default allow all classes in .names file
        # allowed_classes = list(class_names.values())
        
        # custom allowed classes (uncomment line below to customize tracker for only people)
        allowed_classes = ['car']

        # loop through objects and use class index to get class name, allow only classes in allowed_classes list
        names = []
        deleted_indx = []
        for i in range(num_objects):
            class_indx = int(classes[i])
            class_name = class_names[class_indx]
            if class_name not in allowed_classes:
                deleted_indx.append(i)
            else:
                names.append(class_name)
        names = np.array(names)
        # count = len(names)
        # if FLAGS.count:
            # cv2.putText(frame, "Objects being tracked: {}".format(count), (5, 35), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 255, 0), 2)
            # print("Objects being tracked: {}".format(count))
            
            
        # delete detections that are not in allowed_classes
        bboxes = np.delete(bboxes, deleted_indx, axis=0)
        scores = np.delete(scores, deleted_indx, axis=0)

        # encode yolo detections and feed to tracker
        features = encoder(frame, bboxes)
        #  The YOLOv4 model generates bounding boxes
        # around detected objects within an image and provides 
        # a confidence score for each detection. 
        # Additionally, the model outputs the class name 
        # of the detected object and a feature vector 
        # that may be utilized for further processing, such as object tracking.
        detections = [Detection(bbox, score, class_name, feature) for bbox, score, class_name, feature in zip(bboxes, scores, names, features)]

        #initialize color map
        cmap = plt.get_cmap('tab20b')
        colors = [cmap(i)[:3] for i in np.linspace(0, 1, 20)]
        
        
        # run non-maxima supression
        boxs = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        classes = np.array([d.class_name for d in detections])
        indices = preprocessing.non_max_suppression(boxs, classes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]       

        # Call the tracker
        tracker.predict()
        tracker.update(detections)
    
    
        #drawing lines
        # cv2.polylines(frame,[region_of_interest_A1],True,(15,220,10),3)
        # cv2.polylines(frame,[region_of_interest_A2],True,(15,220,10),3)
        # cv2.polylines(frame,[region_of_interest_B1],True,(15,220,10),3)
        # cv2.polylines(frame,[region_of_interest_B2],True,(15,220,10),3)
        # update tracks
        # Loop through tracked objects and store their locations
        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            bbox = track.to_tlbr()
            # object_id = track.track_id
            class_name = track.get_class()
            x = int(bbox[0])
            y = int(bbox[1])
            w = int(bbox[2]) #xmax
            h = int(bbox[3]) #ymax
            centerX=int((x+w)/2)
            centerY= int((y+h)/2)
            object_center = (centerX,centerY)
            
            # LANE B
            is_inside_area_B1 = cv2.pointPolygonTest(region_of_interest_B1, object_center, False) 
            if is_inside_area_B1 >= 0:
                vehicle_in_roi_B[track.track_id] = time.time()

            
            if track.track_id in vehicle_in_roi_B:
            # elif not is_inside and timer_started:
                is_inside_area_B2= cv2.pointPolygonTest(region_of_interest_B2, object_center, False) 
                if is_inside_area_B2>=0:
                    elapsed_time = time.time() - vehicle_in_roi_B[track.track_id]
                    
                    if track.track_id not in vehicle_run_time_B:
                        vehicle_run_time_B[track.track_id] = elapsed_time
                    
                    if track.track_id in vehicle_run_time_B:
                        elapsed_time = vehicle_run_time_B[track.track_id]
                
                    # gap_meter_B = gap_meter_B
                    speed_ms = gap_meter_B/elapsed_time
                    speed = speed_ms * 3.6 
                    # Add the vehicle's ID and speed to the dictionary
                    vehicle_info[track.track_id] = {'Vehicle Type': class_name, 'Vehicle id': track.track_id, 'Speed (km/hr)': round(speed, 2)}
                    # print(vehicle_info)
                    if speed > speedLimit:
                        save_detected_objects(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),track.track_id,class_name,bbox)
                        print("yes")

                    cv2.putText(frame, 'Speed: {:.2f} km/h'.format(speed),(int(bbox[0]), int(bbox[1]-40)),0, 0.75, (255,255,255),2)
            
            # LANE A
            is_inside_area_A1 = cv2.pointPolygonTest(region_of_interest_A1, object_center, False) 
            if is_inside_area_A1 >= 0:
                vehicle_in_roi_A[track.track_id] = time.time()

            
            if track.track_id in vehicle_in_roi_A:
            # elif not is_inside and timer_started:
                is_inside_area_A2= cv2.pointPolygonTest(region_of_interest_A2, object_center, False) 
                if is_inside_area_A2>=0:
                    elapsed_time = time.time() - vehicle_in_roi_A[track.track_id]
                    
                    if track.track_id not in vehicle_run_time_A:
                        vehicle_run_time_A[track.track_id] = elapsed_time
                    
                    if track.track_id in vehicle_run_time_A:
                        elapsed_time = vehicle_run_time_A[track.track_id]
                
                    # gap_meter_A = 250
                    speed_ms = gap_meter_A/elapsed_time
                    speed = speed_ms * 3.6 
                    # Add the vehicle's ID and speed to the dictionary
                    vehicle_info[track.track_id] = {'Vehicle Type': class_name, 'Vehicle id': track.track_id, 'Speed (km/hr)': round(speed, 2)}
                    if speed > speedLimit:
                        save_detected_objects(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),track.track_id,class_name,bbox)
                        print("yes")
                    # print(vehicle_info)
                    cv2.putText(frame, 'Speed: {:.2f} km/h'.format(speed),(int(bbox[0]), int(bbox[1]-40)),0, 0.75, (255,255,255),2)
            # draw bbox on screen
            color = colors[int(track.track_id) % len(colors)]
            color = [i * 255 for i in color]
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1]-30)), (int(bbox[0])+(len(class_name)+len(str(track.track_id)))*17, int(bbox[1])), color, -1)
            cv2.putText(frame, class_name + "-" + str(track.track_id),(int(bbox[0]), int(bbox[1]-10)),0, 0.75, (255,255,255),2)
           
            
        result = np.asarray(frame)
        result = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        
        
        if not FLAGS.dont_show:
            cv2.imshow("Output Video", result)
        
        # if output flag is set, save video file
        # if FLAGS.output:
        out.write(result)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
        
    #after the video ends
    try:
        # Data Manipulation and Analysis Part using Pandas, Matplotlib 

        vehicle_info[track.track_id] = {'Vehicle Type': class_name, 'Vehicle id': track.track_id, 'Speed (km/hr)': round(speed, 2)}
        sorted_data = sorted(vehicle_info.values(), key=lambda x: x['Vehicle id'])

        # Create a DataFrame from the sorted data
        df = pd.DataFrame(sorted_data)

        excel_file= 'vehicle_info.xlsx'
        filename = os.path.join(directory_path, excel_file)
        df.to_excel(filename, index=False)
        
        # only overspeeding vehicles are in a new one
        # Filter the data with speeds greater than the speed limit
        # speed_limit = 60
        filtered_data = [data for data in vehicle_info.values() if data['Speed (km/hr)'] > speedLimit]
        
        # Sort the filtered data by Vehicle id from smallest to highest
        filtered_data = sorted(filtered_data, key=lambda x: x['Vehicle id'])
        # Create a DataFrame from the filtered data
        df_filtered = pd.DataFrame(filtered_data)

        # Write the filtered DataFrame to a new Excel file
        excel_file_overspeeding_only = 'overspeeding_vehicles.xlsx'
        filename_filtered = os.path.join(directory_path, excel_file_overspeeding_only)
        df_filtered.to_excel(filename_filtered, index=False)
        
        # using matplotlib to make a graph
        
        # Create a list of speeds and IDs
        speeds = [vehicle_info[id]['Speed (km/hr)'] for id in vehicle_info]
        ids = [vehicle_info[id]['Vehicle id'] for id in vehicle_info]

        # Create a bar graph
        # plt.bar(ids, speeds)
        plt.scatter(ids, speeds)

        # Add labels and title to the graph
        plt.xlabel('Vehicle IDs')
        plt.ylabel('Speed (km/h)')
        plt.title('Speed Analysis')

        # Save the graph as a PNG image
        graph_name = f'Speed Analysis_of_{base_name}.png'
        plt.savefig(graph_name)
        with open('database_proxy.json') as f:
            data = json.load(f)
        data['graph'] = graph_name
        with open('database_proxy.json', 'w') as f:
            json.dump(data, f)
    except:
        analyze_error = "No Overspeeding Detected"
        with open('database_proxy.json') as f:
            data = json.load(f)
        data['analyze_error'] = analyze_error
        with open('database_proxy.json', 'w') as f:
            json.dump(data, f)

    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
