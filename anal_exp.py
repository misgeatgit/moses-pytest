import os
import pandas
import csv
import argparse
EVAL_TABLE_PATH="/home/addis-ai/opencog_ocpkg/opencog/build/opencog/comboreduct/main/eval-table"
"""Extract the combo programs from a given moses output file
   params
    moses output file,combo file to be saved
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
def values_of_col(csvf,col_name):
	col_values=[]
	with open(csvf,'rb') as f:
		reader=csv.reader(f)
		next(reader) # escape the first line
		for row in reader:
			col_values.append(row[len(row)-1])
	return col_values	
"""recall for fixed train test"""						
def get_recall(predictedf,actualf):
	actual_values = values_of_col(actualf,"OUT")
	predicted_values = values_of_col(predictedf,"OUT")
	true_positve=0
	trues=0
	assert len(actual_values) == len(predicted_values)
	for i in range(0,len(actual_values)):
		if actual_values[i] == '1':
			trues += 1
			if predicted_values[i] == '1':
				true_positve += '1'
	return true_positve/trues	
"""precision for fixed train test"""	
def get_precision(predictedf,actualf):
	actual_values = values_of_col(actualf,"OUT")
	predicted_values = values_of_col(predictedf,"OUT")
	true_positve=0
	positive=0
	assert len(actual_values) == len(predicted_values)
	for i in range(0,len(actual_values)):
		if predicted_values[i] == '1':
			positive += 1
			if actual_values[i] == '1':
				true_positve += 1
	return true_positve/positive
def save_result(data,resultf):
	header=["train_precision","train_recall","test_precision","test_recall"]
	result_csv=[header,data]
	resultf=open(resultf,"wb")
	writer=csv.writer(resultf)
	writer.writerows(result_csv)				
if __name__ == "__main__":
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
	   #check from here
	   eval_output(os.path.join(trtstdir,mtrainfname),combof,mtrain_evalf)
	   eval_output(os.path.join(trtstdir,mtestfname),combof,mtest_evalf)
	   mtrain_prec = get_precision(mtrain_evalf,os.path.join(trtstdir,mtrainfname))
	   mtrain_rec = get_recall(mtrain_evalf,os.path.join(trtstdir,mtrainfname))
	   mtest_prec = get_precision(mtest_evalf,os.path.join(trtstdir,mtestfname))
	   mtest_rec = get_recall(mtest_evalf,os.path.join(trtstdir,mtestfname))
	   save_result([mtrain_prec,mtrain_rec,mtest_prec,mtest_rec],os.path.join(os.path.split(mosesfp_dir)[0],"results.csv"))	   	
	else:
		parser.print_help()   
	print "main"
	dir="/media/MISGE@2AI/fixed-mp-analysis"
	dir2="/home/addis-ai/Desktop/mp/fixed-mp-analysis"
	#parse_output(dir2+"/data/output.combo","/home/addis-ai/Desktop/mp/fixed-mp-analysis/data/onlycombo.combo")
	#print values_of_col(dir+"/data/eval.csv","OUT")
	#data=[0.1,0.3,0.4,0.5]
	#dir_save="/home/addis-ai/Desktop/result.csv"
	#save_result(data,dir_save)
		
	                     
