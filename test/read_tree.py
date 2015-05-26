#!/usr/bin/env python
"""
NAME
    name.py - short description

SYNOPSIS
    Put synposis here.

DESCRIPTION
    Put description here.

OPTIONS
    -h, --help
        Prints this manual and exits.
        
    -n VAL
        Blah blah.

AUTHOR
    Ryan Reece  <ryan.reece@cern.ch>

COPYRIGHT
    Copyright 2010 Ryan Reece
    License: GPL <http://www.gnu.org/licenses/gpl.html>

SEE ALSO
    ROOT <http://root.cern.ch>

TO DO
    - One.
    - Two.

2011-06-15
"""

#------------------------------------------------------------------------------
# imports
#------------------------------------------------------------------------------

## std
import argparse, sys, time

## ROOT
import ROOT
ROOT.gROOT.SetBatch(True)

## my modules
import pyrootutils


#------------------------------------------------------------------------------
# globals
#------------------------------------------------------------------------------
timestamp = time.strftime('%Y-%m-%d-%Hh%M')
GeV = 1000.


#------------------------------------------------------------------------------
# options
#------------------------------------------------------------------------------
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile',  default=None,
            help='A positional argument.')
#    parser.add_argument('-x', '--option',  default=False,  action='store_true',
#            help="Some toggle option.")
#    parser.add_argument('-i', '--input',  default=None,
#            help="Path to directory of datasets")
#    parser.add_argument('-o', '--output',  default='out.txt',
#            help="Name of output file.")   
    ops = parser.parse_args()
    assert ops.infile
    return ops


#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------
def main():
    ops = options()

    print 'Helloworld.  The time is %s.' % timestamp

    ## open file and get the tree
    infile = ops.infile
    tfile = ROOT.TFile.Open(infile)
    tree_name = 'myntuple'
    tree = tfile.Get(tree_name)

    n_entries = tree.GetEntries()
    print 'This tree has %i events.' % n_entries

    ## make a HistManager
    hm = pyrootutils.HistManager()

    for i_entry in xrange(n_entries):
        tree.GetEntry(i_entry)
        # event-by-event code goes here

        weight = 1.0

        hm.hist('h_w', "ROOT.TH1F('$', ';w;Events', 20, -2.0, 3.0)").Fill(tree.w, weight)
        hm.hist('h_n', "ROOT.TH1F('$', ';n;Events', 20, -0.5, 19.5)").Fill(tree.n, weight)

    hm.write_hists('output.hists.root')

    print 'Done.'


#------------------------------------------------------------------------------
# free functions
#------------------------------------------------------------------------------

#______________________________________________________________________________
def fatal(message=''):
    sys.exit("Fatal error in %s: %s" % (__file__, message))


#______________________________________________________________________________
def tprint(s, log=None):
    line = '[%s] %s' % (time.strftime('%Y-%m-%d:%H:%M:%S'), s)
    print line
    if log:
        log.write(line + '\n')
        log.flush()


#------------------------------------------------------------------------------
if __name__ == '__main__': main()

# EOF
