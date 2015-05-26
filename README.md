# pyrootutils

A set of useful tools for taming pyroot.

-   author: Ryan Reece <ryan.reece@cern.ch>
-   created: May 26, 2015


## Requirements

-   Python
-   ROOT


## Getting started

Check out `pyrootutils` and setup:

    git clone https://github.com/rreece/pyrootutils.git
    cd pyrootutils
    source setup.sh

In the test directory, there are some example scripts.

    cd test

Run this first script which makes a tree:

    python write_tree.py 

And then you should be able to run the next script to read the tree and make some histograms:

    python read_tree.py myntuple.root 


