import sys
import os
import time
import re
import datetime

descretion_seconds = 5
alert_prev_diff_perc = 200
alert_first_diff_perc = 200


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

tagsplot=[]
tagsplotx=[]
tagsploty=[]
tagnames=[]


tags_list_temp={}
tags_list={}


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
	      tagsplot[j].append([ll[0],dif])
	      tagsplotx[j].append(datetime.datetime.strptime(ll[0],'%H:%M:%S.%f'))
	      tagsploty[j].append(dif)
              if not rc in t[j][12]: t[j][12]=t[j][12]+','+rc
          if tag_match==0:
            t.append([1,prevs+" - "+currs,prev,curr,dif,dif,dif,dif,ts,ts,ts_ms,ts_ms,rc])
	    tagnames.append(prevs+' - '+currs)
	    tagsplot.append([])
            tagsplot[len(tagsplot)-1].append([ll[0],dif])
	    tagsplotx.append([])
	    tagsploty.append([])
            tagsplotx[len(tagsplotx)-1].append(datetime.datetime.strptime(ll[0],'%H:%M:%S.%f'))
            tagsploty[len(tagsploty)-1].append(dif)
#	  print 'KEY="'+prevs+' - '+currs+'"'
 	  if not tags_list_temp.has_key(prevs+" - "+currs):
#  	    print 'NO TAG OF "'+prevs+' - '+currs+'"'
	    tags_list_temp[prevs+" - "+currs]={}
	    tags_list_temp[prevs+" - "+currs]['total_count']=0
#  	    print 'total_count("'+prevs+' - '+currs+'")='+str(tags_list_temp[prevs+" - "+currs][total_count])
	    tags_list_temp[prevs+" - "+currs]['total_proctime']=0.0
	    tags_list_temp[prevs+" - "+currs]['prev_average']=-1000000
	    tags_list_temp[prevs+" - "+currs]['first_average']=-1000000
	    tags_list_temp[prevs+" - "+currs]['prev_timestamp']=datetime.datetime.strptime('00:00:00.000000','%H:%M:%S.%f')
	    tags_list_temp[prevs+" - "+currs]['curr_timestamp']=datetime.datetime.strptime('00:00:00.000000','%H:%M:%S.%f')
 	  if not tags_list.has_key(prevs+" - "+currs):
#	    tags_list[prevs+" - "+currs]=[]
	    tags_list[prevs+" - "+currs]=[]
#	    tags_list[prevs+" - "+currs].append(datetime.datetime.strptime('00:00:00.000000','%H:%M:%S.%f'))
#	    tags_list[prevs+" - "+currs].append(0.0)
#	    tags_list[prevs+" - "+currs].append(0.0)
#	    tags_list[prevs+" - "+currs].append(0.0)
	  # tags_list_temp
	  #   total_count
	  #   total_time
	  #   prev_average
	  #   first_average
	  # tags_list
	  #   [0] - time_stamp
	  #   [1] - average_time
	  #   [2] - change_in_prec_from_prev
	  #   [3] - change_in_prec_from_first
	  tags_list_temp[prevs+" - "+currs]['prev_timestamp']=tags_list_temp[prevs+" - "+currs]['curr_timestamp']
	  tags_list_temp[prevs+" - "+currs]['curr_timestamp']=datetime.datetime.strptime(ll[0],'%H:%M:%S.%f')
	  date_tmp1=tags_list_temp[prevs+" - "+currs]['prev_timestamp']
	  date_tmp2=tags_list_temp[prevs+" - "+currs]['curr_timestamp']
	  int_tmp1=date_tmp1.second
	  int_tmp2=date_tmp2.second
	  tglst=[]
	  if int_tmp1<>int_tmp2 and (int_tmp2 % descretion_seconds == 0):
#            tags_list[prevs+" - "+currs][0]
	    tglst.append(datetime.datetime.strptime(str(date_tmp1.hour).rjust(2,'0')+':'+str(date_tmp1.minute).rjust(2,'0')+':'+str(date_tmp1.second-date_tmp1.second % descretion_seconds).rjust(2,'0'),'%H:%M:%S'))
	    if tags_list_temp[prevs+" - "+currs]['total_count']>0:
#	      tags_list[prevs+" - "+currs][1]
	      tglst.append(tags_list_temp[prevs+" - "+currs]['total_proctime'] / tags_list_temp[prevs+" - "+currs]['total_count'])
	    else:
#	      tags_list[prevs+" - "+currs][1]=0
	      tglst.append(100.0)
	    if tags_list_temp[prevs+" - "+currs]['prev_average']<>-1000000:
#	      tags_list[prevs+" - "+currs][2]
	      tglst.append((tglst[1] / tags_list_temp[prevs+" - "+currs]['prev_average'] ) * 100)
	    else:
#	      tags_list[prevs+" - "+currs][2]=0.0
	      tglst.append(0.0)
	      tags_list_temp[prevs+" - "+currs]['prev_average']=tglst[1]
	    if tags_list_temp[prevs+" - "+currs]['first_average']<>-1000000:
#	      tags_list[prevs+" - "+currs][3]
#	      tglst.append((tglst[1] / tags_list_temp[prevs+" - "+currs]['first_average'] ) * 100 - 100)
	      tglst.append((tglst[1] / tags_list_temp[prevs+" - "+currs]['first_average'] ) * 100)
	    else:
#	      tags_list[prevs+" - "+currs][3]=0.0
#	      tglst.append(0.0)
	      tglst.append(100.0)
	      tags_list_temp[prevs+" - "+currs]['first_average']=tglst[1]
	    tags_list[prevs+" - "+currs].append(tglst)
	    
            tags_list_temp[prevs+" - "+currs]['total_count']=0
            tags_list_temp[prevs+" - "+currs]['total_proctime']=0.0
            tags_list_temp[prevs+" - "+currs]['prev_timestamp']=tags_list_temp[prevs+" - "+currs]['curr_timestamp']

#	    long_tmp1=0.0
#	    long_tmp1=date_tmp1.hour*60*60+date_tmp1.minute*60+date_tmp1.second+date_tmp1.microsecond/1000000
#	    long_tmp2=0.0
#	    long_tmp2=date_tmp2.hour*60*60+date_tmp2.minute*60+date_tmp2.second+date_tmp2.microsecond/1000000

#	    if (abs(tags_list[prevs+" - "+currs][-1][2]) >= alert_prev_diff_perc or abs(tags_list[-1][prevs+" - "+currs][3]) >= alert_first_diff_perc):
	    if (abs(tglst[2]) >= alert_prev_diff_perc or abs(tglst[3]) >= alert_first_diff_perc):
#	        print '['+prevs+" - "+currs+'] '+datetime.datetime.strftime(tags_list[prevs+" - "+currs][-1][0],'%H:%M:%S')+' = '+('+'+("%.2f" % tags_list[prevs+" - "+currs][-1][2])).replace('+-','-')+'% ('+('+'+("%.2f" % tags_list[prevs+" - "+currs][-1][3])).replace('+-','-')+'%)'
	        print '['+prevs+" - "+currs+'] '+datetime.datetime.strftime(tglst[0],'%H:%M:%S')+' = '+('+'+("%.2f" % tglst[2])).replace('+-','-')+'% ('+('+'+("%.2f" % tglst[3])).replace('+-','-')+'%)'


#  	  print 'total_count("'+prevs+' - '+currs+'")2='+str(tags_list_temp[prevs+" - "+currs][total_count])
          tags_list_temp[prevs+" - "+currs]['total_count']=tags_list_temp[prevs+" - "+currs]['total_count'] + 1
          tags_list_temp[prevs+" - "+currs]['total_proctime']=tags_list_temp[prevs+" - "+currs]['total_proctime'] + dif
#	  print datetime.datetime.strftime(tags_list_temp[prevs+" - "+currs]['curr_timestamp'],'%H:%M:%S.%f')+' = '+str((tags_list_temp[prevs+" - "+currs]['curr_timestamp'].time() - datetime.time(0,0,0)).total_seconds())
#	  print datetime.datetime.strftime(tags_list_temp[prevs+" - "+currs]['curr_timestamp'],'%H:%M:%S.%f')+' = '+("%.6f" % (tags_list_temp[prevs+" - "+currs]['curr_timestamp'].hour*60*60+tags_list_temp[prevs+" - "+currs]['curr_timestamp'].minute*60+tags_list_temp[prevs+" - "+currs]['curr_timestamp'].second+(tags_list_temp[prevs+" - "+currs]['curr_timestamp'].microsecond)/1000000))+' = '+("%.6f" % (tags_list_temp[prevs+" - "+currs]['curr_timestamp'].microsecond/1000000))

	  


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

print '=========================================================='
print '=========================================================='
print '=========================================================='
for i in xrange(len(tagnames)):
  print str(i)+' - '+tagnames[i]
print '=========================================================='
print '=========================================================='
print '=========================================================='




f_out=open(sys.argv[1]+'_PLOT.txt','w')

for i in xrange(len(tagnames)):
#  if 'STIP_START' in tagnames[i] and 'STIP_PARAMS_START' in tagnames[i]:
#  if 'STIP' in tagnames[i] or 'VISA_DMS' in tagnames[i]:
#  if 'STIP_START - STIP_PARAMS_START' in tagnames[i] or 'STIP_ENLARGE_END - STIP_END' in tagnames[i] or 'MESSAGESN_SREV_CALL_B - MESSAGESN_SREV_CALL_E' in tagnames[i] or 'BANKNETA_SEND - BANKNETA_RCV' in tagnames[i] or 'NIF_SEND - NIF_RCV'in tagnames[i] or 'VISA_DMS_SEND - VISA_DMS_RCV' in tagnames[i] or 'AMEX_POS_SEND - AMEX_POS_RCV' in tagnames[i] or 'SWITCH_REQ_B - acq_auth_SQL_B' in tagnames[i] or 'NIF_IN_E - SWITCH_REQ_B' in tagnames[i] or 'SWITCH_REQ_E - STIP_START' in tagnames[i] or 'STIP_END - SWITCH_RESP_B' in tagnames[i]:
	  f_out.write('START|'+tagnames[i]+'\n')
	  for xxi in xrange(len(tagsplotx[i])):
		f_out.write(datetime.datetime.strftime(tagsplotx[i][xxi],'%H:%M:%S.%f')+'|'+str(tagsploty[i][xxi])+'\n')
	  f_out.write('STOP|'+tagnames[i]+'\n')

f_out.close()



f_out=open(sys.argv[1]+'_PLOT_NEW.txt','w')

for key,value in tags_list.items():
	f_out.write('START|'+key+'\n')
	for xxi in xrange(len(value)):
		f_out.write(datetime.datetime.strftime(value[xxi][0],'%H:%M:%S.000000')+'|'+str(value[xxi][3])+'\n')
	f_out.write('STOP|'+key+'\n')

f_out.close()


