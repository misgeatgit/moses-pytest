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
	mfile_dir         = os.path.abspath(args.mfile_dir[0])
	exp_dir_parent    = os.path.abspath(args.exp_dir[0])    
    moses_binfs       = [ f for f in os.listdir(mfile_dir) if os.path.isfile(os.path.join(mfile_dir,f)) ] # assuming no other type of file is listed in this dir
    for moses_binf in moses_binfs:
		mbinf      = os.path.basename(moses_binf)
		mbinf_name = mbinf.split('.',1)[0]
		exp_dir = os.path.join(exp_dir_parent,mbinf_name) # assuming file named as xyz.moses or whatever with only one period		
		if not os.path.exists(exp_dir):
			os.makedir(exp_dir)
			data_dir = os.path.join(exp_dir,DATA_DIR)
			anal_dir = os.path.join(exp_dir,ANAL_DIR)
			log_dir  = os.path.join(exp_dir,LOG_DIR)
			res_dir  = os.path.join(exp_dir,RES_DIR)
			os.makedir(data_dir)
			os.makedir(anal_dir)
			os.makedir(log_dir)
			os.makedir(res_dir)		
			copy(moses_binf,data_dir)
			moses_binf = os.path.join(data_dir,mbinf)
			#run train-test.py
			os.system("python train-test.py -i %s -o %s"%(moses_binf,data_dir)
			#run run_exp.py
			conff  = os.path.abspath(MOSES_PARAMA_CONFIG_FILE)
			logf   = os.join(log_dir,mbinf_name+".train_1to1.moses.log")
			trainf = os.join(data_dir,mbinf+".train_1to1")
			combof = os.join(res_dir,mbinf+".train_1to1.combo")
			os.system("python run_exp.py -i %s -o %s -f %s -c %s"%(trainf,combof,logf,conff))
			#run anal_exp.py
			os.system("python anal_exp.py - %s -d %s -c %s"%())
												
if __name__ == "main":
	usage = "usage: %prog [options]\n"
	parser = argparse.ArgumentParser(usage)						
	parser.add_argument("-d", "--mfile-dir",nargs=1,help = "Input file")
	parser.add_argument("-e","--exp-dir",nargs=1,help="The directory where all the experiment takes place")
	args=parser.parse_args()
	if args.mfile_dir and args.exp_dir:
		start(args)
	else:
		parser.print_help()	
