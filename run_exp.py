
import ConfigParser
import subprocess
import argparse
from os import path
import os


MOSES_PATH="/home/addis-ai/opencog_ocpkg/opencog/build/opencog/learning/moses/main/moses"
#general program options
MGPO=" -u OUT -l debug -V 1 -W 1 -x 1 -t 1 -r 1 "
#learning program options
MLPO=""
#feature selection program options
MFSPO=" --enable-fs 1 "
#message
message=""
"""loads parameter setting of moses
   params
   mfile - file to be analyzed by moses
   cfile - moses param config file
   lfile - the file name that moses should put the log
   ofile - the name of the output file that moses should name"""
def load_configuration(cfile,mfile,lfile,ofile):
	global moses_args,message,MGPO,MLPO,MFSPO
	config = ConfigParser.ConfigParser()
	config.read(cfile)
	#general
	candidates=config.get('general params','candidates')
	#print "DEBUG input="+mfile
	MGPO += " -i %s -o %s -f %s "%(mfile,ofile,lfile)
	MGPO += " --result-count %s"%(candidates)
	#learning options
	evals = config.get('learning params','evals')
	noise = config.get('learning params','noise')
	ctemp = config.get('learning params','ctemp')
	hardness = config.get('learning params','hardness')
	recall_min = config.get('learning params','recall_min')	
	revisit = config.get('learning params','revisit')	
	complexity_ratio = config.get('learning params','complexity_ratio')
	perm_ratio = config.get('learning params','perm_ratio')
	scorer = config.get('learning params','scorer')
	MLPO += "-H %s "%(scorer)
	MLPO += " --hc-allow-resize-deme 0 "
	MLPO += " -m %s "%(evals)
	#MLPO += " -p %s "%(noise)  #similar with complexity ratio
	MLPO += " -v %s "%(ctemp)
	MLPO += " --alpha %s "%(hardness)
	MLPO += " -q %s"%(recall_min)
	MLPO += " --logical-perm-ratio %s "%(perm_ratio)
	MLPO += " --revisit %s"%(revisit)	
	MLPO += " --complexity-ratio %s "%(complexity_ratio)	
	#diversity
	dpressure = config.get('diversity pressure','dpressure')
	dexp = config.get('diversity pressure','dexp')
	dst = config.get('diversity pressure','dst')
	MLPO += " --diversity-pressure %s "%(dpressure)
	MLPO += " --diversity-exponent %s "%(dexp)
	MLPO += " --diversity-dst %s "%(dst)		
	#feature selection
	breadth_first = config.get('feature selection with MOSES param','breadth_first')
	prune = config.get('feature selection with MOSES param','prune')
	smp_pbty = config.get('feature selection with MOSES param','smp_pbty_seq')
	seed = config.get('feature selection with MOSES param','seed_seq')
	focus = config.get('feature selection with MOSES param','focus_seq')
	fsm_nfeats = config.get('feature selection with MOSES param','fsm_nfeats_seq')
	pre_min_activation = config.get('feature selection with MOSES param','pre_min_activation')
	pre_penalty = config.get('feature selection with MOSES param','pre_penalty')
	fsm_scorer = config.get('feature selection with MOSES param','fsm_scorer_seq')
	hc_crossover_pop_size = config.get('feature selection with MOSES param','hc_crossover_pop_size')
	hc_crossover = config.get('feature selection with MOSES param','hc_crossover')
	hc_widen_search = config.get('feature selection with MOSES param','hc_widen_search')
	fsm_conf = config.get('feature selection with MOSES param','fsm_conf_seq')
	hc_evals = config.get('feature selection with MOSES param','hc_evals')
	inc_red_intensity = config.get('feature selection with MOSES param','inc_red_intensity')
	smd_threshold = config.get('feature selection with MOSES param','smd_threshold')
	fsm_algo = config.get('feature selection with MOSES param','fsm_algo')
	#set
	message="~~~~ Learning (feature selection"
	if fsm_algo == "hc":
		message += "fsm_conf ="+fsm_conf
	else:
		message += " fsm_nfeats="+fsm_nfeats	
	message += " focus = %s, seed = %s, smp_pbty = %s, fsm_algo = %s, fsm_scorer = %s ~~~~" %(focus,seed,smp_pbty,fsm_algo,fsm_scorer)
	#algo
	if fsm_algo == "smd":
		MFSPO += " --fs-threshold %s "%(smd_threshold)
	elif fsm_algo == "inc":
		MFSPO+=" --fs-inc-redundant-intensity %s "%(inc_red_intensity)
	elif fsm_algo=="hc":
		MFSPO += " --fs-hc-max-evals %s "%(hc_evals)
		MFSPO += " --fs-mi-penalty %s "%(fsm_conf)
		MFSPO += " --fs-hc-widen-search %s "%(hc_widen_search)
		MFSPO += " --fs-hc-crossover %s "%(hc_crossover)
		MFSPO += " --fs-hc-crossover-pop-size %s "%(hc_crossover_pop_size)			
	MFSPO+=" --fs-scorer %s"%(fsm_scorer)
	#scorer
	if scorer == "pre":
		MFSPO += " --fs-pre-penalty %s"%(pre_penalty)
		MFSPO += " --fs-pre-min-activation %s "%(pre_min_activation)
	MFSPO += " --fs-target-size %s "%(fsm_nfeats)
	# focus
	MFSPO += " --fs-focus %s "%(focus)
	# seed
	MFSPO += " --fs-seed %s "%(seed)
	# Subsampling
	MFSPO += " --fs-subsampling-pbty %s "%(smp_pbty)
	# Prune exemplar
	MFSPO += " --fs-prune-exemplar %s "%(prune)
	# Number of demes for breadth-first search
	MFSPO += " --fs-demes %s "%(breadth_first)								                                 
def run_moses(moses_path,margs):
	#print "DEBUG CMD="+moses_path+margs	
	result = os.system(moses_path+" "+margs) #subprocess.call([moses_path,margs])	     
	if result!=0:
		print "error while executing"
		exit(0)     
if  __name__ == "__main__":
	usage = "usage: %prog [options]\n"
	parser = argparse.ArgumentParser(usage)						
	parser.add_argument("-i", "--ifile",nargs=1,help = "Input file")
	parser.add_argument("-o", "--ofile",nargs=1,help = "output file")
	parser.add_argument("-f", "--lfile",nargs=1,help = "log file")
	parser.add_argument("-c", "--cfile",nargs=1,help = "conf file")
	args = parser.parse_args()
	if args.ifile and args.ofile and args.lfile and args.cfile:
	   load_configuration(path.abspath(args.cfile[0]),path.abspath(args.ifile[0]),path.abspath(args.lfile[0]),path.abspath(args.ofile[0]))
	   margs = "%s %s %s "%(MGPO,MLPO,MFSPO)
	   print margs
	   run_moses(MOSES_PATH,margs)
	  
	else:
	   parser.print_help()
			
		
