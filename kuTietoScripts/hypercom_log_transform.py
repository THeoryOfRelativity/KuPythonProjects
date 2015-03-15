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
		if '| Service HYPERCOM_IN started' in s or '| Key (ASCII) :' in s or '| Service  HYPERCOM_IN End   Type=[RELATIVE] UTime=[' in s or '| Service HYPERCOM_OUT started' in s or '| __________Message to Foreign (FOREIGN FORMAT)_________' in s or '| Key (ASCII) :' in s or '| Service  HYPERCOM_OUT End   Type=[RELATIVE] UTime=[' in s:
			pid=s.split('|')[2]
	except:
		print '!!! ERROR  in line: '+s
		sys.exit(1)

	if '| Service HYPERCOM_IN started' in s and (not pid_state.has_key(pid) or pid_state[pid]=='in finished'):
		pid_state[pid]='in started'
#		print 'in started'

	if '| Key (ASCII) :' in s and pid_state.has_key(pid) and pid_state[pid]=='in started':
		pid_state[pid]='in key'
		pid_keys[pid]=s.split('|')[3].split(' ')[4]
		trn_lines[pid_keys[pid]]=[]
		ss=s.split('|')[0]+'||'+pid_keys[pid]+'|'+pid+' HYPERCOM_IN STARTED'
		trn_lines[pid_keys[pid]].append(ss)
		print ss
#		print 'in key'

	if '| Service  HYPERCOM_IN End   Type=[RELATIVE] UTime=[' in s and pid_state.has_key(pid) and pid_state[pid]=='in key':
		pid_state[pid]='in finished'
#		print 'in finished'



	if '| Service HYPERCOM_OUT started' in s and (not pid_state.has_key(pid) or pid_state[pid]=='out finished'):
		pid_state[pid]='out started'
#		print 'out started'

	if '| __________Message to Foreign (FOREIGN FORMAT)_________' in s and pid_state.has_key(pid) and pid_state[pid]=='out started':
		pid_state[pid]='out foreign'
#		print 'out foreign'

	if '| Key (ASCII) :' in s and pid_state.has_key(pid) and pid_state[pid]=='out foreign':
		pid_state[pid]='out key'
		pid_keys[pid]=s.split('|')[3].split(' ')[4]
		if trn_lines.has_key(pid_keys[pid]):
			ss=s.split('|')[0]+'||'+pid_keys[pid]+'|'+pid+' HYPERCOM_OUT FINISHED'
			trn_lines[pid_keys[pid]].append(ss)
			print ss
#			print 'out key'

	if '| Service  HYPERCOM_OUT End   Type=[RELATIVE] UTime=[' in s and pid_state.has_key(pid) and pid_state[pid]=='out key':
		pid_state[pid]='out finished'
#		print 'out finished'


	s=f.readline()


f.close()

