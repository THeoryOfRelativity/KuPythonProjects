import sys
import datetime


f=open(sys.argv[1],'r')
average_mseconds=int(sys.argv[2])

log={}


s=f.readline()

while s<>'':
	s=s.replace('\n','')
	s=''.join([c for c in s if ord(c) > 31 or ord(c) == 9])

#	t=datetime.datetime.strptime(s,'%H:%M:%S.%f')

	ts=s
	ts_ms=int(ts.split(".")[1])+int(ts.split(":")[2].split(".")[0])*1000+int(ts.split(":")[1])*1000*60+int(ts.split(":")[0])*1000*60*60
	ts_ms_portion=average_mseconds*(ts_ms//average_mseconds)
#	print 'Current portion for "%s" is %s' % (s,ts_ms_portion)
	
	temp_int=ts_ms_portion
	ihours=temp_int//(1000*60*60)
	temp_int=temp_int-ihours*60*60*1000
	iminutes=temp_int//(1000*60)
	temp_int=temp_int-iminutes*60*1000
	iseconds=temp_int//(1000)
	temp_int=temp_int-iseconds*1000
	imiliseconds=temp_int
	ts_ms_portion_str=str(ihours).rjust(2,'0')+':'+str(iminutes).rjust(2,'0')+':'+str(iseconds).rjust(2,'0')+'.'+str(imiliseconds).rjust(3,'0')
#	print 'Current portion for "%s" in str is %s' % (s,ts_ms_portion_str)
	if log.has_key(ts_ms_portion_str):
		log[ts_ms_portion_str]=log[ts_ms_portion_str]+1
	else:
		log[ts_ms_portion_str]=1


	s=f.readline()


f.close()


for key,value in log.items():
#	log[key]=log[key]//(1000*average_mseconds)
#	print 'Before %s=%s, After %s=%s/%s=%s' % (key,log[key],key,log[key],average_mseconds,log[key]//average_mseconds)
	log[key]=value//(average_mseconds/1000)




f_out=open(sys.argv[1]+'_PLOT.txt','w')
f_out.write('START|'+'Average TPS'+'\n')
for key,value in log.items():
	f_out.write(key+'|'+str(value)+'\n')
f_out.write('STOP|'+'Average TPS'+'\n')
f_out.close()
