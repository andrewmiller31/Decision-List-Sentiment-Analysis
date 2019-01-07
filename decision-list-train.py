'''
 By Andrew Miller 
 10/24/2018

 decision-list-train.py

 This is a program that generates a decision list based on movie reviews(or any
 other textual data that has binary classifications). A decision list is a 
 sorted list of features that have attached an list of log liklihoods which are
 used to determined the sentiment of a given word. In this case, the features
 consist of either unigrams(one word) or bigrams(two words) and the sentiments 
 are either positive or negative. To normalize biased data, the ratio of 
 negative log liklihoods to positive are taken into account. Also the threshold
 at which the sentiment is positive or negative is also normalized to 0. 
 So if a feature has a value above 0, it is determined to be positive and if 
 it's below 0 then it's negative.
'''

import sys # used for dealing with arguments
import re # used for regular expressions
import math # used for log

# dictionary of form {feature : weight}
# If postive weight, it will classify postive review
# If negative weight, classify negative review
weights = {}
# the following counts are used for calculating the log liklihood
# they use the same keys as above but the values are the respective counts
countPos = {}
countNeg = {}
# tracks the reviews that have already been handled
# I added this for convenience for when I find a threshold later on
scannedRevs = []

# this function calculates the log liklihood of a word based on the data encountered so far
def calcProb(w,pos):
  # check whether the feature has been encounterd
  if w in weights:
    # if its a positive review, add the feature to the positive dictionary
    if pos == True:
      countPos[w] += 1
    # otherwise it's a negative review
    else:
      countNeg[w] += 1
  # if the feature has already been encountered:
  else:
    # if positive review, set the count to one for pos and 0 for neg
    if pos == True:
      countPos[w] = 1
      countNeg[w] = 0
    # otherwise do opposite for negative reviews
    else:
      countPos[w] = 0
      countNeg[w] = 1
  
  # +1 smoothing if there is a count of zero, to avoid dividing by 0 
  if countNeg[w] == 0 or countPos[w] == 0:
    countNeg[w] += 1
    countPos[w] += 1
    
  # here we calculat the log liklihood
  count = float(countPos[w] + countNeg[w]) # total uses of this feature
  p1 = float(countPos[w])/count # p(positive|feature)
  p2 = float(countNeg[w])/count # p(negative|feature)
  # getting the log liklihoods
  lg1 = math.log(p1/p2) 
  lg2 = math.log(p2/p1)
  # choosing the one thats higher to assign to the word
  weights[w] = lg1 if lg1 > lg2 else (-1*lg2)
      
# Scans a review and adds to the weigths of the unigram dictionary
# If pos is true: +1 weight
# If pos is false: -1 weight 
def calcWeights(pos,words):
  # add to the scanned reviews for later use
  scannedRevs.append((pos,words))
  # lastword - used for bigrams
  lastword = ""
  # keeps track of what has been used; I had better results using each type in a review only one time
  used = {}
  for w in words:
    # if we haven't encountered this word yet, add it to the weights and mark that we used it now
    if w not in used:
      calcProb(w,pos)
      used[w] = 1
    # if bigram is available...
    if lastword != "":
      # create bigram by adding current word to previous
      lastword += " " + w
      # same procedure as above for adding to weights dictionary
      if lastword not in used:
        calcProb(lastword,pos)
        used[lastword] = 1
    # current word is now the last word
    lastword = w

# used for normalizing descrepancies between positive and negetive reviews
def normalize():
  nw = 0
  pw = 0
  # collect totals for all negative and positive words
  for k in weights:
    if weights[k] > 0:
      pw += weights[k]
    else:
      nw += weights[k]
  # get the negative/positve ratio
  r = abs(nw) / pw 
  
  # I used a slight modifier to avoid adding too much of an impact
  # We are normalizing the positive features so if the n/p ratio is above 1,
  # we want to remove weight from the positive features. If it is below 1,
  # then weight needs to be added positive features
  mod = .95 
  if r < 1:
     mod = 1.05
  # normalize the positve features with the modifier determined above
  for k in weights:
    if weights[k] > 0:
      weights[k] *= (mod*r)

# This function determines the threshold at which a review is negative or positive,
# and then normalizes the threshold to 0
def threshold():
  # In order: count of positive reviews, positive avereage score, negative count, negative average
  posCount = 0
  posAv = 0 
  negCount = 0
  negAv = 0
  # Lists that keep track of the highest scoring words for each review
  pos = []
  negs = []
  # for each of the reviews that have been processed...
  # scannedRevs is a touple of the form (sentiment,review)
  for r in scannedRevs:
    # track words already encountered
    used = {}
    # tracks highest scoring word for each review
    score = 0 
    # for each of the words check if it's the best score yet
    for w in r[1]:
      if w not in used:
        if abs(weights[w]) > score:
          score = weights[w]
        used[w] = 1
    # if its a positive reviews, add the score to positive list and add to count
    if r[0] == True:
      posCount += 1
      if score > posAv:
        pos.append(score)
    # same for negative
    else:
      negCount += 1
      if score < negAv:
        negs.append(score)
  # sort the list of positive/negative scores
  pos = sorted(pos,reverse=True)
  negs = sorted(negs,reverse=True,key=abs)
  # average the top 50 for each
  posAv = sum(pos[:50]) / 50
  negAv = sum(negs[:50]) / 50
  # the threshold is the average between the two averages 
  threshold = (posAv+negAv)/(posCount+negCount)
  # before normalizing the threshold to zero, normalize the bias 
  normalize()
  # subtract threshold from each feature so it's now 0
  for k in weights:
    weights[k] -= threshold

# seperates the reviews, extracts vital info
# forwards the information to the weights function
def processReviews(revs):
  # seperate reviews
  revs = revs.splitlines()
  # positive and negative counts
  pc = 0
  nc = 0
  # on each review, extract sentiment, calculate the feature log liklihoods
  for r in revs:
    r = r.split()
    pos = True if int(r[1]) == 1 else False 
    calcWeights(pos,r[2:])
    if pos == True:
      pc += 1
    else:
      nc += 1
  # after all reviews are processed, find the threshold and adjust accordingly
  threshold()
  # sort the dictionary so the highest log liklihood are on top, then print them
  suWeights = sorted(weights, key=lambda k: abs(weights[k]),reverse=True)  
  for w in suWeights:
    print w,weights[w]

def main():
  # read file
  f = open(sys.argv[1])
  reviews = f.read()
  processReviews(reviews)  

if __name__ == "__main__":
  main()
