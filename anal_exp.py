#!/bin/python2.7
import os
import csv
import argparse
EVAL_TABLE_PATH="/home/addis-ai/opencog_ocpkg/opencog/build/opencog/comboreduct/main/eval-table"
"""Extract the combo programs from a given moses output file
   params    moses output file,combo file to be saved
"""
def parse_output(outputf,combof):	
	f = open(outputf,'r')
	combo_line = f.readline()
	f.close()
	combo = combo_line.split(' ',1)[1]
	#print "COMBO="+combo
	combo_file = open(combof,'w')
	combo_file.write(combo)
	combo_file.close()	
"""evaluate the combo program
   params
   -actual file,combo file,output file"""		
def eval_output(ifile,cfile,ofile):
	global EVAL_TABLE_PATH
	EVAL_TABLE_ARGS = "  -i %s -C %s -o %s -u OUT "%(ifile,cfile,ofile)
	#print "eval-table CMD="+EVAL_TABLE_PATH + " " + EVAL_TABLE_ARGS
	result=os.system(EVAL_TABLE_PATH + " " + EVAL_TABLE_ARGS) 
	if result!=0:
		print "error while executing"
		exit(0)	
"""get values of a given column name from a csv file
   returns list of the column values without the column name
   params csv file path,column name,delimiter char in the csv
"""
def values_of_col(csvf,col_name,sepchar):
	col_values=[]
	with open(csvf,'rb') as f:
		reader=csv.reader(f,delimiter=sepchar)
		csv_list=list(reader)
		header_row=csv_list[0]		
		col_name_index=header_row.index(col_name)
		for row in csv_list:
			col_values.append(row[col_name_index])
	del col_values[0] # remove the column name		
	return col_values	
"""recall for fixed train test"""						
def get_recall(predictedf,actualf):
	actual_values = values_of_col(actualf,"OUT","\t")
	predicted_values = values_of_col(predictedf,"OUT","\t")
	true_positve=0.0
	trues=0.0
	assert len(actual_values) == len(predicted_values)
	#DEBUG OUTPUTS
	#print "ACTUALF=%s PREDICTEDF=%s \n"%(actualf,predictedf)
	#for i in range(0,len(actual_values)):
	#	print "%s\t%s %s"%(str(i+1),actual_values[i],predicted_values[i])
	#exit(0)
	#END OF DEBUG	
	for i in range(0,len(actual_values)):
		if actual_values[i] == '1':
			trues += 1
			if predicted_values[i] == '1':
				true_positve += 1
	#print "TRUES=%s TRUE_POSITIVE=%s"%(str(trues),str(true_positve))
	rounded_recall = true_positve/trues
	return round(rounded_recall,4)
"""precision for fixed train test"""	
def get_precision(predictedf,actualf):
	actual_values = values_of_col(actualf,"OUT","\t")
	predicted_values = values_of_col(predictedf,"OUT","\t")
	true_positve = 0.0
	positive = 0.0
	assert len(actual_values) == len(predicted_values)
	for i in range(0,len(actual_values)):
		if predicted_values[i] == '1':
			positive += 1
			if actual_values[i] == '1':
				true_positve += 1
	rounded_prec = true_positve/positive			
	return round(rounded_prec,4)
def save_result(data,resultf):
	#print "RESULT FILE:%s"%resultf
	header=["train_precision","train_recall","test_precision","test_recall"]
	result_csv=[header,data]
	resultf=open(resultf,"wb")
	writer=csv.writer(resultf)
	writer.writerows(result_csv)				
if __name__ == "__main__":
	print "parsing...evaluatin...scoring"	
	usage = "usage: %prog [options]\n"
	parser = argparse.ArgumentParser(usage)						
	parser.add_argument("-i", "--mosesf",nargs=1,help = "moses binary file")
	parser.add_argument("-d", "--trtstdir",nargs=1,help = "output file")
	parser.add_argument("-c", "--combof",nargs=1,help = "file where combo program is within")	
	args = parser.parse_args()
	if args.mosesf and args.trtstdir and args.combof:
	   trtstdir = os.path.abspath(args.trtstdir[0])
	   mose_resf = os.path.abspath(args.combof[0])
	   mosesf = os.path.abspath(args.mosesf[0])
	   mosesfp_dir = os.path.split(mosesf)[0]
	   combofp_dir = os.path.split(mose_resf)[0]
	   mosesfname = os.path.split(mosesf)[1]
	   mtrainfname = "%s.train_1to1"%(mosesfname)	   
	   mtestfname = "%s.test_1to1"%(mosesfname)
	   combof = os.path.join(combofp_dir,"%s.combo"%(mosesfname))
	   parse_output(mose_resf,combof)
	   mtrain_evalf = os.path.join(mosesfp_dir,mtrainfname+".eval")
	   mtest_evalf = os.path.join(mosesfp_dir,mtestfname+".eval")
	   #start
	   eval_output(os.path.join(trtstdir,mtrainfname),combof,mtrain_evalf)
	   eval_output(os.path.join(trtstdir,mtestfname),combof,mtest_evalf)
	   mtrain_prec = get_precision(mtrain_evalf,os.path.join(trtstdir,mtrainfname))
	   mtrain_rec = get_recall(mtrain_evalf,os.path.join(trtstdir,mtrainfname))
	   mtest_prec = get_precision(mtest_evalf,os.path.join(trtstdir,mtestfname))
	   mtest_rec = get_recall(mtest_evalf,os.path.join(trtstdir,mtestfname))
	   save_result([mtrain_prec,mtrain_rec,mtest_prec,mtest_rec],os.path.join(mosesfp_dir,"results.csv"))	   	
	else:
		parser.print_help()   
	
		
	                     
