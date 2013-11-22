import os
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
result_files=[]
precision_train=[]
precision_test=[]
recall_train=[]
recall_test=[]
def read_all_files(path):
   print path
   for dir_entry in os.listdir(path):
       #print dir_entry
       dir_entry_path=os.path.join(path,dir_entry)
       if os.path.isfile(dir_entry_path):
          result_files.append(dir_entry_path)
def set_trts():
	for results in result_files:
		#print results
		f=open(results,'r')
		result_arr=[]
		read=csv.reader(f)
		for row in read:
			#print row
			result_arr.append(row)
		pr_tr_index=result_arr[0].index("train_precision")
		pr_ts_index=result_arr[0].index("test_precision")
		rec_tr_index=result_arr[0].index("train_recall")
		rec_ts_index=result_arr[0].index("test_recall")
		#print "pr_tr"+result_arr[1][pr_tr_index]
		if result_arr[1][pr_ts_index]:
			precision_train.append(float(result_arr[1][pr_tr_index]))
		#print "pr_ts"+result_arr[1][pr_ts_index]
		if result_arr[1][pr_ts_index]:
			precision_test.append(float(result_arr[1][pr_ts_index]))
		if result_arr[1][rec_tr_index]:
			recall_train.append(float(result_arr[1][rec_tr_index]))
		if result_arr[1][rec_ts_index]:
			recall_test.append(float(result_arr[1][rec_ts_index]))
def plot(data,legend_dict):
   print "DEBUG@plot() data length=%d"%len(data)
   for val in data:
	   print val
   xlabel = legend_dict['xlabel'] if 'xlabel' in legend_dict else ""
   ylabel = legend_dict['ylabel'] if 'ylabel' in legend_dict else ""
   title  = legend_dict['title'] if 'title' in legend_dict   else "" 
   #plt.bar(range(0,len(data)),data)
   plt.hist(data,bins=25) 
   plt.title(title)
   plt.xlabel(xlabel)
   plt.ylabel(ylabel)
   plt.show()
def plot_xy(x,y,legend_dict):
	xlabel = legend_dict['xlabel'] if 'xlabel' in legend_dict else ""
	ylabel = legend_dict['ylabel'] if 'ylabel' in legend_dict else ""
	title  = legend_dict['title'] if 'title' in legend_dict   else ""
	area = np.pi * (10* np.random.rand(150))**2
	plt.scatter(x,y,s=[45],alpha=0.5)
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.show()
def main():
   path=sys.argv[1]   
   read_all_files(path)
   set_trts()
   #plot(recall_test,{'xlabel':'precision','ylabel':'frequency','title':'recall on test'})
   plot_xy(precision_test,recall_test,{'xlabel':'precision on test','ylabel':'recall on test','title':'precisoin on test vs recall on test'})
   plot_xy(precision_train,recall_train,{'xlabel':'precision on train','ylabel':'recall on train','title':'precisoin on train vs recall on train'})
   print "trains:%s and tests:%s" %(str(len(precision_train)),str(len(precision_test)))
if __name__=="__main__":
     main()       	
