# Kian
Kian is the neural network designed to serve Wikidata.

This library in current shape add statements to items based on categories in Wikis (Wikipedia, Wikisource, etc.)

How to run this code for a run on classifying humans based on Persian Wikipedia:

```
   python scripts/initiate_model.py -n faHuman -w fawiki -p P31 -v Q5
   python scripts/train_model.py -n faHuman
   python scripts/evaluate.py -n faHuman #To see AUC and fitness parameters
   python scripts/parser.py -lang:fa -newpages:100 -n faHuman #Requires pywikibot installed
```

Bottlenecks of speed in Kian are:
1. Loading category links from Wikipedia. Since it caches them training different models from one wiki tends to work better
2. Training the model. Since it's an ANN and ANNs are resource consuming to train, this may take a while but depends on Wiki you are working with.

TODOs:
1. Add possible mistakes finder
2. Add system to work with claimless items and add statements


DI:
1. Kian is usable for any kind of training, you can simply inject the training set and get the result:
```
>>> from kian import Kian
>>> bot = Kian(training_set=the_training_set)
>>> bot.train()
>>> bot.theta
```
