import ROOT

#------------------------------------------------------------------------------
# TreeReader class
#------------------------------------------------------------------------------
class TreeReader(object):
    """
    A helper class for reading trees.
    """
    #__________________________________________________________________________
    def __init__(self, tree='myntuple'):
        self.tree_name = tree
        self.chain = ROOT.TChain(self.tree_name)
        self.branches = set()
        self.branches_on = set()
        self.i_entry = -1
        self._cache = dict()
        self.input_files = list()

    #__________________________________________________________________________
    def add_file(self, file_path):
        self.chain.Add(file_path)
        self.input_files.append(file_path)

    #__________________________________________________________________________
    def add_files(self, input_files):
        for input_file in input_files:
            self.add_file(input_file)

    #_________________________________________________________________________
    def clear_cache(self):
        self._cache.clear()

    #__________________________________________________________________________
    def reset_branches(self):
        ## cache the branch names
        self.branches.clear()
        self.branches_on.clear()
        for b in self.chain.GetListOfBranches():
            self.branches.add( b.GetName() )
        ## set branch status off
        self.chain.SetBranchStatus("*", 0)
        ## clear the cache
        self.clear_cache()

    #_________________________________________________________________________
    def get_entries(self):
        return self.chain.GetEntries()

    #_________________________________________________________________________
    def get_entry(self, i_entry):
        self.clear_cache()
        self.i_entry = i_entry
        self.chain.GetEntry(i_entry)

    #_________________________________________________________________________
    def __repr__(self):
        s = "TreeReader(input_files=['%s'])" % ("', '".join(self.input_files))
        return s
    #_________________________________________________________________________
    def __getattr__(self, name):
        """
        This function is called if name is not a normal attribute, it is
        assumed to be the name of a branch in self.chain.  The branches are
        cached after being read the first time to increase performance by
        avoiding reading the chain.  clear_cache() is called before every
        call of chain.GetEntry() in EventLoop.run().
        """
        try:
            return self._cache[name]
        except KeyError:
            if not name in self.branches:
                raise AttributeError("The %s branch does not exist in this tree." % name)
            if not name in self.branches_on:
#                raise AttributeError("The %s branch is not turned-on." % name)
                # on-demand branches
                self.chain.SetBranchStatus(name, 1)
                local_entry = self.chain.LoadTree(self.i_entry)
                self.chain.GetBranch(name).GetEntry(local_entry)
                self.branches_on.add(name)
            val = getattr(self.chain, name)
            self._cache[name] = val
            return val

    #_________________________________________________________________________
    def build_var_proxies(self, prefix, n):
        """
        A function that builds a list of n VarProxys for a TTree/TChain chain.
        The chain is assumed to have a set of branches of type array or
        std::vector<T>, each of length n, and having names with a common prefix.

        Example:

        Given a tree with the following branches

            int                 el_n;
            std::vector<float>  el_pt;       
            std::vector<float>  el_eta;
            std::vector<float>  el_phi;

        One could could build VarProxys for each of the electrons and treat
        them like objects by:

            electrons = pyframe.core.build_var_proxies(tree, tree.el_n, 'el_')
            print 'el_n =', tree.el_n
            for el in electrons:
                print '  pt, eta, phi =', el.pt, el.eta, el.phi
        """
        return [ VarProxy(self, i, prefix) for i in xrange(n) ]


#-----------------------------------------------------------------------------
class VarProxy(object):
    """
    This is where the money is.
    """
    #_________________________________________________________________________
    def __init__(self, tree_proxy, index, prefix=""):
        self.tree_proxy = tree_proxy
        self.index = index
        self.prefix = prefix
    #_________________________________________________________________________
    def __getattribute__(self, name):
        prefix_and_name = object.__getattribute__(self, "prefix") + name
        tree_proxy =  object.__getattribute__(self, "tree_proxy")
        if prefix_and_name in tree_proxy.branches:
            index = object.__getattribute__(self, "index")
            try:
                return getattr(tree_proxy, prefix_and_name)[index]
            except:
                log.error("Failed to read tree_proxy, prefix_and_name = %s, index = %s" % (prefix_and_name, index))
                log.error("  in TChain.GetCurrentFile().GetName() = %s" % tree_proxy.chain.GetCurrentFile().GetName() )
                log.error("  in RunNumber=%i  EventNumber=%i" % (tree_proxy.RunNumber, tree_proxy.EventNumber) )
                log.error("  exiting program...")
                sys.exit()
        return object.__getattribute__(self, name)


