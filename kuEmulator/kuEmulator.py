import socket
import time
import sys
import select
import re
import datetime
import random
import threading
import os

current_loglevel=-1
current_protocol_name='HYPERCOM'
current_host_ip='127.0.0.1'
current_port=7174
current_script_filename=''
current_message_file_type='SIMON'
current_message_filename=''

current_threads_count=1
current_threads=[]

current_pid = os.getpid()
thread_id=0

cards=[
 {
  'Card Number': '4255200016948846',
  'Card Expiry': '1912',
  'Card Sequence': '1',
  'Card Track 2': '4255200016948846D19126011045500820000'
 }
]

terminals=[
 {
  'Merchant ID': '9010001',
  'Terminal ID': '90010001',
  'MCC': '5999'
 }
]

def load_cards_from_file(filename):
	if len(filename)<=0: return []
	cards=[]
	f=open(filename,'r')
	s=f.readline()
	while s<>'':
		s=s.replace('\n','')
		if s[0]<>'#':
			cards.append({})
			cards[-1]['Card Number']=s.split(';')[0]
			cards[-1]['Card Expiry']=s.split(';')[1]
			cards[-1]['Card Sequence']=s.split(';')[2]
			cards[-1]['Card Track 2']=s.split(';')[3]
		s=f.readline()
	f.close()
#	print '    +++CARDS: %s' % len(cards)
	return cards


def load_terminals_from_file(filename):
	if len(filename)<=0: return []
	terminals=[]
	f=open(filename,'r')
	s=f.readline()
	while s<>'':
		s=s.replace('\n','')
		if s[0]<>'#':
			terminals.append({})
			terminals[-1]['Merchant ID']=s.split(';')[0]
			terminals[-1]['Terminal ID']=s.split(';')[1]
			terminals[-1]['MCC']=s.split(';')[2]
		s=f.readline()
	f.close()
#	print '    +++TERMINALS: %s' % len(terminals)
	return terminals


protocol_formats={
'HYPERCOM':
 {
  'Name': 'HYPERCOM',
  'Network Protocol Name': 'tc2',
  'Header Fields':
  [
   {'Name': 'H.1.-1', 'Default Value': chr(96)},
   {'Name': 'H.2.-1', 'Default Value': '\\00\\03'},
   {'Name': 'H.3.-1', 'Default Value': '\\00\\00'}
  ]
 }
}

network_protocol_formats={
'tc2':
 {
  'Header Length': 2,
  'Header Format': 'BIN',
  'Include Header Flag': False,
  'Suffix': ''
 }
}

fields_config={}


def logwrite(message_type, pid, thread_id, function_name, message, loglevel):
	if loglevel<=current_loglevel:
		ds=datetime.datetime.strftime(datetime.datetime.now(),'%H:%M:%S.%f')
		s = '%s|%s_%s|%s|%s| %s' % (ds, pid, str(thread_id).rjust(3,'0'), message_type, function_name, message)
		print s
		f=open('kuEmulator_'+datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d')+'.log','a')
		f.write(s+'\n')
		f.close()


def int_to_bytes(data):
	buff=''
	if type(data)==int:
		data1=data
		bytes=[]
		while data1>255:
			bytes.append(chr(data1//256))
			data1=data1%256
		bytes.append(chr(data1))
		for d in bytes:
			buff=buff+d
	else:
		buff=data
	return buff


def bin_to_printable(data):
	import string
	printable=string.ascii_letters + string.digits + string.punctuation + ' '
	st=''
	data1=data
	if type(data1)==int: data1=int_to_bytes(data1)
	for d in data1:
		if d in printable:
			st=st+d
		else:
			st=st+'\\x'+hex(ord(d))[2:].rjust(2,'0').upper()
	return st

def bin_to_printable_all_hex(data):
	import string
#	printable=string.ascii_letters + string.digits + string.punctuation + ' '
	st=''
	data1=data
	if type(data1)==int: data1=int_to_bytes(data1)
	for d in data1:
		st=st+'\\x'+hex(ord(d))[2:].rjust(2,'0').upper()
	return st


def has_all_printable_characters(data):
	buff=True
	import string
	printable=string.ascii_letters + string.digits + string.punctuation + ' '
	for d in data:
		if not d in printable:
			buff=False
			break
	return buff


def has_all_hex_characters(data):
	buff=True
	hex_characters='0123456789ABCDEF'
	for d in data:
		if not d.upper() in hex_characters:
			buff=False
			break
	return buff





def fields_config_from_file_tietoformsg(filename):
	fields_config={}
	f=open(filename,'r')
	s=f.readline()
	while s<>'':
		s=s.replace('\n','')
		if len(s)>10 and s[0]=='I':
			s_field_name='B.'
			if re.sub(' +',' ',s).split(' ')[1]=='HEAD': s_field_name='H.'
			if re.sub(' +',' ',s).split(' ')[1]=='MTI': s_field_name='M.'
			s_field_id=re.sub(' +',' ',s).split(' ')[2]
			if re.sub(' +',' ',s).split(' ')[3]=='FULL':
				s_field_subfield_id='-1'
			else:
				s_field_subfield_id=re.sub(' +',' ',s).split(' ')[3]
			s_field_length=re.sub(' +',' ',s).split(' ')[4]
			s_field_length_format=re.sub(' +',' ',s).split(' ')[5]
			s_field_data_format=re.sub(' +',' ',s).split(' ')[6]
			s_field_data_justify=re.sub(' +',' ',s).split(' ')[7]
			s_field_data_padding=s.split('[')[1].split(']')[0]
			if s_field_data_padding[0:2]=='\\x' and len(s_field_data_padding)>=4: s_field_data_padding=chr(int(s_field_data_padding[2]+s_field_data_padding[3],16))
			s_field_description=s.split('[')[2].split(']')[0]
			fieldstr=s_field_name+s_field_id+'.'+s_field_subfield_id
			fields_config[fieldstr]={}
			fields_config[fieldstr]['Field Type']=s_field_name[0]
			fields_config[fieldstr]['Field ID']=s_field_id
			fields_config[fieldstr]['Sub Field ID']=s_field_subfield_id
			fields_config[fieldstr]['Length']=int(s_field_length)
			fields_config[fieldstr]['Length Format']=s_field_length_format
			fields_config[fieldstr]['Data Format']=s_field_data_format
			fields_config[fieldstr]['Justify']=s_field_data_justify
			fields_config[fieldstr]['Padding Character']=s_field_data_padding
			fields_config[fieldstr]['Description']=s_field_description
			if fieldstr.split('.')[2][0]=='-':
				fields_config[fieldstr]['FIELD_ALIAS'] = fieldstr.split('.')[0].replace('B','F') + fieldstr.split('.')[1]
			else:
				fields_config[fieldstr]['FIELD_ALIAS'] = fieldstr.split('.')[0].replace('B','F') + fieldstr.split('.')[1] + '.' + fieldstr.split('.')[2]
			if fields_config[fieldstr]['FIELD_ALIAS'] == 'M1': fields_config[fieldstr]['FIELD_ALIAS'] = 'MTI'
		s=f.readline()
	f.close()
	return fields_config




def get_msg_from_text_file_IF(filename, fields_config):
	f=open(filename,'r')
	s=f.readline()
	msg={}
	msg_fields_order=[]
	while s<>'':
		s=s.replace('\n','')
		if 'MTI  : ' in s or '\' H.' in s or ('\' B.' in s and not '\' B.0.' in s):
			fieldname=''
			s_data=''
			if 'MTI  : ' in s:
				fieldname='M.1.-1'
				s_data=s[s.find('MTI  : ')+7:]
			if '\' H.' in s: fieldname='H.'+s[s.find('\' H.')+4:].split(' ')[0]
			if '\' B.' in s: fieldname='B.'+s[s.find('\' B.')+4:].split(' ')[0]
			if len(fieldname)>=3 and len(fieldname.split('.'))<3: fieldname=fieldname+'.-1'
			if len(fieldname)>=3 and len(fieldname.split('.'))>=3 and fieldname.split('.')[2]=='': fieldname=fieldname+'-1'
			msg[fieldname]={}
			msg_fields_order.append(fieldname)
			if s_data=='':
				if len(s.split('|'))>=4:
					s_data='|'.join(s.split('|')[3:])
				else:
					s_data=s
				s_data=s.split('[')[1].split(']')[0]
			
			s_data_new=''
			s1=''
			for i in xrange(len(s_data)):
				s1=s1+s_data[i]
				if s1[0]<>'\\':
					s_data_new=s_data_new+s1
					s1=''
				else:
					if len(s1)>=3:
						s_data_new=s_data_new+chr(int(s1[1]+s1[2],16))
						s1=''

			if fieldname in ['B.2.-1','B.35.-1','B.45.-1']: s_data_new=s_data_new.replace('*','0')
			if fieldname in ['B.52.-1','B.53.-1']: s_data_new=s_data_new.replace('*','0')

#			if fieldname.split('.')[2][0]=='-':
#				msg[fieldname]['FIELD_ALIAS'] = fieldname.split('.')[0].replace('B','F') + fieldname.split('.')[1]
#			else:
#				msg[fieldname]['FIELD_ALIAS'] = fieldname.split('.')[0].replace('B','F') + fieldname.split('.')[1] + '.' + fieldname.split('.')[2]
#			if msg[fieldname]['FIELD_ALIAS'] == 'M1': msg[fieldname]['FIELD_ALIAS'] = 'MTI'
			msg[fieldname]['DATA_TEXT']=s_data

			msg[fieldname]['DATA_PRINTABLE']=s_data_new
			msg[fieldname]['DATA_PRINTABLE_UNWRAPPED']=''
			msg[fieldname]['DATA_ENCODED']=''
			msg[fieldname]['DATA_ENCODED_FORMAT_LENGTH'] = 0
			msg[fieldname]['DATA_ENCODED_BYTES_LENGTH'] = 0
			msg[fieldname]['DATA_ENCODED_PADDED'] = ''
			msg[fieldname]['LENGTH_ENCODED'] = ''
			msg[fieldname]['LENGTH_ENCODED_FORMAT_LENGTH'] = 0
			msg[fieldname]['LENGTH_ENCODED_BYTES_LENGTH'] = 0
			msg[fieldname]['LENGTH_ENCODED_PADDED'] = ''
		s=f.readline()
	f.close()
	return msg, msg_fields_order


def fieldalias_to_fieldname(fieldalias):
	fieldname=''
	if fieldalias[0]=='H': fieldname='H.'+fieldalias[1:]
	if fieldalias[0]=='M': fieldname='M.1.-1'
	if fieldalias[0]=='B' or fieldalias[0]=='F': fieldname='B.'+fieldalias[1:]
	if len(fieldname.split('.'))<3: fieldname = fieldname + '.-1'
#	print '+0+0+ %s = %s' % (fieldalias, fieldname)
	fieldname = fieldname.split('.')[0] + '.' + fieldname.split('.')[1].lstrip('0') + '.' + fieldname.split('.')[2]
	return fieldname


def fieldname_to_fieldalias(fieldname):
	fieldalias=''
	if fieldname.split('.')[2][0]=='-':
#		fieldalias = fieldname.split('.')[0].replace('B','F') + fieldname.split('.')[1].rstrip('0')
		fieldalias = fieldname.split('.')[0].replace('B','F') + fieldname.split('.')[1].rjust(3,'0')
	else:
#		fieldalias = fieldname.split('.')[0].replace('B','F') + fieldname.split('.')[1].rstrip('0') + '.' + fieldname.split('.')[2]
		fieldalias = fieldname.split('.')[0].replace('B','F') + fieldname.split('.')[1].rjust(3,'0') + '.' + fieldname.split('.')[2]
	if fieldalias == 'M1': fieldalias = 'MTI'
	return fieldalias


def msglist_to_internalformat(message):
	msg_fields_order=[]
	msg={}
	for key, value in message.items():
		fieldname=fieldalias_to_fieldname(key)
		msg_fields_order.append(fieldname)
		msg[fieldname]={}
		msg[fieldname]['DATA_TEXT']=value
		msg[fieldname]['DATA_PRINTABLE']=value
		msg[fieldname]['DATA_PRINTABLE_UNWRAPPED']=''
		msg[fieldname]['DATA_ENCODED']=''
		msg[fieldname]['DATA_ENCODED_FORMAT_LENGTH'] = 0
		msg[fieldname]['DATA_ENCODED_BYTES_LENGTH'] = 0
		msg[fieldname]['DATA_ENCODED_PADDED'] = ''
		msg[fieldname]['LENGTH_ENCODED'] = ''
		msg[fieldname]['LENGTH_ENCODED_FORMAT_LENGTH'] = 0
		msg[fieldname]['LENGTH_ENCODED_BYTES_LENGTH'] = 0
		msg[fieldname]['LENGTH_ENCODED_PADDED'] = ''
	return msg_fields_order, msg

def internalformat_to_msglist(internal_message):
	msg={}
	for key, value in internal_message.items():
		if not (('B.0.' in key) or ('B.1.' in key)):
			fieldalias=fieldname_to_fieldalias(key)
			msg[fieldalias]=value['DATA_TEXT']
	return msg


def internal_fieldlist_sort(msg_fields, msg):
#	print '------------------------------'
#	print '-  internal_fieldlist_sort 1 -'
#	print '------------------------------'
#	for fieldname in msg_fields:
#		print '   '+fieldname
#	print '------------------------------'
	msg_fields_sort = []
	msg_fields1 = []
	msg_fields2 = {}
	for fieldname in msg_fields:
		msg_fields1.append(fieldname_to_fieldalias(fieldname))
		msg_fields2[fieldname_to_fieldalias(fieldname)]=fieldname
	msg_fields1.sort()
#	print '------------------------------'
#	print '-  internal_fieldlist_sort 2 -'
#	print '------------------------------'
#	for fieldname in msg_fields1:
#		print '   '+fieldname
#	print '------------------------------'
	for fieldalias in msg_fields1:
		if fieldalias[0]=='H': msg_fields_sort.append(msg_fields2[fieldalias])
	for fieldalias in msg_fields1:
		if fieldalias[0]=='M': msg_fields_sort.append(msg_fields2[fieldalias])
	for fieldalias in msg_fields1:
		if fieldalias[0] in ['B','F']: msg_fields_sort.append(msg_fields2[fieldalias])
	for fieldalias in msg_fields1:
		if not (fieldalias[0] in ['H','M','B','F']): msg_fields_sort.append(msg_fields2[fieldalias])
	return msg_fields_sort


def msglist_fieldlist_sort(msg_fields):
	msg_fields_sort = []
	msg_fields1 = msg_fields
	msg_fields1.sort()
#	for fieldname in msg_fields1:
#		print '   '+fieldname
#	print '------------------------------'
	for fieldname in msg_fields1:
		if fieldname[0]=='H': msg_fields_sort.append(fieldname)
	for fieldname in msg_fields1:
		if fieldname[0]=='M': msg_fields_sort.append(fieldname)
	for fieldname in msg_fields1:
		if fieldname[0] in ['B','F']: msg_fields_sort.append(fieldname)
	for fieldname in msg_fields1:
		if not (fieldname[0] in ['H','M','B','F']): msg_fields_sort.append(fieldname)
	return msg_fields_sort


def print_internal_fieldlist(msg_fields_sorted, msg, title):
#	print ''.rjust(40,'=')
	if len(title)>0:
#		print (''.rjust((40-len(title)-2)//2,'=')+' '+title+' ').ljust(40,'=')
		logwrite('DEBUG', current_pid, thread_id, title, (''.rjust((40-len(title)-2)//2,'=')+' '+title+' ').ljust(40,'='), 1)
#	else:
#		print ''.rjust(40,'=')
	for fieldname in msg_fields_sorted:
#		print '   %s = "%s"' % (fieldname_to_fieldalias(fieldname), bin_to_printable(msg[fieldname]['DATA_TEXT']))
		logwrite('DEBUG', current_pid, thread_id, title, '   %s = "%s"' % (fieldname_to_fieldalias(fieldname), bin_to_printable(msg[fieldname]['DATA_TEXT'])), 1)
#		print '   %s = "%s"' % (fieldname_to_fieldalias(fieldname), bin_to_printable(msg[fieldname]['DATA_PRINTABLE_UNWRAPPED']))
#	print ''.rjust(40,'=')
	logwrite('DEBUG', current_pid, thread_id, title, ''.rjust(40,'='), 1)


def print_msglist(msg, title):
#	print ''.rjust(40,'=')
	if len(title)>0:
#		print (''.rjust((40-len(title)-2)//2,'=')+' '+title+' ').ljust(40,'=')
		logwrite('DEBUG', current_pid, thread_id, title, (''.rjust((40-len(title)-2)//2,'=')+' '+title+' ').ljust(40,'='), 1)
#	else:
#		print ''.rjust(40,'=')
#	if len(title)>0: print title
	msg_fields=[]
	for fieldalias in msg.keys():
		msg_fields.append(fieldalias)
#	msg_fields_sorted=internal_fieldlist_sort(msg_fields)
	msg_fields_sorted=msglist_fieldlist_sort(msg_fields)
	for fieldalias in msg_fields_sorted:
#		print '   %s = "%s"' % (fieldalias, msg[fieldalias])
		logwrite('DEBUG', current_pid, thread_id, title, '   %s = "%s"' % (fieldalias, msg[fieldalias]), 1)
#	print ''.rjust(40,'=')
	logwrite('DEBUG', current_pid, thread_id, title, ''.rjust(40,'='), 1)


def get_msg_from_text_file_SIMON(filename, fields_config):
	f=open(filename,'r')
	s=f.readline()
	msg={}
	msg_fields_order=[]
	while s<>'':
		s=s.replace('\n','')
#		print 'filename="%s"    ="%s"' % (filename, s)
		if s[:3]=='MTI' or s[0]=='H' or s[0]=='F':
			fieldname=''
			s_data=''
			i=s.find(':')
			while i>0:
				if s[i-1]==' ':
					s=s[:i-1]+s[i:]
					i=s.find(':')
				else:
					i=0
			i=s.find(':')
			while i>0:
				if len(s)>i+1 and s[i+1]==' ':
					s=s[:i+1]+s[i+1+1:]
					i=s.find(':')
				else:
					i=0
			fieldname=s.split(':')[0]
			s_data=':'.join(s.split(':')[1:])
			if fieldname=='MTI':
				fieldname='M.1'
			else:
				if fieldname[0]=='H':
					fieldname='H.'+fieldname[1:]
				else:
					fieldname='B.'+fieldname[1:]

			if len(fieldname)>=3 and len(fieldname.split('.'))<3: fieldname=fieldname+'.-1'
			if len(fieldname)>=3 and len(fieldname.split('.'))>=3 and fieldname.split('.')[2]=='': fieldname=fieldname+'-1'


#			print '+++DEBUG 001: '+ fieldname
			fieldname = fieldname.split('.')[0] + '.' + fieldname.split('.')[1].lstrip('0') + '.' + fieldname.split('.')[2]
			if fieldname.split('.')[1]=='': fieldname.split('.')[0] + '.' + '0' + '.' + fieldname.split('.')[2]
#			print '+++DEBUG 002: '+ fieldname

			msg[fieldname]={}
			msg_fields_order.append(fieldname)
			s_data_new=''
			s1=''
			for i in xrange(len(s_data)):
				s1=s1+s_data[i]
				if s1[0]<>'\\':
					s_data_new=s_data_new+s1
					s1=''
				else:
					if len(s1)>=3:
						s_data_new=s_data_new+chr(int(s1[1]+s1[2],16))
						s1=''

			if fieldname in ['B.2.-1','B.35.-1','B.45.-1']: s_data_new=s_data_new.replace('*','0')
			if fieldname in ['B.52.-1','B.53.-1']: s_data_new=s_data_new.replace('*','0')

			if fieldname.split('.')[2][0]=='-':
				msg[fieldname]['FIELD_ALIAS'] = fieldname.split('.')[0].replace('B','F') + fieldname.split('.')[1].rjust(3,'0')
			else:
				msg[fieldname]['FIELD_ALIAS'] = fieldname.split('.')[0].replace('B','F') + fieldname.split('.')[1].rjust(3,'0') + '.' + fieldname.split('.')[2]
			if msg[fieldname]['FIELD_ALIAS'] == 'M1': msg[fieldname]['FIELD_ALIAS'] = 'MTI'
			msg[fieldname]['DATA_TEXT']=s_data

			msg[fieldname]['DATA_PRINTABLE']=s_data_new
			msg[fieldname]['DATA_PRINTABLE_UNWRAPPED']=''
			msg[fieldname]['DATA_ENCODED']=''
			msg[fieldname]['DATA_ENCODED_FORMAT_LENGTH'] = 0
			msg[fieldname]['DATA_ENCODED_BYTES_LENGTH'] = 0
			msg[fieldname]['DATA_ENCODED_PADDED'] = ''
			msg[fieldname]['LENGTH_ENCODED'] = ''
			msg[fieldname]['LENGTH_ENCODED_FORMAT_LENGTH'] = 0
			msg[fieldname]['LENGTH_ENCODED_BYTES_LENGTH'] = 0
			msg[fieldname]['LENGTH_ENCODED_PADDED'] = ''
		s=f.readline()
	f.close()
	return msg, msg_fields_order




def unwrap_message_fields2(fields_config,msg_fields_order,msg):
	for fieldname in msg_fields_order:
		msg[fieldname]['DATA_PRINTABLE_UNWRAPPED']=uwrap_printable_text(msg[fieldname]['DATA_PRINTABLE'])
	return msg



def encode_message_fields2(fields_config,msg_fields_order,msg):
	for fieldname in msg_fields_order:
		logwrite('DEBUG', current_pid, thread_id, 'encode_message_fields2', 'Field=%s' % (fieldname), 9)
		msg[fieldname]['DATA_ENCODED']=''
#		if fields_config.has_key(fieldname): msg[fieldname].update(fields_config[fieldname])
		if fields_config[fieldname].has_key('Data Format'):
			msg[fieldname]['DATA_ENCODED'], msg[fieldname]['DATA_ENCODED_FORMAT_LENGTH'], msg[fieldname]['DATA_ENCODED_BYTES_LENGTH'] = data_encode2(msg[fieldname]['DATA_PRINTABLE_UNWRAPPED'], 'TEXT', fields_config[fieldname]['Data Format'])
#			msg[fieldname]['DATA_ENCODED_PADDED'] = data_padding2(msg[fieldname]['DATA_ENCODED'],fields_config[fieldname]['Data Format'],msg[fieldname]['DATA_ENCODED_FORMAT_LENGTH'],fields_config[fieldname]['Justify'],fields_config[fieldname]['Padding Character'])
			msg[fieldname]['DATA_ENCODED_PADDED'] = data_padding2(msg[fieldname]['DATA_ENCODED'],fields_config[fieldname]['Data Format'],fields_config[fieldname]['Length'],fields_config[fieldname]['Justify'],fields_config[fieldname]['Padding Character'])
#			if fieldname=='B.42.-1':
#				print '------------------ DATA_ENCODED="%s"' % bin_to_printable(msg[fieldname]['DATA_ENCODED'])
#				print '------------------ DATA_ENCODED_PADDED="%s"' % bin_to_printable(msg[fieldname]['DATA_ENCODED_PADDED'])
		if fields_config[fieldname].has_key('Length') and fields_config[fieldname]['Length']<0 and fields_config[fieldname].has_key('Length Format'):
			#Variable length (negative length)
#			if fieldname=='B.35.-1':
#				print '   +++ VARIABLE FORMAT: '
			msg[fieldname]['LENGTH_ENCODED'], msg[fieldname]['LENGTH_ENCODED_FORMAT_LENGTH'], msg[fieldname]['LENGTH_ENCODED_BYTES_LENGTH'] = data_encode2(msg[fieldname]['DATA_ENCODED_FORMAT_LENGTH'], 'INT', fields_config[fieldname]['Length Format'])
			d, msg[fieldname]['LENGTH_ENCODED_FORMAT_LENGTH'], msg[fieldname]['LENGTH_ENCODED_BYTES_LENGTH'] = data_encode2(abs(fields_config[fieldname]['Length']),'INT',fields_config[fieldname]['Length Format'])
#			msg[fieldname]['LENGTH_ENCODED_PADDED'] = data_padding2(msg[fieldname]['LENGTH_ENCODED'],fields_config[fieldname]['Length Format'],msg[fieldname]['LENGTH_ENCODED_FORMAT_LENGTH'],'LEFT','')
			msg[fieldname]['LENGTH_ENCODED_PADDED'] = data_padding2(msg[fieldname]['LENGTH_ENCODED'],fields_config[fieldname]['Length Format'],msg[fieldname]['LENGTH_ENCODED_BYTES_LENGTH'],'LEFT','')
		else:
			#Fixed length (positive length)
			msg[fieldname]['LENGTH_ENCODED'], msg[fieldname]['LENGTH_ENCODED_FORMAT_LENGTH'], msg[fieldname]['LENGTH_ENCODED_BYTES_LENGTH'] = '', 0, 0
			msg[fieldname]['LENGTH_ENCODED_PADDED'] = ''
	return msg



def uwrap_printable_text(data):
	buff=''
	length_binary=0
	length_virtually=0
	if (data[0]=='"' and data[len(data)-1]=='"') or (data[0]=='\'' and data[len(data)-1]=='\'') or (data[0]=='[' and data[len(data)-1]==']'):
		data1=data[1:len(data)-1]
	else:
		data1=data
	if len(data1)>=2 and data1[:2]=='0x':
		dd=''
		data1=data1[2:]
		length_binary=len(data1)
		if len(data1)%2>0: data1=data1.rjust((len(data1)//2)*2+2,'0')
		for d in data1:
			dd=dd+d
			if len(dd)>=2:
				buff=buff+chr(int(dd,16))
				dd=''
	else:
		if len(data1)>=2 and data1[:2]=='0b':
			dd=''
			data1=data1[2:]
			length_binary=len(data1)
			if len(data1)%8>0: data1=data1.rjust((len(data1)//8)*8+8,'0')
			for d in data1:
				dd=dd+d
				if len(dd)>=8:
					buff=buff+chr(int(dd,2))
					dd=''
		else:
			if '\\x' in data1:
				dd=''
				for d in data1:
					dd=dd+d
					if dd[0]<>'\\':
						buff=buff+dd
						dd=''
					else:
						if len(dd)>=4:
							buff=buff+chr(int(dd[2:],16))
							dd=''
				length_binary=len(buff)
			else:
				if '\\' in data1:
					dd=''
					for d in data1:
						dd=dd+d
						if dd[0]<>'\\':
							buff=buff+dd
							dd=''
						else:
							if len(dd)>=3:
								buff=buff+chr(int(dd[1:],16))
								dd=''
					length_binary=len(buff)
				else:
					buff=data1
					length_binary=len(buff)
	return buff


def text_to_ebcdic2(data):
	buff=''
	length_output_format=0
	length_output_bytes=0
	buff=data.encode('cp500','strict')
	length_output_format=len(buff)
	length_outbut_bytes=length_output_format
	return buff, length_output_format, length_output_bytes


def text_to_bcd2(data):
	buff=''
	length_output_format=0
	length_output_bytes=0
	if len(data)==0:
		return '', 0, 0
	data1=data
	dd=''
	for d in data1[::-1]:
		if d.upper() in '0123456789ABCDEF':
			dd=d+dd
		else:
			if ord(d) & 0xFFFFFFF0 == 0:
				dd=hex(ord(d))[-1:]+dd
			else:
				print '!!! ERROR: bin_to_bcd2: input data "%s" contains non-BCD data "%s".' % (bin_to_printable_all_hex(data),bin_to_printable_all_hex(d))
				return '', 0, 0
		if len(dd)>=2:
			buff=dd+buff
			dd=''
	length_output_format=len(buff)
	if len(dd)>0:
		length_output_format=len(buff)+len(dd)
		if len(dd)%2<>0:
			buff='0'+dd+buff
		else:
			buff=dd+buff
	dd=''
	data1=buff
	buff=''
	for d in data1:
		dd=dd+d
		if len(dd)>=2:
			buff=buff+chr(int(dd,16))
			dd=''
	length_output_bytes=len(buff)
	return buff, length_output_format, length_output_bytes


###NEW
def bcd_to_text2(data):
	buff=''
	length_output_format=0
	length_output_bytes=0
	for d in data:
		dd=hex( (ord(d) & 0xF0) >> 4 )[-1:]
		buff = buff + dd.upper()
		dd=hex( ord(d) & 0x0F )[-1:]
		buff = buff + dd.upper()
	length_output_bytes = len(buff)
	length_output_format = length_output_bytes
	return buff, length_output_format, length_output_bytes


def bin_to_text2(data):
	buff=''
	length_output_format=0
	length_output_bytes=0
	for d in data:
		if has_all_printable_characters(d):
			buff = buff + d
		else:
			buff = buff + '\\'+hex(ord(d))[-2:].replace('x','0').upper()
	length_output_bytes = len(buff)
	length_output_format = length_output_bytes
	return buff, length_output_format, length_output_bytes


def ebcdic_to_text2(data):
	buff=''
	length_output_format=0
	length_output_bytes=0
	buff=data.decode('cp500','strict')
	length_output_format=len(buff)
	length_outbut_bytes=length_output_format
	return buff, length_output_format, length_output_bytes



def text_to_hex2(data):
	buff=''
	length_output_format=0
	length_output_bytes=0
	for d in data:
		buff=buff+hex(ord(d))[2:].rjust(2,'0').upper()
	length_output_format=len(buff)
	length_output_bytes=length_output_format
	return buff, length_output_format, length_output_bytes
	


def int_to_bcd2(data):
	buff=''
	length_output_format=0
	length_output_bytes=0
	if type(data)==int:
		data1=str(data)
		length_output_format=len(data1)
		if len(data1)%2>0: data1='0'+data1
		dd=''
		for d in data1:
			dd=dd+d
			if len(dd)>=2:
				buff=buff+chr(((ord(dd[-2:][0]) << 4) | (ord(dd[-2:][1]) & 0x0F)) & 0xFF)
				dd=''
	length_output_bytes=len(buff)
	return buff, length_output_format, length_output_bytes



def int_to_bin2(data):
#	print '    ++++ int_to_bin2: incoming = data="%s"' % (bin_to_printable_all_hex(data))
	buff=''
	length_output_format=0
	length_output_bytes=0
	if type(data)==int:
		data1=data
		dd=''
		while data1>=256:
			d=data1//256
			dd=dd+chr(d)
			data1=data1%256
		dd=dd+chr(data1)
		buff=dd
	length_output_format=len(buff)
	length_output_bytes=length_output_format
#	print '    ++++ int_to_bin2: outgoing = data="%s", length_format="%s", length_bytes="%s"' % (bin_to_printable_all_hex(buff), length_output_format, length_output_bytes)
	return buff, length_output_format, length_output_bytes


def int_to_ascii2(data):
	buff=''
	length_output_format=0
	length_output_bytes=0
	if type(data)==int:
		buff=str(data)
		length_output_format=len(buff)
		length_output_bytes=length_output_format
	return buff, length_output_format, length_output_bytes





def bin_to_int2(data):
#	print '    ++++ bin_to_int2: incoming = data="%s"' % (bin_to_printable_all_hex(data))
	buff=0
	length_output_format=0
	length_output_bytes=0
	data1=data[::-1]
	for i in xrange(len(data1)):
		d=data1[i]
		buff=buff + ord(d)*(256**i)
	length_output_format=len(str(buff))
	i=len(hex(buff)[2:])
	length_output_bytes=i//2+i%2
#	print '    ++++ bin_to_int2: outgoing = data="%s", length_format="%s", length_bytes="%s"' % (buff, length_output_format, length_output_bytes)
	return buff, length_output_format, length_output_bytes



def bin_to_strbits(data):
	buff=bin(ord(data))[2:]
	buff=buff.rjust(8,'0')
	return buff


def data_encode2(data,format_from,format_to):
	logwrite('DEBUG', current_pid, thread_id, 'data_encode2', 'start: data="%s", format_from="%s", format_to="%s"' % (bin_to_printable_all_hex(data), format_from, format_to), 9)
	buff=''
	length_format=0
	length_bytes=0
	if format_from=='TEXT':
		if format_to=='ASCII':
			buff=data
			length_format=len(data)
			length_bytes=length_format
		else:
			if format_to=='BIN':
				buff=data
				length_format=len(data)
				length_bytes=length_format
			else:
				if format_to=='BCD':
					buff, length_format, length_bytes = text_to_bcd2(data)
				else:
					if format_to=='EBCDIC':
						buff, length_format, length_bytes = text_to_ebcdic2(data)
					else:
						if format_to=='HEX':
							buff, length_format, length_bytes = text_to_hex2(data)
						else:
							print '!!! ERROR: Output format "%s" not found: data_encode2("%s","%s","%s")' % (format_to,bin_to_printable_all_hex(data),format_from,format_to)
							buff=''
							length_format=0
							length_bytes=0
	else:
		if format_from=='INT':
			if format_to=='BIN':
				buff, length_format, length_bytes = int_to_bin2(data)
			else:
				if format_to=='BCD':
					buff, length_format, length_bytes = int_to_bcd2(data)
				else:
					if format_to=='ASCII':
						buff, length_format, length_bytes = int_to_ascii2(data)
					else:
						print '!!! ERROR: Output format "%s" not found: data_encode2("%s","%s","%s")' % (format_to,bin_to_printable_all_hex(data),format_from,format_to)
						buff=''
						length_format=0
						length_bytes=0
		else:
			if format_from=='BIN':
				if format_to=='BIN':
					buff, length_format, length_bytes = data, len(data), len(data)
				else:
					if format_to=='INT':
						buff, length_format, length_bytes = bin_to_int2(data)
					else:
######### NEW NEW NEW
						if format_to=='TEXT':
							buff, length_format, length_bytes = bin_to_text2(data)
						else:
							print '!!! ERROR: Output format "%s" not found: data_encode2("%s","%s","%s")' % (format_to,bin_to_printable_all_hex(data),format_from,format_to)
							buff=''
							length_format=0
							length_bytes=0
			else:
######### NEW NEW NEW
				if format_from=='BCD':
					if format_to=='TEXT':
						buff, length_format, length_bytes = bcd_to_text2(data)
					else:
						print '!!! ERROR: Output format "%s" not found: data_encode2("%s","%s","%s")' % (format_to,bin_to_printable_all_hex(data),format_from,format_to)
						buff=''
						length_format=0
						length_bytes=0
				else:
					if format_from=='EBCDIC':
						if format_to=='TEXT':
							buff, length_format, length_bytes = ebcdic_to_text2(data)
						else:
							print '!!! ERROR: Output format "%s" not found: data_encode2("%s","%s","%s")' % (format_to,bin_to_printable_all_hex(data),format_from,format_to)
							buff=''
							length_format=0
							length_bytes=0
					else:
######### NEW NEW NEW
						if format_from=='ASCII':
							if format_to=='TEXT':
#								buff, length_format, length_bytes = data, len(data), len(data)
								buff, length_format, length_bytes = bin_to_text2(data)
							else:
								print '!!! ERROR: Output format "%s" not found: data_encode2("%s","%s","%s")' % (format_to,bin_to_printable_all_hex(data),format_from,format_to)
								buff=''
								length_format=0
								length_bytes=0
						else:
							print '!!! ERROR: Input format "%s" not found: data_encode2("%s","%s","%s")' % (format_from,bin_to_printable_all_hex(data),format_from,format_to)
	logwrite('DEBUG', current_pid, thread_id, 'data_encode2', 'end: data="%s", length_format="%s", length_bytes="%s"' % (bin_to_printable_all_hex(buff), length_format, length_bytes), 9)
	return buff, length_format, length_bytes



def data_padding2(data,format,length,padding,padchar):
	logwrite('DEBUG', current_pid, thread_id, 'data_padding2', 'start: data="%s", format="%s", length="%s", padding="%s", padchar="%s"' % (bin_to_printable(data),format,length,padding,bin_to_printable(padchar)), 9)
	buff=data
	ipadchar=padchar
	# LEFT Padding = Right Justifying
	if len(ipadchar)==0 and len(format)>0:
		if format=='ASCII':
			ipadchar=' '
		else:
			if format=='BCD':
				ipadchar=chr(0)
			else:
				if format=='BIN':
					ipadchar=chr(0)
				else:
					if format=='EBCDIC':
						ipadchar=chr(0)
					else:
						if format=='HEX':
							ipadchar='0'
						else:
							if format=='INT':
								ipadchar=chr(0)
							else:
								ipadchar=chr(0)
	if len(format)>0 and format=='BCD':
#		ilength=length//2+length%2
		ilength=length
#		print '                ----------------- padchar="%s"' % padchar
		if ipadchar in '0123456789ABCDEF': ipadchar=chr(ord(ipadchar) & 0x0F)
	else:
		ilength=length
	if len(padding)>0 and padding[0].upper()=='L':
		buff=data.rjust(ilength,ipadchar)
	else:
		buff=data.ljust(ilength,ipadchar)

	logwrite('DEBUG', current_pid, thread_id, 'data_padding2', 'end: returned data="%s"' % (bin_to_printable(buff)), 9)
	return buff




def compose_network_message2(msg_fields_order,msg,network_protocol_format_name):
#	print '##########################################################'
	logwrite('DEBUG', current_pid, thread_id, 'compose_network_message2', 'START OF NETWORK MESSAGE', 7)
	buff=''
	bitmap=compose_bitmaps(msg_fields_order)
	message=''
	mti=''
	header_fields=''
#	print ' ### BITMAPS = "%s"' % (bin_to_printable_all_hex(bitmap))
	logwrite('DEBUG', current_pid, thread_id, 'compose_network_message2', ' BITMAPS = "%s"' % (bin_to_printable_all_hex(bitmap)), 7)
	for s in msg_fields_order:
		if len(s)>=3 and s[0]=='B':
			message=message+msg[s]['LENGTH_ENCODED_PADDED']+msg[s]['DATA_ENCODED_PADDED']
#			print ' +++ FIELD %s = "%s" "%s"' % (s, bin_to_printable_all_hex(msg[s]['LENGTH_ENCODED_PADDED']), bin_to_printable_all_hex(msg[s]['DATA_ENCODED_PADDED']))
			logwrite('DEBUG', current_pid, thread_id, 'compose_network_message2', ' FIELD %s = "%s" "%s"' % (s, bin_to_printable_all_hex(msg[s]['LENGTH_ENCODED_PADDED']), bin_to_printable_all_hex(msg[s]['DATA_ENCODED_PADDED'])), 7)
		if len(s)>=3 and s[0]=='M':
			mti=mti+msg[s]['LENGTH_ENCODED_PADDED']+msg[s]['DATA_ENCODED_PADDED']
#			print ' +++ FIELD %s = "%s" "%s"' % (s, bin_to_printable_all_hex(msg[s]['LENGTH_ENCODED_PADDED']), bin_to_printable_all_hex(msg[s]['DATA_ENCODED_PADDED']))
			logwrite('DEBUG', current_pid, thread_id, 'compose_network_message2', ' FIELD %s = "%s" "%s"' % (s, bin_to_printable_all_hex(msg[s]['LENGTH_ENCODED_PADDED']), bin_to_printable_all_hex(msg[s]['DATA_ENCODED_PADDED'])), 7)
		if len(s)>=3 and s[0]=='H':
			header_fields=header_fields+msg[s]['LENGTH_ENCODED_PADDED']+msg[s]['DATA_ENCODED_PADDED']
#			print ' +++ FIELD %s = "%s" "%s"' % (s, bin_to_printable_all_hex(msg[s]['LENGTH_ENCODED_PADDED']), bin_to_printable_all_hex(msg[s]['DATA_ENCODED_PADDED']))
			logwrite('DEBUG', current_pid, thread_id, 'compose_network_message2', ' FIELD %s = "%s" "%s"' % (s, bin_to_printable_all_hex(msg[s]['LENGTH_ENCODED_PADDED']), bin_to_printable_all_hex(msg[s]['DATA_ENCODED_PADDED'])), 7)
	buff=header_fields+mti+bitmap+message
	if network_protocol_formats[network_protocol_format_name].has_key('Include Header Flag') and network_protocol_formats[network_protocol_format_name]['Include Header Flag']:
		h=len(buff)+network_protocol_formats[network_protocol_format_name]['Header Length']
	else:
		h=len(buff)
	h, lf, lb = data_encode2(h, 'INT', network_protocol_formats[network_protocol_format_name]['Header Format'])
	h=data_padding2(h,network_protocol_formats[network_protocol_format_name]['Header Format'],network_protocol_formats[network_protocol_format_name]['Header Length'],'LEFT','')
	buff=h+buff
#	print '##########################################################'
	logwrite('DEBUG', current_pid, thread_id, 'compose_network_message2', 'END OF NETWORK MESSAGE', 7)
	return buff


#========================================================================================================================================================
#========================================================================================================================================================
#========================================================================================================================================================
#========================================================================================================================================================
#========================================================================================================================================================
#========================================================================================================================================================


def compose_bitmaps(msg_fields_order):
	buff=''
	bitmaps=[chr(0)*8]
	for s in msg_fields_order:
		if len(s)>=3 and s[0]=='B':
			fieldid=int(s.split('.')[1])
			bitmapid=fieldid//64+1
			if len(bitmaps)<bitmapid:
				bitmaps.append(chr(0)*8)
				if bitmapid>1:
					bitmaps[bitmapid-1-1] = chr(int('0b10000000',2)) + chr(0) * 7

	for s in msg_fields_order:
		if len(s)>=3 and s[0]=='B':
			fieldid=int(s.split('.')[1])
			bitmapid=fieldid//64+1
			byteid=(fieldid-(bitmapid-1)*64-1)//8+1
			fieldid_in_byte=fieldid-(byteid-1)*8
			d=bitmaps[bitmapid-1]
			dd=ord(d[byteid-1]) | (int(('0b'+''.rjust(fieldid_in_byte-1,'0')+'1').ljust(8+2,'0'),2))
			d=d[:byteid-1]+chr(dd)+d[byteid:]
			bitmaps[bitmapid-1]=d
	for i in xrange(len(bitmaps)):
		buff=buff+bitmaps[i]
	return buff


#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================

def check_network_data_completion(data, current_protocol_name):
	buff=False
	if len(data) >= network_protocol_formats[protocol_formats[current_protocol_name]['Network Protocol Name']]['Header Length']:
		d, lf, lb = data_encode2(data[:network_protocol_formats[protocol_formats[current_protocol_name]['Network Protocol Name']]['Header Length']], network_protocol_formats[protocol_formats[current_protocol_name]['Network Protocol Name']]['Header Format'], 'INT')
		if len(data[network_protocol_formats[protocol_formats[current_protocol_name]['Network Protocol Name']]['Header Length']:]) >= lb:
#			print '!!!!!!!! RECEIVING FINISHED SUCESSFULLY !!!!!!!!!'
			buff=True
	return buff

def extract_message_from_network_data(data, current_protocol_name):
	buff_header=''
	buff_msg=''
	length_data=0
	logwrite('DEBUG', current_pid, thread_id, 'extract_message_from_network_data', 'Full network message with header "%s"' % (bin_to_printable_all_hex(data)), 9)
	l=network_protocol_formats[protocol_formats[current_protocol_name]['Network Protocol Name']]['Header Length']
	d, lf, lb = data_encode2(data[:l], network_protocol_formats[protocol_formats[current_protocol_name]['Network Protocol Name']]['Header Format'], 'INT')
	buff_header = data[:l]
	buff_msg = data[l:]
	if len(buff_msg)<d:
		print '!!! ERROR: extract_message_from_network_data: received data is shorter (%s) than expected (%s). Invalid data: header="%s", message="%s".' % (len(buff_msg),d,bin_to_printable_all_hex(buff_header),bin_to_printable_all_hex(buff_msg))
	else:
		if len(buff_msg)>d:
			buff_msg=buff_msg[:d]
	return buff_header, buff_msg


def extract_header_fields_from_network_data(data, protocol_name):
	headers_list=[]
	headers_data={}
	rest_of_data=data
	for i in xrange(len(protocol_formats[protocol_name]['Header Fields'])):
		fn=protocol_formats[protocol_name]['Header Fields'][i]['Name']
		logwrite('DEBUG', current_pid, thread_id, 'extract_header_fields_from_network_data', 'Trying to extract header field "%s" from network data "%s"' % (fn,bin_to_printable_all_hex(rest_of_data)), 9)
		field_lengthdat, field_data, rest_of_data = extract_field_by_name_from_network_data(fn, protocol_name, rest_of_data)
		headers_list.append(fn)
		headers_data[fn]={}
		headers_data[fn]['DATA_NETWORK_LENGTH'] = field_lengthdat
		headers_data[fn]['DATA_NETWORK_DATA'] = field_data
		logwrite('DEBUG', current_pid, thread_id, 'extract_header_fields_from_network_data', 'Field "%s" extracted sucessfully: "%s" "%s"' % (fn,bin_to_printable_all_hex(field_lengthdat),bin_to_printable_all_hex(field_data)), 9)
	return headers_list, headers_data, rest_of_data


def extract_mti_from_network_data(data, protocol_name):
	rest_of_data=data
	logwrite('DEBUG', current_pid, thread_id, 'extract_mti_from_network_data', 'Trying to extract MTI from network data "%s"' % (bin_to_printable_all_hex(rest_of_data)), 9)
	field_lengthdat, field_data, rest_of_data = extract_field_by_name_from_network_data('M.1.-1', protocol_name, rest_of_data)
	logwrite('DEBUG', current_pid, thread_id, 'extract_mti_from_network_data', 'MTI extracted sucessfully: "%s" "%s"' % (bin_to_printable_all_hex(field_lengthdat),bin_to_printable_all_hex(field_data)), 9)
	return field_lengthdat, field_data, rest_of_data


def extract_bitmaps_from_network_data(data):
	buff_bitmaps=[]
	next_bitmap=True
	rest_of_data=data
	i=1
	while next_bitmap:
		buff=rest_of_data[:8]
		rest_of_data=rest_of_data[8:]
		buff_bitmaps.append(buff)
		next_bitmap = (ord(buff[0]) & 0x80 == 1)
		logwrite('DEBUG', current_pid, thread_id, 'extract_bitmaps_from_network_data', 'Extracted Bitmap %s: HEX="%s"' % (i, bin_to_printable_all_hex(buff)), 9)
		i=i+1
	return buff_bitmaps, rest_of_data



def extract_fields_list_by_bitmaps(bitmaps):
	fields=[]
	for i in xrange(len(bitmaps)):
		for j in xrange(len(bitmaps[i])):
			b=bin_to_strbits(bitmaps[i][j])
#			print 'BITMAP=%s, BYTE=%s = "%s"' % (i, j, b)
			for k in xrange(len(b)):
				if not (j==0 and k==0) and b[k]=='1':
					fieldid=i*64+j*8+k+1
					fn='B.'+str(fieldid)+'.-1'
					fields.append(fn)
					logwrite('DEBUG', current_pid, thread_id, 'extract_fields_list_by_bitmaps', 'Bitmap %s, byte %s, extracted Field "%s"' % (i, j, fn), 9)
	return fields


def extract_fields_data_from_network_data(data, protocol_name, fields):
	fields_data={}
	rest_of_data = data
	for fn in fields:
		fields_data[fn]={}
		fields_data[fn]['Name'] = fn
		fields_data[fn]['DATA_NETWORK_LENGTH'], fields_data[fn]['DATA_NETWORK_DATA'], rest_of_data = extract_field_by_name_from_network_data(fn, protocol_name, rest_of_data)
###NEW
#		fields_data[fn]['DATA_TEXT_DATA'], fields_data[fn]['DATA_TEXT_LENGTH'], l = data_encode2(fields_data[fn]['DATA_NETWORK_DATA'], fields_config[fn]['Data Format'], 'TEXT')

		logwrite('DEBUG', current_pid, thread_id, 'extract_fields_data_from_network_data', '%s = "%s" "%s"' % (fields_data[fn]['Name'], bin_to_printable_all_hex(fields_data[fn]['DATA_NETWORK_LENGTH']), bin_to_printable_all_hex(fields_data[fn]['DATA_NETWORK_DATA'])), 9)
		logwrite('DEBUG', current_pid, thread_id, 'extract_fields_data_from_network_data', 'Rest of Data = "%s"' % (bin_to_printable_all_hex(rest_of_data)), 9)
	return fields_data



def extract_field_by_name_from_network_data(field_name, protocol_name, data):
	field_lengthdat=''
	field_data=''
	rest_of_data=''
	if fields_config.has_key(field_name):
		if fields_config[field_name]['Length']<0:
			logwrite('DEBUG', current_pid, thread_id, 'extract_field_by_name_from_network_data', 'Field "%s" has variable data length' % (field_name), 9)
			d, lf, lb = data_encode2(abs(fields_config[field_name]['Length']), 'INT', fields_config[field_name]['Length Format'])
			d, lf, lb2 = data_encode2(data[:lb], 'BIN', 'INT')
			field_lengthdat=data[:lb]
			field_data = data[lb:d]
			rest_of_data = data[lb+d:]
		else:
			logwrite('DEBUG', current_pid, thread_id, 'extract_field_by_name_from_network_data', 'Field "%s" has fixed data length' % (field_name), 9)
			field_lengthdat=''
			lb=fields_config[field_name]['Length']
			field_data = data[:lb]
			rest_of_data = data[lb:]
	else:
		logwrite('ERROR', current_pid, thread_id, 'extract_field_by_name_from_network_data', 'Not found field configuration for "%s"' % (field_name), 0)
	return field_lengthdat, field_data, rest_of_data






def parse_network_message(data, protocol_name):
	fields_list=[]
	fields_data={}
	rest_of_data=data
	network_header, rest_of_data = extract_message_from_network_data(rest_of_data, protocol_name)

#	print '----------------------------------------------------------------------'
#	print '                BEFORE: "%s"' % (bin_to_printable_all_hex(rest_of_data))
	header_fields_list, header_fields_data, rest_of_data = extract_header_fields_from_network_data(rest_of_data, protocol_name)
#	print '                 AFTER: "%s"' % (bin_to_printable_all_hex(rest_of_data))
#	print '----------------------------------------------------------------------'
	fields_list = fields_list + header_fields_list
	fields_data.update(header_fields_data)

	mti_length, mti_data, rest_of_data = extract_mti_from_network_data(rest_of_data, protocol_name)
	fn='M.1.-1'
	fields_list.append(fn)
	fields_data[fn]={}
	fields_data[fn]['DATA_NETWORK_LENGTH'] = mti_length
	fields_data[fn]['DATA_NETWORK_DATA'] = mti_data

	bitmaps, rest_of_data = extract_bitmaps_from_network_data(rest_of_data)
	for i in xrange(len(bitmaps)):
		fn = ('B.0.%s' % (i+1))
		fields_list.append(fn)
		fields_data[fn]={}
		fields_data[fn]['DATA_NETWORK_LENGTH'] = 8
		fields_data[fn]['DATA_NETWORK_DATA'] = bitmaps[i]

	body_fields_list = extract_fields_list_by_bitmaps(bitmaps)
	fields_list = fields_list + body_fields_list
	fields_data.update(extract_fields_data_from_network_data(rest_of_data, protocol_name, body_fields_list))

	for fn in fields_list:
		fields_data[fn]['DATA_TEXT'], fields_data[fn]['DATA_TEXT_LENGTH'], l = data_encode2(fields_data[fn]['DATA_NETWORK_DATA'], fields_config[fn]['Data Format'], 'TEXT')


	return 	fields_list, fields_data




def send_message_to_network(message_source, protocol_name, host_ip, host_port, **kwargs):
	response_message={}

	if message_source=='list' and kwargs and kwargs.has_key('message'):
		msg_fields, msg = msglist_to_internalformat(kwargs['message'])
		msg_fields_order = internal_fieldlist_sort(msg_fields, msg)
	else:
		if message_source=='file_if' and kwargs and kwargs.has_key('message_filename'):
			msg, msg_fields = get_msg_from_text_file_IF(kwargs['message_filename'], fields_config)
			msg_fields_order = internal_fieldlist_sort(msg_fields, msg)
		else:
			if message_source=='file_simon' and kwargs and kwargs.has_key('message_filename'):
				msg, msg_fields = get_msg_from_text_file_SIMON(kwargs['message_filename'], fields_config)
				msg_fields_order = internal_fieldlist_sort(msg_fields, msg)
#				msg_fields_order = msg_fields
		

	msg = unwrap_message_fields2(fields_config,msg_fields_order,msg)
	msg = encode_message_fields2(fields_config,msg_fields_order,msg)

	print_internal_fieldlist(msg_fields_order, msg, 'REQUEST ')

	m=compose_network_message2(msg_fields_order,msg,protocol_formats[current_protocol_name]['Network Protocol Name'])

	if kwargs and kwargs.has_key('network_timeout'):
		network_timeout=kwargs['network_timeout']
	else:
		network_timeout=5

	sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.settimeout(network_timeout)
	try:
		sock.connect((host_ip,host_port))
	except socket.error:
		print "Error happened while openning the socket"
#	time.sleep(1)


	sock.send(m)

	datetime_now=datetime.datetime.now()
	received_data=''
	while datetime.datetime.now() < (datetime_now+datetime.timedelta(seconds=network_timeout)):
		try:
			received_data = received_data + sock.recv(1024)
			if check_network_data_completion(received_data, current_protocol_name):
				resp_fields_list, resp_fields_data = parse_network_message(received_data, current_protocol_name)
				break
#			else: print '!!!!!!!!!!!!!!!!!   NOT COMPLETE   !!!!!!!!!!!!!!!!!!!!!!!'
		except socket.error:
			socket.close() 
# 	time.sleep(5)
	if sock: sock.close()

	response_message = internalformat_to_msglist(resp_fields_data)

	return response_message

#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================


import getopt
opts, args = getopt.getopt(sys.argv[1:], '', ['config_dir=', 'debug', 'loglevel=', 'filename=', 'script=', 'protocol=', 'ip=', 'port=', 'network_timeout=', 'filetype=', 'threads=', 'cards_file=', 'terminals_file='])

#print opts

for opt, arg in opts:
#	print 'INCOMING PARAMETERS:  %s = "%s"' % (opt, arg)
	if opt in ('--loglevel'):
		current_loglevel=int(arg)
	if opt in ('-debug', '--debug'):
		current_loglevel=9
	if opt in ('--ip'):
		current_host_ip=arg
	if opt in ('--port'):
		current_port=int(arg)
	if opt in ('--config_dir'):
		filename=arg+'/for_msg.cfg'
		print 'Config File Name ="'+filename+'"'
		fields_config=fields_config_from_file_tietoformsg(filename)
	if opt in ('--protocol'):
		current_protocol_name=arg
	if opt in ('--script'):
		current_script_filename=arg
	if opt in ('--filetype'):
#		print '++INCOMING PARAMETERS:  %s = "%s"' % (opt, arg)
		current_message_file_type=arg.upper()
	if opt in ('--filename'):
		current_message_filename=arg
	if opt in ('--threads'):
		current_threads_count=int(arg)
	if opt in ('--cards_file'):
		filename=arg
		cards=load_cards_from_file(filename)
#		print 'CARDS: %s' % len(cards)
	if opt in ('--terminals_file'):
		filename=arg
		terminals=load_terminals_from_file(filename)
#		print 'TERMINALS: %s' % len(terminals)



#current_loglevel=-1
#current_protocol_name='HYPERCOM'
#current_host_ip='127.0.0.1'
#current_port=7174
#current_script_filename=''
#current_message_file_type='SIMON'
#current_message_filename=''

#print_msglist(request_msg,'REQUEST')

#=============================================================================================


def thread_start(thread_id, run_seconds, **kwargs):

	d_now = datetime.datetime.now()
	d_stop = d_now + +datetime.timedelta(seconds=run_seconds)
	
	if kwargs.has_key('card_id_begin_index') and kwargs.has_key('card_id_end_index'):
		card_id_begin_index=kwargs['card_id_begin_index']
		card_id_end_index=kwargs['card_id_end_index']
	else:
		card_id_begin_index=0
		card_id_end_index=0
	if kwargs.has_key('terminal_id_begin_index') and kwargs.has_key('terminal_id_end_index'):
		terminal_id_begin_index=kwargs['terminal_id_begin_index']
		terminal_id_end_index=kwargs['terminal_id_end_index']
	else:
		terminal_id_begin_index=0
		terminal_id_end_index=0

	current_card_id=card_id_begin_index
	current_terminal_id=terminal_id_begin_index
	while d_stop>d_now:

		msgs={}
		msgs['0100_00:001']={}
		msgs['0100_00:001']['req']={}
		msgs['0100_00:001']['resp']={}
		msgs['0100_00:001']['req']['H001']='`'
		msgs['0100_00:001']['req']['H002']='0003'
		msgs['0100_00:001']['req']['H003']='0000'
		msgs['0100_00:001']['req']['MTI']='0100'
		msgs['0100_00:001']['req']['F002']=cards[current_card_id]['Card Number']
		msgs['0100_00:001']['req']['F014']=cards[current_card_id]['Card Expiry']
		msgs['0100_00:001']['req']['F003']='000000'
		msgs['0100_00:001']['req']['F004']= str(random.randint(100,10000))
		msgs['0100_00:001']['req']['F011']= str(random.randint(1,999999)).rjust(6,'0')
		msgs['0100_00:001']['req']['F022']='0012'
		msgs['0100_00:001']['req']['F024']='0003'
		msgs['0100_00:001']['req']['F025']='00'
		msgs['0100_00:001']['req']['F041']=terminals[current_terminal_id]['Terminal ID']
		msgs['0100_00:001']['req']['F042']=terminals[current_terminal_id]['Merchant ID']
		msgs['0100_00:001']['req']['F049']='0974'
		msgs['0100_00:001']['req']['F062']= str(random.randint(1,999999)).rjust(6,'0')
		msgs['0100_00:001']['req']['F063']='\\00\\08\\33\\37\\30\\30\\31\\33\\31\\30'

		msgs['0100_00:002']={}
		msgs['0100_00:002']['req']={}
		msgs['0100_00:002']['resp']={}

		msgs['0400_00:001']={}
		msgs['0400_00:001']['req']={}
		msgs['0400_00:001']['resp']={}
		msgs['0400_00:001']['req']['H001']='`'
		msgs['0400_00:001']['req']['H002']='0003'
		msgs['0400_00:001']['req']['H003']='0000'
		msgs['0400_00:001']['req']['MTI']='0400'
		msgs['0400_00:001']['req']['F002']=msgs['0100_00:001']['req']['F002']
		msgs['0400_00:001']['req']['F014']=msgs['0100_00:001']['req']['F014']
		msgs['0400_00:001']['req']['F003']=msgs['0100_00:001']['req']['F003']
		msgs['0400_00:001']['req']['F004']=msgs['0100_00:001']['req']['F004']
		msgs['0400_00:001']['req']['F011']=msgs['0100_00:001']['req']['F011']
		msgs['0400_00:001']['req']['F022']=msgs['0100_00:001']['req']['F022']
		msgs['0400_00:001']['req']['F024']=msgs['0100_00:001']['req']['F024']
		msgs['0400_00:001']['req']['F025']=msgs['0100_00:001']['req']['F025']
		msgs['0400_00:001']['req']['F041']=msgs['0100_00:001']['req']['F041']
		msgs['0400_00:001']['req']['F042']=msgs['0100_00:001']['req']['F042']
		msgs['0400_00:001']['req']['F049']=msgs['0100_00:001']['req']['F049']
		msgs['0400_00:001']['req']['F062']=msgs['0100_00:001']['req']['F062']
		msgs['0400_00:001']['req']['F063']=''

		msgs['0200_20:001']={}
		msgs['0200_20:001']['req']={}
		msgs['0200_20:001']['resp']={}
		msgs['0200_20:001']['req']['H001']='`'
		msgs['0200_20:001']['req']['H002']='0003'
		msgs['0200_20:001']['req']['H003']='0000'
		msgs['0200_20:001']['req']['MTI']='0200'
		msgs['0200_20:001']['req']['F002']=cards[current_card_id]['Card Number']
		msgs['0200_20:001']['req']['F014']=cards[current_card_id]['Card Expiry']
		msgs['0200_20:001']['req']['F003']='200000'
		msgs['0200_20:001']['req']['F004']= str(random.randint(100,10000))
		msgs['0200_20:001']['req']['F011']= str(random.randint(1,999999)).rjust(6,'0')
		msgs['0200_20:001']['req']['F022']='0012'
		msgs['0200_20:001']['req']['F024']='0003'
		msgs['0200_20:001']['req']['F025']='00'
		msgs['0200_20:001']['req']['F041']=terminals[current_terminal_id]['Terminal ID']
		msgs['0200_20:001']['req']['F042']=terminals[current_terminal_id]['Merchant ID']
		msgs['0200_20:001']['req']['F049']='0974'
		msgs['0200_20:001']['req']['F062']= str(random.randint(1,999999)).rjust(6,'0')
		msgs['0200_20:001']['req']['F063']='\\00\\08\\33\\37\\30\\30\\31\\33\\31\\30'

		msgs['0200_22:001']={}
		msgs['0200_22:001']['req']={}
		msgs['0200_22:001']['resp']={}
		msgs['0200_22:001']['req']['H001']='`'
		msgs['0200_22:001']['req']['H002']='0003'
		msgs['0200_22:001']['req']['H003']='0000'
		msgs['0200_22:001']['req']['MTI']='0200'
		msgs['0200_22:001']['req']['F002']=msgs['0200_20:001']['req']['F002']
		msgs['0200_22:001']['req']['F014']=msgs['0200_20:001']['req']['F014']
		msgs['0200_22:001']['req']['F003']='220000'
		msgs['0200_22:001']['req']['F004']=msgs['0200_20:001']['req']['F004']
		msgs['0200_22:001']['req']['F011']= str(random.randint(1,999999)).rjust(6,'0')
		msgs['0200_22:001']['req']['F022']=msgs['0200_20:001']['req']['F022']
		msgs['0200_22:001']['req']['F024']=msgs['0200_20:001']['req']['F024']
		msgs['0200_22:001']['req']['F025']=msgs['0200_20:001']['req']['F025']
		msgs['0200_22:001']['req']['F041']=msgs['0200_20:001']['req']['F041']
		msgs['0200_22:001']['req']['F042']=msgs['0200_20:001']['req']['F042']
		msgs['0200_22:001']['req']['F049']=msgs['0200_20:001']['req']['F049']
		msgs['0200_22:001']['req']['F062']=msgs['0200_20:001']['req']['F062']
		msgs['0200_22:001']['req']['F063']=''


		#Preauthorization
		msgs['0100_00:003']={}
		msgs['0100_00:003']['req']={}
		msgs['0100_00:003']['resp']={}
		msgs['0100_00:003']['req']['H001']='`'
		msgs['0100_00:003']['req']['H002']='0003'
		msgs['0100_00:003']['req']['H003']='0000'
		msgs['0100_00:003']['req']['MTI']='0100'
		msgs['0100_00:003']['req']['F002']=cards[current_card_id]['Card Number']
		msgs['0100_00:003']['req']['F014']=cards[current_card_id]['Card Expiry']
		msgs['0100_00:003']['req']['F003']='000000'
		#msgs['0100_00:003']['req']['F004']= str(random.randint(1000,9000))
		msgs['0100_00:003']['req']['F004']= '1000'
		msgs['0100_00:003']['req']['F011']= str(random.randint(1,999999)).rjust(6,'0')
		msgs['0100_00:003']['req']['F022']='0012'
		msgs['0100_00:003']['req']['F024']='0003'
		msgs['0100_00:003']['req']['F025']='06'
		msgs['0100_00:003']['req']['F041']=terminals[current_terminal_id]['Terminal ID']
		msgs['0100_00:003']['req']['F042']=terminals[current_terminal_id]['Merchant ID']
		msgs['0100_00:003']['req']['F049']='0974'
		msgs['0100_00:003']['req']['F062']= str(random.randint(1,999999)).rjust(6,'0')
		msgs['0100_00:003']['req']['F063']='\\00\\08\\33\\37\\30\\30\\31\\33\\31\\30'

		#Increment 1
		msgs['0100_00:004']={}
		msgs['0100_00:004']['req']={}
		msgs['0100_00:004']['resp']={}
		msgs['0100_00:004']['req']['H001']='`'
		msgs['0100_00:004']['req']['H002']='0003'
		msgs['0100_00:004']['req']['H003']='0000'
		msgs['0100_00:004']['req']['MTI']='0100'
		msgs['0100_00:004']['req']['F002']=msgs['0100_00:003']['req']['F002']
		msgs['0100_00:004']['req']['F014']=msgs['0100_00:003']['req']['F014']
		msgs['0100_00:004']['req']['F003']=msgs['0100_00:003']['req']['F003']
		#msgs['0100_00:004']['req']['F004']= str(int(msgs['0100_00:003']['req']['F004'].lstrip('0')) // 2)
		msgs['0100_00:004']['req']['F004']= '200'
		msgs['0100_00:004']['req']['F011']= str(random.randint(1,999999)).rjust(6,'0')
		msgs['0100_00:004']['req']['F022']=msgs['0100_00:003']['req']['F022']
		msgs['0100_00:004']['req']['F024']=msgs['0100_00:003']['req']['F024']
		msgs['0100_00:004']['req']['F025']='51'
		msgs['0100_00:004']['req']['F041']=msgs['0100_00:003']['req']['F041']
		msgs['0100_00:004']['req']['F042']=msgs['0100_00:003']['req']['F042']
		msgs['0100_00:004']['req']['F049']=msgs['0100_00:003']['req']['F049']
		msgs['0100_00:004']['req']['F062']=msgs['0100_00:003']['req']['F062']
		msgs['0100_00:004']['req']['F063']=''

		#Full Increment Reversal 1
		msgs['0400_00:004']={}
		msgs['0400_00:004']['req']={}
		msgs['0400_00:004']['resp']={}
		msgs['0400_00:004']['req']['H001']='`'
		msgs['0400_00:004']['req']['H002']='0003'
		msgs['0400_00:004']['req']['H003']='0000'
		msgs['0400_00:004']['req']['MTI']='0400'
		msgs['0400_00:004']['req']['F002']=msgs['0100_00:004']['req']['F002']
		msgs['0400_00:004']['req']['F014']=msgs['0100_00:004']['req']['F014']
		msgs['0400_00:004']['req']['F003']=msgs['0100_00:004']['req']['F003']
		msgs['0400_00:004']['req']['F004']='200'
		msgs['0400_00:004']['req']['F011']=msgs['0100_00:004']['req']['F011']
		msgs['0400_00:004']['req']['F022']=msgs['0100_00:004']['req']['F022']
		msgs['0400_00:004']['req']['F024']=msgs['0100_00:004']['req']['F024']
		msgs['0400_00:004']['req']['F025']='51'
		msgs['0400_00:004']['req']['F041']=msgs['0100_00:004']['req']['F041']
		msgs['0400_00:004']['req']['F042']=msgs['0100_00:004']['req']['F042']
		msgs['0400_00:004']['req']['F049']=msgs['0100_00:004']['req']['F049']
		#msgs['0400_00:004']['req']['F060']='1200'
		msgs['0400_00:004']['req']['F062']=msgs['0100_00:004']['req']['F062']
		msgs['0400_00:004']['req']['F063']=''


		#Increment 2
		msgs['0100_00:005']={}
		msgs['0100_00:005']['req']={}
		msgs['0100_00:005']['resp']={}
		msgs['0100_00:005']['req']['H001']='`'
		msgs['0100_00:005']['req']['H002']='0003'
		msgs['0100_00:005']['req']['H003']='0000'
		msgs['0100_00:005']['req']['MTI']='0100'
		msgs['0100_00:005']['req']['F002']=msgs['0100_00:003']['req']['F002']
		msgs['0100_00:005']['req']['F014']=msgs['0100_00:003']['req']['F014']
		msgs['0100_00:005']['req']['F003']=msgs['0100_00:003']['req']['F003']
		msgs['0100_00:005']['req']['F004']= '300'
		msgs['0100_00:005']['req']['F011']= str(random.randint(1,999999)).rjust(6,'0')
		msgs['0100_00:005']['req']['F022']=msgs['0100_00:003']['req']['F022']
		msgs['0100_00:005']['req']['F024']=msgs['0100_00:003']['req']['F024']
		msgs['0100_00:005']['req']['F025']='51'
		msgs['0100_00:005']['req']['F041']=msgs['0100_00:003']['req']['F041']
		msgs['0100_00:005']['req']['F042']=msgs['0100_00:003']['req']['F042']
		msgs['0100_00:005']['req']['F049']=msgs['0100_00:003']['req']['F049']
		msgs['0100_00:005']['req']['F062']=msgs['0100_00:003']['req']['F062']
		msgs['0100_00:005']['req']['F063']=''


		#Full Whole Preauthorisation Partial Reversal
		msgs['0400_00:003']={}
		msgs['0400_00:003']['req']={}
		msgs['0400_00:003']['resp']={}
		msgs['0400_00:003']['req']['H001']='`'
		msgs['0400_00:003']['req']['H002']='0003'
		msgs['0400_00:003']['req']['H003']='0000'
		msgs['0400_00:003']['req']['MTI']='0420'
		msgs['0400_00:003']['req']['F002']=msgs['0100_00:003']['req']['F002']
		msgs['0400_00:003']['req']['F014']=msgs['0100_00:003']['req']['F014']
		msgs['0400_00:003']['req']['F003']=msgs['0100_00:003']['req']['F003']
		msgs['0400_00:003']['req']['F004']='70'
		msgs['0400_00:003']['req']['F011']=msgs['0100_00:003']['req']['F011']
		msgs['0400_00:003']['req']['F022']=msgs['0100_00:003']['req']['F022']
		msgs['0400_00:003']['req']['F024']=msgs['0100_00:003']['req']['F024']
		msgs['0400_00:003']['req']['F025']='06'
		msgs['0400_00:003']['req']['F041']=msgs['0100_00:003']['req']['F041']
		msgs['0400_00:003']['req']['F042']=msgs['0100_00:003']['req']['F042']
		msgs['0400_00:003']['req']['F049']=msgs['0100_00:003']['req']['F049']
		msgs['0400_00:003']['req']['F060']='1230'
		msgs['0400_00:003']['req']['F062']=msgs['0100_00:003']['req']['F062']
		msgs['0400_00:003']['req']['F063']=''

		#Completetion
		msgs['0220_00:003']={}
		msgs['0220_00:003']['req']={}
		msgs['0220_00:003']['resp']={}
		msgs['0220_00:003']['req']['H001']='`'
		msgs['0220_00:003']['req']['H002']='0003'
		msgs['0220_00:003']['req']['H003']='0000'
		msgs['0220_00:003']['req']['MTI']='0220'
		msgs['0220_00:003']['req']['F002']=msgs['0100_00:003']['req']['F002']
		msgs['0220_00:003']['req']['F014']=msgs['0100_00:003']['req']['F014']
		msgs['0220_00:003']['req']['F003']=msgs['0100_00:003']['req']['F003']
		msgs['0220_00:003']['req']['F004']='1230'
		msgs['0220_00:003']['req']['F011']=msgs['0100_00:003']['req']['F011']
		msgs['0220_00:003']['req']['F022']=msgs['0100_00:003']['req']['F022']
		msgs['0220_00:003']['req']['F024']=msgs['0100_00:003']['req']['F024']
		msgs['0220_00:003']['req']['F025']='06'
		msgs['0220_00:003']['req']['F041']=msgs['0100_00:003']['req']['F041']
		msgs['0220_00:003']['req']['F042']=msgs['0100_00:003']['req']['F042']
		msgs['0220_00:003']['req']['F049']=msgs['0100_00:003']['req']['F049']
		#msgs['0220_00:003']['req']['F060']='1230'
		msgs['0220_00:003']['req']['F062']=msgs['0100_00:003']['req']['F062']
		msgs['0220_00:003']['req']['F063']=''


		response_msg={}

		if current_message_file_type=='SIMON':
			response_msg = send_message_to_network('file_simon', current_protocol_name, current_host_ip, current_port, message_filename=current_message_filename)
		if current_message_file_type=='INTERNAL':
			msg={}
			msg['H001']='`'
			msg['H002']='0003'
			msg['H003']='0000'
			msg['MTI']='0200'
			msg['F003']='000000'
			msg['F004']='10400'
			msg['F011']='141338'
			msg['F022']='0021'
			msg['F024']='0003'
			msg['F025']='00'
			msg['F035']='676280000000000919D15101010000000000'
			msg['F041']='25018185'
			msg['F042']='9294645882'
			msg['F049']='0643'
			msg['F052']='FFFFFFFF'
			msg['F062']='482533'
			msg['F063']='\\00\\08\\33\\37\\30\\30\\30\\30\\37\\35'
		#	response_msg = send_message_to_network('list', current_protocol_name, current_host_ip, current_port, message=msg)


			if True:
				title='ORIGINAL AND REVERSAL, MTI=0100:00,0400:00'
				print ''
				print ''
				print '   '+''.rjust(50,'#')
				print '   '+(''.rjust((50-len(title)-2)//2,'#')+' '+title+' ').ljust(50,'#')
				print '   '+''.rjust(50,'#')
				msgs['0100_00:001']['resp'] = send_message_to_network('list', current_protocol_name, current_host_ip, current_port, message=msgs['0100_00:001']['req'])
				print_msglist(msgs['0100_00:001']['resp'],'RESPONSE')
#				time.sleep(5)
				print ''
				msgs['0400_00:001']['req']['F063']=msgs['0100_00:001']['resp']['F063']
				msgs['0400_00:001']['resp'] = send_message_to_network('list', current_protocol_name, current_host_ip, current_port, message=msgs['0400_00:001']['req'])
				print_msglist(msgs['0400_00:001']['resp'],'RESPONSE')


			if True:
#				time.sleep(5)
				title='CREDIT AND ADJUSTMENT, MTI=0200:20,0200:22'
				print ''
				print ''
				print '   '+''.rjust(50,'#')
				print '   '+(''.rjust((50-len(title)-2)//2,'#')+' '+title+' ').ljust(50,'#')
				print '   '+''.rjust(50,'#')
				msgs['0200_20:001']['resp'] = send_message_to_network('list', current_protocol_name, current_host_ip, current_port, message=msgs['0200_20:001']['req'])
				print_msglist(msgs['0200_20:001']['resp'],'RESPONSE')
#				time.sleep(5)
				print ''
				msgs['0200_22:001']['req']['F063']=msgs['0200_20:001']['resp']['F063']
				if msgs['0200_20:001']['resp'].has_key('F037'): msgs['0200_22:001']['req']['F037']=msgs['0200_20:001']['resp']['F037']
				msgs['0200_22:001']['resp'] = send_message_to_network('list', current_protocol_name, current_host_ip, current_port, message=msgs['0200_22:001']['req'])
				print_msglist(msgs['0200_22:001']['resp'],'RESPONSE')


			if True:
#				time.sleep(5)
				title='REPEATED MESSAGE, MTI=0100:00'
				print ''
				print ''
				print '   '+''.rjust(50,'#')
				print '   '+(''.rjust((50-len(title)-2)//2,'#')+' '+title+' ').ljust(50,'#')
				print '   '+''.rjust(50,'#')
				msgs['0100_00:002']['req']=msgs['0100_00:001']['req']
				msgs['0100_00:002']['resp'] = send_message_to_network('list', current_protocol_name, current_host_ip, current_port, message=msgs['0100_00:002']['req'])
				print_msglist(msgs['0100_00:002']['resp'],'RESPONSE')


			if True:
#				time.sleep(5)
				title='PREAUTH,INC-REV,INC,PREV,COMPL MTI=0100,0100-0400,0100,0420,0220'
				print ''
				print ''
				print '   '+''.rjust(50,'#')
				print '   '+(''.rjust((50-len(title)-2)//2,'#')+' '+title+' ').ljust(50,'#')
				print '   '+''.rjust(50,'#')
				msgs['0100_00:003']['resp'] = send_message_to_network('list', current_protocol_name, current_host_ip, current_port, message=msgs['0100_00:003']['req'])
				print_msglist(msgs['0100_00:003']['resp'],'RESPONSE')


#				time.sleep(5)
				print ''
				msgs['0100_00:004']['req']['F063']=msgs['0100_00:003']['resp']['F063']
				msgs['0100_00:004']['resp'] = send_message_to_network('list', current_protocol_name, current_host_ip, current_port, message=msgs['0100_00:004']['req'])
				print_msglist(msgs['0100_00:004']['resp'],'RESPONSE')

#				time.sleep(5)
				print ''
				msgs['0400_00:004']['req']['F063']=msgs['0100_00:004']['resp']['F063']
				if msgs['0100_00:004']['resp'].has_key('F037'): msgs['0400_00:004']['req']['F037']=msgs['0100_00:004']['resp']['F037']
				if msgs['0100_00:004']['resp'].has_key('F038'): msgs['0400_00:004']['req']['F038']=msgs['0100_00:004']['resp']['F038']
				if msgs['0100_00:004']['resp'].has_key('F012'): msgs['0400_00:004']['req']['F012']=msgs['0100_00:004']['resp']['F012']
				if msgs['0100_00:004']['resp'].has_key('F013'): msgs['0400_00:004']['req']['F013']=msgs['0100_00:004']['resp']['F013']
				if msgs['0100_00:004']['resp'].has_key('F011'): msgs['0400_00:004']['req']['F011']=msgs['0100_00:004']['resp']['F011']
				msgs['0400_00:004']['resp'] = send_message_to_network('list', current_protocol_name, current_host_ip, current_port, message=msgs['0400_00:004']['req'])
				print_msglist(msgs['0400_00:004']['resp'],'RESPONSE')


#				time.sleep(5)
				print ''
				msgs['0100_00:005']['req']['F063']=msgs['0100_00:003']['resp']['F063']
				msgs['0100_00:005']['resp'] = send_message_to_network('list', current_protocol_name, current_host_ip, current_port, message=msgs['0100_00:005']['req'])
				print_msglist(msgs['0100_00:005']['resp'],'RESPONSE')


#				time.sleep(5)
				print ''
				msgs['0400_00:003']['req']['F063']=msgs['0100_00:003']['resp']['F063']
				if msgs['0100_00:003']['resp'].has_key('F037'): msgs['0400_00:003']['req']['F037']=msgs['0100_00:003']['resp']['F037']
				if msgs['0100_00:003']['resp'].has_key('F038'): msgs['0400_00:003']['req']['F038']=msgs['0100_00:003']['resp']['F038']
				if msgs['0100_00:003']['resp'].has_key('F012'): msgs['0400_00:003']['req']['F012']=msgs['0100_00:003']['resp']['F012']
				if msgs['0100_00:003']['resp'].has_key('F013'): msgs['0400_00:003']['req']['F013']=msgs['0100_00:003']['resp']['F013']
				if msgs['0100_00:003']['resp'].has_key('F011'): msgs['0400_00:003']['req']['F011']=msgs['0100_00:003']['resp']['F011']
				msgs['0400_00:003']['resp'] = send_message_to_network('list', current_protocol_name, current_host_ip, current_port, message=msgs['0400_00:003']['req'])
				print_msglist(msgs['0400_00:003']['resp'],'RESPONSE')


#				time.sleep(5)
				print ''
				msgs['0220_00:003']['req']['F063']=msgs['0100_00:003']['resp']['F063']
				if msgs['0100_00:003']['resp'].has_key('F037'): msgs['0220_00:003']['req']['F037']=msgs['0100_00:003']['resp']['F037']
				if msgs['0100_00:003']['resp'].has_key('F038'): msgs['0220_00:003']['req']['F038']=msgs['0100_00:003']['resp']['F038']
				if msgs['0100_00:003']['resp'].has_key('F012'): msgs['0220_00:003']['req']['F012']=msgs['0100_00:003']['resp']['F012']
				if msgs['0100_00:003']['resp'].has_key('F013'): msgs['0220_00:003']['req']['F013']=msgs['0100_00:003']['resp']['F013']
				if msgs['0100_00:003']['resp'].has_key('F011'): msgs['0220_00:003']['req']['F011']=msgs['0100_00:003']['resp']['F011']
				msgs['0220_00:003']['resp'] = send_message_to_network('list', current_protocol_name, current_host_ip, current_port, message=msgs['0220_00:003']['req'])
				print_msglist(msgs['0220_00:003']['resp'],'RESPONSE')


		if len(response_msg)>0: print_msglist(response_msg,'RESPONSE')

		d_now=datetime.datetime.now()
		current_card_id+=1
		if current_card_id>card_id_end_index: current_card_id=card_id_begin_index
		current_terminal_id+=1
		if current_terminal_id>terminal_id_end_index: current_terminal_id=terminal_id_begin_index



for i in xrange(current_threads_count):
	i1 = i * (len(cards)//current_threads_count)
	i2 = i1 + len(cards)//current_threads_count
	i3 = i * (len(terminals)//current_threads_count)
	i4 = i3 + len(terminals)//current_threads_count
#	print '+++ Thread %s start: i1=%s, i2=%s, i3=%s, i4=%s' % (i,i1,i2,i3,i4)
	
#	current_threads.append(threading.Thread(target=thread_start, args=(i, 1), kwargs={'card_id_begin_index':0, 'card_id_end_index':0, 'terminal_id_begin_index':0, 'terminal_id_end_index':0}))
	current_threads.append(threading.Thread(target=thread_start, args=(i, 60), kwargs={'card_id_begin_index':i1, 'card_id_end_index':i2, 'terminal_id_begin_index':i3, 'terminal_id_end_index':i4}))
	current_threads[-1].start()

