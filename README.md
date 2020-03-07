# TSRTC-Bus-data-extraction-and-modelling
## 1. Data extraction from raw csv files.
Run Python Code - `python Data_conversion.py`
### Results - 
### Raw Csv File
![Image description](https://github.com/Pranjalbond007/TSRTC-Bus-data-extraction-and-modelling/blob/master/images/rawcsv.png)
### Parameter Csv File
![Image description](https://github.com/Pranjalbond007/TSRTC-Bus-data-extraction-and-modelling/blob/master/images/paracsv.png)

## 2. Data Segmentation into acceleration and deceleration events in a real time data
Run Python Code - `python Data_segmentation.py`
### Results - 
### Graph Showing acceleration events - higher to lower dotted point and deceleration events - lower to higher dotted points
![Image description](https://github.com/Pranjalbond007/TSRTC-Bus-data-extraction-and-modelling/blob/master/images/segmentation.jpg)

### Extracted Acceleration Events with significant parameters (each row belongs to an acceleration events)
Parameters:- T1-initial time, T2-final time	V1-initial velocity, V2-final velocity, V2-V1-Total velocity, D2-D1-Total distance covered, T2-T1- Total time, Max LA- Maximum longitudinal acceleration, Avg LA- Average longitudinal acceleration, yaw_max- Maximum yawrate, yaw_avg- Average yawrate, max_jerk- Maximum jerk, avg_jerk- Average jerk, init_lat- intial lattitude, init_long- initial longitude, final_lat- final lattitude, final_long- final longitude, FileName- Driver csv file 

![Image description](https://github.com/Pranjalbond007/TSRTC-Bus-data-extraction-and-modelling/blob/master/images/events.png)

### Extracted Deceleration Events with significant parameters (each row belongs to an acceleration events)
Parameters:- T1-initial time, T2-final time	V1-initial velocity, V2-final velocity, V2-V1-Total velocity, D2-D1-Total distance covered, T2-T1- Total time, Min LA- Minimum longitudinal acceleration, Avg LA- Average longitudinal acceleration, yaw_max- Maximum yawrate, yaw_avg- Average yawrate, min_jerk- Minimum jerk, avg_jerk- Average jerk, init_lat- intial lattitude, init_long- initial longitude, final_lat- final lattitude, final_long- final longitude, FileName- Driver csv file
![Image description](https://github.com/Pranjalbond007/TSRTC-Bus-data-extraction-and-modelling/blob/master/images/dec_events.png)

## 3. Predicting Driver Behaviour using Unsupervised Clustering for Acceleration events
Run Python Code - `python Acceleration_events_Clustering.py`
### Results - 
### Scatter Plot of driver characteristics in 6 different clusters
![Image description](https://github.com/Pranjalbond007/TSRTC-Bus-data-extraction-and-modelling/blob/master/images/acc_3d_plot.png)
### Box Plot of driver characteristics in 6 different clusters
![Image description](https://github.com/Pranjalbond007/TSRTC-Bus-data-extraction-and-modelling/blob/master/images/box_plot_acc.jpg)


## 3. Predicting Driver Behaviour using Unsupervised Clustering for Deceleration events
Run Python Code - `python Deceleration_events_Clustering.py`
### Results - 
### Scatter Plot of driver characteristics in 6 different clusters
![Image description](https://github.com/Pranjalbond007/TSRTC-Bus-data-extraction-and-modelling/blob/master/images/dec_3dplot_v2-v1.png)
### Box Plot of driver characteristics in 6 different clusters
![Image description](https://github.com/Pranjalbond007/TSRTC-Bus-data-extraction-and-modelling/blob/master/images/box_plot_dec.jpg)
