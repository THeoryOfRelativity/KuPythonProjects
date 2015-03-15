import sys
import datetime
import collections



f=open(sys.argv[1],'r')
average_mseconds=int(sys.argv[2])

log={}
log_count={}

s=f.readline()

while s<>'':
	s=s.replace('\n','')
	s=''.join([c for c in s if ord(c) > 31 or ord(c) == 9])

	if 'START|' in s:
		tag_name=s.split('|')[1]
		log[tag_name]={}
		log_count[tag_name]={}
	else:
		if 'STOP|' in s:
			tag_name=''
		else:
		
			ts=s.split('|')[0]
			vt=float(s.split('|')[1])
			ts_ms=int(ts.split(".")[1])//1000+int(ts.split(":")[2].split(".")[0])*1000+int(ts.split(":")[1])*1000*60+int(ts.split(":")[0])*1000*60*60
			if tag_name=='hpt (Receiving data from POS Time in sec)':
#				print 'Was %s, Now is %s (-%s)' % (ts_ms,ts_ms-vt*1000,vt)
				ts_ms=int(ts_ms-vt*1000)
			ts_ms_portion=average_mseconds*(ts_ms//average_mseconds)
#			if '18:15:' in ts:
#				print 'Current portion for "%s" is %s' % (s,ts_ms_portion)
	
			temp_int=ts_ms_portion
			ihours=temp_int//(1000*60*60)
			temp_int=temp_int-ihours*60*60*1000
			iminutes=temp_int//(1000*60)
			temp_int=temp_int-iminutes*60*1000
			iseconds=temp_int//(1000)
			temp_int=temp_int-iseconds*1000
			imiliseconds=temp_int
			ts_ms_portion_str=str(ihours).rjust(2,'0')+':'+str(iminutes).rjust(2,'0')+':'+str(iseconds).rjust(2,'0')+'.'+str(imiliseconds).rjust(3,'0')
#			if '18:15:' in ts_ms_portion_str:
#				print 'Current portion for "%s" in str is %s' % (s,ts_ms_portion_str)
			if log[tag_name].has_key(ts_ms_portion_str):
				log[tag_name][ts_ms_portion_str]=log[tag_name][ts_ms_portion_str]+vt
				log_count[tag_name][ts_ms_portion_str]=log_count[tag_name][ts_ms_portion_str]+1
			else:
				log[tag_name][ts_ms_portion_str]=vt
				log_count[tag_name][ts_ms_portion_str]=1


	s=f.readline()


f.close()


for key,value in log.items():
	for key2,value2 in value.items():
		log[key][key2]=value2//log_count[key][key2]


f_out=open(sys.argv[1]+('_AVERAGE_%sms_PLOT.txt' % average_mseconds),'w')
for key,value in log.items():
	f=0.0
	f=average_mseconds/1000
	s=("%.3f" % f)
	f_out.write('START|'+key+(' (Average %s sec)' % s)+'\n')
	olog2=collections.OrderedDict(sorted(value.items()))
	for key2,value2 in olog2.items():
		f_out.write(key2+'|'+str(value2)+'\n')
	f_out.write('STOP|'+key+(' (Average %s sec)' % s)+'\n')
#f_out.write('STOP|'+'Average TPS'+'\n')
f_out.close()
