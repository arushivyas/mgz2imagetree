#System imports
import os, sys

# Project specific imports
import      pfmisc
from        pfmisc._colors      import  Colors
from        pfmisc              import  other
from        pfmisc              import  error
import argparse
import pftree

class mgz2imagetree():
    """ 
    A class based on 'pftree' structure that walks through the inputdir, 
    and filters mgz volumes for each subject into its constituent labels as indivdual directories 
    and stores them in an outputdir structure similar to the inputdir.

    """

    def declare_selfvars(self):
        """
        A block to declare self variables
        """

        #
        # Object desc block
        #
        self.str_desc                   = ''
        self.__name__                   = "pfdicom_tagExtract"
        self.str_version                = "2.2.20"

        # pftree dictionary
        self.pf_tree                    = None

    def inputReadCallback(self, *args, **kwargs):
        """

        Callback for reading files from specific directory.

        In the context of mgz2imagetree, this implies reading
        files from each target directory and returning 
        the mgz data set of each subject.

        """
    
    def inputAnalyzeCallback(self, *args, **kwargs):
        """
        Callback for doing actual work on the read data.

        In the context of mgz2imagetree, this implies running the 
        mgz2imgslices utility on each subject's mgz files and creating the 
        required output files.

        **The 'data' component passed to this method is the 
        dictionary returned by the inputReadCallback()
        method.**

        """

    def outputSaveCallback(self, at_data, **kwargs):
        """

        Callback for saving outputs.

        In order to be thread-safe, all directory/file 
        descriptors must be *absolute* and no chdir()'s
        must ever be called!

        The input 'data' is the return dictionary from the
        inputAnalyzeCallback method.

        """

    def create_imagetree(self, **kwargs):
        """
        A simple "alias" for calling the pftree method.
        """
        d_create_imagetree    = {}
        d_create_imagetree    = self.pf_tree.tree_process(
                                inputReadCallback       = self.inputReadCallback,
                                analysisCallback        = self.inputAnalyzeCallback,
                                outputWriteCallback     = self.outputSaveCallback,
                                persistAnalysisResults  = False
        )
        return d_create_imagetree