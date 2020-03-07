#!/usr/bin/env python
# coding: utf-8

#Aim:- To Segment Data into Acceleration and Deceleration events for all csv data files in folder

# In[1]:
#Imported Required Python Libraries
import pandas as pd
import glob
from math import sqrt
from statistics import mean 

#Specify Path of folder in which file is located
path = r'C:\Users\pranjal\Desktop\IITH project\Data2\Ramesh_csv' # use your path

#Reads all .csv from the folder
all_files = glob.glob(path + "/*.csv")

#Initialize array which contains Acceleration and Deceleration events
lia=[]
lid=[]
#Main Loop which takes each file and implement in the code
for csvfile in all_files:
	
	####
    splitlist=[]
    route=[]
    splitlist=csvfile.split('\\')
    print(splitlist[-1])
    strlist=str(splitlist[-1])
    route=strlist.split('_')
    #Returns route[2] of the data file ie LI,IL,MiyaIIT etc
    #Returns strlist which contains name of the data file
    
    #Read csv file
    df=pd.read_csv(csvfile,index_col=0, header=0)
    
    #Removing the datapoints which are inside certain GPS coordinate 
    #For IL route , Removing datapoints which are inside IIT campus and after Bhel circle 
    if route[2]=='IL':
        print(route[2])
        # Goal GPS coordinates provided for data reduction
        # Abbreviations - mg = main gate IIT, lin = lingampally station, lat = lattitude, long = longitude
        mg_lat=17.579800     
        mg_long=78.121580
        lin_lat=17.49528
        lin_long=78.31685

        #List which stores lat and long of data
        latlist=[]
        longlist=[]
        #List which stores distance from goal lat and long to current lat and long
        dist_mglist=[]
        dist_linlist=[]
        
        full_list=df.values.tolist()
        #Loop for appending all lat and long values
        for i in range(len(full_list)):
            latlist.append(full_list[i][5])
            longlist.append(full_list[i][6])
            
        #Loop for calculating distance of current position and goal position and appending it to a list
        for lat,long in zip(latlist,longlist):
            #print("{},{}".format(lat,long))
            distancemg=sqrt(pow(mg_lat-lat,2)+pow(mg_long-long,2))
            dist_mglist.append(distancemg)
            distancelin=sqrt(pow(lin_lat-lat,2)+pow(lin_long-long,2))
            dist_linlist.append(distancelin)
        
        #Taking index which has smallest distance in both cases ie towards mg and lin   
        row_reduce_start=dist_mglist.index(min(dist_mglist))
        row_reduce_end=dist_linlist.index(min(dist_linlist))
        print('{},{}'.format(row_reduce_start,row_reduce_end))
        
        #Finally reducing the start and end datapoints
        df1=df.iloc[row_reduce_start:row_reduce_end+1]
    
    #For LI route , Removing datapoints which are inside bhel circle and after main gate IIT
    elif route[2]=='LI':
        print(route[2])
        mg_lat=17.579800
        mg_long=78.121580
        lin_lat=17.49556
        lin_long=78.3154
        latlist=[]
        longlist=[]
        dist_mglist=[]
        dist_linlist=[]
        full_list=df.values.tolist()
        for i in range(len(full_list)):
            latlist.append(full_list[i][5])
            longlist.append(full_list[i][6])
            
        for lat,long in zip(latlist,longlist):
            #print("{},{}".format(lat,long))
            distancemg=sqrt(pow(mg_lat-lat,2)+pow(mg_long-long,2))
            dist_mglist.append(distancemg)
            distancelin=sqrt(pow(lin_lat-lat,2)+pow(lin_long-long,2))
            dist_linlist.append(distancelin)
            
        row_reduce_start=dist_linlist.index(min(dist_linlist))
        row_reduce_end=dist_mglist.index(min(dist_mglist))
        print('{},{}'.format(row_reduce_start,row_reduce_end))
        
        df1=df.iloc[row_reduce_start:row_reduce_end+1]
        
    #For OTHER route , Removing datapoints which are main gate IIT.    
    else:
        print(route[2])
        mg_lat=17.579800
        mg_long=78.121580
        latlist=[]
        longlist=[]
        dist_list=[]
        full_list=df.values.tolist()
        for i in range(len(full_list)):
            latlist.append(full_list[i][5])
            longlist.append(full_list[i][6])
            
        for lat,long in zip(latlist,longlist):
            #print("{},{}".format(lat,long))
            distance=sqrt(pow(mg_lat-lat,2)+pow(mg_long-long,2))
            dist_list.append(distance)
            
        row_reduce=dist_list.index(min(dist_list))
        print(row_reduce)
        if row_reduce>10000:
            df1=df.iloc[:row_reduce+1,]
        else:
            df1=df.iloc[row_reduce:len(df),]

    full_list=df1.values.tolist()
    vlist1=[]
    for i in range(len(full_list)):
        vlist1.append(full_list[i][0])
    
    #from datetime import datetime
    #df = pd.read_csv('iithproject1.csv')
    #df1['acceleration'] = (df1['Velocity'] - df1['Velocity'].shift(1)) / (df1['ElapsedTime'] - df1['ElapsedTime'].shift(1))
    df1['yaw_rate']=abs(df1['Heading'] - df1['Heading'].shift(1)) #8
    
    ind1=df1[(df1['Heading'].shift(1)<90) & (df1['Heading']>270)]['Heading'].index.tolist()
    df1['yaw_rate'].loc[ind1]=abs((360-df1['Heading'])+df1['Heading'].shift(1))
    
    ind2=df1[(df1['Heading'].shift(1)>270) & (df1['Heading']<90)]['Heading'].index.tolist()
    df1['yaw_rate'].loc[ind2]=abs(df1['Heading']+(360-df1['Heading'].shift(1)))
    
    df1['jerk']=(df1['LongitudinalAcceleration'] - df1['LongitudinalAcceleration'].shift(1)) / (df1['ElapsedTime'] - df1['ElapsedTime'].shift(1)) #9
    cumsum, vlist_mavg = [0], []
    N = 3
    for i, x in enumerate(vlist1, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            vlist_mavg.append(moving_ave)
    vlist_mavg.append(0)
    vlist_mavg.append(0)
    df1['mavg_velocity']=vlist_mavg #10
    
    df1['mavg_acceleration']=((df1['mavg_velocity'] - df1['mavg_velocity'].shift(1)) / (df1['ElapsedTime'] - df1['ElapsedTime'].shift(1)))*5/18 #11
    df1['mavg_jerk']=(df1['mavg_acceleration'] - df1['mavg_acceleration'].shift(1)) / (df1['ElapsedTime'] - df1['ElapsedTime'].shift(1)) #12
    
    df=df1.fillna(0)
    df=df1.fillna(0)
    
    # Appending all values of velocity, distance, elapsed time, long acceleration into different list
    full_list=[]
    full_list=df.values.tolist()
    alist=[]
    vlist=[]
    tlist=[]
    lolist=[]
    dlist=[]
    ylist=[]
    jlist=[]
    mavg_jlist=[]
    for i in range(len(full_list)):
        vlist.append(full_list[i][0])
        dlist.append(full_list[i][1])
        tlist.append(full_list[i][2])
        lolist.append(full_list[i][4])
        ylist.append(full_list[i][8])
        jlist.append(full_list[i][9])
        mavg_jlist.append(full_list[i][12])
    
    alist=lolist
    # Seperating Positive acceleration and negative acceleration into seperate dictionary
    # Here dictionary is taken as it stores index as key and acceleration as values
    positive={}
    negative={}
    d={}
    k=0
    for i in range(1,len(alist)):
    
        if alist[i-1]>0 and alist[i]<0:
            d[k]=positive
            k=k+1
            positive={}
    
        if alist[i-1]<0 and alist[i]>0:
            d[k]=negative
            k=k+1
            negative={}
    
        if alist[i]>0:
            positive[i]=alist[i]
    
    
        elif alist[i]<0:
            negative[i]=alist[i]
    
    # Removing all dictionary which have less than 3 elements
    j=0
    for j in range(len(d)):
        #print('{} is {}'.format(j,len(l[j])))
        if len(d[j].values())<3:
            del d[j]
    

    # Seperating the dictionary into consecutive positive and negative acceleration 
    k=[]
    k=list(d.values())
    d1={}
    for i in range(len(k)):
        d1.update(dict(k[i]))
    
    v2=[]
    k2=[]
    for i,(k,v) in enumerate(d1.items()):
        k2.append(k)
        v2.append(v)

    
    # Making seperate dictionary for positive and negative acceleration 
    j=0
    pos={}
    neg={}
    dct={}
    for i,(k,v) in enumerate(d1.items()):
        #print(i)
        if v>=0:
            pos[k]=v
            
        else:
            neg[k]=v
            
        if i==(len(d1)-1):
            
            if len(pos)>0:
                dct[j]=pos
            if len(neg)>0:
                dct[j]=neg
            break
                
        if v2[i]>0 and v2[i+1]<0:
            dct[j]=pos
            j=j+1
            pos={}
            
        if v2[i]<0 and v2[i+1]>0:
            dct[j]=neg
            j=j+1
            neg={}

    # if first element is positve in dictionary
    # Taking only indexes of events and storing it into first positive list(plist) and then negative list(nlist) 
    posdct={}
    poslst=[]
    plist=[]
    negdct={}
    neglst=[]
    nlist=[]
    
    if sum(dct[0].values())>0:
        for i in range(0,len(dct),2):
            plist.append(list(dct[i].keys()))
            
    else:
        for i in range(0,len(dct),2):
            nlist.append(list(dct[i].keys()))

    # if first element is negative in dictionary
    # Taking only indexes of events and storing it into first negative list(nlist) and then positive list(plist)
    posdct={}
    poslst=[]
    negdct={}
    neglst=[]
    
    if sum(dct[1].values())>0:
        for i in range(1,len(dct),2):
            plist.append(list(dct[i].keys()))
            
    else:
        for i in range(1,len(dct),2):
            nlist.append(list(dct[i].keys()))
    
    # Removing datapoints which has differene of consecutive velocities greater than 2 or less than 2 for acceleration
    plist1=[]
    for k,v in enumerate(plist):
        val_remove=[]
        for j in range(len(v)-1):
            #print('{},{}'.format(v[j],vlist[v[j]]))
            if vlist[v[j+1]]-vlist[v[j]] > 2 or vlist[v[j+1]]-vlist[v[j]] < -2:
                val_remove.append(v[j+1])
        if len(val_remove)>0:
            #print(val_remove)
            i=v.index(val_remove[-1])
            if len(v[i:])>=3:
                plist1.append(v[i:])
        else:
            plist1.append(v)    
    
    # Removing datapoints which has differene of consecutive velocities greater than 2 or less than 2 for deceleration
    nlist1=[]
    for k,v in enumerate(nlist):
        val_remove=[]
        for j in range(len(v)-1):
            #print('{},{}'.format(v[j],vlist[v[j]]))
            if vlist[v[j+1]]-vlist[v[j]] > 2 or vlist[v[j+1]]-vlist[v[j]] < -2:
                val_remove.append(v[j+1])
        if len(val_remove)>0:
            #print(val_remove)
            i=v.index(val_remove[-1])
            if len(v[i:])>=3:
                nlist1.append(v[i:])
        else:
            nlist1.append(v) 
    
    
    # Taking necessary parameters for acceleration events ie
	# V1= initial veloctiy, V2= final velocity, T1= initial time, T2= final time, Name= name of file in which that event belongs
	# V2-V1,D2-D1,T2-T1 = Differnce of final and initial velocity, distance and time respectively
	# Max LA= maximum longitudinal acceleration of events
	# Avg LA= average longitudinal acceleration of events

    # Thresholding is done for selecting the events ie 
    # v>=5 and v2>15 - final velocity > 15kmph and v2-v1(velocity difference) >= 5kmph 
    # d<350 and d>1 - distance should be greater than 1m and less than 350m
    # t<30 and t>1 - time difference should be greater than 1s and less than 30s
    va1list=[]
    va2list=[]
    valist=[]
    ialist=[]
    ta1list=[]
    ta2list=[]
    talist=[]
    dalist=[]
    da1list=[]
    da2list=[]
    maxalist=[]
    avgalist=[]
    namelist=[]
    loalist=[]
    maxalist_sort=[]
    yralist=[]
    yawalist=[]
    yawalist_sort=[]
    jerk_alist=[]

    for i in range(len(plist1)):
        #print(i)
        yralist=[]
        loalist=[]
        jalist=[]
        i1=plist1[i][0]
        i2=plist1[i][-1]
        v1=vlist[i1]
        v2=vlist[i2]
        v=v2-v1
        d=(dlist[i2]-dlist[i1])
        t1=tlist[i1]
        t2=tlist[i2]
        t=t2-t1
        if v>=5 and v2>15 and d<350 and d>1 and t<30 and t>1:
            loalist=[]
            va1list.append(v1)
            va2list.append(v2)
            valist.append(v)
            #ialist.append(plist[i])
            namelist.append(route[0])
            ta1list.append(t1)
            ta2list.append(t2)
            talist.append(t)
            #da1list.append(dlist[i1])
            #da2list.append(dlist[i2])
            dalist.append(d)
            for k,v in enumerate(plist1[i]):
                if k>=1:
                    loalist.append(lolist[v])
                    #jalist.append(jlist[v])
                    jalist.append(mavg_jlist[v])
                if ylist[v]<6:
                    yralist.append(ylist[v])
            loalist.sort()
            maxalist_sort.append(loalist[-5:])
            maxalist.append(max(loalist))
            avgalist.append(mean(loalist)) 
            yralist.sort()
            yawalist_sort.append(yralist[-5:])
            yawalist.append(max(yralist))
            jerk_alist.append(max(jalist))
           
    yawa_array=[]
    for yalist in yawalist_sort:
        dataa = [round(x,2) for x in yalist] 
        yawa_array.append(dataa) 
    # Saving all the parameters in csv file dataframe of one file
    accdata={'T1':ta1list,'T2':ta2list,'V1':va1list,'V2':va2list,'V2-V1':valist,'D2-D1':dalist,'T2-T1':talist,'Max LA':maxalist,'Avg LA':avgalist,'yaw_rate':yawalist,'mavg_jerk':jerk_alist,'yaw array':yawa_array,'LA array':maxalist_sort,'FileName':namelist}
    accdf=pd.DataFrame(accdata,columns=['T1','T2','V1','V2','V2-V1','D2-D1','T2-T1','Max LA','Avg LA','yaw_rate','mavg_jerk','yaw array','LA array','FileName'])
    
    # Merging all the events dataframe into one csv file dataframe
    lia.append(accdf)


    # Taking necessary parameters for acceleration events ie
	# V1= initial veloctiy, V2= final velocity, T1= initial time, T2= final time, Name= name of file in which that event belongs
	# V2-V1,D2-D1,T2-T1 = Differnce of final and initial velocity, distance and time respectively
	# Max LA= minimum longitudinal acceleration of events
	# Avg LA= average longitudinal acceleration of events

    # Thresholding is done for selecting the events ie 
    # v<-5 and v1>1 - final velocity > 1kmph and v2-v1(velocity difference) < -5kmph 
    # d<350 and d>1 - distance should be greater than 1m and less than 350m
    # t<30 and t>1 - time difference should be greater than 1s and less than 30s

    vd1list=[]
    vd2list=[]
    idlist=[]
    td1list=[]
    td2list=[]
    dd1list=[]
    dd2list=[]
    mindlist=[]
    avgdlist=[]
    vdlist=[]
    tdlist=[]
    ddlist=[]
    lodlist=[]
    mindlist_sort=[]
    namelist=[]
    yrdlist=[]
    yawdlist=[]
    yawdlist_sort=[]
    jerk_dlist=[]

    for i in range(len(nlist1)):
        #print(i)
        yrdlist=[]
        lodlist=[]
        jdlist=[]
        i1=nlist1[i][0]
        i2=nlist1[i][-1]
        v1=vlist[i1]
        v2=vlist[i2]
        v=v2-v1
        t1=tlist[i1]
        t2=tlist[i2]
        t=t2-t1
        d=(dlist[i2]-dlist[i1])
        if v<-5 and v1>10 and d>1 and d<350 and t>1 and t<30:
            vd1list.append(v1)
            vd2list.append(v2)
            vdlist.append(v)
            #idlist.append(nlist[i])
            namelist.append(splitlist[-1])
            td1list.append(t1)
            td2list.append(t2)
            tdlist.append(t)
            #dd1list.append(dlist[i1])
            #dd2list.append(dlist[i2])
            ddlist.append(d)
            for k,v in enumerate(nlist1[i]):
                if k>=1:
                    lodlist.append(lolist[v])
                    jdlist.append(mavg_jlist[v])
                if ylist[v]<6:
                    yrdlist.append(ylist[v])
            lodlist.sort()
            mindlist_sort.append(lodlist[:5])
            mindlist.append(min(lodlist))
            avgdlist.append(mean(lodlist)) 
            yrdlist.sort()
            yawdlist_sort.append(yrdlist[-5:])
            yawdlist.append(max(yrdlist))
            jerk_dlist.append(min(jdlist))
    
    yawd_array=[]
    for ydlist in yawdlist_sort:
        datad = [round(x,2) for x in ydlist] 
        yawd_array.append(datad)
    
    # Saving all the parameters in csv file dataframe of one file
    decdata={'T1':td1list,'T2':td2list,'V1':vd1list,'V2':vd2list,'V2-V1':vdlist,'D2-D1':ddlist,'T2-T1':tdlist,'Min LA':mindlist,'Avg LA':avgdlist,'yaw_rate':yawdlist,'mavg_jerk':jerk_dlist,'yaw array':yawd_array,'LA array':mindlist_sort,'FileName':namelist}
    decdf=pd.DataFrame(decdata,columns=['T1','T2','V1','V2','V2-V1','D2-D1','T2-T1','Min LA','Avg LA','yaw_rate','mavg_jerk','yaw array','LA array','FileName'])
    # Merging all the events dataframe into one csv file dataframe
    lid.append(decdf)


print('reached')
frame_acc = pd.concat(lia, axis=0, ignore_index=True)
frame_dec = pd.concat(lid, axis=0, ignore_index=True)

# Saving the acceleration events, specify name of the file here
frame_acc.to_csv('ramesh_acceleration_mavg.csv')
# Saving the deceleration events, specify name of the file here
frame_dec.to_csv('ramesh_deceleration_mavg.csv')

