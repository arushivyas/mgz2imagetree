#System imports
import os, sys

# Project specific imports
import      nibabel             as nib
import      pfmisc
from        pfmisc._colors      import  Colors
from        pfmisc.debug        import  debug
from        pfmisc              import  other
from        pfmisc              import  error
from        mgz2imgslices       import mgz2imgslices
import argparse
import pftree
import time


class mgz2imagetree(object):
    """ 
    A class based on 'pftree' structure that walks through the inputdir, 
    and filters mgz volumes for each subject into its constituent labels as indivdual directories 
    and stores them in an outputdir structure similar to the inputdir.

    """

    def __init__(self, **kwargs):
        """
        A block to declare self variables
        """

        #
        # Object desc block
        #
        self.str_desc                   = ''
        self.__name__                   = "mgz2imagetree"
        self.str_version                = "1.0.0"
        self.verbosity                  = 1
        self.dp                         = pfmisc.debug(
                                            verbosity   = self.verbosity,
                                            within      = self.__name__
                                            )

         # Directory and filenames
        self.str_workingDir             = ''
        self.str_outputLeafDir          = ''
        self.str_extension              = 'mgz'
        self.str_inputDir               = ''
        self.str_inputFile              = ''
        self.str_outputFileStem         = ''
        self.str_outputDir              = ''
        self.str_outputFileType         = ''        
        self.str_label                  = 'label'
        self.str_feature                = ''
        self.str_image                  = ''
        self.b_normalize                = False
        self.str_lookuptable            = '__val__'
        self.str_skipLabelValueList     = ''
        self.str_filterLabelValueList   = ''
        self.str_wholeVolume            = ''
        self.maxDepth                   = -1

        # pftree dictionary
        self.pf_tree                    = None
        self.numThreads                 = 1
        self.b_followLinks              = False

        self.str_stdout                 = ''
        self.str_stderr                 = ''
        self.exitCode                   = 0

        for key, value in kwargs.items():
            if key == "inputFile":              self.str_inputFile              = value
            if key == "inputDir":               self.str_inputDir               = value
            if key == "outputDir":              self.str_outputDir              = value
            if key == "outputFileStem":         self.str_outputFileStem         = value
            if key == "outputFileType":         self.str_outputFileType         = value
            if key == "label":                  self.str_label                  = value
            if key == "feature":                self.str_feature                = value
            if key == "image":                  self.str_image                  = value
            if key == "normalize":              self.b_normalize                = value
            if key == "lookuptable":            self.str_lookuptable            = value
            if key == "skipLabelValueList":     self.str_skipLabelValueList     = value
            if key == "filterLabelValueList":   self.str_filterLabelValueList   = value
            if key == "wholeVolume":            self.str_wholeVolume            = value

        # Declare pf_tree
        self.pf_tree    = pftree.pftree(
                            inputDir                = self.str_inputDir,
                            maxDepth                = self.maxDepth,
                            inputFile               = self.str_inputFile,
                            outputDir               = self.str_outputDir,
                            outputLeafDir           = self.str_outputLeafDir,
                            threads                 = self.numThreads,
                            verbosity               = self.verbosity,
                            followLinks             = self.b_followLinks,
                            relativeDir             = True
        )

    def tic(self):
        """
            Port of the MatLAB function of same name
        """

        global Gtic_start
        Gtic_start = time.time()

    def toc(self, *args, **kwargs):
        """
            Port of the MatLAB function of same name

            Behaviour is controllable to some extent by the keyword
            args:


        """
        global Gtic_start
        f_elapsedTime = time.time() - Gtic_start
        for key, value in kwargs.items():
            if key == 'sysprint':   return value % f_elapsedTime
            if key == 'default':    return "Elapsed time = %f seconds." % f_elapsedTime
        return f_elapsedTime

    def env_check(self, *args, **kwargs):
        """
        This method provides a common entry for any checks on the 
        environment (input / output dirs, etc)
        """
        b_status    = True
        str_error   = ''
        if not len(self.str_outputDir): 
            b_status = False
            str_error   = 'output directory not specified.'
            self.dp.qprint(str_error, comms = 'error')
            error.warn(self, 'outputDirFail', drawBox = True)
        return {
            'status':       b_status,
            'str_error':    str_error
        }

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

    # def MGZFileRead(self, *args, **kwargs):
    #     """

    #     Extracts all the MGZ files from the inputdir and 
    #     returns them as dictionary
    #     """

    #     # pudb.set_trace()
    #     mgz_featureFile = ""
    #     mgz_imageFile   = ""

    #     for root, dirs, files in os.walk(self.str_inputDir):
    #         for file in files:
    #             if file==self.str_feature:
    #                 mgz_featureFile = nib.load("%s/%s" % (root, file))
    #             elif file==self.str_image:
    #                 mgz_imageFile = nib.load("%s/%s" % (root, file))

    #     # mgz_featureFile = nib.load("%s/%s" (str_path, self.str_feature))
    #     # mgz_imageFile = nib.load("%s/%s" (str_path,self.str_image))
    #     return {
    #         "featureFile":    mgz_featureFile,
    #         "imageFile":      mgz_imageFile,   
    #     }
       
    def inputReadCallback(self, *args, **kwargs):
        """

        Callback for reading files from specific directory.

        In the context of mgz2imagetree, this implies reading
        files from each target directory and returning 
        the mgz data set of each subject.

        """

        b_status            = True
        str_file            = ''
        filesRead           = 0


        for k, v in kwargs.items():
            if k == 'file':     str_file    = v
            if k == 'path':     str_path    = v

        # pudb.set_trace()

        if len(args):
            at_data         = args[0]
            str_path        = at_data[0]
            l_files          = at_data[1]

        if self.str_feature in l_files and self.str_image in l_files:
            self.dp.qprint("reading: %s" % (str_path), level = 1)
            b_status = True
            filesRead += 2
        else:
            b_status        = False

        return {
            'status':           b_status,
            'str_path':         str_path,
            'l_files':           l_files,
            'filesRead':        filesRead
        }

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
    
        b_status            = False
        filesRead           = 0
        filesAnalyzed       = 0

        # for k, v in kwargs.items():
        #     if k == 'filesRead':    d_MGZRead   = v
        #     if k == 'path':         str_path    = v

        if len(args):
            at_data         = args[0]
            str_path        = at_data[0]
            d_read          = at_data[1]
            l_files         = d_read['l_files']

        d_args = {
            "inputFile":            self.str_feature,
            "inputDir":             str_path,
            "outputDir":            self.str_outputDir,
            "outputFileStem":       self.str_outputFileStem, 
            "outputFileType":       self.str_outputFileType,
            "label":                self.str_label,
            "normalize":            self.b_normalize,
            "lookuptable":          self.str_lookuptable,
            "skipLabelValueList":   self.str_skipLabelValueList,
            "filterLabelValueList": self.str_filterLabelValueList,
            "wholeVolume":          self.str_wholeVolume    
        }

        if self.str_feature in l_files and self.str_image in l_files:   
            b_status        = True   
            imgConverter    = mgz2imgslices.object_factoryCreate(d_args).C_convert
            imgConverter.run()          
        
        return {
            'status':           b_status,
            'filesAnalyzed':    filesAnalyzed,
        }

    def outputSaveCallback(self, at_data, **kwargs):
        """

        Callback for saving outputs.

        In order to be thread-safe, all directory/file 
        descriptors must be *absolute* and no chdir()'s
        must ever be called!

        The input 'data' is the return dictionary from the
        inputAnalyzeCallback method.

        """

        # print("in output save call back")
        
        return {
            'status':       True,
            'outputFile':   "",
            'filesSaved':   0
        }

    def create_imagetree(self, **kwargs):
        """
        A simple "alias" for calling the pftree method.
        """
        d_create_imagetree    = {}
        d_create_imagetree    = self.pf_tree.tree_process(
                                inputReadCallback       = self.inputReadCallback,
                                analysisCallback        = self.inputAnalyzeCallback,
                                outputWriteCallback     = None,
                                persistAnalysisResults  = False,
                                )
        return d_create_imagetree

    def run(self, *args, **kwargs):
        """
        The run method is merely a thin shim down to the 
        embedded pftree run method.
        """
        b_status            = True
        d_pftreeRun         = {}
        d_inputAnalysis     = {}
        d_env               = self.env_check()
        b_timerStart        = False

        self.dp.qprint(
                "\tStarting pfdicom run... (please be patient while running)", 
                level = 1
                )

        for k, v in kwargs.items():
            if k == 'timerStart':   b_timerStart    = bool(v)

        if b_timerStart:
            self.tic()

        if d_env['status']:
            d_pftreeRun = self.pf_tree.run(timerStart = False)
        else:
            b_status    = False 

        str_startDir    = os.getcwd()
        os.chdir(self.str_inputDir)
        if b_status:
            d_create_imagetree    = self.create_imagetree()
            b_status        = b_status and d_create_imagetree['status']
        os.chdir(str_startDir)

        # str_startDir    = os.getcwd()
        # os.chdir(self.str_inputDir)
        if b_status:
            if len(self.str_extension):
                d_inputAnalysis = self.pf_tree.tree_process(
                                inputReadCallback       = None,
                                analysisCallback        = self.filelist_prune,
                                outputWriteCallback     = None,
                                applyResultsTo          = 'inputTree',
                                applyKey                = 'l_file',
                                persistAnalysisResults  = True
                )
        os.chdir(str_startDir)

        d_ret = {
            'status':           b_status and d_pftreeRun['status'],
            'd_env':            d_env,
            'd_pftreeRun':      d_pftreeRun,
            'd_inputAnalysis':  d_inputAnalysis,
            'runTime':          self.toc()
        }

        # if self.b_json:
        #     self.ret_dump(d_ret, **kwargs)

        self.dp.qprint('\tReturning from pfdicom run...', level = 1)

        return d_ret