import sys
import os
import time
import re

t=[]
intervals=[]

#t
#[0] - Count
#[1] - Tag From - Tag To
#[2] - Time From
#[3] - Time To
#[4] - Min Delta time To-From
#[5] - Average Delta time To-From
#[6] - Max Delta time To-From
#[7] - Sum of all deltas To-From
#[8] - Min Timestamp str
#[9] - Max Timestamp str
#[10] - Min Timestamp milisec
#[11] - Max Timestamp milisec
#[12] - Response codes

xmode='RSW'
#default is 0 seconds
maxtime=0
#default is 24 hours (24*60 minutes)
intervalmin=24*60
#default is empty - all tags
tags=""
if len(sys.argv)>2:
  xmode=str(sys.argv[2])
  if len(sys.argv)>3:
    maxtime=float(sys.argv[3])
    if len(sys.argv)>4:
      intervalmin=float(sys.argv[4])
      if len(sys.argv)>5:
        tags=str(sys.argv[5])
if xmode=="RSW":
  difavg=0.0
  f=open(sys.argv[1],'r')
  for l in f:
    if l.find('| TIME_STAT |')>=0:
      ll=l.split('|')
      rc=l.split('|')[8].split('-')[1]
      prev=0.0
      curr=0.0
#      difmin=0.0
#      difmax=0.0
      ts=ll[0]
      prevs=""
      currs=""
      for i in range(10,len(ll)):
        prev=curr
        prevs=currs
        curr=float(ll[i].split('-')[1])
        currs=re.sub('[^A-Za-z0-9\_\-\. ]', '',ll[i].split('-')[0])
        dif=curr-prev
#        if prevs!="" and dif>=maxtime:
#        if prevs!="" and dif>=maxtime and not (dif>110 and currs=='SWITCH_REQ_B') and ( (len(tags)>0 and (prevs in tags or currs in tags)) or len(tags)==0):
        if prevs!="" and dif>=maxtime and not (dif>110 and currs=='SWITCH_REQ_B') and ( (len(tags)>0 and (tags in prevs or tags in currs)) or len(tags)==0):
          tag_match=0
          ts_ms=int(ts.split(".")[1])+int(ts.split(":")[2].split(".")[0])*1000+int(ts.split(":")[1])*1000*60+int(ts.split(":")[0])*1000*60*60
          for j in range(len(t)):
#            if t[j][1]==prevs+" - "+currs:
#            if t[j][1]==prevs+" - "+currs and ts_ms-t[j][11]<10*60*1000:
#            if t[j][1]==prevs+" - "+currs and (ts_ms-t[j][11])>(intervalmin*1000):
            if t[j][1]==prevs+" - "+currs:
              tag_match=1
              t[j][0]=t[j][0]+1
              if dif<t[j][4]: t[j][4]=dif
              if dif>t[j][6]: t[j][6]=dif
              t[j][7]=t[j][7]+dif
              t[j][5]=t[j][7]/t[j][0]
              t[j][9]=ts
              t[j][11]=ts_ms
              if not rc in t[j][12]: t[j][12]=t[j][12]+','+rc
          if tag_match==0:
            t.append([1,prevs+" - "+currs,prev,curr,dif,dif,dif,dif,ts,ts,ts_ms,ts_ms,rc])
  f.close()
  print ("COUNT").rjust(6)+" "+("FROM-TO").ljust(55)+("MIN TIME DELTA").ljust(15)+("AVG TIME DELTA").ljust(15)+("MAX TIME DELTA").ljust(15)+("MIN TIMESTAMP").ljust(14)+("MAX TIMESTAMP").ljust(14)+("Interval").ljust(14)+("RC").ljust(20)
  for i in range(len(t)):
    if t[i][0]>0:
      irem=t[i][11]-t[i][10]
      ihours=irem//(1000*60*60)

      irem=irem-ihours*60*60*1000
      iminutes=irem//(1000*60)

      irem=irem-iminutes*60*1000
      iseconds=irem//(1000)

      irem=irem-iseconds*1000
      imiliseconds=irem

#      interval="%s hours %s minutes %s seconds %s miliseconds" % (ihours, iminutes, iseconds, imiliseconds)
      interval="%s:%s:%s.%s" % (str(ihours).rjust(2,'0'), str(iminutes).rjust(2,'0'), str(iseconds).rjust(2,'0'), str(imiliseconds).rjust(3,'0'))
      print str(t[i][0]).rjust(6)+" "+t[i][1].ljust(55)+str("%.6f" % t[i][4]).ljust(15)+str("%.6f" % t[i][5]).ljust(15)+str("%.6f" % t[i][6]).ljust(15)+t[i][8].ljust(14)+t[i][9].ljust(14)+interval.ljust(14)+t[i][12].ljust(20)

