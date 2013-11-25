import os
import sys
import csv
import argparse
from random import randint


def get_test_list(f):
	test_dict = {}
	fobject   = open(f,'r')	
	try:		
		rows         = csv.reader(fobject)		
		mlist        = list(rows)
		test_dict[0] = mlist[0] #add the header
		prev_rands   = [0]		
		ln           = int((len(mlist)-1)/3)				
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
	test_dict  = get_test_list(f)
	fobject    = open(f,'r')
	try:		
		rows  = csv.reader(fobject)
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
def save_train_file(saving_dir,dataset_name,dtype):
	train_list = {}
	ofile=""
	if dtype == "COMBINED":	
		train_list = get_combined_train(dataset_name) # in this case dataset name is a parent directory
		ofile      = open(get_path(saving_dir,"%s.train_1to1"%("combined.moses")),"w") 
		#print "no of columns in combined train list = %s"%(len(train_list[0]))
	if dtype == "SINGLE":
		train_list = get_train_list(dataset_name)
		ofile      = open(get_path(saving_dir,"%s.train_1to1"%dataset_name),"w") 	
	try:
		writer = csv.writer(ofile)    
		for key in train_list:					
			writer.writerow(train_list[key])
	finally:		
		ofile.close()				
def save_test_file(saving_dir,dataset_name,dtype):	
	test_list = {}	
	if dtype == "COMBINED":	
		test_list = get_combined_test(dataset_name) # in this case dataset name is a parent directory
		ofile     = open(get_path(saving_dir,"%s.test_1to1"%("combined.moses")),"w")
	if dtype == "SINGLE":
		test_list = get_test_list(dataset_name)
		ofile     = open(get_path(saving_dir,"%s.test_1to1"%dataset_name),"w") 	
	try:				
		writer = csv.writer(ofile)    
		for key in test_list:					
			writer.writerow(test_list[key])
	finally:		
		ofile.close()
def get_combined_test(mfile_dir):
	moses_binfs    = [ f for f in os.listdir(mfile_dir) if os.path.isfile(os.path.join(mfile_dir,f)) ] # assuming no other type of file is listed in this dir	
	test           = {}
	rand_mfile     = os.path.join(mfile_dir,moses_binfs[0])
	fobject        = open(rand_mfile,'r')
	i              = 0	
	try:				
		rows    = csv.reader(fobject)
		mlist   = list(rows)			
		test[0] = mlist[0]  # add the header to test	
		i      += 1	
	finally:
		fobject.close()			
	for m_binf in moses_binfs:
		m_binf    = os.path.join(mfile_dir,m_binf)							
		test_temp = get_test_list(m_binf)
		del test_temp[0] # delete header since its already added 						
		for key in test_temp:			
			test[i] = test_temp[key] # append each test files
			i      += 1					
	return test
def get_combined_train(mfile_dir):
	#print "@DEBUG get_combined_train() mfile_dir=%s"%(mfile_dir)	
	moses_binfs    = [ f for f in os.listdir(mfile_dir) if os.path.isfile(os.path.join(mfile_dir,f)) ] # assuming no other type of file is listed in this dir	
	train          = {}
	rand_mfile     = os.path.join(mfile_dir,moses_binfs[0])
	fobject        = open(rand_mfile,'r')
	i              = 0	
	try:				
		rows     = csv.reader(fobject)
		mlist    = list(rows)			
		train[0] = mlist[0]  # add the header to test
		i       += 1				
	finally:
		fobject.close()				
	for m_binf in moses_binfs:
		m_binf     = os.path.join(mfile_dir,m_binf)							
		train_temp = get_train_list(m_binf)
		del train_temp[0] 	# delete header since its already added						
		for key in train_temp:			
			train[i] = train_temp[key] # append each test files
			i       += 1						
	return train							
if __name__ == "__main__":
	usage  = "usage: %prog [options]\n"
	parser = argparse.ArgumentParser(usage)						
	parser.add_argument("-i", "--dataset_file",nargs=1,help = "Input dataset file to be divided in to train and test")
	parser.add_argument("-o", "--saving_dir",nargs=1,help = "saving directory for training and testing files")
	parser.add_argument("-r","--recursive",nargs=1,help="prepare training and testing of all files in a directory")
	args = parser.parse_args()
	if args.dataset_file and args.saving_dir:			
		#print "PATH="+args.dataset_file[0]	
		file_path  = os.path.abspath(args.dataset_file[0])		
		saving_dir = os.path.abspath(args.saving_dir[0])
		if args.recursive:
			print "started saving combined train test file preparation..."
			save_train_file(saving_dir,file_path,"COMBINED")
			save_test_file(saving_dir,file_path,"COMBINED")
			print "saved combined train test to %s"%(saving_dir)
		else:	
			#print "SAVING DIR="+saving_dir
			save_test_file(saving_dir,file_path,"SINGLE")
			save_train_file(saving_dir,file_path,"SINGLE")
	else:
		print parser.print_help()	                				
	 
	
	
		
				
				
