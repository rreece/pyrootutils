import array

import ROOT
import rootutils

#------------------------------------------------------------------------------
# TreeWriter class
#------------------------------------------------------------------------------
class TreeWriter(object):
    """
    A helper class for writing trees.
    """
    #__________________________________________________________________________
    def __init__(self, tfile='myntuple.root', tree='myntuple'):
        self._tfile_name = tfile
        self._tree_name = tree
        self._tfile = ROOT.TFile.Open(tfile, 'RECREATE')
        self._tree = ROOT.TTree(tree, tree)
        self._n_events = 0 
        self._branch_contents = dict()
        self._branch_types    = dict()

    #__________________________________________________________________________
    def fill(self, event):
        if self._n_events == 0:
            self.initialize_branches(event)
        else:
            self.update_branches(event)
        assert len(self._branch_contents) > 0
        assert len(self._branch_types) == len(self._branch_contents)
        self._tree.Fill()
        self._n_events += 1

    #__________________________________________________________________________
    def initialize_branches(self, event):
        for key, val in event.iteritems():
            branch_type, branch_data = val
            branch_content = self.convert_branch_content(branch_data, branch_type)

            ## cache branch info (keeping these contents/arrays persisently)
            self._branch_types[key] = branch_type
            self._branch_contents[key] = branch_content

            ## add new branch to the tree
            # ints, floats
            if branch_type in ('I', 'F'):
                # construct TLeaf name (eg. "RunNumber/I")
                leafname = '%s/%s' % (key, branch_type)
                self._tree.Branch(key, branch_content, leafname)
            # vectors
            else:
                self._tree.Branch(key, branch_content)

    #__________________________________________________________________________
    def update_branches(self, event):
        for key, val in event.iteritems():
            branch_type, branch_data = val
            branch_content = self.convert_branch_content(branch_data, branch_type)

            assert self._branch_types[key] == branch_type

            if branch_type in ('I', 'F'):
                self._branch_contents[key][0] = branch_content[0]
            else:
                vec = self._branch_contents[key]
                vec.clear()
                for x in branch_content:
                    vec.push_back(x)
            
    #__________________________________________________________________________
    def convert_branch_content(self, branch_data, branch_type):
        branch_content = None
        if branch_type == 'I':
            branch_content = array.array('i', [branch_data])
        elif branch_type == 'F':
            branch_content = array.array('f', [branch_data])
        else:
            branch_content = rootutils.rootify(branch_data, branch_type)
        assert not branch_content is None
        return branch_content

    #__________________________________________________________________________
    def close(self):
        self._tree.GetCurrentFile().Write()
        self._tree.GetCurrentFile().Close()


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
