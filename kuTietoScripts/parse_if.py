import sys

def parse_block(bl,fn):
	ff={}
	if len(bl)>0:
		ff['P.FILENAME']=fn
		ff['P.PID']=bl[0].split('|')[2]
		ff['P.TIME_BEGIN']=bl[0].split('|')[0]
		ff['P.TIME_END']=bl[-1].split('|')[0]
	for i in xrange(len(bl)):
		if '| Type : ' in bl[i]: ff['P.TYPE']=bl[i].split('|')[3].split(':')[1].strip()
		if '| Class : ' in bl[i]: ff['P.CLASS']=bl[i].split('|')[3].split(':')[1].strip()
		if '| Function: ' in bl[i]:
			ff['P.FUNCTION_NUMBER']=bl[i].split('|')[3].split(':')[1].split('[')[0].strip()
			ff['P.FUNCTION_NAME']=bl[i].split('|')[3].split(':')[1].split('[')[1].split(']')[0]
		if '| Key  : ' in bl[i]: ff['P.KEY']=bl[i].split('|')[3].split(':')[1].strip()
		if '| Key (ASCII) : ' in bl[i]: ff['P.KEY_ASCII']=bl[i].split('|')[3].split(':')[1].strip()
		if '| MTI  : ' in bl[i]: ff['M.001']=bl[i].split('|')[3].split(':')[1].strip()
		if '\' H.' in bl[i]:
			s=bl[i].split('\'')[2].split(':')[0].strip()
			s='H.'+s.split('.')[1].rjust(3,'0')
			if len(s.split('.'))>2:
				s=s+'.'+s.split('.')[2].rjust(3,'0')+'.'+'.'.join(s.split('.')[3:])
			if len(s.split('.'))>3:
				s=s+'.'+'.'.join(s.split('.')[3:])
			ff[s]=bl[i].split('\'')[2].split(':')[1].split('[')[1].split(']')[0]
		if '\' B.' in bl[i]:
			s=bl[i].split('\'')[2].split(':')[0].strip()
			s='B.'+s.split('.')[1].rjust(3,'0')
			if len(s.split('.'))>2:
				s=s+'.'+s.split('.')[2].rjust(3,'0')+'.'+'.'.join(s.split('.')[3:])
			if len(s.split('.'))>3:
				s=s+'.'+'.'.join(s.split('.')[3:])
			ff[s]=bl[i].split('\'')[2].split(':')[1].split('[')[1].split(']')[0]
	return ff

def parse_files(files):
	fml=[]
	fml_temp={}
	for filename in files:
		filename=filename
#		print 'Parsing file "%s" ...' % filename
		f=open(filename,'r')
		fn=filename
		if '\\' in fn: fn=fn.split('\\')[-1]
		s=f.readline()
		while s<>'':
			if not '|' in s or len(s.split('|'))<3:
				s=f.readline()
				continue
			sys.stdout.write('\r ... Parsing file "%s": %s' % (filename, s.split('|')[0]))
			sys.stdout.flush()
#			try:
			if True:
				s=s.replace('\n','')
				pid=s.split('|')[2]
				if '_Message from Foreign (FOREIGN FORMAT)_' in s:
					fml_temp[fn+'_'+pid]=[]
					fml_temp[fn+'_'+pid].append(s)
				else:
					if fml_temp.has_key(fn+'_'+pid) and type(fml_temp[fn+'_'+pid]) is list and len(fml_temp[fn+'_'+pid])>0:
						if  '____________' in s:
							fml.append(parse_block(fml_temp[fn+'_'+pid],fn))
							del fml_temp[fn+'_'+pid]
						else:
							fml_temp[fn+'_'+pid].append(s)
#			except:
#				print '!!! ERROR in line "%s". continue processing ...' % s
			s=f.readline()

		sys.stdout.write('\n')
		sys.stdout.flush()
		f.close()

	return fml



cmode=''

if len(sys.argv)<2:
	print 'Please give input parameter'
	sys.exit(0)

if sys.argv[1]=='-r':
	cmode='r'
	if len(sys.argv)<3:
		print 'Please give file names separated by comma as parameter for -r (read IF files) option'
		print 'Example:'
		print ' python parse_if.py -r VISA_DMS_SRV_VISA_DMS_140901.log VISA_DMS_SRV_VISA_DMS_140902.log VISA_DMS_SRV_VISA_DMS_140903.log'
		sys.exit(0)
else:
	if sys.argv[1]=='-l':
		cmode='l'
		if len(sys.argv)<3:
			print 'Please give file names separated by comma as parameter for -l (load messages from file) option'
			print 'Example:'
			print ' python parse_if.py -l parse_if_messages.dat'
			sys.exit(0)


if cmode=='r':
	print 'Started parsing interface log files : "%s"' % ','.join(sys.argv[2:])
	fml=parse_files(sys.argv[2:])
	f=open('parse_if_messages.dat','w')
	f.write(str(fml))
	f.close()
	print 'Finished parsing interface log files : "%s"' % ','.join(sys.argv[2:])
else:
	if cmode=='l':
		print 'Started reading messages file "%s"' % sys.argv[2]
		f=open(sys.argv[2],'r')
		fml=eval(f.read())
		f.close()
		print 'Finished reading messages file "%s"' % sys.argv[2]



for i in xrange(len(fml)):
	temp_list1=[]
	temp_list2=[]
	temp_list3=[]
	temp_list4=[]
	for key in fml[i].keys():
		if key.find('P.')==0:
			temp_list1.append(key)
		else:
			if key.find('H.')==0:
				temp_list2.append(key)
			else:
				if key.find('B.')==0:
					temp_list4.append(key)
				else:
					temp_list3.append(key)
	temp_list1.sort()
	temp_list2.sort()
	temp_list3.sort()
	temp_list4.sort()
	temp_list0=temp_list1+temp_list2+temp_list3+temp_list4
#	if fml[i].has_key('B.018') and fml[i]['B.018']=='6012' and fml[i].has_key('B.003') and fml[i]['B.003']=='100000' and fml[i].has_key('B.055') and fml[i].has_key('P.TYPE') and fml[i]['P.TYPE']=='REQUEST':
#	if fml[i].has_key('B.018') and fml[i]['B.018']=='7995' and fml[i].has_key('B.003') and fml[i]['B.003']=='110000' and not fml[i].has_key('B.055') and fml[i].has_key('P.TYPE') and fml[i]['P.TYPE']=='REQUEST':
	if fml[i].has_key('B.018') and fml[i]['B.018']=='7995' and fml[i].has_key('P.TYPE') and fml[i]['P.TYPE']=='REQUEST':
#	if fml[i].has_key('B.018') and not fml[i]['B.018'] in ['6012','7995'] and fml[i].has_key('B.003') and fml[i]['B.003']=='110000' and not fml[i].has_key('B.055') and fml[i].has_key('P.TYPE') and fml[i]['P.TYPE']=='REQUEST':
		for j in xrange(len(temp_list0)):
			if temp_list0[j] in ['B.002','B.003','B.055',]:
				print '%s = [%s]' % (temp_list0[j], fml[i][temp_list0[j]])
#		print ''
		print '--------------------------------------------------------------------------------'
#		print ''



