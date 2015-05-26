# pyrootutils

A set of useful tools for taming pyroot.

## Getting started

If you have python and root setup ok, you should be able to source the setup script in this directory:

    source setup.sh

In the test directory, there are some example scripts.

    cd test

Run this first script which makes a tree:

    python write_tree.py 

And then you should be able to run the next script to read the tree and make some histograms:

    python read_tree.py myntuple.root 

