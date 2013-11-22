#!/bin/python2.7

import argparse
import os
import shutil


DATA_DIR="data"
ANAL_DIR="anal"
LOG_DIR="log"
RES_DIR="res"
MOSES_PARAMA_CONFIG_FILE="mparam.cnf"
def start(args):
	exp_count      = 0
	mfile_dir      = os.path.abspath(args.mfile_dir[0])
	exp_dir_parent = os.path.abspath(args.exp_dir[0])    
	moses_binfs    = [ f for f in os.listdir(mfile_dir) if os.path.isfile(os.path.join(mfile_dir,f)) ] # assuming no other type of file is listed in this dir
	for moses_binf in moses_binfs:
		print "Info:running experiment on %s..."%moses_binf
		moses_binf_path=os.path.join(mfile_dir,moses_binf)
		mbinf      = os.path.basename(moses_binf)
		mbinf_name = mbinf.split('.',1)[0]
		exp_dir = os.path.join(exp_dir_parent,mbinf_name) # assuming file named as xyz.moses or whatever with only one period		
		if not os.path.exists(exp_dir):
			os.mkdir(exp_dir)
			data_dir = os.path.join(exp_dir,DATA_DIR)
			anal_dir = os.path.join(exp_dir,ANAL_DIR)
			log_dir  = os.path.join(exp_dir,LOG_DIR)
			res_dir  = os.path.join(exp_dir,RES_DIR)
			os.mkdir(data_dir)
			os.mkdir(anal_dir)
			os.mkdir(log_dir)
			os.mkdir(res_dir)
			#print "DEBUG copy path %s"%	moses_binf_path
			#exit(0)	
			shutil.copy(moses_binf_path,data_dir)			
			#run train-test.py
			print "\t*Generating train test files..."
			os.system("python train_test.py -i %s -o %s"%(os.path.join(data_dir,mbinf),data_dir))
			print "\tfinished"			
			#run run_exp.py
			configf  = os.path.abspath(MOSES_PARAMA_CONFIG_FILE)
			logf     = os.path.join(log_dir,mbinf_name+".train_1to1.moses.log")
			trainf   = os.path.join(data_dir,mbinf+".train_1to1")
			moutf    = os.path.join(res_dir,mbinf+".train_1to1.mout")
			print "\t*learning on train..."
			os.system("python run_exp.py -i %s -o %s -f %s -c %s"%(trainf,moutf,logf,configf))
			print "\tfinished"			
			#run anal_exp.py
			print "\t*saving scores..."
			os.system("python anal_exp.py -i %s -d %s -c %s"%(os.path.join(data_dir,mbinf),data_dir,moutf))
			print "\tfinished"			
			print "finished experiment on %s"%moses_binf 
			exp_count+=1
	print "Info:finished experiment on %d files"%exp_count		           												
if __name__ == "__main__":
	usage = "usage: %prog [options]\n"
	parser = argparse.ArgumentParser(usage)						
	parser.add_argument("-d", "--mfile-dir",nargs=1,help = "moses bin files directory")
	parser.add_argument("-e","--exp-dir",nargs=1,help="The directory where all the experiment takes place")
	args=parser.parse_args()
	if args.mfile_dir and args.exp_dir:
		start(args)
	else:
		parser.print_help()	
