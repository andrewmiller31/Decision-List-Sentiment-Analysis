'''
 By Andrew Miller 10/24/2018

 decision-list-test.py

 This program is designed to test a decision list model for movie reviews.
 It takes a generated decision list, reads the features and corresponding 
 values, and assigns a sentiment based on the decision list. 
'''

import sys # used for dealing with arguments
import re # used for regular expressions

sentiments = []
# the decision list from input will be stored here
dList = {}

# this function determines the sentiment of a review
def detSentiment(rev):
  # extract the title and save it as the name
  # n = re.search(r"^(\S+\.txt)",rev)
  # name = n.group(0)
  rev = rev.split()
  name = rev[0]
  rev = rev[1:]
  # list the sentiment decision for each word of the review
  decision = []
  # track words used already so there is no bias from reviews that say the same word
  # many times.
  used = {}
  # used to track bigrams
  lastword = ""
  # for each word in the review...
  for w in rev:
    # if word hasn't already been used
    if w not in used:
      used[w] = 1 # mark as used
      # append the liklihood to the decision list
      if w in dList:
	decision.append(float(dList[w]))
    # if a bigram is available...
    if lastword != "":
      # create the bigram
      lastword += " " + w
      # get the decision, same as above
      if lastword not in used:
	if lastword in dList:
	  decision.append(float(dList[lastword]))
    # this word is now the first word of the next bigram
    lastword = w
  # sort the decisions
  decision = sorted(decision, key=abs, reverse=True)
  # Add all the decisions together with a .9 decay to make sure that
  # the stronger sentiments have more weight
  weightedChoice = decision[0]
  for d in range(1,len(decision)):
    weightedChoice += (.9/d) * decision[d]
  # if the overall choice is above zero, output positve review, otherwise negative
  if weightedChoice > 0:
    print name,1
    return 1 
  else:
    print name,0
    return 0

# processes the dictionary(decision list) from input
def processDict(dl):
  for e in dl:
    # split into array, using spaces as delimiter
    e = e.split()
    k = ""
    # last element of array is sentiment, rest is the feature so add it together
    for w in e[:-1]:
      k += w
    dList[k] = e[-1]
 
# for each review, determine sentiment
def processReviews(revs):
  for r in revs:
    s = detSentiment(r) 

def main():
  # read files
  f = open(sys.argv[1])
  dl = f.read()
  dl = dl.splitlines() # seperate reviews
  f2 = open(sys.argv[2])
  reviews = f2.read()
  reviews = reviews.splitlines() # seperate elements
  processDict(dl) # use input to get decision list
  processReviews(reviews) # process each review

if __name__ == "__main__":
  main()
