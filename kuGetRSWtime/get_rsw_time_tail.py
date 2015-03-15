#!/usr/bin/env python
# Irakli Khubashvili, 03.06.2014

#Running example from command line with CardSuite RTPS Environment
#tail -f /add_rtps_log/ROUTING_SWITCH_140602.log | pytool get_rsw_time_tail.py 2 STIP_START,HYEPERCOM1


import sys
import datetime

init_date=datetime.datetime.now()
init_day=int(init_date.strftime('%d'))

min_time=0
max_time=0
avg_time=0
count=0
total_time=0.0

min_time1=0
max_time1=0
avg_time1=0
count1=0
total_time1=0.0

min_time5=0
max_time5=0
avg_time5=0
count5=0
total_time5=0.0

min_time60=0
max_time60=0
avg_time60=0
count60=0
total_time60=0.0

start_index=9
stop_index=10

max_start_index=9
max_stop_index=10
max_tag_name1=""
max_tag_name2=""
max_tag_time=0.0
cur_tag_time=0.0
max_tag_time=0.0

alert_time=3.0
text_match_list=[]

if len(sys.argv)>1:
	alert_time=float(sys.argv[1])
else:
	alert_time=3.0

if len(sys.argv)>2:
	text_match_list=sys.argv[2].split(",")
else:
	text_match_list=[]

print "Initial Patrameters:"
print "  ALERT TIME = %s" % alert_time
print "  TEXT MATCH LIST = %s" % text_match_list
print "  Starting Date and Time is "+init_date.strftime('%d-%m-%Y  %H:%M:%S')
print "---------------------"

curr_date=datetime.datetime.now()
curr60=int(curr_date.strftime('%H'))
prev60=curr60
curr5=int(curr_date.strftime('%M'))//5
prev5=curr5
curr1=int(curr_date.strftime('%M'))
prev1=curr1

while True:
	s=sys.stdin.readline();
	if s<>"":
		if '| TIME_STAT |' in s:
			if len(text_match_list)>0 and len([ss for ss in text_match_list if ss in s])>0:
				s1=s.split('|')[9]
				start_index=9
				if s1=='':
					s1=s.split('|')[10]
					start_index=10
				s1=s1.split('-')[1]
				start_time=float(s1)
				stop_time=float(s.split('|')[-1].split('-')[1])
				ttime=stop_time-start_time
				if ttime>100:
					s1=s[s.find('SWITCH_REQ_B'):].split('|')[0].split('-')[1]
					start_time=float(s1)
					ttime=stop_time-start_time
					start_index=s.find('SWITCH_REQ_B')

				if ttime>max_time: max_time=ttime
				if ttime>max_time60: max_time60=ttime
				if ttime>max_time5: max_time5=ttime
				if ttime>max_time1: max_time1=ttime

				if ttime<min_time or min_time==0: min_time=ttime
				if ttime<min_time60 or min_time60==0: min_time60=ttime
				if ttime<min_time5 or min_time5==0: min_time5=ttime
				if ttime<min_time1 or min_time1==0: min_time1=ttime

				count=count+1
				count60=count60+1
				count5=count5+1
				count1=count1+1

				total_time=total_time+ttime
				total_time60=total_time60+ttime
				total_time5=total_time5+ttime
				total_time1=total_time1+ttime

				if count>0: avg_time=total_time/count
				else: avg_time=0
				if count60>0: avg_time60=total_time60/count60
				else: avg_time60=0
				if count5>0: avg_time5=total_time5/count5
				else: avg_time5=0
				if count1>0: avg_time1=total_time1/count1
				else: avg_time1=0

				count1_str=("%.0f" % count1).rjust(4,' ')
				count5_str=("%.0f" % count5).rjust(5,' ')
				count60_str=("%.0f" % count60).rjust(6,' ')
				count_str=("%.0f" % count).rjust(7,' ')
				ttime_str=("%.3f" % ttime).rjust(8,' ')

				min_time1_str=("%.3f" % min_time1).rjust(8,' ')
				max_time1_str=("%.3f" % max_time1).rjust(8,' ')
				avg_time1_str=("%.3f" % avg_time1).rjust(8,' ')

				min_time5_str=("%.3f" % min_time5)
				max_time5_str=("%.3f" % max_time5)
				avg_time5_str=("%.3f" % avg_time5)

				min_time60_str=("%.3f" % min_time60)
				max_time60_str=("%.3f" % max_time60)
				avg_time60_str=("%.3f" % avg_time60)

				min_time_str=("%.3f" % min_time)
				max_time_str=("%.3f" % max_time)
				avg_time_str=("%.3f" % avg_time)

				if ttime>=alert_time:
					colors="\033[91m"
					colore="\033[0m"
					colorts=""
					colorte=""
					pref="!!!(OVERLOADED)!!!"
					for si in xrange(start_index+1,len(s.split('|'))):
						cur_tag_time=float(s.split('|')[si].split("-")[1])-float(s.split('|')[si-1].split("-")[1])
						if cur_tag_time>max_tag_time:
							max_tag_name1=s.split('|')[si-1].split("-")[0]
							max_tag_name2=s.split('|')[si].split("-")[0]
							max_tag_time=cur_tag_time
					max_tag_time_str=("%.3f" % max_tag_time).rjust(8,' ')
					pref=pref+" ("+max_tag_name1+" - "+max_tag_name2+" time="+max_tag_time_str+")"
				else:
					colors=""
					colore=""
					colorts="\033[94m"
					colorte="\033[0m"
					pref=""
					max_tag_name1=""
					max_tag_name2=""
#				rown=s.split("|")[0]+"|"+s.split("|")[1]+"|"+s.split("|")[2].rjust(7," ")+"|"+s.split("|")[3]+"|"+s.split("|")[4]+"|"+(s.split("|")[5]).ljust(11," ")+"|"+s.split("|")[6]+"|"+s.split("|")[7]+"|"+s.split("|")[8]
				rown=s.split("|")[0]+"|"+s.split("|")[2].rjust(7," ")+"|"+s.split("|")[4]+"|"+(s.split("|")[5]).ljust(11," ")+"|"+s.split("|")[8]
				print colors+(('%s| count='+colorts+'%s'+colorte+colors+'(%s,%s,%s), '+colorts+'TIME=%s'+colorte+colors+', MIN_Time='+colorts+'%s'+colorte+colors+'(%s,%s,%s), MAX_Time='+colorts+'%s'+colorte+colors+'(%s,%s,%s), AVG_Time='+colorts+'%s'+colorte+colors+'(%s,%s,%s)') % (rown,count1_str,count5_str,count60_str,count_str,ttime_str,min_time1_str,min_time5_str,min_time60_str,min_time_str,max_time1_str,max_time5_str,max_time60_str,max_time_str,avg_time1_str,avg_time5_str,avg_time60_str,avg_time_str))+pref+colore
		s=""
	curr_date=datetime.datetime.now()
	curr_day=int(curr_date.strftime('%d'))
	curr60=int(curr_date.strftime('%H'))
	curr5=int(curr_date.strftime('%M'))//5
	curr1=int(curr_date.strftime('%M'))
	if curr1<>prev1:
		prev1=curr1
		min_time1=0
		max_time1=0
		avg_time1=0
		count1=0
		total_time1=0.0
		print "==========    Resetting 1 minute accumulators    =========="
	if curr5<>prev5:
		prev5=curr5
		min_time5=0
		max_time5=0
		avg_time5=0
		count5=0
		total_time5=0.0
		print "==========    Resetting 5 minute accumulators    =========="
	if curr60<>prev60:
		prev60=curr60
		min_time60=0
		max_time60=0
		avg_time60=0
		count60=0
		total_time60=0.0
		print "==========    Resetting 1 HOUR accumulators    =========="
	if curr_day<>init_day:
		print "============================================="
		print "Day Changed to "+curr_date.strftime('%d-%m-%Y  %H:%M:%S')
		print "Exiting ...."
		break

	





