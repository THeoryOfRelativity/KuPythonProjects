import sys
import re
import math
import datetime

def timestr_to_seconds(timestr):
	h=int(timestr.split(':')[0])
        m=int(timestr.split(':')[1])
        s=float(timestr.split(':')[2])
	ss=h*60*60+m*60+s
	return ss




test_enable_flag=True


f=open('20130628_vpsc.log','r')

start_flag=False
break_flag=True

vpsc=[]

s=f.readline()

while s<>'':
	s=s.replace('\n','')
	if not start_flag and 'Service Name' in s:
		if s[0]=='>': s=s.replace('>','')
		vpsc.append({})
		start_flag=True
	if start_flag and len(s)>0 and s[0]=='>':
		start_flag=False
		if vpsc[-1]=={}: del vpsc[-1]
		break
	if start_flag:
		if s=='':
			vpsc.append({})
			break_flag=True
		else:
			break_flag=False
			if 'Process ID:' in s:
				vpsc[-1]['Process ID']=s.split(':')[1].split(',')[0].strip()
				vpsc[-1]['Machine ID']=s.split(':')[2].strip()
			else:
	                        if 'Group ID:' in s:
        	                        vpsc[-1]['Group ID']=s.split(':')[1].split(',')[0].strip()
                	                vpsc[-1]['Server ID']=s.split(':')[2].strip()
				else:
		                        if 'Prog Name:' in s:
        		                        vpsc[-1]['Prog Name']=s.split(':')[1].strip()
                		                vpsc[-1]['Server Name']=s.split(':')[1].strip().split('/')[-1]
					else:
						s1=s.split(':')[0].strip()
						s2=s.split(':')[1].strip()
	                                        vpsc[-1][s1]=s2

	s=f.readline()

f.close()






def get_servers_count(server_name):
	servers_count=0
	server_ids=[]
	for row_ind in xrange(len(vpsc)):
#		print 'UUU: '+vpsc[row_ind]['Service Name']
#                print service_name
		if vpsc[row_ind]['Server Name']==server_name and not vpsc[row_ind]['Server ID'] in server_ids:
			servers_count=servers_count+1
			server_ids.append(str(vpsc[row_ind]['Server ID']))
#                        print 'XXX: '+str(servers_count)
	return servers_count







tags=[

#['pos_conctr',[
#  ['RECEIVE',['|000200|\t\t{ ReceiveEtxStxCrc16Message'],['|000201|\t\t\t  Recieved ']]
#  ]
#],

#['posc',[
#  ['SESSION',['|000071|\t Possible new connection receieved. Let'],['|000079|\t Closing connection']]
#  ]
#],

#['posc_th',[
#  ['THREAD',['|000071|...\t Possible new connection receieved. Let'],['|000079|...\t Closing connection']]
#  ]
#],

#['posc_all',[
#  ['SESSION',['|000071|\t Possible new connection receieved. Let','|000071|...\t Possible new connection receieved. Let'],['|000079|\t Closing connection','|000079|...\t Closing connection']]
#  ]
#],



['pos_conctr',[
#  ['POS_CONCENTRATOR',['000055|\t{ ReceiveMessageFromPos(','000055|...\t{ ReceiveMessageFromPos(','000055|{ ReceiveMessageFromPos('],['000062|\t} ReceiveMessageFromPos()','000062|...\t} ReceiveMessageFromPos()','000062|} ReceiveMessageFromPos()']]
#  ['POS_CONCENTRATOR',['000055|\t{ ReceiveMessageFromPos(','000055|...\t{ ReceiveMessageFromPos(','000055|{ ReceiveMessageFromPos('],['000070|...\t Waiting condition','000070|\t Waiting condition','000070| Waiting condition']]

  ['POS_CONCENTRATOR',['|000071|'],['|000070|']],
#  ['POS_IN',['|000071|'],['|000212|']]
  ['POS_IN',['|000218|\t\t\t{ Accept('],['|000221|\t\t\t} Accept()']],
  ]
],



['POS_ISO_SRV',[
  ['POS_ISO_IN',['Service POS_ISO_IN started'],['Service  POS_ISO_IN End   TimeStat']],
  ['POS_ISO_OUT',['Service POS_ISO_OUT started'],['Service  POS_ISO_OUT End   TimeStat']],
  ['POS_ISO_FAULT',['Service  POS_ISO_FAULT START'],['Service  POS_ISO_FAULT End   TimeStat']],
  ['POS_ISO_NET',['?????????????????'],['?????????????????']]
  ]
],



['HYPERCOM_SRV',[
  ['HYPERCOM_IN',['Service HYPERCOM_IN started'],['| Service  HYPERCOM_IN End   Type=[RELATIVE] UTime=']],
  ['HYPERCOM_OUT',['Service HYPERCOM_OUT started'],['| Service  HYPERCOM_OUT End   Type=[RELATIVE] UTime=']],
  ['HYPERCOM_FAULT',['Service  HYPERCOM_FAULT START'],['| Service  HYPERCOM_FAULT End   Type=[RELATIVE] UTime=']],
  ['HYPERCOM_NET',['?????????????????'],['?????????????????']]
  ]
],


['SYMBOLS_SRV',[
  ['SYMBOLS_IN',['Service BOG_SYNC_IN started'],['Service  BOG_SYNC_IN End   Type=[RELATIVE] UTime=']],
  ['SYMBOLS_OUT',['Service BOG_SYNC_OUT started'],['Service  BOG_SYNC_OUT End   Type=[RELATIVE] UTime=']],
  ['SYMBOLS_FAULT',['Service BOG_SYNC_FAULT started'],['Service  BOG_SYNC_FAULT End   Type=[RELATIVE] UTime=']],
  ['SYMBOLS_NET',['Service BOG_SYNC_NET started'],['Service  BOG_SYNC_NET End   Type=[RELATIVE] UTime=']]
  ]
],


['HYPERCOM_RS',[
  ['HYPERCOM',[' HYPERCOM_IN STARTED'],[' HYPERCOM_OUT FINISHED']]
  ]
],

['HPT_RS',[
  ['HPT',[' HPT_REQ STARTED'],[' HPT_REQ FINISHED',' HPT_RESP FINISHED']]
  ]
],



['CRYPTO',[
  ['MESSAGCR_ARQC_MCHPES_ACQ',['#-> CR_ARQC_MCHP begin'],['<-# CR_ARQC_MCHP ']],
  ['CR_ARQC_VSDC',['#-> CR_ARQC_VSDC begin'],['<-# CR_ARQC_VSDC ']],
  ['CR_SECMES_MCHP',['#-> CR_SECMES_MCHP begin'],['<-# CR_SECMES_MCHP ']],
  ['CR_SECMES_VSDC',['#-> CR_SECMES_VSDC begin'],['<-# CR_SECMES_VSDC ']],
  ['CRYPTO_CVC',['|CRYPTO_CVC begin'],['|CRYPTO_CVC end']],
  ['CRYPTO_PIN',['|CRYPTO_PIN begin'],['|CRYPTO_PIN end']],
  ['CRYPTO_PINCH',['|CRYPTO_PINCH begin'],['|CRYPTO_PINCH end']],
  ['CRYPTO_ZPK',['|CRYPTO_ZPK begin'],['|CRYPTO_ZPK end']]
  ]
],



['IIA_CRYPTO_CVV',[
  ['IIA_CRYPTO_CVV',['####====---->>>> [ IIA_CRYPTO_CVV started ] <<<<----====####'],['<<<<----====#### [ IIA_CRYPTO_CVV finished']]
  ]
],


['MESSAGES',[
  ['MESSAGES_ACQ',[' MESSAGES_ACQ '],[' TIME']],
  ['MESSAGES_BATCH',[' MESSAGES_BATCH '],[' TIME']],
  ['MESSAGES_STORE',[' MESSAGES_STORE '],[' TIME']],
  ['MESSAGES_AGR',[' MESSAGES_AGR '],[' TIME']],
  ['MESSAGES_REV',[' MESSAGES_REV '],[' TIME']],
  ['MESSAGES_DECL',[' MESSAGES_DECL '],[' TIME']]
  ]
],

['MESSAGESN',[
  ['MESSAGESN',['begin_trans'],['end_trans']]
  ]
],

['RSW_MESSAGES',[
  ['MESSAGES_ACQ',['| call_service(MESSAGES_ACQ)'],['| Lattency of service MESSAGES_ACQ']],
  ['MESSAGES_BATCH',['| call_service(MESSAGES_BATCH)'],['| Lattency of service MESSAGES_BATCH']],
  ['MESSAGES_STORE',['| call_service(MESSAGES_STORE)'],['| Lattency of service MESSAGES_STORE']],
  ['MESSAGES_AGR',['| call_service(MESSAGES_AGR)'],['| Lattency of service MESSAGES_AGR']],
  ['MESSAGES_REV',['| call_service(MESSAGES_REV)'],['| Lattency of service MESSAGES_REV']],
  ['MESSAGES_DECL',['| call_service(MESSAGES_DECL)'],['| Lattency of service MESSAGES_DECL']]
  ]
],

['MESSAGES_DB',[
  ['MESSAGES_DB',
    ['TRANSACTION_MATCHING started',
     'RECONCILATION started',
     'ACQ_AUTH started',
     'ACQ_AGREEMENTS started',
     'ACQ_AUTH started',
     'GEN_BATCH_ID started',
     'TRANSACTION started',
     'DECLINED started',
     'AUTHORISATION started',
     'REVERSAL started'
    ],
    ['TRANSACTION_MATCHING finished',
     'RECONCILATION finished',
     'ACQ_AUTH finished',
     'ACQ_AGREEMENTS finished',
     'ACQ_AUTH finished',
     'GEN_BATCH_ID finished',
     'TRANSACTION finished',
     'DECLINED finished',
     'AUTHORISATION finished',
     'REVERSAL finished'
    ]
  ]
]],

['RSW_MESSAGESN',[
  ['MESSAGESN_STORE',['| call_service(MESSAGESN_STORE)'],['| Lattency of service MESSAGESN_STORE']],
  ['MESSAGESN_SREV',['| call_service(MESSAGESN_SREV)'],['| Lattency of service MESSAGESN_SREV']],
  ['MESSAGESN_CREV',['| call_service(MESSAGESN_CREV)'],['| Lattency of service MESSAGESN_CREV']],
  ['MESSAGESN_SREP',['| call_service(MESSAGESN_SREP)'],['| Lattency of service MESSAGESN_SREP']],
  ['MESSAGESN_SFML',['| call_service(MESSAGESN_SFML)'],['| Lattency of service MESSAGESN_SFML']],
  ['MESSAGESN_GMSG',['| call_service(MESSAGESN_GMSG)'],['| Lattency of service MESSAGESN_GMSG']],
  ['MESSAGESN_GFML',['| call_service(MESSAGESN_GFML)'],['| Lattency of service MESSAGESN_GFML']],
  ['MESSAGESN_CREP',['| call_service(MESSAGESN_CREP)'],['| Lattency of service MESSAGESN_CREP']]
  ]
],

#['ASY_SWITCH',[
#  ['SWITCH_REQ',
#    ['| ROUTING_SWITCH() '
#    ],
#    ['| routing_switch_req()',
#     '| SWITCH_REQ end'
#    ]
#  ],
#  ['SWITCH_RESP',
#    ['| routing_switch_resp()'
#    ],
#    ['| TIME_STAT |',
#     '| PATH|'
#    ]
#  ]
#]],

['SWITCH_REQ',[
  ['SWITCH_REQ',
    ['| ROUTING_SWITCH() '
    ],
    ['| routing_switch_req()',
     '| SWITCH_REQ end'
    ]
  ]
]],

['SWITCH_RESP',[
  ['SWITCH_RESP',
    ['| routing_switch_resp()'
    ],
    ['| TIME_STAT |',
     '| PATH|'
    ]
  ]
]],

['ACNT_PRMRY_LCK',[
  ['ACNT_PRMRY_LCK',
    ['|->=>->=>->=>->=>->=>->=>->=>->=>[ Start of ACNT_PRMRY_LCK service ]->=>->=>->=>->=>->=>->=>->=>->=>->=>'
    ],
    ['|<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-[ End of ACNT_PRMRY_LCK service '
    ]
  ],
  ['ACNT_PRMRY_LCK2',
    ['|->=>->=>->=>->=>->=>->=>->=>->=>[ Start of ACNT_PRMRY_LCK2 service ]->=>->=>->=>->=>->=>->=>->=>->=>->=>'
    ],
    ['|<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-[ End of ACNT_PRMRY_LCK2 service '
    ]
  ]
]],

['ACNT_PRMRY_LCK_FEE_SVC_TYPE',[
  ['FEE_SVC_TYPE',
    ['#-> CallFeeService()'
    ],
    ['<-# CallFeeService()'
    ]
  ]
]],

['ACNT_PRMRY_MLT',[
  ['ACNT_PRMRY_MLT',
    ['ACNT_PRMRY_MLT','|->=>->=>->=>->=>->=>->=>->=>->=>[ Start of ACNT_PRMRY_MLT service ]->=>->=>->=>->=>->=>->=>->=>->=>->=>'
    ],
    ['|<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-[ End of ACNT_PRMRY_MLT service '
    ]
  ],
  ['ACNT_PRMRY_MLT2',
    ['|->=>->=>->=>->=>->=>->=>->=>->=>[ Start of ACNT_PRMRY_MLT2 service ]->=>->=>->=>->=>->=>->=>->=>->=>->=>'
    ],
    ['|<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-[ End of ACNT_PRMRY_MLT2 service '
    ]
  ]
]],

['ACNT_PRMRY_OFL',[
  ['ACNT_PRMRY_OFL',
    ['|->=>->=>->=>->=>->=>->=>->=>->=>[ Start of ACNT_PRMRY_OFL service ]->=>->=>->=>->=>->=>->=>->=>->=>->=>'
    ],
    ['|<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-[ End of ACNT_PRMRY_OFL service '
    ]
  ],
  ['ACNT_PRMRY_OFL2',
    ['|->=>->=>->=>->=>->=>->=>->=>->=>[ Start of ACNT_PRMRY_OFL2 service ]->=>->=>->=>->=>->=>->=>->=>->=>->=>'
    ],
    ['|<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-[ End of ACNT_PRMRY_OFL2 service '
    ]
  ]
]],

['ACNT_PRMRY_FLX',[
  ['ACNT_PRMRY_FLX',
    ['|->=>->=>->=>->=>->=>->=>->=>->=>[ Start of ACNT_PRMRY_FLX service ]->=>->=>->=>->=>->=>->=>->=>->=>->=>'
    ],
    ['|<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-[ End of ACNT_PRMRY_FLX service '
    ]
  ],
  ['ACNT_PRMRY_FLX2',
    ['|->=>->=>->=>->=>->=>->=>->=>->=>[ Start of ACNT_PRMRY_FLX2 service ]->=>->=>->=>->=>->=>->=>->=>->=>->=>'
    ],
    ['|<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-[ End of ACNT_PRMRY_FLX2 service '
    ]
  ]
]],

['ACNT_BLOCK_LCK',[
  ['ACNT_BLOCK_LCK',
    ['|->=>->=>->=>->=>->=>->=>->=>->=>[ Start of ACNT_BLOCK_LCK service ]->=>->=>->=>->=>->=>->=>->=>->=>->=>'
    ],
    ['|<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-[ End of ACNT_BLOCK_LCK '
    ]
  ]
]],

['ACNT_BLOCK_MLT',[
  ['ACNT_BLOCK_MLT',
    ['|->=>->=>->=>->=>->=>->=>->=>->=>[ Start of ACNT_BLOCK_MLT service ]->=>->=>->=>->=>->=>->=>->=>->=>->=>'
    ],
    ['|<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-[ End of ACNT_BLOCK_MLT '
    ]
  ]
]],

['STIP',[
  ['STIP_SUBSTIT',
    ['|->=>->=>->=>->=>->=>-[Start of STIP_SUBSTIT'
    ],
    ['|-<=<-<=<-<=<-<=<-<=<-[End of STIP_SUBSTIT'
    ]
  ]
]],

['STIP_ACCOUNT_SELECTION_SERVICE',[
  ['ACCOUNT_SELECTION_SERVICE',
    ['#-> CallAccountService()'
    ],
    ['<-# CallAccountService()'
    ]
  ]
]],

['STIP_ACCOUNT_BLOCKING_SERVICE',[
  ['ACCOUNT_BLOCKING_SERVICE',
    ['#-> CallBlockAmounttService('
    ],
    ['<-# CallBlockService()'
    ]
  ]
]],

['STIP_PARAMS',[
  ['STIP_PARAMS',
    ['|->=>->=>->=>->=>->=>->=>->=>->=>[ Start of STIP_PARAMS'
    ],
    ['|<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-[ End of STIP_PARAMS'
    ]
  ],
  ['STIP_ENLARGE',
    ['|->=>->=>->=>->=>->=>->=>->=>->=>[ Start of STIP_ENLARGE'
    ],
    ['|<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-<=<-[ End of STIP_ENLARGE'
    ]
  ]
]],

['STIP_CRD_ACTVT',[
  ['STIP_CRD_ACTVT',
    ['|->=>->=>->=>->=>->=>-[Start of STIP_CRD_ACTVT'
    ],
    ['|-<=<-<=<-<=<-<=<-<=<-[End of STIP_CRD_ACTVT '
    ]
  ],
  ['STIP_ACTVT_RULE',
    ['|->=>->=>->=>->=>->=>-[Start of STIP_ACTVT_RULE'
    ],
    ['|-<=<-<=<-<=<-<=<-<=<-[End of STIP_ACTVT_RULE'
    ]
  ],
  ['STIP_CRD_ACT',
    ['|->=>->=>->=>->=>->=>-[Start of STIP_CRD_ACT '
    ],
    ['|-<=<-<=<-<=<-<=<-<=<-[End of STIP_CRD_ACT '
    ]
  ]
]],

['IFSVR',[
  ['CURRENCY_CODE',
    ['| CURRENCY_CODE version 2: Begin'
    ],
    ['| CURRENCY_CODE version 2: End'
    ]
  ],
  ['COUNTRY_CODE',
    ['| COUNTRY_CODE: Begin'
    ],
    ['| COUNTRY_CODE: End'
    ]
  ],
  ['STORE_STR',
    ['| Begin STORE_STR'
    ],
    ['| End STORE_STR'
    ]
  ],
  ['RTPS_SVC',
    ['| #-> RTPS_SVC()'
    ],
    ['| <-# RTPS_SVC() '
    ]
  ],
  ['RTPS_SET_ACTION',
    ['#-> RTPS_SET_ACTION()'
    ],
    ['<-# RTPS_SET_ACTION() '
    ]
  ],
  ['RTPS_RSW_STOP',
    ['| #-> RTPS_RSW_STOP()'
    ],
    ['| <-# RTPS_RSW_STOP() '
    ]
  ],
  ['GET_MESSAGE_ID',
    ['| GET_MESSAGE_ID: Begin'
    ],
    ['| GET_MESSAGE_ID: End'
    ]
  ],
  ['GET_G3_LINKS',
    ['| GET_G3_LINKS: Begin'
    ],
    ['| GET_G3_LINKS: End'
    ]
  ],
  ['GET_CONV_RATE',
    ['| GET_CONV_RATE: Begin'
    ],
    ['| GET_CONV_RATE: End'
    ]
  ],
  ['GENIF_GET_ID',
    ['???????????????'
    ],
    ['???????????????'
    ]
  ],
  ['CHG_G3_LINKS',
    ['???????????????'
    ],
    ['???????????????'
    ]
  ],
  ['ANSWER_CODE',
    ['ANSWER_CODE: Begin'
    ],
    ['ANSWER_CODE: End'
    ]
  ],
]]

]



proc={}
proc_start={}
proc_stop={}
svc_proc={}
svc_proc_start={}
svc_proc_stop={}

log='MESSAGES'
server_ind=0
if len(sys.argv)>=3: log=sys.argv[2]
for i in xrange(len(tags)):
	if log==tags[i][0]: server_ind=i


alert_count=0
if len(sys.argv)>=4: alert_count=int(sys.argv[3])

proc_total=0
#proc_total=get_servers_count(tags[server_ind][0])
#print '111: '+str(proc_total)
#print '122: '+str(len(sys.argv))
#proc_total=len(tags[server_ind][1])
if len(sys.argv)>=5: proc_total=int(sys.argv[4])
if proc_total>0: proc_total_str=str(proc_total).rjust(2,' ')
else: proc_total_str=' ?'
#print '222: '+str(proc_total)
#sys.exit(1)

tpsin_list=[]
tpsin_avg_dict={}
tpsin_max=0.0
tpsin_avg=0.0
tpsin=0
tpsin_str=''
tpsin_max_str=''
tpsin_avg_str=''
occ_tpsin_seconds_prev=0
occ_tpsin_seconds_curr=0
tpsin_max_time=0
svc_in_count={}

svc_tpsin_list={}
svc_tpsin_avg_dict={}
svc_tpsin_max={}
#svc_tpsin_avg={}
svc_tpsin_avg=0.0
svc_tpsin={}
svc_tpsin_str=''
svc_tpsin_max_str=''
svc_tpsin_avg_str=''
svc_tpsin_max_time={}
svc_occ_tpsin_seconds_prev={}
svc_occ_tpsin_seconds_curr={}
svc_proc_total=0
svc_occ_max={}
#svc_occ_avg={}
svc_occ_avg=0.0
svc_occ_avg_dict={}

tpsout_list=[]
tpsout_avg_dict={}
tpsout_max=0.0
tpsout_avg=0.0
tpsout=0
tpsout_str=''
tpsout_max_str=''
tpsout_avg_str=''
occ_tpsout_seconds_prev=0
occ_tpsout_seconds_curr=0

svc_tpsout_list={}
svc_tpsout_avg_dict={}
svc_tpsout_max={}
#svc_tpsout_avg={}
svc_tpsout_avg=0.0
svc_tpsout={}
svc_tpsout_str=''
svc_tpsout_max_str=''
svc_tpsout_avg_str=''
svc_tpsout_max_time={}
svc_time_total={}
svc_time_avg={}
svc_time_max={}
svc_count_total={}
svc_occ_tpsout_seconds_prev={}
svc_occ_tpsout_seconds_curr={}


time_total=0.0
time_avg=0.0
time_max=0.0
count_total=0
occ_avg_dict={}
#occ=0
occ_max=0
occ_avg=0

time_avg_str=''
time_max_str=''
occ_max_str=''
occ_avg_str=''

plot_tpsin_time={}
plot_tpsin_tpsin={}

plot_proctime_time={}
plot_proctime_proctime={}
plot_proctime_proc_count={}
plot_tpsout_tpsout={}


f=open(sys.argv[1],'r')

s=f.readline()
s_prev=''

while s<>'':
  s=s.replace('\n','')
  s=''.join([c for c in s if ord(c) > 31 or ord(c) == 9])
  if not '99915' in s.split('|')[0].split(':')[0]: 
        for service_ind in xrange(len(tags[server_ind][1])):
		server_name=tags[server_ind][0]
		service_name=tags[server_ind][1][service_ind][0]
		service_name_str=service_name.ljust(15,' ')
		if not svc_proc.has_key(service_name): svc_proc[service_name]={}
		if not svc_proc_start.has_key(service_name): svc_proc_start[service_name]={}
		if not svc_proc_stop.has_key(service_name): svc_proc_stop[service_name]={}
		if not svc_tpsin_list.has_key(service_name): svc_tpsin_list[service_name]=[]
		if not svc_tpsin.has_key(service_name): svc_tpsin[service_name]=0.0
		if not svc_tpsin_max.has_key(service_name): svc_tpsin_max[service_name]=0.0
#		if not svc_tpsin_avg.has_key(service_name): svc_tpsin_avg[service_name]=0.0

		if not svc_occ_tpsin_seconds_prev.has_key(service_name): svc_occ_tpsin_seconds_prev[service_name]=0.0
		if not svc_tpsin_avg_dict.has_key(service_name): svc_tpsin_avg_dict[service_name]={}
		if not svc_occ_max.has_key(service_name): svc_occ_max[service_name]=0
#		if not svc_occ_avg.has_key(service_name): svc_occ_avg[service_name]=0
		if not svc_occ_avg_dict.has_key(service_name): svc_occ_avg_dict[service_name]={}


		if not svc_tpsout.has_key(service_name): svc_tpsout[service_name]=0.0
		if not svc_tpsout_list.has_key(service_name): svc_tpsout_list[service_name]=[]
		if not svc_tpsout_max.has_key(service_name): svc_tpsout_max[service_name]=0.0
#		if not svc_tpsout_avg.has_key(service_name): svc_tpsout_avg[service_name]=0.0
		if not svc_tpsout_avg_dict.has_key(service_name): svc_tpsout_avg_dict[service_name]={}
		if not svc_time_total.has_key(service_name): svc_time_total[service_name]=0.0
		if not svc_time_avg.has_key(service_name): svc_time_avg[service_name]=0.0
		if not svc_time_max.has_key(service_name): svc_time_max[service_name]=0.0
		if not svc_count_total.has_key(service_name): svc_count_total[service_name]=0

		if not svc_occ_tpsout_seconds_prev.has_key(service_name): svc_occ_tpsout_seconds_prev[service_name]=0
		if not svc_occ_tpsout_seconds_curr.has_key(service_name): svc_occ_tpsout_seconds_curr[service_name]=0

		if not svc_in_count.has_key(service_name): svc_in_count[service_name]=0


		if not plot_tpsin_time.has_key(service_name): plot_tpsin_time[service_name]=[]
		if not plot_tpsin_tpsin.has_key(service_name): plot_tpsin_tpsin[service_name]=[]
		if not plot_proctime_time.has_key(service_name): plot_proctime_time[service_name]=[]
		if not plot_proctime_proctime.has_key(service_name): plot_proctime_proctime[service_name]=[]
		if not plot_proctime_proc_count.has_key(service_name): plot_proctime_proc_count[service_name]=[]
		if not plot_tpsout_tpsout.has_key(service_name): plot_tpsout_tpsout[service_name]=[]


		ignore_flag=False
		start_patterns=[ss for ss in tags[server_ind][1][service_ind][1] if ss in s]
#		print "============================================="
#		print ss
#		print tags[server_ind][1][service_ind][1]
#		print "server_ind=%s" % server_ind
#		print "service_ind=%s" % service_ind
#		print s
#		print "start_patterns: %s" % start_patterns
		if len(start_patterns)>0:
#			print "START"
			try:
				s_test=s.split('|')[2]+procid.rjust(10,' ')+s.split('|')[0][-12:]
			except:
				s=s_prev+s
			try:
				procid=s.split('|')[2]
				procid_str=procid.rjust(10,' ')
#				ts=s.split('|')[0][-12:]
				ts=s.split('|')[0][:12]
			except:
				print 'ERROR 1 in line: "'+s+'"'
				sys.exit(1)
			if proc.has_key(procid):
				proc[procid]=proc[procid]+1
			else:
				proc[procid]=1

			if svc_proc[service_name].has_key(procid):
				svc_proc[service_name][procid]=svc_proc[service_name][procid]+1
			else:
				svc_proc[service_name][procid]=1
			try:
				proc_start[procid]=timestr_to_seconds(ts)
			except:
				print 'ERROR 2 in line (ts="'+ts+'") : "'+s+'"'
				sys.exit(1)
			svc_proc_start[service_name][procid]=proc_start[procid]
			tpsin_list.append(proc_start[procid])
			svc_tpsin_list[service_name].append(svc_proc_start[service_name][procid])

			#Calculate TPS IN
			tpsin_max_time=proc_start[procid]
			while tpsin_max_time-tpsin_list[0]>1 and len(tpsin_list)>1:
				del tpsin_list[0]
			tpsin=len(tpsin_list)
			if tpsin>tpsin_max: tpsin_max=tpsin
			tpsin_str=("%.1f" % tpsin).rjust(6,' ')
			tpsin_max_str=("%.1f" % tpsin_max).rjust(6,' ')

			svc_tpsin_max_time[service_name]=svc_proc_start[service_name][procid]
			while svc_tpsin_max_time[service_name]-svc_tpsin_list[service_name][0]>1 and len(svc_tpsin_list[service_name])>1:
				del svc_tpsin_list[service_name][0]
			svc_tpsin[service_name]=len(svc_tpsin_list[service_name])
			if svc_tpsin[service_name]>svc_tpsin_max[service_name]: svc_tpsin_max[service_name]=svc_tpsin[service_name]
			svc_tpsin_str=("%.1f" % svc_tpsin[service_name]).rjust(6,' ')
			svc_tpsin_max_str=("%.1f" % svc_tpsin_max[service_name]).rjust(6,' ')


			#Calculate time period
			occ_tpsin_seconds_curr=timestr_to_seconds(ts)
			if occ_tpsin_seconds_prev==0: occ_tpsin_seconds_prev=occ_tpsin_seconds_curr
			if tpsin_avg_dict.has_key(tpsin):
				tpsin_avg_dict[tpsin]=tpsin_avg_dict[tpsin]+(occ_tpsin_seconds_curr-occ_tpsin_seconds_prev)
			else:
				tpsin_avg_dict[tpsin]=(occ_tpsin_seconds_curr-occ_tpsin_seconds_prev)

			svc_occ_tpsin_seconds_curr[service_name]=timestr_to_seconds(ts)
			if svc_occ_tpsin_seconds_prev[service_name]==0: svc_occ_tpsin_seconds_prev[service_name]=svc_occ_tpsin_seconds_curr[service_name]
			if svc_tpsin_avg_dict[service_name].has_key(svc_tpsin[service_name]):
				svc_tpsin_avg_dict[service_name][svc_tpsin[service_name]]=svc_tpsin_avg_dict[service_name][svc_tpsin[service_name]]+(svc_occ_tpsin_seconds_curr[service_name]-svc_occ_tpsin_seconds_prev[service_name])
			else:
				svc_tpsin_avg_dict[service_name][svc_tpsin[service_name]]=(svc_occ_tpsin_seconds_curr[service_name]-svc_occ_tpsin_seconds_prev[service_name])


			#Calculate Occurances
			proc_count=0
			for key,value in proc.items():
				proc_count=proc_count+value
			if proc_total>0 and proc_count>=proc_total: status_str='+++FULL+++'
			else: status_str='          '
			proc_count_str=str(proc_count).rjust(2,' ')
			if proc_count>occ_max: occ_max=proc_count
			occ_max_str=("%.2f" % occ_max).rjust(5,' ')

			svc_proc_count=0
			for key,value in svc_proc[service_name].items():
				svc_proc_count=svc_proc_count+value
			if svc_proc_total>0 and svc_proc_count>=svc_proc_total: svc_status_str='+++FULL+++'
			else: svc_status_str='          '
			svc_proc_count_str=str(svc_proc_count).rjust(2,' ')
			if svc_proc_count>svc_occ_max[service_name]: svc_occ_max[service_name]=svc_proc_count
			svc_occ_max_str=("%.2f" % svc_occ_max[service_name]).rjust(5,' ')


			if occ_avg_dict.has_key(proc_count):
				occ_avg_dict[proc_count]=occ_avg_dict[proc_count]+(occ_tpsin_seconds_curr-occ_tpsin_seconds_prev)
			else:
				occ_avg_dict[proc_count]=(occ_tpsin_seconds_curr-occ_tpsin_seconds_prev)
			occ_time_total=0.0
			for value in occ_avg_dict.values(): occ_time_total=occ_time_total+value
			occ_avg=0.0
			tpsin_avg=0.0
			if occ_time_total>0:
				for key,value in occ_avg_dict.items(): occ_avg=occ_avg+int(key)*(value/occ_time_total)
				for key,value in tpsin_avg_dict.items(): tpsin_avg=tpsin_avg+int(key)*(value/occ_time_total)
			occ_avg_str=("%.2f" % occ_avg).rjust(5,' ')
			tpsin_avg_str=("%.1f" % tpsin_avg).rjust(6,' ')

			if svc_occ_avg_dict[service_name].has_key(proc_count):
				svc_occ_avg_dict[service_name][proc_count]=svc_occ_avg_dict[service_name][proc_count]+(svc_occ_tpsin_seconds_curr[service_name]-svc_occ_tpsin_seconds_prev[service_name])
			else:
				svc_occ_avg_dict[service_name][svc_proc_count]=(svc_occ_tpsin_seconds_curr[service_name]-svc_occ_tpsin_seconds_prev[service_name])
			svc_occ_time_total=0.0
			for value in svc_occ_avg_dict[service_name].values(): svc_occ_time_total=svc_occ_time_total+value
			svc_occ_avg=0.0
			svc_tpsin_avg=0.0
			if svc_occ_time_total>0:
				for key,value in svc_occ_avg_dict[service_name].items(): svc_occ_avg=svc_occ_avg+int(key)*(value/svc_occ_time_total)
				for key,value in svc_tpsin_avg_dict[service_name].items(): svc_tpsin_avg=svc_tpsin_avg+int(key)*(value/svc_occ_time_total)
			svc_occ_avg_str=("%.2f" % svc_occ_avg).rjust(5,' ')
			svc_tpsin_avg_str=("%.1f" % svc_tpsin_avg).rjust(6,' ')

			svc_in_count[service_name]=svc_in_count[service_name]+1


			plot_tpsin_time[service_name].append(datetime.datetime.strptime(ts,'%H:%M:%S.%f'))
			plot_tpsin_tpsin[service_name].append(svc_tpsin[service_name])
			plot_proctime_proc_count[service_name].append(svc_proc_count)


#			if proc_count>=alert_count: print '%s|%s|%s|+|%s|                                                   |TPS  IN=%s (avg=%s, max=%s)|%s of %s (avg=%s, max=%s)|%s' % (ts,procid_str,service_name_str,status_str,tpsin_str,tpsin_str,tpsin_avg_str,tpsin_max_str,proc_count_str,proc_total_str,occ_avg_str,occ_max_str,start_patterns[0])
			if proc_count>=alert_count: print '%s|%s|%s|+|%s|                                                                              |TPS  IN=%s/%s (avg=%s/%s, max=%s/%s)|%s/%s of %s (avg=%s/%s, max=%s/%s)|%s' % (ts,procid_str,service_name_str,status_str,svc_tpsin_str,tpsin_str.lstrip(),svc_tpsin_avg_str,tpsin_avg_str.lstrip(),svc_tpsin_max_str,tpsin_max_str.lstrip(),svc_proc_count_str,proc_count_str.lstrip(),proc_total_str,svc_occ_avg_str,occ_avg_str.lstrip(),svc_occ_max_str,occ_max_str.lstrip(),start_patterns[0])


		else:
#		  if '000071|' in s: print '!!!!!!!!!!!!!! ERROR222 in "'+s+'"'
		  stop_patterns=[ss for ss in tags[server_ind][1][service_ind][2] if ss in s]
		  if len(stop_patterns)>0:
#			print "STOP"
			try:
				s_test=s.split('|')[2]+procid.rjust(10,' ')+s.split('|')[0][-12:]
			except:
				s=s_prev+s
			try:
				procid=s.split('|')[2]
				procid_str=procid.rjust(10,' ')
#				ts=s.split('|')[0][-12:]
				ts=s.split('|')[0][:12]
			except:
				print 'ERROR 3 in line: "'+s+'"'
				sys.exit(1)
			if proc.has_key(procid):
				if proc[procid]-1<0:
					ignore_flag=True
					if proc[procid]-1<-1: print 'HM!!! '+s
				else:
					proc[procid]=proc[procid]-1
			else:
				proc[procid]=0

			if svc_proc[service_name].has_key(procid):
				if svc_proc[service_name][procid]-1<0:
					ignore_flag=True
				else:
					svc_proc[service_name][procid]=svc_proc[service_name][procid]-1
			else:
				svc_proc[service_name][procid]=0

			if not ignore_flag:
				try:
					proc_stop[procid]=timestr_to_seconds(ts)
				except:
					print 'ERROR 4 in line: "'+s+'"'
					sys.exit(1)
				svc_proc_stop[service_name][procid]=proc_stop[procid]
				tpsout_list.append(proc_stop[procid])
				svc_tpsout_list[service_name].append(svc_proc_stop[service_name][procid])

				#Calculate Time
				if proc_start.has_key(procid): proc_duration=proc_stop[procid]-proc_start[procid]
				else: proc_duration=0
				proc_duration_str="%.6f" % proc_duration
				proc_duration_str=proc_duration_str.rjust(11,' ')
				time_total=time_total+proc_duration
				if proc_duration>time_max: time_max=proc_duration
				count_total=count_total+1
				if count_total>0: time_avg=time_total/count_total
				else: time_avg=0.0
				time_avg_str=("%.6f" % time_avg).rjust(11,' ')
				time_max_str=("%.6f" % time_max).rjust(11,' ')
		
				if svc_proc_start[service_name].has_key(procid): svc_proc_duration=svc_proc_stop[service_name][procid]-svc_proc_start[service_name][procid]
				else: svc_proc_duration=0
				if svc_proc_duration==0.474000 or '13:19:11.923' in s:
					print "!!!!!!!! start=%s      stop=%s" % (svc_proc_start[service_name][procid],svc_proc_stop[service_name][procid])
				svc_proc_duration_str="%.6f" % svc_proc_duration
				svc_proc_duration_str=svc_proc_duration_str.rjust(11,' ')
				svc_time_total[service_name]=svc_time_total[service_name]+svc_proc_duration
				if svc_proc_duration>svc_time_max[service_name]: svc_time_max[service_name]=svc_proc_duration
				svc_count_total[service_name]=svc_count_total[service_name]+1
				if svc_count_total[service_name]>0: svc_time_avg[service_name]=svc_time_total[service_name]/svc_count_total[service_name]
				else: svc_time_avg[service_name]=0.0
				svc_time_avg_str=("%.6f" % time_avg).rjust(11,' ')
				svc_time_max_str=("%.6f" % time_max).rjust(11,' ')


				#Calculate TPS OUT
				tpsout_max_time=proc_stop[procid]
				while tpsout_max_time-tpsout_list[0]>1 and len(tpsout_list)>1:
					del tpsout_list[0]
				tpsout=len(tpsout_list)
				if tpsout>tpsout_max: tpsout_max=tpsout
				tpsout_str=("%.1f" % tpsout).rjust(6,' ')
				tpsout_max_str=("%.1f" % tpsout_max).rjust(6,' ')

				#Calculate time period
				occ_tpsout_seconds_curr=timestr_to_seconds(ts)
				if occ_tpsout_seconds_prev==0: occ_tpsout_seconds_prev=occ_tpsout_seconds_curr
				if tpsout_avg_dict.has_key(tpsout):
					tpsout_avg_dict[tpsout]=tpsout_avg_dict[tpsout]+(occ_tpsout_seconds_curr-occ_tpsout_seconds_prev)
				else:
					tpsout_avg_dict[tpsout]=(occ_tpsout_seconds_curr-occ_tpsout_seconds_prev)

				svc_tpsout_max_time=svc_proc_stop[service_name][procid]
				while svc_tpsout_max_time-svc_tpsout_list[service_name][0]>1 and len(svc_tpsout_list[service_name])>1:
					del svc_tpsout_list[service_name][0]
				svc_tpsout[service_name]=len(svc_tpsout_list[service_name])
				if svc_tpsout[service_name]>svc_tpsout_max[service_name]: svc_tpsout_max[service_name]=svc_tpsout[service_name]
				svc_tpsout_str=("%.1f" % svc_tpsout[service_name]).rjust(6,' ')
				svc_tpsout_max_str=("%.1f" % svc_tpsout_max[service_name]).rjust(6,' ')

				#Calculate time period
				occ_tpsout_seconds_curr=timestr_to_seconds(ts)
				if occ_tpsout_seconds_prev==0: occ_tpsout_seconds_prev=occ_tpsout_seconds_curr
				if tpsout_avg_dict.has_key(tpsout):
					tpsout_avg_dict[tpsout]=tpsout_avg_dict[tpsout]+(occ_tpsout_seconds_curr-occ_tpsout_seconds_prev)
				else:
					tpsout_avg_dict[tpsout]=(occ_tpsout_seconds_curr-occ_tpsout_seconds_prev)

				svc_occ_tpsout_seconds_curr[service_name]=timestr_to_seconds(ts)
				if svc_occ_tpsout_seconds_prev[service_name]==0: svc_occ_tpsout_seconds_prev[service_name]=svc_occ_tpsout_seconds_curr[service_name]
				if svc_tpsout_avg_dict[service_name].has_key(svc_tpsout[service_name]):
					svc_tpsout_avg_dict[service_name][svc_tpsout[service_name]]=svc_tpsout_avg_dict[service_name][svc_tpsout[service_name]]+(svc_occ_tpsout_seconds_curr[service_name]-svc_occ_tpsout_seconds_prev[service_name])
				else:
					svc_tpsout_avg_dict[service_name][svc_tpsout[service_name]]=(svc_occ_tpsout_seconds_curr[service_name]-svc_occ_tpsout_seconds_prev[service_name])


				#Calculate Occurances
				proc_count=0
				for key,value in proc.items():
					proc_count=proc_count+value
				status_str='          '
				proc_count_str=str(proc_count).rjust(2,' ')
				if proc_count>occ_max: occ_max=proc_count
				occ_max_str=("%.2f" % occ_max).rjust(5,' ')

				svc_proc_count=0
				for key,value in svc_proc[service_name].items():
					svc_proc_count=svc_proc_count+value
				svc_status_str='          '
				svc_proc_count_str=str(svc_proc_count).rjust(2,' ')
				if svc_proc_count>svc_occ_max[service_name]: svc_occ_max[service_name]=svc_proc_count
				svc_occ_max_str=("%.2f" % svc_occ_max[service_name]).rjust(5,' ')


				if occ_avg_dict.has_key(proc_count):
					occ_avg_dict[proc_count]=occ_avg_dict[proc_count]+(occ_tpsout_seconds_curr-occ_tpsout_seconds_prev)
				else:
					occ_avg_dict[proc_count]=(occ_tpsout_seconds_curr-occ_tpsout_seconds_prev)
				occ_time_total=0.0
				for value in occ_avg_dict.values(): occ_time_total=occ_time_total+value
				occ_avg=0.0
				tpsout_avg=0.0
				if occ_time_total>0:
					for key,value in occ_avg_dict.items(): occ_avg=occ_avg+int(key)*(value/occ_time_total)
					for key,value in tpsout_avg_dict.items(): tpsout_avg=tpsout_avg+int(key)*(value/occ_time_total)
				occ_avg_str=("%.2f" % occ_avg).rjust(5,' ')
				tpsout_avg_str=("%.1f" % tpsout_avg).rjust(6,' ')

				if svc_occ_avg_dict[service_name].has_key(svc_proc_count):
					svc_occ_avg_dict[service_name][svc_proc_count]=svc_occ_avg_dict[service_name][svc_proc_count]+(svc_occ_tpsout_seconds_curr[service_name]-svc_occ_tpsout_seconds_prev[service_name])
				else:
					svc_occ_avg_dict[service_name][svc_proc_count]=(svc_occ_tpsout_seconds_curr[service_name]-svc_occ_tpsout_seconds_prev[service_name])
				svc_occ_time_total=0.0
				for value in svc_occ_avg_dict[service_name].values(): svc_occ_time_total=svc_occ_time_total+value
				svc_occ_avg=0.0
				svc_tpsout_avg=0.0
				if svc_occ_time_total>0:
					for key,value in svc_occ_avg_dict[service_name].items(): svc_occ_avg=svc_occ_avg+int(key)*(value/svc_occ_time_total)
					for key,value in svc_tpsout_avg_dict[service_name].items(): svc_tpsout_avg=svc_tpsout_avg+int(key)*(value/svc_occ_time_total)
				svc_occ_avg_str=("%.2f" % svc_occ_avg).rjust(5,' ')
				svc_tpsout_avg_str=("%.1f" % svc_tpsout_avg).rjust(6,' ')

#				print '+++++++++++++++++++++++++   '+server_name+(' : %s' % svc_proc_duration)
#				if not test_enable_flag and s[:5]=='13:15': test_enable_flag=True
				if server_name=='pos_conctr' and svc_proc_duration>120:
					pass
				else:
					if test_enable_flag:
						plot_proctime_time[service_name].append(datetime.datetime.strptime(ts,'%H:%M:%S.%f'))
						plot_proctime_proctime[service_name].append(svc_proc_duration)
#						plot_proctime_proc_count[service_name].append(svc_proc_count)
						plot_tpsout_tpsout[service_name].append(svc_tpsout[service_name])
				

#				if proc_count>=alert_count: print '%s|%s|%s|-|          |TIME=%s (avg=%s, max=%s)|TPS OUT=%s (avg=%s, max=%s)|%s of %s (avg=%s, max=%s)|%s' % (ts,procid_str,service_name_str,proc_duration_str,time_avg_str,time_max_str,tpsout_str,tpsout_avg_str,tpsout_max_str,proc_count_str,proc_total_str,occ_avg_str,occ_max_str,stop_patterns[0])
				if proc_count>=alert_count: print '%s|%s|%s|-|          |TIME=%s/%s (avg=%s/%s, max=%s/%s)|TPS OUT=%s/%s (avg=%s/%s, max=%s/%s)|%s/%s of %s (avg=%s/%s, max=%s/%s)|%s' % (ts,procid_str,service_name_str,svc_proc_duration_str,proc_duration_str.lstrip(),svc_time_avg_str,time_avg_str.lstrip(),svc_time_max_str,time_max_str.lstrip(),svc_tpsout_str,tpsout_str.lstrip(),svc_tpsout_avg_str,tpsout_avg_str.lstrip(),svc_tpsout_max_str,tpsout_max_str.lstrip(),svc_proc_count_str,proc_count_str.lstrip(),proc_total_str,svc_occ_avg_str,occ_avg_str.lstrip(),svc_occ_max_str,occ_max_str.lstrip(),stop_patterns[0])
#		  else:
#			if '000070|' in s: print '!!!!!!!!!!!!!! ERROR333 in "'+s+'"'

		if not ignore_flag and (any(ss in s for ss in tags[server_ind][1][service_ind][1]) or any(ss in s for ss in tags[server_ind][1][service_ind][2])):
			occ_tpsin_seconds_prev=occ_tpsin_seconds_curr
			occ_tpsout_seconds_prev=occ_tpsout_seconds_curr

			if svc_occ_tpsin_seconds_curr.has_key(service_name):
				svc_occ_tpsin_seconds_prev[service_name]=svc_occ_tpsin_seconds_curr[service_name]
			else:
				svc_occ_tpsin_seconds_prev[service_name]=0
			if svc_occ_tpsout_seconds_prev.has_key(service_name):
				svc_occ_tpsout_seconds_prev[service_name]=svc_occ_tpsout_seconds_curr[service_name]
			else:
				svc_occ_tpsout_seconds_prev[service_name]=0
			break

  s_prev=s
  s=f.readline()

f.close()



print '================================='


suggested_servers_count_float_acc=0.0
services_report={}
for service_ind in xrange(len(tags[server_ind][1])):
	service_name=tags[server_ind][1][service_ind][0]
	service_name_str=service_name.ljust(15,' ')
	services_report[service_name]={}
	current_servers_count=proc_total
	if current_servers_count<>0 and svc_time_avg[service_name]<>0:
		current_max_tps=1/(current_servers_count*svc_time_avg[service_name])
		suggested_servers_count=(svc_tpsin_max[service_name]-current_max_tps)*svc_time_avg[service_name]
#DEBUG
#		print "***DEBUG current_servers_count/svc_time_max[service_name] = %s/%s" % (current_servers_count,svc_time_max[service_name])
#DEBUG
		current_max_tps=current_servers_count/svc_time_max[service_name]
#		suggested_servers_count=math.ceil((current_servers_count+(svc_tpsin_max[service_name]-current_max_tps)*svc_time_max[service_name])*1.5)
		suggested_servers_count=math.ceil((svc_tpsin_max[service_name]*svc_time_max[service_name])*1.5)
		suggested_servers_count_float=(svc_tpsin_max[service_name]*svc_time_max[service_name])*1.5
#		suggested_servers_count_float=suggested_servers_count_float+(current_servers_count+(svc_tpsin_max[service_name]-current_max_tps)*svc_time_max[service_name])*1.5
		suggested_servers_count_float_acc=suggested_servers_count_float_acc+suggested_servers_count_float
		if suggested_servers_count<=0: suggested_servers_count=1
	else:
		current_max_tps=0
		suggested_servers_count=0
		suggested_servers_count_float=0.0

	current_max_tps_str=("%.2f" % current_max_tps).rjust(8,' ')
	svc_tpsin_max_str=("%.2f" % svc_tpsin_max[service_name]).rjust(6,' ')
	svc_time_max_str=("%.6f" % svc_time_max[service_name]).rjust(11,' ')
	suggested_servers_count_str=str(int(suggested_servers_count)).rjust(4,' ')
	suggested_servers_count_float_str=("%.4f" % suggested_servers_count_float).rjust(10,' ')

	services_report[service_name]['service_name']=service_name
	services_report[service_name]['service_name_str']=service_name_str
	services_report[service_name]['current_servers_count']=current_servers_count
	services_report[service_name]['current_max_tps']=current_max_tps
	services_report[service_name]['current_max_tps_str']=current_max_tps_str
	services_report[service_name]['svc_tpsin_max']=svc_tpsin_max[service_name]
	services_report[service_name]['svc_tpsin_max_str']=svc_tpsin_max_str
#	services_report[service_name]['svc_tpsin_avg']=svc_tpsin_avg[service_name]
	services_report[service_name]['svc_tpsout_max']=svc_tpsout_max[service_name]
#	services_report[service_name]['svc_tpsout_avg']=svc_tpsout_avg[service_name]
	services_report[service_name]['svc_time_max']=svc_time_max[service_name]
	services_report[service_name]['svc_time_max_str']=svc_time_max_str
	services_report[service_name]['svc_time_avg']=svc_time_avg[service_name]
	services_report[service_name]['suggested_servers_count']=suggested_servers_count
	services_report[service_name]['suggested_servers_count_str']=suggested_servers_count_str
	services_report[service_name]['suggested_servers_count_float']=suggested_servers_count_float
	services_report[service_name]['suggested_servers_count_float_str']=suggested_servers_count_float_str
	services_report[service_name]['svc_in_count']=svc_in_count[service_name]

#	print 'Server: %s, Service: %s, log name: "%s". Current maximum available TPS resorce for %s server(s) is %s (from log: MAX_TPS_IN=%s, MAX_TIME=%s). Suggested MIN value for tuxedo server (+50%%) = %s/%s' % (log,service_name_str,sys.argv[1],current_servers_count,current_max_tps_str,svc_tpsin_max_str,svc_time_max_str,suggested_servers_count_str,suggested_servers_count_float_str)

for services_dict in services_report.values():
	print 'Server: %s, Service: %s, log name: "%s". Current maximum available TPS resorce for %s server(s) is %s (from log: MAX_TPS_IN=%s, MAX_TIME=%s). Suggested MIN value for tuxedo server (+50%%) = %s/%s' % (log,services_dict['service_name_str'],sys.argv[1],services_dict['current_servers_count'],services_dict['current_max_tps_str'],services_dict['svc_tpsin_max_str'],services_dict['svc_time_max_str'],services_dict['suggested_servers_count_str'],services_dict['suggested_servers_count_float_str'])

print '================================='
print ' Allocation by Max Process Time  '
print '================================='
total_time=0.0
for services_dict in services_report.values():
	total_time=total_time+services_dict['svc_time_max']
for services_dict in services_report.values():
	svc_time_perc_str=("%.2f" % (100*(float(services_dict['svc_time_max'])/float(total_time)))).rjust(6,' ')
	print "%s %s%%" % (services_dict['service_name_str'],svc_time_perc_str)
print '================================='

print '================================='
print '   Allocation by Max TPS IN      '
print '================================='
total_tps=0.0
for services_dict in services_report.values():
	total_tps=total_tps+services_dict['svc_tpsin_max']
for services_dict in services_report.values():
	svc_tps_perc_str=("%.2f" % (100*(float(services_dict['svc_tpsin_max'])/float(total_tps)))).rjust(6,' ')
	print "%s %s%%" % (services_dict['service_name_str'],svc_tps_perc_str)
print '================================='

print '================================='
print '   Incoming Messages Count      '
print '================================='
svc_in_count_total=0
for services_dict in services_report.values():
	svc_in_count_total=svc_in_count_total+services_dict['svc_in_count']
for services_dict in services_report.values():
	svc_in_count_perc_str=("%.2f" % (100*(float(services_dict['svc_in_count'])/float(svc_in_count_total)))).rjust(6,' ')
	print "%s %s%% (%s)" % (services_dict['service_name_str'],svc_in_count_perc_str,services_dict['svc_in_count'])
print '================================='

print '================================='
#print occ_avg_dict
#for value in occ_avg_dict.values(): print '+++ occ_time_total=%s' % (value)

current_servers_count=proc_total
#DEBUG
print '***DEBUG: current_servers_count=%s, time_avg=%s' % (current_servers_count,time_avg)
#DEBUG
#current_max_tps=1/(current_servers_count*time_avg)
#suggested_servers_count=(tpsin_max-current_max_tps)*time_avg


#current_max_tps=1/(current_servers_count*time_max)
current_max_tps=current_servers_count/time_max
#suggested_servers_count=(tpsin_max-current_max_tps)*time_max
suggested_servers_count=math.ceil((current_servers_count+(tpsin_max-current_max_tps)*time_max)*1.5)
if suggested_servers_count<=0: suggested_servers_count=1
#DEBUG
#print '***DEBUG: tpsin_max=%s, current_max_tps=%s, time_max=%s, current_servers_count=%s, suggested_servers_count=%s' % (tpsin_max,current_max_tps,time_max,current_servers_count,suggested_servers_count)
#DEBUG


suggested_servers_count_float=math.ceil(suggested_servers_count_float)
#print 'Server: %s, log name: "%s". Current maximum available TPS for %s server(s) is %s. Suggested MIN value for tuxedo server (+50%%) =%s' % (log,sys.argv[1],current_servers_count,current_max_tps,int(suggested_servers_count))
print 'Server: %s, log name: "%s". Suggested MIN value for tuxedo server (+50%%) = %s' % (log,sys.argv[1],math.ceil(suggested_servers_count_float_acc*1.5))




##########################
# PLOT DATA SAVE TO FILE
##########################
f_out=open(sys.argv[1]+'_PLOT.txt','w')

for services_dict in services_report.values():
######
#  IN
######
	f_out.write('START|'+services_dict['service_name']+' (TPS IN)'+'\n')
	for xxi in xrange(len(plot_tpsin_time[services_dict['service_name']])):
		f_out.write(datetime.datetime.strftime(plot_tpsin_time[services_dict['service_name']][xxi],'%H:%M:%S.%f')+'|'+str(plot_tpsin_tpsin[services_dict['service_name']][xxi])+'\n')
	f_out.write('STOP|'+services_dict['service_name']+' (TPS IN)'+'\n')

	f_out.write('START|'+services_dict['service_name']+' (Used Proc Count)'+'\n')
	for xxi in xrange(len(plot_tpsin_time[services_dict['service_name']])):
		f_out.write(datetime.datetime.strftime(plot_tpsin_time[services_dict['service_name']][xxi],'%H:%M:%S.%f')+'|'+str(plot_proctime_proc_count[services_dict['service_name']][xxi])+'\n')
	f_out.write('STOP|'+services_dict['service_name']+' (Used Proc Count)'+'\n')

######
#  OUT
######
	f_out.write('START|'+services_dict['service_name']+' (TPS OUT)'+'\n')
	for xxi in xrange(len(plot_proctime_time[services_dict['service_name']])):
		f_out.write(datetime.datetime.strftime(plot_proctime_time[services_dict['service_name']][xxi],'%H:%M:%S.%f')+'|'+str(plot_tpsout_tpsout[services_dict['service_name']][xxi])+'\n')
	f_out.write('STOP|'+services_dict['service_name']+' (TPS OUT)'+'\n')

	f_out.write('START|'+services_dict['service_name']+' (TRN PROC TIME, sec)'+'\n')
	for xxi in xrange(len(plot_proctime_time[services_dict['service_name']])):
		f_out.write(datetime.datetime.strftime(plot_proctime_time[services_dict['service_name']][xxi],'%H:%M:%S.%f')+'|'+str(plot_proctime_proctime[services_dict['service_name']][xxi])+'\n')
	f_out.write('STOP|'+services_dict['service_name']+' (TRN PROC TIME, sec)'+'\n')


f_out.close()

##########################
##########################



###################
# PLOT
###################
import matplotlib.pyplot as plt
import datetime

col=['b-','r-','g-','c-','m-','k-']
coli=0
for services_dict in services_report.values():
#	if services_dict['service_name']=='SWITCH_REQ':
#	if services_dict['service_name'] in ['POS_CONCENTRATOR','POS_IN']:
	if True:
		print 'LENGTH 1 = %s' % len(plot_tpsin_time[services_dict['service_name']])
		print 'LENGTH 2 = %s' % len(plot_tpsin_tpsin[services_dict['service_name']])
		plt.plot(plot_tpsin_time[services_dict['service_name']],plot_tpsin_tpsin[services_dict['service_name']],col[coli],label=services_dict['service_name'],linewidth=0.4)
		coli=coli+1
	if coli>len(col)-1: coli=0

plt.gcf().autofmt_xdate()
plt.legend(loc=2,prop={'size':12})
plt.grid()
font={'size':12}
plt.rc('font',**font)
plt.savefig('PLOT_'+server_name+'_TPSIN.png', dpi=300)
plt.show()



coli=0
for services_dict in services_report.values():
#	if services_dict['service_name']=='SWITCH_REQ':
#	if services_dict['service_name'] in ['POS_CONCENTRATOR','POS_IN']:
	if True:
		print 'LENGTH 3 = %s' % len(plot_proctime_proctime[services_dict['service_name']])
		plt.plot(plot_proctime_time[services_dict['service_name']],plot_proctime_proctime[services_dict['service_name']],col[coli],label=services_dict['service_name'],linewidth=0.4)
		coli=coli+1
	if coli>len(col)-1: coli=0

plt.gcf().autofmt_xdate()
plt.legend(loc=2,prop={'size':12})
plt.grid()
font={'size':12}
plt.rc('font',**font)
plt.savefig('PLOT_'+server_name+'_TIME.png', dpi=300)
plt.show()



#PROC COUNT and PROCESS TIME together

col=['b-','r-','g-','c-','m-','k-']
coli=0
for services_dict in services_report.values():
#	if services_dict['service_name']=='SWITCH_REQ':
#	if services_dict['service_name'] in ['POS_CONCENTRATOR','POS_IN']:
	if True:
#		if services_dict['service_name'] in ['POS_CONCENTRATOR']:
		if False:
#			plt.plot(plot_proctime_time[services_dict['service_name']],plot_proctime_proc_count[services_dict['service_name']],col[coli],marker='.',markersize=4,label='Used Threads Count',linestyle='None')
			plt.plot(plot_proctime_time[services_dict['service_name']],plot_proctime_proc_count[services_dict['service_name']],col[coli],label='Used Threads Count',linewidth=1)
			coli=coli+1
#		plt.plot(plot_proctime_time[services_dict['service_name']],plot_proctime_proctime[services_dict['service_name']],col[coli],marker='.',markersize=4,label='Transaction Process Time (seconds)',linestyle='None')
		plt.plot(plot_proctime_time[services_dict['service_name']],plot_proctime_proctime[services_dict['service_name']],col[coli],label='Transaction Process Time (seconds)',linewidth=1)
		coli=coli+1
#		if services_dict['service_name'] in ['POS_CONCENTRATOR','POS_IN']:
		if True:
			l='TPS'
			if services_dict['service_name'] in ['POS_CONCENTRATOR']: l='TPS (Received and Processed)'
			if services_dict['service_name'] in ['POS_IN']: l='TPS (All incoming traffic)'
			plt.plot(plot_proctime_time[services_dict['service_name']],plot_tpsout_tpsout[services_dict['service_name']],col[coli],label=l,linewidth=1)
			coli=coli+1
	if coli>len(col)-1: coli=0

plt.gcf().autofmt_xdate()
plt.legend(loc=2,prop={'size':12})
plt.grid()
font={'size':12}
plt.rc('font',**font)
plt.savefig('PLOT_'+server_name+'_PROCC_TIME.png', dpi=300)
plt.show()





###################
