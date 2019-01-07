# Decision-List-Sentiment-Analysis

A decision list approach for binary classification of sentiment analysis. From a list of texts with an attached binary classification,
the program is able to learn it's features in a decision list and classify new data. I trained the classifier on a little over 1000 movie
reviews, each marked either 0 for a negative review or 1 for a positive. On a test set of 200 reviews, the decision list achieved an 
accuracy of 80%. 

## Data Format
Here is how the data needs to be formatted, I also included the dataset I used for an example.

#### Training data, each on a single line
file_name classification(0/1) text

Ex)
review_001.txt 0 This movie is so bad, I would not recommend it to anyone!

#### Testing data, each on a single line
file_name text

Ex)
review_578.txt This movie wasn't really what I expected, but I think I rather enjoyed it.

#### Gold standard, each on its own line and in same order as test data
file_name classification

Ex)
review_578.txt 1

## How to run:

__decision-list-train.py__

Generates a decision list. The program prints the list so you'll want to redirect the output to a file. The resulting list is human
readable so it may by interesting for some to check it out. 

*python decision-list-train.py training-data.txt > list.txt*

__decision-list-test.py__

Tests the decision list generated above. Again, redirect the output.

*python decision-list.test.py list.txt test-data.txt > answers.txt*

__decision-list-eval.py__

Checks the answers against the gold standards and generates a confusion matrix.

*python decision-list-eval.py answers.txt gold-standard.txt*





