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

        