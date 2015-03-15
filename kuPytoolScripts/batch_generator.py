#!/usr/bin/env pytool
#
# Created by Irakli Khubashvili 02.07.2014
#
# Script run format:
#   pytool batch_generator.py [auth=<MTI=1100 authorisations count>] [tps=<TPS value>] [debug]
# Example:
#   pytool batch_generator.py auth=10 tps=1
#



import tuxedo
import time
import os
import sys
import getopt
import random
import datetime


def get_tag_data(st,tagname):
	i1=st.find('<'+tagname+'>')
	i1=i1+len('<'+tagname+'>')
        i2=st.find('</'+tagname+'>')
	if i2-i1>0: s=st[i1:i2]
	else: s=''
	return s

def log(message):
	import datetime
	global RTPSLOGPATH
	try:
	       	f=open(RTPSLOGPATH+'/batch_generator_'+datetime.datetime.now().strftime('%Y%m%d')+'.log','a')
	except:
		print '\033[91m'+'!!! ERROR: Failed to open/create file "%s"'+'\033[0m' % (RTPSLOGPATH+'/batch_generator_'+datetime.datetime.now().strftime('%Y%m%d')+'.log')
	try:
       	        f.write(datetime.datetime.now().strftime('%H:%M:%S.%f')+'|'+message+'\n')
	except:
                print '\033[91m'+'!!! ERROR: Failed writing data to file "%s"'+'\033[0m' % (RTPSLOGPATH+'/batch_generator_'+datetime.datetime.now().strftime('%Y%m%d')+'.log')
	finally:
		f.close()

def PrintMessage(message,type='MSG'):
	global params
	if type=='ERR':
		colors='\033[91m'
		colore='\033[0m'
		messpref='!!! ERROR: '
	if type=='MSG' or type=='DBG':
                colors='\033[92m'
                colore='\033[0m'
                messpref='  '
        if type=='HDR':
                colors='\033[94m'
                colore='\033[0m'
                messpref=''

        if not (type=='DBG' and not params['debug_mode']):
		print colors+messpref+message+colore
		log('|'+type+'|'+messpref+message)



def generate_1100(parameters):
	fml={}
	fml['MSG_TYPE']='1100'
	fml['FLD_004']=random.randint(500,1000)
	fml['FLD_002']=params['card:exp:track1:track2'].split(':')[0]
	fml['FLD_003']='000000'
	fml['FLD_012']=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	fml['FLD_014']=params['card:exp:track1:track2'].split(':')[1]
	fml['FLD_022']=params['point_code']
	fml['FLD_024']='100'
#	fml['FLD_024']='101'
#	fml['FLD_025']='1510'
	fml['FLD_025']='1806'
	fml['FLD_028']=datetime.datetime.now().strftime('%Y%m%d')+'000000'
	fml['FLD_029']=params['reoncile_counter']
	fml['FLD_031']='BATCH GENERATOR'
	fml['FLD_033']=params['forwarder']
#	fml['FLD_035']=params['card:exp:track1:track2'].split(':')[2]
	fml['FLD_037']=datetime.datetime.now().strftime('%Y%m%d')+str(parameters['refnr_counter']).rjust(4,'0')
#	fml['FLD_037']=datetime.datetime.now().strftime('%H%M%S')+str(parameters['refnr_counter']).rjust(4,'0')
	fml['FLD_041']=params['terminal_id']
	fml['FLD_042']=params['merchant_id']
	fml['FLD_049']=params['trn_currency']
	fml['FLD_094']=params['forwarder']
#	fml['FLD_123']='?222'

# for TEST CH transformer
#        if auth_id<=1:
#		fml['MSG_TYPE']='1200'
#		fml['FLD_024']='200'
#		fml['FLD_003']='200000'
#		fml['FLD_042']='8000120'
#		fml['FLD_041']='IPOS0004'


#	if auth_id==1 or auth_id==5: fml['FLD_003']='000000'
#	if auth_id==2 or auth_id==4:
#		fml['MSG_TYPE']='1200'
#		fml['FLD_024']='200'
#		fml['FLD_003']='200000'
#	if auth_id==3: fml['FLD_003']='100000'



#	if auth_id==2 or auth_id==6: fml['FLD_003']='000000'
#        if auth_id==3 or auth_id==5:
#		fml['MSG_TYPE']='1200'
#		fml['FLD_024']='200'
#		fml['FLD_003']='200000'
#	if auth_id==4: fml['FLD_003']='100000'
#	if auth_id==1 or auth_id==7:
#		fml['FLD_003']='310000'
#		fml['FLD_024']='108'
#		fml['FLD_004']=0



#        if auth_id>=4:
#		fml['MSG_TYPE']='1200'
#		fml['FLD_024']='200'
#		fml['FLD_003']='260000'


# RS TEST
#	fml['MSG_TYPE']='1420'
#	fml['FLD_024']='400'
#	fml['FLD_025']='4000'
#	fml['FLD_038']=datetime.datetime.now().strftime('%H%M%S')
#	fml['FLD_039']='400'
#	fml['FLD_030A']=fml['FLD_004']
#	fml['FLD_030B']=0
#	fml['FLD_056A']='1100'
#	fml['FLD_056B']='331021'
#	fml['FLD_056C']='20140721101847'
#	fml['FLD_056D']='10000001194'
#	fml['FLD_033']='1120109222'

#	fml['MSG_TYPE']='1200'
#	fml['FLD_024']='200'
#	fml['FLD_003']='260000'


	return fml
	



def generate_1200(parameters):
	fml={}
	fml['MSG_TYPE']='1200'
	fml['FLD_004']=random.randint(1,1000)
	fml['FLD_002']=params['card:exp:track1:track2'].split(':')[0]
	fml['FLD_003']='000000'
	fml['FLD_012']=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	fml['FLD_014']=params['card:exp:track1:track2'].split(':')[1]
	fml['FLD_022']=params['point_code']
	fml['FLD_024']='200'
	fml['FLD_025']='1510'
	fml['FLD_028']=datetime.datetime.now().strftime('%Y%m%d')+'000000'
	fml['FLD_029']=params['reoncile_counter']
	fml['FLD_031']='BATCH GENERATOR'
	fml['FLD_033']=params['forwarder']
	fml['FLD_035']=params['card:exp:track1:track2'].split(':')[2]
	fml['FLD_037']=datetime.datetime.now().strftime('%Y%m%d')+str(parameters['refnr_counter']).rjust(4,'0')
	fml['FLD_041']=params['terminal_id']
	fml['FLD_042']=params['merchant_id']
	fml['FLD_049']=params['trn_currency']
	fml['FLD_094']=params['forwarder']
	return fml
	



def generate_1120(fml_req,fml_resp,parameters):
	fml={}
	fml['MSG_TYPE']='1120'
	fml['FLD_004']=fml_req['FLD_004']
	fml['FLD_002']=fml_req['FLD_002']
	fml['FLD_003']=fml_req['FLD_003']
	fml['FLD_012']=fml_req['FLD_012']
	fml['FLD_014']=fml_req['FLD_014']
	if fml_resp.has_key('FLD_015'): fml['FLD_015']=fml_resp['FLD_015']
	fml['FLD_022']=fml_req['FLD_022']
	fml['FLD_024']='100'
	fml['FLD_025']='1510'
	fml['FLD_028']=fml_req['FLD_028']
	fml['FLD_029']=fml_req['FLD_029']
	fml['FLD_031']='BATCH GENERATOR'
	fml['FLD_033']=fml_req['FLD_033']
	fml['FLD_035']=params['card:exp:track1:track2'].split(':')[2]
	fml['FLD_037']=fml_req['FLD_037']
	fml['FLD_038']=fml_resp['FLD_038']
	fml['FLD_039']=fml_resp['FLD_039']
	fml['FLD_041']=fml_req['FLD_041']
	fml['FLD_042']=fml_req['FLD_042']
	fml['FLD_049']=fml_req['FLD_049']
	fml['FLD_094']=fml_req['FLD_094']
	if fml_resp.has_key('FLD_095'): fml['FLD_095']=fml_resp['FLD_095']
	return fml




def generate_partial_1420(fml_req,fml_resp,parameters):
	fml={}
	fml['MSG_TYPE']='1420'
#	fml['FLD_004']=fml_req['FLD_004']
	fml['FLD_004']=fml_req['FLD_004']/2
	fml['FLD_002']=fml_req['FLD_002']
	fml['FLD_003']=fml_req['FLD_003']
	fml['FLD_012']=fml_req['FLD_012']
	fml['FLD_014']=fml_req['FLD_014']
#	if fml_resp.has_key('FLD_015'): fml['FLD_015']=fml_resp['FLD_015']
	fml['FLD_022']=fml_req['FLD_022']
	fml['FLD_024']='400'
#	fml['FLD_024']='401'
#	fml['FLD_025']='4000'
#	fml['FLD_025']='4004'
	fml['FLD_025']='1806'
	fml['FLD_028']=fml_req['FLD_028']
	fml['FLD_029']=fml_req['FLD_029']
	fml['FLD_030A']=fml_req['FLD_004']
#	fml['FLD_030B']=fml_req['FLD_004']
	fml['FLD_031']='BATCH GENERATOR'
	fml['FLD_033']=fml_req['FLD_033']
	fml['FLD_035']=params['card:exp:track1:track2'].split(':')[2]
	fml['FLD_037']=fml_req['FLD_037']
	fml['FLD_038']=fml_resp['FLD_038']
	fml['FLD_039']='400'
	fml['FLD_041']=fml_req['FLD_041']
	fml['FLD_042']=fml_req['FLD_042']
	fml['FLD_049']=fml_req['FLD_049']
	fml['FLD_056A']=fml_req['MSG_TYPE']
#	fml['FLD_056A']='1200'
#	fml['FLD_056B']=fml_resp['FLD_011']
	fml['FLD_056C']=fml_req['FLD_012']
#	fml['FLD_056D']=fml_resp['FLD_033']
	fml['FLD_094']=fml_req['FLD_094']
#	if fml_resp.has_key('FLD_095'): fml['FLD_095']=fml_resp['FLD_095']
	return fml




def generate_1220(fml_req,fml_resp,parameters):
	fml={}
	fml['MSG_TYPE']='1220'
	fml['FLD_004']=fml_req['FLD_004']
	fml['FLD_002']=fml_req['FLD_002']
	fml['FLD_003']=fml_req['FLD_003']
	fml['FLD_012']=fml_req['FLD_012']
	fml['FLD_014']=fml_req['FLD_014']
	if fml_resp.has_key('FLD_015'): fml['FLD_015']=fml_resp['FLD_015']
	fml['FLD_022']=fml_req['FLD_022']
	fml['FLD_024']='201'
	fml['FLD_025']='1510'
	fml['FLD_028']=fml_req['FLD_028']
	fml['FLD_029']=fml_req['FLD_029']
	fml['FLD_031']='BATCH GENERATOR'
	fml['FLD_033']=fml_req['FLD_033']
	fml['FLD_035']=params['card:exp:track1:track2'].split(':')[2]
	fml['FLD_037']=fml_req['FLD_037']
	fml['FLD_038']=fml_resp['FLD_038']
	fml['FLD_039']=fml_resp['FLD_039']
	fml['FLD_041']=fml_req['FLD_041']
	fml['FLD_042']=fml_req['FLD_042']
	fml['FLD_049']=fml_req['FLD_049']
	fml['FLD_094']=fml_req['FLD_094']
	if fml_resp.has_key('FLD_095'): fml['FLD_095']=fml_resp['FLD_095']
	return fml




def generate_1520(fmls,parameters):
#	amount_sign=1
	f028=''
	f029=-1
	f074_cred_trn_count=0
	f075_cred_rev_count=0
	f076_deb_trn_count=0
	f077_deb_rev_count=0
	f078_transfer_trn_count=0
	f079_transfer_rev_count=0
	f080_inquiry_trn_count=0
	f082_inquiry_rev_count=0
	f083_payment_trn_count=0
	f084_payment_rev_count=0
	f085_feecol_trn_count=0

	f081_all_auth_count=0

	f086_cred_trn_amount=0
	f087_cred_rev_amount=0
	f088_deb_trn_amount=0
	f089_deb_rev_amount=0

	f090_all_auth_reversals_count=0
	f097_total_net_amount=0

	for i in xrange(len(fmls)):
		if fmls[i].has_key('1100_resp') and fmls[i]['1100_resp'].has_key('FLD_039') and fmls[i]['1100_resp']['FLD_039']=='000' and fmls[i]['1100_resp'].has_key('FLD_003') and fmls[i]['1100_resp'].has_key('FLD_004'):
			if fmls[i]['1100_resp'].has_key('FLD_028') and f028=='': f028=fmls[i]['1100_resp']['FLD_028']
			if fmls[i]['1100_resp'].has_key('FLD_029') and f029==-1: f029=fmls[i]['1100_resp']['FLD_029']
			if fmls[i]['1100_resp']['FLD_003'][0] in ['0','1']:
#				f076_deb_trn_count=f076_deb_trn_count+1
#				f088_deb_trn_amount=f088_deb_trn_amount+fmls[i]['1100_req']['FLD_004']
				amount_sign=1
			if fmls[i]['1100_resp']['FLD_003'][0]=='3':
				f080_inquiry_trn_count=f080_inquiry_trn_count+1
#				f088_deb_trn_amount=f088_deb_trn_amount+fmls[i]['1100_req']['FLD_004']
				amount_sign=1
#			f090_all_auth_reversals_count=f090_all_auth_reversals_count+1
#			f097_total_net_amount=f097_total_net_amount + amount_sign*fmls[i]['1100_req']['FLD_004']
			f081_all_auth_count=f081_all_auth_count+1

		if fmls[i].has_key('1220_resp') and fmls[i]['1220_resp'].has_key('FLD_039') and fmls[i]['1220_resp']['FLD_039']=='000' and fmls[i]['1220_resp'].has_key('FLD_003') and fmls[i]['1220_resp'].has_key('FLD_004'):
			if fmls[i]['1220_resp'].has_key('FLD_028') and f028=='': f028=fmls[i]['1220_resp']['FLD_028']
			if fmls[i]['1220_resp'].has_key('FLD_029') and f029==-1: f029=fmls[i]['1220_resp']['FLD_029']
			if fmls[i]['1220_resp']['FLD_003'][0]=='2':
				f074_cred_trn_count=f074_cred_trn_count+1
				f086_cred_trn_amount=f086_cred_trn_amount+fmls[i]['1220_resp']['FLD_004']
				amount_sign=-1
			if fmls[i]['1220_resp']['FLD_003'][0] in ['0','1']:
				f076_deb_trn_count=f076_deb_trn_count+1
				f088_deb_trn_amount=f088_deb_trn_amount+fmls[i]['1220_resp']['FLD_004']
				amount_sign=1
			if fmls[i]['1220_resp']['FLD_003'][0]=='4':
				f078_transfer_trn_count=f078_transfer_trn_count+1
				f088_deb_trn_amount=f088_deb_trn_amount+fmls[i]['1220_resp']['FLD_004']
				amount_sign=1
			if fmls[i]['1220_resp']['FLD_003'][0]=='5':
				f083_payment_trn_count=f083_payment_trn_count+1
				f088_deb_trn_amount=f088_deb_trn_amount+fmls[i]['1220_resp']['FLD_004']
				amount_sign=1

		if fmls[i].has_key('1200_resp') and fmls[i]['1200_resp'].has_key('FLD_039') and fmls[i]['1200_resp']['FLD_039']=='000' and fmls[i]['1200_resp'].has_key('FLD_003') and fmls[i]['1200_resp'].has_key('FLD_004'):
			if fmls[i]['1200_resp'].has_key('FLD_028') and f028=='': f028=fmls[i]['1200_resp']['FLD_028']
			if fmls[i]['1200_resp'].has_key('FLD_029') and f029==-1: f029=fmls[i]['1200_resp']['FLD_029']
			if fmls[i]['1200_resp']['FLD_003'][0]=='2':
				f074_cred_trn_count=f074_cred_trn_count+1
				f086_cred_trn_amount=f086_cred_trn_amount+fmls[i]['1200_req']['FLD_004']
				amount_sign=-1
			if fmls[i]['1200_resp']['FLD_003'][0] in ['0','1']:
				f076_deb_trn_count=f076_deb_trn_count+1
				f088_deb_trn_amount=f088_deb_trn_amount+fmls[i]['1200_req']['FLD_004']
				amount_sign=1
			if fmls[i]['1200_resp']['FLD_003'][0]=='4':
				f078_transfer_trn_count=f078_transfer_trn_count+1
				f088_deb_trn_amount=f088_deb_trn_amount+fmls[i]['1200_req']['FLD_004']
				amount_sign=1
			if fmls[i]['1200_resp']['FLD_003'][0]=='5':
				f083_payment_trn_count=f083_payment_trn_count+1
				f088_deb_trn_amount=f088_deb_trn_amount+fmls[i]['1200_req']['FLD_004']
				amount_sign=1
#			f090_all_auth_reversals_count=f090_all_auth_reversals_count+1
#			f097_total_net_amount=f097_total_net_amount + amount_sign*fmls[i]['1200_req']['FLD_004']

		if fmls[i].has_key('1420_resp') and fmls[i]['1420_resp'].has_key('FLD_039') and fmls[i]['1420_resp']['FLD_039']=='400' and fmls[i]['1420_resp'].has_key('FLD_003') and fmls[i]['1420_resp'].has_key('FLD_004'):
			if fmls[i]['1420_resp'].has_key('FLD_028') and f028=='': f028=fmls[i]['1420_resp']['FLD_028']
			if fmls[i]['1420_resp'].has_key('FLD_029') and f029==-1: f029=fmls[i]['1420_resp']['FLD_029']
			if fmls[i]['1420_resp']['FLD_003'][0]=='2':
				f075_cred_rev_count=f075_cred_rev_count+1
				f087_cred_rev_amount=f087_cred_rev_amount+fmls[i]['1420_req']['FLD_004']
				amount_sign=1
			if fmls[i]['1420_resp']['FLD_003'][0] in ['0','1']:
				f077_deb_rev_count=f077_deb_rev_count+1
				f089_deb_rev_amount=f089_deb_rev_amount+fmls[i]['1420_req']['FLD_004']
				amount_sign=-1
			if fmls[i]['1420_resp']['FLD_003'][0]=='3':
				f082_inquiry_rev_count=f082_inquiry_rev_count+1
				f089_deb_rev_amount=f089_deb_rev_amount+fmls[i]['1420_req']['FLD_004']
				amount_sign=-1
			if fmls[i]['1420_resp']['FLD_003'][0]=='4':
				f078_transfer_trn_count=f078_transfer_trn_count+1
				f089_deb_rev_amount=f089_deb_rev_amount+fmls[i]['1420_req']['FLD_004']
				amount_sign=-1
			if fmls[i]['1420_resp']['FLD_003'][0]=='5':
				f084_payment_rev_count=f084_payment_rev_count+1
				f089_deb_rev_amount=f089_deb_rev_amount+fmls[i]['1420_req']['FLD_004']
				amount_sign=-1
			f090_all_auth_reversals_count=f090_all_auth_reversals_count+1
#			f097_total_net_amount=f097_total_net_amount + amount_sign*fmls[i]['1420_req']['FLD_004']


	fml = {}
	fml['MSG_TYPE']='1520'
#	fml['FLD_003']='000000'
	fml['FLD_012']=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
#	fml['FLD_022']=fml_1100_out[i]['FLD_022']
	fml['FLD_024']='500'
#	fml['FLD_025']='1510'
	fml['FLD_028']=f028
	fml['FLD_029']=f029
	fml['FLD_031']='BATCH GENERATOR'
	fml['FLD_033']=params['forwarder']
	fml['FLD_037']=datetime.datetime.now().strftime('%Y%m%d')+str(random.randint(1,9999)).rjust(4,'0')
	fml['FLD_041']=params['terminal_id']
	fml['FLD_042']=params['merchant_id']
	fml['FLD_094']=params['forwarder']
	fml['FLD_100']=params['RTPSID']

	fml['FLD_074']=f074_cred_trn_count
	fml['FLD_075']=f075_cred_rev_count
	fml['FLD_076']=f076_deb_trn_count
	fml['FLD_077']=f077_deb_rev_count
	fml['FLD_078']=f078_transfer_trn_count
	fml['FLD_079']=f079_transfer_rev_count
	fml['FLD_080']=f080_inquiry_trn_count
	fml['FLD_082']=f082_inquiry_rev_count
	fml['FLD_083']=f083_payment_trn_count
	fml['FLD_084']=f084_payment_rev_count
	fml['FLD_085']=f085_feecol_trn_count

	fml['FLD_081']=f081_all_auth_count

	fml['FLD_086']=f086_cred_trn_amount
	fml['FLD_087']=f087_cred_rev_amount
	fml['FLD_088']=f088_deb_trn_amount
	fml['FLD_089']=f089_deb_rev_amount

	fml['FLD_090']=f090_all_auth_reversals_count
#	fml['FLD_097']=-1*f097_total_net_amount
	fml['FLD_097']=fml['FLD_086']+fml['FLD_087']-fml['FLD_088']-fml['FLD_089']

	return fml





helpstring='\033[94m'+'Script run format:\n   pytool return_expired_cashbycode.py <DB login string to EBPP> [<TPS value>] [debug]\n Example:\n   pytool return_expired_cashbycode.py rtps_ebpp/rtps_ebpp@rtps 1\n\n'+'\033[0m'

if len(sys.argv)>=2 and sys.argv[1] in ('help','h','-h','--help'):
	print helpstring
	sys.exit(0)


CSHOME= os.environ.get('CSHOME')
if not CSHOME:
    print 'Environment variable CSHOME not set'
    sys.sys.exit(1)
sys.path.insert(0,CSHOME+'/lib/dbobj')
sys.path.insert(0,CSHOME+'/lib')

RTPSLOGPATH=os.environ.get('RTPSLOGPATH')

import dbobj



PrintMessage('STARTED BATCH GENERATOR','HDR')
footerfailed='FINISHED BATCH GENERATOR - FAILED'

try:
	tp = tuxedo.init(0)
	PrintMessage('Connected to tuxedo OK: %s' % tp,'DBG')
except:
        PrintMessage('Failed connecting to tuxedo. RTPS should be booted','ERR')
        PrintMessage(footerfailed,'HDR')
#        sys.exit(1)

fml_messages=[]
#fml_1100_out = []
#fml_1100_resp = []
#fml_1220_out = []
#fml_1220_resp = []
#fml_1520_out = {}
#fml_1520_resp = {}

params={}

params['debug_mode']=True

#Functional test
params['auth_count']=1
params['tps']=1

#Load test
#params['auth_count']=1000
#params['tps']=200


params['refnr_counter']=912

params['reoncile_counter']=26

#params['card:exp:track1:track2']='9000800000002794:1309::'
#params['trn_currency']='978'
#params['point_code']='600010S04100'
#params['RTPSID']='EDUSRV'

#On Us
params['card:exp:track1:track2']='4XXXXX0016948846:1412::'
params['trn_currency']='974'
params['merchant_id']='8000110'
params['terminal_id']='IPOS0003'
params['point_code']='200100054140'
params['forwarder']='1120051'
params['RTPSID']='112010'


#AFD to MC
#params['card:exp:track1:track2']='5999990000000001:1412:5999990000000001=00014122011839000950000:'
#params['trn_currency']='974'
#params['merchant_id']='8000150'
#params['terminal_id']='IPOS0050'
#params['point_code']='200100954140'
#params['forwarder']='1120051'
#params['RTPSID']='112010'


#Karlis Venters
#params['card:exp:track1:track2']='4166764000085285:1506::'
#params['trn_currency']='974'
#params['merchant_id']='8000110'
#params['terminal_id']='IPOS0003'
#params['point_code']='200100054140'
#params['forwarder']='1120051'
#params['RTPSID']='112010'

#To VISA_DMS
#params['card:exp:track1:track2']='4010000000000001:1412::'
#params['trn_currency']='974'
#params['merchant_id']='8000110'
#params['terminal_id']='IPOS0003'
#params['point_code']='200100054140'
#params['forwarder']='1120051'
#params['RTPSID']='112010'



#debug_mode=True
#auth_count=2
#tps=1

refnr_counter=0


user_confirm=raw_input('Do you wish to perform Authorisations (MTI=1100) ? (y,n): ')
if user_confirm<>'n': user_confirm='y'
############################
#           1100
############################
if user_confirm=='y':
	PrintMessage('### Start Processing Authorizations (MTI=1100)','DBG')
	for i in xrange(params['auth_count']):
		auth_id=i+1
		PrintMessage('Start processing Authorization(1100) N %s' % (auth_id),'DBG')
		fml = generate_1100({'refnr_counter' : refnr_counter, 'auth_id' : auth_id})
		refnr_counter=refnr_counter+1
		#print fml
		try:
			resp = tp.call("ROUTING_SWITCH",fml,tuxedo.TPNOTRAN)
	        except:
        	        PrintMessage('Failed to call service ROUTING_SWITCH during Authorization(1100) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s"' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']),'ERR')
#               	 continue
		if resp:
			respc39=eval(str(resp))['FLD_039']
#			PrintMessage('!!! RETURNED FML: %s' % resp,'HDR')

			if respc39=='000':
				fml_messages.append({'1100_req' : fml, '1100_resp' : resp})
				PrintMessage('Authorization(1100) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" processed successfully' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']),'MSG')
			else:
				PrintMessage('Authorization(1100) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" declined, FLD_039="%s"' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004'],respc39),'ERR')
		else:
       		        PrintMessage('Authorization(1100) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" processed with undefined error' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']), 'ERR')

		PrintMessage('...TPS=%s, waiting for %s seconds...' % (params['tps'],1/params['tps']),'DBG')
		time.sleep(1/params['tps'])

	PrintMessage('### Finished Processing Authorizations (MTI=1100)','DBG')







user_confirm=raw_input('Do you wish to perform Reversals (MTI=1420) on Authorisations (MTI=1100) ? (y,n): ')
if user_confirm<>'n': user_confirm='y'
############################
#           1420 on 1100
############################
if user_confirm=='y':
	PrintMessage('### Start Processing Reversals (MTI=1420) on Authorisations (MTI=1100)','DBG')
	for i in xrange(len(fml_messages)):
		auth_id=i+1
		if fml_messages[i]['1100_resp'].has_key('FLD_039') and fml_messages[i]['1100_resp']['FLD_039']=='000':
			PrintMessage('Start processing Advice(1420) N %s' % (auth_id),'DBG')
			fml = generate_partial_1420(fml_messages[i]['1100_req'],fml_messages[i]['1100_resp'],{})
			#print fml
			try:
				resp = tp.call("ROUTING_SWITCH",fml,tuxedo.TPNOTRAN)
		        except:
        		        PrintMessage('Failed to call service ROUTING_SWITCH during Reversal(1420) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s"' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']),'ERR')
#                		continue
			if resp:
				respc39=eval(str(resp))['FLD_039']
#				PrintMessage('!!! RETURNED FML: %s' % resp,'HDR')
				
				if respc39=='400':
					fml_messages[i]['1420_req']=fml
					fml_messages[i]['1420_resp']=resp
					PrintMessage('Reversal(1420) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" processed successfully' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']),'MSG')
				else:
					PrintMessage('Reversal(1420) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" declined, FLD_039="%s"' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004'],respc39),'ERR')
			else:
       		        	PrintMessage('Reversal(1420) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" processed with undefined error' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']), 'ERR')

			PrintMessage('...TPS=%s, waiting for %s seconds...' % (params['tps'],1/params['tps']),'DBG')
			time.sleep(1/params['tps'])
		else:
			PrintMessage('!!! Skipped processing Reversal(1420) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" in cae of original Authorization declined with FLD_039="%s"' % (auth_id,fml_messages[i]['1100_resp']['FLD_012'],fml_messages[i]['1100_resp']['FLD_037'],fml['FLD_004'],fml_messages[i]['1100_resp']['FLD_039']),'DBG')

	PrintMessage('### Finished Processing Reversals (MTI=1420)','DBG')






user_confirm=raw_input('Do you wish to perform Transactions (MTI=1120)? (y,n): ')
if user_confirm<>'n': user_confirm='y'
############################
#           1120
############################
if user_confirm=='y':
	PrintMessage('### Start Processing Advices (MTI=1120)','DBG')
	for i in xrange(len(fml_messages)):
		auth_id=i+1
		if fml_messages[i]['1100_resp'].has_key('FLD_039') and fml_messages[i]['1100_resp']['FLD_039']=='000':
			PrintMessage('Start processing Advice(1120) N %s' % (auth_id),'DBG')
			fml = generate_1120(fml_messages[i]['1100_req'],fml_messages[i]['1100_resp'],{})
			#print fml
			try:
				resp = tp.call("ROUTING_SWITCH",fml,tuxedo.TPNOTRAN)
		        except:
        		        PrintMessage('Failed to call service ROUTING_SWITCH during Advice(1120) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s"' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']),'ERR')
#                		continue
			if resp:
				respc39=eval(str(resp))['FLD_039']
#				PrintMessage('!!! RETURNED FML: %s' % resp,'HDR')
				
				if respc39=='000':
					fml_messages[i]['1120_req']=fml
					fml_messages[i]['1120_resp']=resp
					PrintMessage('Advice(1120) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" processed successfully' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']),'MSG')
				else:
					PrintMessage('Advice(1120) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" declined, FLD_039="%s"' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004'],respc39),'ERR')
			else:
       		        	PrintMessage('Advice(1120) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" processed with undefined error' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']), 'ERR')

			PrintMessage('...TPS=%s, waiting for %s seconds...' % (params['tps'],1/params['tps']),'DBG')
			time.sleep(1/params['tps'])
		else:
			PrintMessage('!!! Skipped processing Advice(1120) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" in cae of original Authorization declined with FLD_039="%s"' % (auth_id,fml_messages[i]['1100_resp']['FLD_012'],fml_messages[i]['1100_resp']['FLD_037'],fml['FLD_004'],fml_messages[i]['1100_resp']['FLD_039']),'DBG')

	PrintMessage('### Finished Processing Advices (MTI=1120)','DBG')






user_confirm=raw_input('Do you wish to perform Transactions (MTI=1220)? (y,n): ')
if user_confirm<>'n': user_confirm='y'
############################
#           1220
############################
if user_confirm=='y':
	PrintMessage('### Start Processing Transactions (MTI=1220)','DBG')
	for i in xrange(len(fml_messages)):
		auth_id=i+1
		if fml_messages[i]['1100_resp'].has_key('FLD_039') and fml_messages[i]['1100_resp']['FLD_039']=='000':
			PrintMessage('Start processing Transaction(1220) N %s' % (auth_id),'DBG')
			fml = generate_1220(fml_messages[i]['1100_req'],fml_messages[i]['1100_resp'],{})
			#print fml
			try:
				resp = tp.call("ROUTING_SWITCH",fml,tuxedo.TPNOTRAN)
		        except:
        		        PrintMessage('Failed to call service ROUTING_SWITCH during Transaction(1220) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s"' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']),'ERR')
#                		continue
			if resp:
				respc39=eval(str(resp))['FLD_039']
#				PrintMessage('!!! RETURNED FML: %s' % resp,'HDR')
				
				if respc39=='000':
					fml_messages[i]['1220_req']=fml
					fml_messages[i]['1220_resp']=resp
					PrintMessage('Transaction(1220) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" processed successfully' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']),'MSG')
				else:
					PrintMessage('Transaction(1220) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" declined, FLD_039="%s"' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004'],respc39),'ERR')
			else:
       		        	PrintMessage('Transaction(1220) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" processed with undefined error' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']), 'ERR')

			PrintMessage('...TPS=%s, waiting for %s seconds...' % (params['tps'],1/params['tps']),'DBG')
			time.sleep(1/params['tps'])
		else:
			PrintMessage('!!! Skipped processing Transaction(1220) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" in cae of original Authorization declined with FLD_039="%s"' % (auth_id,fml_messages[i]['1100_resp']['FLD_012'],fml_messages[i]['1100_resp']['FLD_037'],fml['FLD_004'],fml_messages[i]['1100_resp']['FLD_039']),'DBG')

	PrintMessage('### Finished Processing Transactions (MTI=1220)','DBG')






user_confirm=raw_input('Do you wish to perform Transactions (MTI=1200)? (y,n): ')
if user_confirm<>'n': user_confirm='y'
############################
#           1200
############################
if user_confirm=='y':
	PrintMessage('### Start Processing Transactions (MTI=1200)','DBG')
	for i in xrange(params['auth_count']):
		auth_id=i+1
		PrintMessage('Start processing Transaction(1200) N %s' % (auth_id),'DBG')
		fml = generate_1200({'refnr_counter' : refnr_counter})
		refnr_counter=refnr_counter+1
		try:
			resp = tp.call("ROUTING_SWITCH",fml,tuxedo.TPNOTRAN)
	        except:
        	        PrintMessage('Failed to call service ROUTING_SWITCH during Transaction(1200) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s"' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']),'ERR')
		if resp:
			respc39=eval(str(resp))['FLD_039']

			if respc39=='000':
				fml_messages.append({'1200_req' : fml, '1200_resp' : resp})
				PrintMessage('Transaction(1200) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" processed successfully' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']),'MSG')
			else:
				PrintMessage('Transaction(1200) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" declined, FLD_039="%s"' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004'],respc39),'ERR')
		else:
       		        PrintMessage('Transaction(1200) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" processed with undefined error' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']), 'ERR')

		PrintMessage('...TPS=%s, waiting for %s seconds...' % (params['tps'],1/params['tps']),'DBG')
		time.sleep(1/params['tps'])

	PrintMessage('### Finished Processing Transactions (MTI=1200)','DBG')






user_confirm=raw_input('Do you wish to perform Reversals (MTI=1420) on Transactions (MTI=1200) ? (y,n): ')
if user_confirm<>'n': user_confirm='y'
############################
#           1420 on 1200
############################
if user_confirm=='y':
	PrintMessage('### Start Processing Reversals (MTI=1420) on Transactions (MTI=1200)','DBG')
	for i in xrange(len(fml_messages)):
		if  fml_messages[i].has_key('1200_resp'):
			auth_id=i+1
			if fml_messages[i]['1200_resp'].has_key('FLD_039') and fml_messages[i]['1200_resp']['FLD_039']=='000':
				PrintMessage('Start processing Advice(1420) N %s' % (auth_id),'DBG')
				fml = generate_partial_1420(fml_messages[i]['1200_req'],fml_messages[i]['1200_resp'],{})
				#print fml
				try:
					resp = tp.call("ROUTING_SWITCH",fml,tuxedo.TPNOTRAN)
		        	except:
        		        	PrintMessage('Failed to call service ROUTING_SWITCH during Reversal(1420) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s"' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']),'ERR')
#	                		continue
				if resp:
					respc39=eval(str(resp))['FLD_039']
#					PrintMessage('!!! RETURNED FML: %s' % resp,'HDR')
				
					if respc39=='400':
						fml_messages[i]['1420_1200_req']=fml
						fml_messages[i]['1420_1200_resp']=resp
						PrintMessage('Reversal(1420) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" processed successfully' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']),'MSG')
					else:
						PrintMessage('Reversal(1420) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" declined, FLD_039="%s"' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004'],respc39),'ERR')
				else:
       			        	PrintMessage('Reversal(1420) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" processed with undefined error' % (auth_id,fml['FLD_012'],fml['FLD_037'],fml['FLD_004']), 'ERR')

				PrintMessage('...TPS=%s, waiting for %s seconds...' % (params['tps'],1/params['tps']),'DBG')
				time.sleep(1/params['tps'])
			else:
				PrintMessage('!!! Skipped processing Reversal(1420) N %s, FLD_012="%s", FLD_037="%s", FLD_004="%s" in cae of original Authorization declined with FLD_039="%s"' % (auth_id,fml_messages[i]['1100_resp']['FLD_012'],fml_messages[i]['1100_resp']['FLD_037'],fml['FLD_004'],fml_messages[i]['1100_resp']['FLD_039']),'DBG')

	PrintMessage('### Finished Processing Reversals (MTI=1420)','DBG')







user_confirm=raw_input('Do you wish to Close the Day (MTI=1520)? (y,n): ')
if user_confirm<>'n': user_confirm='y'
############################
#           1520
############################
if user_confirm=='y':

	PrintMessage('### Start Processing Close the Day (MTI=1520)','DBG')
	fml=generate_1520(fml_messages,{})

	#print fml
	try:
		resp = tp.call("ROUTING_SWITCH",fml,tuxedo.TPNOTRAN)
        except:
		PrintMessage('Failed to call service ROUTING_SWITCH during Close the Day (1520), FLD_012="%s", FLD_037="%s"' % (fml['FLD_012'],fml['FLD_037']),'ERR')
#               		continue
	if resp:
		respc39=eval(str(resp))['FLD_039']
#		PrintMessage('!!! RETURNED FML: %s' % resp,'HDR')
		
		if respc39=='500':
			fml_messages.append({'1520_req' : fml, '1520_resp' : resp})
			PrintMessage('Close the Day (1520), FLD_012="%s", FLD_037="%s" processed successfully' % (fml['FLD_012'],fml['FLD_037']),'MSG')
		else:
			PrintMessage('Close the Day (1520), FLD_012="%s", FLD_037="%s" declined, FLD_039="%s"' % (fml['FLD_012'],fml['FLD_037'],respc39),'ERR')
	else:
		PrintMessage('Close the Day (1520), FLD_012="%s", FLD_037="%s" processed with undefined error' % (fml['FLD_012'],fml['FLD_037']), 'ERR')


	PrintMessage('### Finished Processing Close the Day (MTI=1520)','DBG')





PrintMessage('FINISHED BATCH GENERATOR - OK','HDR')

