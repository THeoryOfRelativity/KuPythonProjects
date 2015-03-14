#python kuEmulator.py --protocol=HYPERCOM --ip=127.0.0.1 --port=7174 --filetype=internal --loglevel=-1 --config_dir=/usr2/tuxedo/rtps/irakli/python/IFEMUL


#single
#python kuEmulator.py --protocol=HYPERCOM --ip=127.0.0.1 --port=7174 --filetype=internal --loglevel=1 --config_dir=/usr2/tuxedo/rtps/irakli/python/IFEMUL --threads=1

#stress
python kuEmulator.py --protocol=HYPERCOM --ip=127.0.0.1 --port=7174 --filetype=internal --loglevel=1 --config_dir=/usr2/tuxedo/rtps/irakli/python/IFEMUL --cards_file=iss.txt --terminals_file=acq.txt --threads=5

