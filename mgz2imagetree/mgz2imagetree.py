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

         # Directory and filenames
        self.str_workingDir             = ''
        self.str_inputDir               = ''
        self.str_inputFile              = ''
        self.str_extension              = 'mgz'
        self.str_outputFileStem         = ''
        self.str_ouptutDir              = ''
        self.str_outputLeafDir          = ''
        self.maxDepth                   = -1

        # pftree dictionary
        self.pf_tree                    = None
        self.numThreads                 = 1

        self.str_stdout                 = ''
        self.str_stderr                 = ''
        self.exitCode                   = 0

    def filelist_prune(self, at_data, *args, **kwargs):
        """
        Given a list of files, possibly prune list by 
        extension.
        """

        b_status    = True
        l_file      = []
        str_path    = at_data[0]
        al_file     = at_data[1]
        if len(self.str_extension):
            al_file = [x for x in al_file if self.str_extension in x]

        if len(al_file):
            al_file.sort()
            l_file      = al_file
            b_status    = True
        else:
            self.dp.qprint( "No valid files to analyze found in path %s!" % str_path, 
                            comms = 'error', level = 3)
            l_file      = None
            b_status    = False
        return {
            'status':   b_status,
            'l_file':   l_file
        }

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