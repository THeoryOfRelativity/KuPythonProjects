import socket
import time
import sys
import select
import re
import datetime

current_protocol_name='HYPERCOM'

protocol_formats={
'HYPERCOM':
 {
  'Name': 'HYPERCOM',
  'Network Protocol Name': 'tc2'
  'Header Fields':
  {
   'H.1.-1': '',
   'H.2.-1': '',
   'H.3.-1': ''
  }
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



def fields_config_from_file(filename):
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
		s=f.readline()
	f.close()
	return fields_config


def get_msg_from_text_file_OLD(filename, fields_config):
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
			msg[fieldname]['DATA_PRINTABLE']=s_data_new
			msg[fieldname]['DATA_PRINTABLE_UNWRAPPED']=uwrap_printable_text(msg[fieldname]['DATA_PRINTABLE'])
#			print '***   %s="%s".' % (fieldname,bin_to_printable_all_hex(msg[fieldname]['DATA_PRINTABLE_UNWRAPPED']))
			msg[fieldname]['DATA_ENCODED']=''
			if fields_config.has_key(fieldname): msg[fieldname].update(fields_config[fieldname])
			if msg[fieldname].has_key('Data Format'):
				msg[fieldname]['DATA_ENCODED'], msg[fieldname]['DATA_ENCODED_FORMAT_LENGTH'], msg[fieldname]['DATA_ENCODED_BYTES_LENGTH'] = data_encode2(msg[fieldname]['DATA_PRINTABLE_UNWRAPPED'], 'TEXT', msg[fieldname]['Data Format'])
				msg[fieldname]['DATA_ENCODED_PADDED'] = data_padding2(msg[fieldname]['DATA_ENCODED'],msg[fieldname]['Data Format'],msg[fieldname]['DATA_ENCODED_FORMAT_LENGTH'],msg[fieldname]['Justify'],msg[fieldname]['Padding Character'])
			if msg[fieldname].has_key('Length') and msg[fieldname]['Length']<0 and msg[fieldname].has_key('Length Format'):
				#Variable length (negative length)
				msg[fieldname]['LENGTH_ENCODED'], msg[fieldname]['LENGTH_ENCODED_FORMAT_LENGTH'], msg[fieldname]['LENGTH_ENCODED_BYTES_LENGTH'] = data_encode2(msg[fieldname]['DATA_ENCODED_FORMAT_LENGTH'], 'INT', msg[fieldname]['Length Format'])
				d, msg[fieldname]['LENGTH_ENCODED_FORMAT_LENGTH'], msg[fieldname]['LENGTH_ENCODED_BYTES_LENGTH'] = data_encode2(abs(msg[fieldname]['Length']),'INT',msg[fieldname]['Length Format'])
				msg[fieldname]['LENGTH_ENCODED_PADDED'] = data_padding2(msg[fieldname]['LENGTH_ENCODED'],msg[fieldname]['Length Format'],msg[fieldname]['LENGTH_ENCODED_FORMAT_LENGTH'],'LEFT','')
			else:
				#Fixed length (positive length)
				msg[fieldname]['LENGTH_ENCODED'], msg[fieldname]['LENGTH_ENCODED_FORMAT_LENGTH'], msg[fieldname]['LENGTH_ENCODED_BYTES_LENGTH'] = '', 0, 0
				msg[fieldname]['LENGTH_ENCODED_PADDED'] = ''
			print '***   %s="%s" "%s"' % (fieldname,bin_to_printable_all_hex(msg[fieldname]['LENGTH_ENCODED_PADDED']),bin_to_printable_all_hex(msg[fieldname]['DATA_ENCODED_PADDED']))
		s=f.readline()
	f.close()
	return msg, msg_fields_order



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



def get_msg_from_text_file_SIMON(filename, fields_config):
	f=open(filename,'r')
	s=f.readline()
	msg={}
	msg_fields_order=[]
	while s<>'':
		s=s.replace('\n','')
		if s[:3]=='MTI' or s[0]=='H' or s[0]=='F':
			fieldname=''
			s_data=''
			i=s.find(':')
			while i>0:
				if s[i-1]==' ':
#					print '++++ was: "'+s+'"'
					s=s[:i-1]+s[i:]
#					print '++++ now: "'+s+'"'
#					print '=============================='
					i=s.find(':')
				else:
					i=0
			i=s.find(':')
			while i>0:
				if len(s)>i+1 and s[i+1]==' ':
#					print '++++ was: "'+s+'"'
					s=s[:i+1]+s[i+1+1:]
#					print '++++ now: "'+s+'"'
#					print '=============================='
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
#			print '+++   FIELD NAME = "%s"' % fieldname
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
		msg[fieldname]['DATA_ENCODED']=''
		if fields_config.has_key(fieldname): msg[fieldname].update(fields_config[fieldname])
		if msg[fieldname].has_key('Data Format'):
			msg[fieldname]['DATA_ENCODED'], msg[fieldname]['DATA_ENCODED_FORMAT_LENGTH'], msg[fieldname]['DATA_ENCODED_BYTES_LENGTH'] = data_encode2(msg[fieldname]['DATA_PRINTABLE_UNWRAPPED'], 'TEXT', msg[fieldname]['Data Format'])
			msg[fieldname]['DATA_ENCODED_PADDED'] = data_padding2(msg[fieldname]['DATA_ENCODED'],msg[fieldname]['Data Format'],msg[fieldname]['DATA_ENCODED_FORMAT_LENGTH'],msg[fieldname]['Justify'],msg[fieldname]['Padding Character'])
		if msg[fieldname].has_key('Length') and msg[fieldname]['Length']<0 and msg[fieldname].has_key('Length Format'):
			#Variable length (negative length)
			msg[fieldname]['LENGTH_ENCODED'], msg[fieldname]['LENGTH_ENCODED_FORMAT_LENGTH'], msg[fieldname]['LENGTH_ENCODED_BYTES_LENGTH'] = data_encode2(msg[fieldname]['DATA_ENCODED_FORMAT_LENGTH'], 'INT', msg[fieldname]['Length Format'])
			d, msg[fieldname]['LENGTH_ENCODED_FORMAT_LENGTH'], msg[fieldname]['LENGTH_ENCODED_BYTES_LENGTH'] = data_encode2(abs(msg[fieldname]['Length']),'INT',msg[fieldname]['Length Format'])
			msg[fieldname]['LENGTH_ENCODED_PADDED'] = data_padding2(msg[fieldname]['LENGTH_ENCODED'],msg[fieldname]['Length Format'],msg[fieldname]['LENGTH_ENCODED_FORMAT_LENGTH'],'LEFT','')
		else:
			#Fixed length (positive length)
			msg[fieldname]['LENGTH_ENCODED'], msg[fieldname]['LENGTH_ENCODED_FORMAT_LENGTH'], msg[fieldname]['LENGTH_ENCODED_BYTES_LENGTH'] = '', 0, 0
			msg[fieldname]['LENGTH_ENCODED_PADDED'] = ''
	return msg



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




#def ascii_to_bcd2(data):
#	buff=''
#	if not has_all_hex_characters(data):
#		print '!!! ERROR: ascii_to_bcd2: Incoming data can\'t be converted to BCD, because have non-hex characters. data="%s".' % data
#		return
##	for 

def uwrap_printable_text(data):
	buff=''
	length_binary=0
	length_virtually=0
	if (data[0]=='"' and data[len(data)-1]=='"') or (data[0]=='\'' and data[len(data)-1]=='\'') or (data[0]=='[' and data[len(data)-1]==']'):
		data1=data[1:len(data)-1]
#		print '---------------------------'
#		print 'was: "%s"' % bin_to_printable(data)
#		print 'now: "%s"' % bin_to_printable(data1)
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
#	return buff, length_binary
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


#def int_to_bin2(data):
#	print '    ++++ int_to_bin2: incoming = data="%s"' % (bin_to_printable_all_hex(data))
#	buff=''
#	length_output_format=0
#	length_output_bytes=0
#	if type(data)==int:
#		data1=str(data)
#		for d in data1:
#			buff=buff+chr(int(d))
#	length_output_format=len(buff)
#	length_output_bytes=length_output_format
#	print '    ++++ int_to_bin2: outgoing = data="%s", length_format="%s", length_bytes="%s"' % (bin_to_printable_all_hex(buff), length_output_format, length_output_bytes)
#	return buff, length_output_format, length_output_bytes
def int_to_bin2(data):
	print '    ++++ int_to_bin2: incoming = data="%s"' % (bin_to_printable_all_hex(data))
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
	print '    ++++ int_to_bin2: outgoing = data="%s", length_format="%s", length_bytes="%s"' % (bin_to_printable_all_hex(buff), length_output_format, length_output_bytes)
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
	print '    ++++ bin_to_int2: incoming = data="%s"' % (bin_to_printable_all_hex(data))
	buff=0
	length_output_format=0
	length_output_bytes=0
	data1=data[::-1]
#	print '++++++++++++++++'
#	print type(data)
#	print '++++++++++++++++'
#	print type(data1)
#	print '++++++++++++++++'
	for i in xrange(len(data1)):
		d=data1[i]
		buff=buff + ord(d)*(256**i)
	length_output_format=len(str(buff))
	i=len(hex(buff)[2:])
	length_output_bytes=i//2+i%2
	print '    ++++ bin_to_int2: outgoing = data="%s", length_format="%s", length_bytes="%s"' % (buff, length_output_format, length_output_bytes)
	return buff, length_output_format, length_output_bytes





def data_encode2(data,format_from,format_to):
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
						print '!!! ERROR: Output format "%s" not found: data_encode2("%s","%s","%s")' % (format_to,bin_to_printable_all_hex(data),format_from,format_to)
						buff=''
						length_format=0
						length_bytes=0
			else:
				print '!!! ERROR: Input format "%s" not found: data_encode2("%s","%s","%s")' % (format_from,bin_to_printable_all_hex(data),format_from,format_to)
	return buff, length_format, length_bytes



def data_padding2(data,format,length,padding,padchar):
#	print '    ++++ data_padding2: incoming = data="%s", format="%s", length="%s", padding="%s", padchar="%s"'% (bin_to_printable_all_hex(data), format, length, padding, padchar)
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
		ilength=length//2+length%2
	else:
		ilength=length
	if len(padding)>0 and padding[0].upper()=='L':
		buff=data.rjust(ilength,ipadchar)
	else:
		buff=data.rjust(ilength,ipadchar)

#	print '    ++++ data_padding2: outgoing = data="%s"'% (bin_to_printable_all_hex(buff))
	return buff




def compose_message2(msg_fields_order,msg,network_protocol_format_name):
	print '##########################################################'
	buff=''
	bitmap=compose_bitmaps(msg_fields_order)
	message=''
	mti=''
	header_fields=''
	print ' ### BITMAPS = "%s"' % (bin_to_printable_all_hex(bitmap))
	for s in msg_fields_order:
		if len(s)>=3 and s[0]=='B':
			message=message+msg[s]['LENGTH_ENCODED_PADDED']+msg[s]['DATA_ENCODED_PADDED']
			print ' +++ FIELD %s = "%s" "%s"' % (s, bin_to_printable_all_hex(msg[s]['LENGTH_ENCODED_PADDED']), bin_to_printable_all_hex(msg[s]['DATA_ENCODED_PADDED']))
		if len(s)>=3 and s[0]=='M':
			mti=mti+msg[s]['LENGTH_ENCODED_PADDED']+msg[s]['DATA_ENCODED_PADDED']
			print ' +++ FIELD %s = "%s" "%s"' % (s, bin_to_printable_all_hex(msg[s]['LENGTH_ENCODED_PADDED']), bin_to_printable_all_hex(msg[s]['DATA_ENCODED_PADDED']))
		if len(s)>=3 and s[0]=='H':
			header_fields=header_fields+msg[s]['LENGTH_ENCODED_PADDED']+msg[s]['DATA_ENCODED_PADDED']
			print ' +++ FIELD %s = "%s" "%s"' % (s, bin_to_printable_all_hex(msg[s]['LENGTH_ENCODED_PADDED']), bin_to_printable_all_hex(msg[s]['DATA_ENCODED_PADDED']))
	buff=header_fields+mti+bitmap+message
	if network_protocol_formats[network_protocol_format_name].has_key('Include Header Flag') and network_protocol_formats[network_protocol_format_name]['Include Header Flag']:
		h=len(buff)+network_protocol_formats[network_protocol_format_name]['Header Length']
	else:
		h=len(buff)
	h, lf, lb = data_encode2(h, 'INT', network_protocol_formats[network_protocol_format_name]['Header Format'])
	h=data_padding2(h,network_protocol_formats[network_protocol_format_name]['Header Format'],network_protocol_formats[network_protocol_format_name]['Header Length'],'LEFT','')
	buff=h+buff
	print '##########################################################'
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
#			print "--------------------------"
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
	if len(received_data) >= network_protocol_formats[protocol_formats[current_protocol_name]['Network Protocol Name']]['Header Length']:
		d, lf, lb = data_encode2(received_data[:network_protocol_formats[protocol_formats[current_protocol_name]['Network Protocol Name']]['Header Length']], network_protocol_formats[protocol_formats[current_protocol_name]['Network Protocol Name']]['Header Format'], 'INT')
		if len(received_data[network_protocol_formats[protocol_formats[current_protocol_name]['Network Protocol Name']]['Header Length']:]) >= lb:
#			print '!!!!!!!! RECEIVING FINISHED SUCESSFULLY !!!!!!!!!'
			buff=True
	return buff

def extract_message_from_network_data(data, current_protocol_name):
	buff_header=''
	buff_msg=''
	length_data=0
	d, lf, lb = data_encode2(received_data[:network_protocol_formats[protocol_formats[current_protocol_name]['Network Protocol Name']]['Header Length']], network_protocol_formats[protocol_formats[current_protocol_name]['Network Protocol Name']]['Header Format'], 'INT')
	buff_header = received_data[:len(data)-d]
	buff_msg = received_data[len(data)-d:]
	return buff_header, buff_msg

def extract_bitmaps_from_network_data(data):
	buff_bitmaps=[]
	buff_msg=''
	next_bitmap=True
	buff_msg=data
	while next_bitmap:
		buff=buff_msg[:8]
		buff_msg=buff_msg[8:]
		buff_bitmaps.append(buff)
		next_bitmap = (buff[0] & 0x80 == 1)
	return buff_bitmaps, buff_msg


#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================


d=chr(1)+chr(2)+chr(3)
d='456789D'+chr(16)+'1010002'
#d2, lf, lb = text_to_bcd2(d)
#print 'LENGTH(bytes): %s (length by format=%s), iDATA="%s", oDATA="%s", oDATA(str)="%s"' % (lb,lf,d,bin_to_printable_all_hex(d2),d2)

d=chr(0x9F)+chr(0x10)+chr(0x01)+chr(0xAA)
#d2, lf, lb = text_to_hex2(d)
#print 'LENGTH(bytes): %s (length by format=%s), iDATA="%s", oDATA="%s", oDATA(str)="%s"' % (lb,lf,d,bin_to_printable_all_hex(d2),d2)


#import sys
#sys.exit(0)

#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================



sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#sock.setblocking(0)
sock.settimeout(10)

#s.close()
host='10.57.10.148'
#host=''
#port=5501
port=5050
#port=95077

#CUP
host='127.0.0.1'
port=6088

#HYPERCOM1
host='127.0.0.1'
port=7174

try:
	sock.connect((host,port))
except socket.error:
	print "Error happened while openning the socket"


time.sleep(1)

if len(sys.argv)>=3:
	filename=sys.argv[2]+'/for_msg.cfg'
	print 'Config File Name ="'+filename+'"'
	fields_config=fields_config_from_file(filename)

#for key, value in fields_config.items():
#	print key
#	for key1, value1 in value.items():
#		print '   %s = [%s]' % (key1, value1)
#	print ''

if len(sys.argv)>=2:
	filename=sys.argv[1]
	print 'File Name ="'+filename+'"'
#	msg, msg_fields_order = get_msg_from_text_file(filename, fields_config)

#	msg, msg_fields_order = get_msg_from_text_file_IF(filename, fields_config)
	msg, msg_fields_order = get_msg_from_text_file_SIMON(filename, fields_config)
	msg = unwrap_message_fields2(fields_config,msg_fields_order,msg)
	msg = encode_message_fields2(fields_config,msg_fields_order,msg)


	print '====================================================='
###	for s in msg_fields_order:
###		print s
###		for key1, value1 in msg[s].items():
###			print '   %s = [%s]' % (key1, value1)
#		print '   ### NETWORK DATA ### = [%s]' % bin_to_printable_all_hex(compose_field_data_for_network(msg[s]))
###		msg[s]['DATA_ENCODED']=compose_field_data_for_network(msg[s])

#		if s=='H.2.-1':
#			msg[s]['DATA_NEW']=msg[s]['DATA_NEW']+chr(0)+chr(0)
#			print '    H.2.-1 (data)= '+bin_to_printable_all_hex(msg[s]['DATA'])
#			print '    H.2.-1 (netw)= '+bin_to_printable_all_hex(msg[s]['DATA_NEW'])
#		if s=='H.3.-1':
#			msg[s]['DATA_NEW']=msg[s]['DATA_NEW']+chr(0)+chr(0)
###		print ""



#	sendbuf=''
#	s1=''
#	for i in xrange(len(s)):
#		s1=s1+s[i]
#		if s1[0]<>'\\':
#			sendbuf=sendbuf+s1
#			s1=''
#		else:
#			if len(s1)>=3:
#				sendbuf=sendbuf+chr(int(s1[1]+s1[2],16))
#				s1=''
#else:
#	sendbuf="11007000000000000000164255200016948846010000000000000001"
#messlen=len(sendbuf)
#print "length is %s" % messlen
#byte1=messlen//256
#byte2=messlen%256
#print "byte1=%s" % byte1
#print "byte2=%s" % byte2


m=compose_message2(msg_fields_order,msg,protocol_formats[current_protocol_name]['Network Protocol Name'])

print 'MESSAGE='+bin_to_printable_all_hex(m)

sock.send(m)


datetime_now=datetime.datetime.now()
timeout_seconds=5
print '----------------------------------------------------'
print 'Receiving ...'
received_data=''
while datetime.datetime.now() < (datetime_now+datetime.timedelta(seconds=timeout_seconds)):
	try:
		received_data = received_data + sock.recv(1024)
		if check_network_data_completion(received_data, current_protocol_name):
			print '!!!!!!!! RECEIVING FINISHED SUCESSFULLY !!!!!!!!!'
			d1, d2 = extract_message_from_network_data(received_data, current_protocol_name)
			print 'RECEIVED LENGTH=%s, HEADER="%s", DATA="%s"' % (len(d2), bin_to_printable_all_hex(d1), bin_to_printable_all_hex(d2))
			break
	except socket.error:
		socket.close() 

print 'Receiving finished'
print '----------------------------------------------------'

time.sleep(5)


if sock: sock.close()




