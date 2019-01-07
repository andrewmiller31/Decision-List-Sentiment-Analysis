'''
 By Andrew Miller 10/24/2018

 decision-list-eval.py

 This is a program that evaluates the performance of a decision list.
 It compares a list of given results with a list of gold standard to 
 find the True Positive, True Negative, False Positive, and False
 Negative rates.
'''

import sys # used for dealing with arguments
import re # used for regular expressions
 
# this function finds the results 
def results(gold,pred):
  # counts for all the important values
  correct = 0
  tp = 0
  fp = 0
  tn = 0
  fn = 0 
  # for each review, compare the sentiment
  for e in range(0,len(gold)):
    # if they're the same,it's correct so it's either tp or tn
    if gold[e] == pred[e]:
      correct += 1
      # if end of line is 1, then it's tp , else tn
      if int(gold[e][-1]) == 1:
	tp += 1
      else:
	tn += 1
    else:
      # if they do not match, it's either fp or fn
      if int(gold[e][-1]) == 1: # fp
        fp += 1
      else: # fn
	fn += 1
  # print results
  print "total correct:",correct,"of 200"
  print "Confusion Matrix:\n"
  print "TP | FP"
  print "-------"
  print "FN | TN\n"
  print tp,"|",fp
  print "-------"
  print fn,"|",tn,"\n"

def main():
  # read files
  f = open(sys.argv[1])
  gold = f.read()
  gold = gold.splitlines() # seperate gold standards
  f2 = open(sys.argv[2])
  pred = f2.read()
  pred = pred.splitlines() # seperate predictions

  results(gold,pred) # evaluate
    

if __name__ == "__main__":
  main()
