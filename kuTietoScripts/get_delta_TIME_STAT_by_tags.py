# 2014.12.05 by irakli khubashvili
# Script for calculate delta in seconds between two tags of TIME_STAT row
# Execute script by:
#   pytool get_delta_TIME_STAT_by_tags.py <log file name> <mode(RSW|IF), default value is RSW> <min alert time, default value is 0> <Tag From, default value is SWITCH_REQ_B> <Tag To, default value is SWITCH_RESP_E>


import sys
import os
import time
import re

xmode='RSW'
#default is 0 seconds
mintime=0
#defaults are tag_from=SWITCH_REQ_B and tag_to=SWITCH_RESP_E
tag_from='SWITCH_REQ_B'
tag_to='SWITCH_RESP_E'
if len(sys.argv)>2:
	xmode=str(sys.argv[2])
	if len(sys.argv)>3:
		mintime=float(sys.argv[3])
		if len(sys.argv)>4:
			tag_from=str(sys.argv[4])
			if len(sys.argv)>5:
				tag_to=str(sys.argv[5])
print '  Incoming parameters:'
print '    Log file = "%s"' % sys.argv[1]
print '    Mode = "%s"' % xmode
print '    Minimal time = %s' % mintime
print '    Tag From = "%s"' % tag_from
print '    Tag To = "%s"' % tag_to

if xmode=='RSW':
	f=open(sys.argv[1],'r')
	for l in f:
		if l.find('| TIME_STAT |')>=0:
			ll=l.split('|')
			tagfrom_time=0.0
			tagto_time=0.0
			tagfrom_tag=''
			tagto_tag=''
			for i in range(10,len(ll)):
				curr=float(ll[i].split('-')[1])
				currs=re.sub('[^A-Za-z0-9\_\-\. ]', '',ll[i].split('-')[0])
				if len(tagfrom_tag)<=0 and tag_from in currs:
					tagfrom_tag=currs
					tagfrom_time=curr
				else:
					if len(tagfrom_tag)>0 and tag_to in currs:
						dif=curr-tagfrom_time
						if dif>=mintime:
							print '%s|%s|from "%s" to "%s"|%s|++++++|%s|%s|%s|%s|%s' % (ll[0],ll[2],tag_from,tag_to,dif,ll[4],ll[5],ll[6],ll[7],ll[8])
							break
	f.close()



if xmode=='IF':
	f=open(sys.argv[1],'r')
	for l in f:
		if l.find('\tTIME_STAT\t|')>=0:
			ll=l.split('|')
			tagfrom_time=0.0
			tagto_time=0.0
			tagfrom_tag=''
			tagto_tag=''
			for i in range(4,len(ll)):
				curr=float(ll[i].split('-')[1])
				currs=re.sub('[^A-Za-z0-9\_\-\. ]', '',ll[i].split('-')[0])
				if len(tagfrom_tag)<=0 and tag_from in currs:
					tagfrom_tag=currs
					tagfrom_time=curr
				else:
					if len(tagfrom_tag)>0 and tag_to in currs:
						dif=curr-tagfrom_time
						if dif>=mintime:
							print '%s|%s|from "%s" to "%s"|%s' % (ll[0],ll[2],tag_from,tag_to,dif)
							break
	f.close()
