import os
import ROOT
import fileutils

#------------------------------------------------------------------------------
# HistManager class
#------------------------------------------------------------------------------
class HistManager(object):
    """
    A helper class for writing trees.
    """
    #__________________________________________________________________________
    def __init__(self):
        self._hists = dict()

    #__________________________________________________________________________
    def hist(self, name, decl, dir=''):

        if dir:
            name = os.path.join(dir, name)

        if not self._hists.has_key(name):

            # So that the temporary objects would be
            # created in a general memory space.
            ROOT.gROOT.cd()
                           
            # create new
            if decl.count("$"):
                decl = decl.replace("$", os.path.basename(name))
            h = eval(decl)
            assert h
    
            # set to be memory-resident
            h.SetDirectory(0)
    
            # calculate the statistical uncertainties correctly for
            # weighted histograms:
            if isinstance(h, ROOT.TH1):
                h.Sumw2()
    
            self._hists[name] = h
     
        return self._hists[name]

    #__________________________________________________________________________
    def write_hists(self, outfile):
        print 'Writing histograms.'
        root_file = ROOT.TFile(outfile, "RECREATE") # "UPDATE")
        root_file.cd()
        for key, h in self._hists.iteritems():
            if isinstance(h, ROOT.TObject):
                h.SetName(os.path.basename(key))  # HACK to remove ";*" e.g. h_n_events;1
                fileutils.write(h, outfile, os.path.dirname(key))
        root_file.Close()


