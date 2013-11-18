import os
import sys
import csv
import argparse
from random import randint


def get_test_list(f):
	test_dict = {}	
	try:
		fobject = open(f,'r')
		rows = csv.reader(fobject)		
		mlist = list(rows)
		test_dict[0] = mlist[0] #add the header
		prev_rands = [0]		
		ln = int((len(mlist)-1)/3)				
		for r in range(0,ln):
			i = randint(1,len(mlist)-1)
			while i in prev_rands: #make sure a new valide index is selected
				i = randint(1,len(mlist)-1)
			prev_rands.append(i)
			test_dict[i] = mlist[i]			
	finally:		
		fobject.close()			
	return test_dict
def	 get_train_list(f):
	train_dict = {}
	test_dict = get_test_list(f)
	try:
		fobject = open(f,'r')
		rows = csv.reader(fobject)
		mlist = list(rows)
		train_dict[0] = mlist[0] # add the header		
		for r in range(1,len(mlist)):
			if  r not in test_dict:			
			    train_dict[r] = mlist[r]
	finally:
		fobject.close()
	return train_dict	
def get_path(saving_dir,file_name):
	return os.path.join(saving_dir,file_name)			
def save_train_file(saving_dir,dataset_name):	
	train_list = get_train_list(dataset_name)	
	try:
		ofile = open(get_path(saving_dir,"%s.train_1to1"%dataset_name),"w")		
		writer = csv.writer(ofile)    
		for key in train_list:					
			writer.writerow(train_list[key])
	finally:		
		ofile.close()				
def save_test_file(saving_dir,dataset_name):	
	test_list = get_test_list(dataset_name)	
	try:
		ofile=open(get_path(saving_dir,"%s.test_1to1"%dataset_name),"w")		
		writer = csv.writer(ofile)    
		for key in test_list:					
			writer.writerow(test_list[key])
	finally:		
		ofile.close()
if __name__ == "__main__":
	usage = "usage: %prog [options]\n"
	parser = argparse.ArgumentParser(usage)						
	parser.add_argument("-i", "--dataset_file",nargs=1,help = "Input dataset file to be divided in to train and test")
	parser.add_argument("-o", "--saving_dir",nargs=1,help = "saving directory for training and testing files")
	args = parser.parse_args()
	if args.dataset_file and args.saving_dir:	
		print "PATH="+args.dataset_file[0]	
		file_path = os.path.abspath(args.dataset_file[0])		
		saving_dir = os.path.abspath(args.saving_dir)
		print "SAVING DIR="+saving_dir
		save_test_file(saving_dir,file_path)
		save_train_file(saving_dir,file_path)
	else:
		print parser.print_help()	                				
	 
	
	
		
				
				
