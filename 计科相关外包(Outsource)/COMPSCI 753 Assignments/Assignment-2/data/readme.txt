Title:  Bag of Words Data Set

Abstract: This data set contains five text collections in the form of bags-of-words.

-----------------------------------------------------	

Data Set Characteristics: Text
Number of Instances: 8000000
Area: N/A
Attribute Characteristics: Integer
Number of Attributes: 100000
Date Donated: 2008-03-12
Associated Tasks: Clustering
Missing Values? N/A

-----------------------------------------------------		

Source:

David Newman
newman '@' uci.edu
University of California, Irvine

-----------------------------------------------------	

Data Set Information:

For each text collection, D is the number of documents, W is the
number of words in the vocabulary, and N is the total number of words
in the collection (below, NNZ is the number of nonzero counts in the
bag-of-words). After tokenization and removal of stopwords, the
vocabulary of unique words was truncated by only keeping words that
occurred more than ten times. Individual document names (i.e. a
identifier for each docID) are not provided for copyright reasons.

These data sets have no class labels, and for copyright reasons no
filenames or other document-level metadata.  These data sets are ideal
for clustering and topic modeling experiments.

For each text collection we provide docword.*.txt (the bag of words
file in sparse format) and vocab.*.txt (the vocab file).

Enron Emails:
orig source: www.cs.cmu.edu/~enron
D=39861
W=28102
N=6,400,000 (approx)

NIPS full papers:
orig source: books.nips.cc
D=1500
W=12419
N=1,900,000 (approx)

KOS blog entries:
orig source: dailykos.com
D=3430
W=6906
N=467714

NYTimes news articles:
orig source: ldc.upenn.edu
D=300000
W=102660
N=100,000,000 (approx)

PubMed abstracts:
orig source: www.pubmed.gov
D=8200000
W=141043
N=730,000,000 (approx)


-----------------------------------------------------	

Attribute Information:

The format of the docword.*.txt file is 3 header lines, followed by
NNZ triples:
---
D
W
NNZ
docID wordID count
docID wordID count
docID wordID count
docID wordID count
...
docID wordID count
docID wordID count
docID wordID count
---

The format of the vocab.*.txt file is line contains wordID=n.

