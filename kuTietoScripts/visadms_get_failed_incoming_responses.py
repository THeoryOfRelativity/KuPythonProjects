import sys
import os
import time
import re
#import matplotlib.pyplot as plt
import datetime

in_msg=[]

in_svc={}

f2=open('VISADMS_analyze.log','w')

f=open(sys.argv[1],'r')
for s in f:
	s=s.replace('\n','')
	if '|' in s and len(s.split('|'))>=3:
		current_pid=s.split('|')[2]
	if 'Service VISA_DMS_IN started' in s:
		in_svc[current_pid]=[]
#	if ('| Key  : ' in s or '| Key (ASCII) : ' in s or '| MTI  : ' in s or '\' H.' in s or '\'	 B.' in s or '| 209 | |VISA_DMS| Can\'t get session' in s or '| Can\'t find request: Error 128 - No entry found' in s) and in_svc.has_key(current_pid):
	if in_svc.has_key(current_pid):
		in_svc[current_pid].append(s)
	if '| Service  VISA_DMS_IN End   Type=[ABSOLUTE] UTime=[' in s:
		if in_svc.has_key(current_pid):
			matched1=False
			matched2=False
			matched3=False
			msgdet=''
			for i in xrange(len(in_svc[current_pid])):
				if '| MTI  : ' in in_svc[current_pid][i]: msgdet=msgdet+in_svc[current_pid][i].split('|')[0]+'|MTI='+in_svc[current_pid][i].split('|')[3].split(':')[1].replace(' ','')+'|'
				if '\' B.2 ' in in_svc[current_pid][i] and '[' in in_svc[current_pid][i] and ']' in in_svc[current_pid][i]: msgdet=msgdet+'B.002='+in_svc[current_pid][i].split('[')[1].split(']')[0]+'|'
				if '\' B.3 ' in in_svc[current_pid][i] and '[' in in_svc[current_pid][i] and ']' in in_svc[current_pid][i]: msgdet=msgdet+'B.003='+in_svc[current_pid][i].split('[')[1].split(']')[0]+'|'
				if '\' B.4 ' in in_svc[current_pid][i] and '[' in in_svc[current_pid][i] and ']' in in_svc[current_pid][i]: msgdet=msgdet+'B.004='+in_svc[current_pid][i].split('[')[1].split(']')[0]+'|'
				if '\' B.49 ' in in_svc[current_pid][i] and '[' in in_svc[current_pid][i] and ']' in in_svc[current_pid][i]: msgdet=msgdet+'B.049='+in_svc[current_pid][i].split('[')[1].split(']')[0]+'|'
				if '\' B.11 ' in in_svc[current_pid][i] and '[' in in_svc[current_pid][i] and ']' in in_svc[current_pid][i]: msgdet=msgdet+'B.011='+in_svc[current_pid][i].split('[')[1].split(']')[0]+'|'
				if '\' B.37 ' in in_svc[current_pid][i] and '[' in in_svc[current_pid][i] and ']' in in_svc[current_pid][i]: msgdet=msgdet+'B.037='+in_svc[current_pid][i].split('[')[1].split(']')[0]+'|'
				if '\' B.39 ' in in_svc[current_pid][i] and '[' in in_svc[current_pid][i] and ']' in in_svc[current_pid][i]: msgdet=msgdet+'B.039='+in_svc[current_pid][i].split('[')[1].split(']')[0]+'|'
				if '\' B.62.2 ' in in_svc[current_pid][i] and '[' in in_svc[current_pid][i] and ']' in in_svc[current_pid][i]: msgdet=msgdet+'B.062.2='+in_svc[current_pid][i].split('[')[1].split(']')[0]+'|'
				if '\' B.38 ' in in_svc[current_pid][i] and '[' in in_svc[current_pid][i] and ']' in in_svc[current_pid][i]: msgdet=msgdet+'B.038='+in_svc[current_pid][i].split('[')[1].split(']')[0]+'|'
				if '| 209 | |VISA_DMS| Can\'t get session' in in_svc[current_pid][i]:
					matched1=True
				if '| Type : RESPONSE' in in_svc[current_pid][i]:
					matched2=True
				if 'B.39    : [00]' in in_svc[current_pid][i]:
					matched3=True
				if matched1 and matched2 and matched3:
					break
			if matched1 and matched2:
				print 'Matched: '+msgdet
			if matched1 and matched2 and matched3:
#				in_msg.append(in_svc[current_pid])
				for i2 in xrange(len(in_svc[current_pid])):
					f2.write(in_svc[current_pid][i2]+'\n')
				f2.write('----------------------------------------------------------------------------'+'\n')
			del in_svc[current_pid]


f.close()

f2.close()


