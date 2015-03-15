import sys



pid_state={}
pid_keys={}

trn_lines={}

f=open(sys.argv[1],'r')

s=f.readline()

while s<>'':
	s=s.replace('\n','')
	s=''.join([c for c in s if ord(c) > 31 or ord(c) == 9])

	try:
#		if '| Service HYPERCOM_IN started' in s or '| Key (ASCII) :' in s or '| Service  HYPERCOM_IN End   Type=[RELATIVE] UTime=[' in s or '| Service HYPERCOM_OUT started' in s or '| __________Message to Foreign (FOREIGN FORMAT)_________' in s or '| Key (ASCII) :' in s or '| Service  HYPERCOM_OUT End   Type=[RELATIVE] UTime=[' in s:
		pid=s.split('|')[2]
	except:
		print '!!! ERROR  in line: '+s
		sys.exit(1)

	if '|<--#|' in s and ' hpt:' in s and (not pid_state.has_key(pid) or pid_state[pid]=='in finished'):
		pid_state[pid]='in finished'
		pid_keys[pid]=s.split('|')[3].split(' ')[1].split(':')[0]
		trn_lines[pid_keys[pid]]=[]
		ss=s.split('|')[0]+'||'+pid_keys[pid]+'|'+pid+' HPT_REQ STARTED'
		trn_lines[pid_keys[pid]].append(ss)
		print ss



#BETWEEN INCOMING ANS DISCON
#	if '|<--#|' in s and ': discon ' in s and pid_state.has_key(pid) and pid_state[pid]=='in finished':
#BETWEEN INCOMING AND DATA FROM POS (POS data receiving time)
	if (('|<--+|' in s and ' bytes' in s) or ('discon' in s)) and pid_state.has_key(pid) and pid_state[pid]=='in finished':
#	if 'discon' in s and pid_state.has_key(pid) and pid_state[pid]=='in finished':
		pid_state[pid]='out finished'
		pid_keys[pid]=s.split('|')[3].split(' ')[1].split(':')[0]
		if trn_lines.has_key(pid_keys[pid]):
			ss=s.split('|')[0]+'||'+pid_keys[pid]+'|'+pid+' HPT_REQ FINISHED'
			trn_lines[pid_keys[pid]].append(ss)
			print ss


	s=f.readline()


f.close()

