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
