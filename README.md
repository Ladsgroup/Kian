# Kian
Kian is the neural network designed to serve Wikidata.

First TODO: Write a wrapper for Kian

The main file is kian3.py which is the core of ANN, other codes are just parsers and don't matter

How to run this code for a run on classifying humans:

1. Write a file named Human.txt and put Q# of humans in it. Do the same for NotHuman.txt
2. Run these commands:

```
   sql dewiki <kian.sql> en_kian.txt
   sql dewiki <kian2.sql> en_kian2.txt
   sql dewiki <kian3.sql> en_kian4.txt  #Historical reasons
   python kian1.py
   python kian4.py
   python kian5.py
   python kian3.py
   python kian7.py
   python p31.py #Optional, uses pywikibot compat.
```
