#!/usr/bin/env python3
#
# (c) 2017 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import sys, os
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../mgz2imagetree'))

import mgz2imagetree
from mgz2imgslices          import mgz2imgslices
from    argparse            import RawTextHelpFormatter
from    argparse            import ArgumentParser
import  pudb

import  pfmisc
from    pfmisc._colors      import Colors
from    pfmisc              import other

str_version = "2.2.20"
str_desc = Colors.CYAN + """

                      _____ _                            _                 
                     / __  (_)                          | |                
 _ __ ___   __ _ ____`' / /'_ _ __ ___   __ _  __ _  ___| |_ _ __ ___  ___ 
| '_ ` _ \ / _` |_  /  / / | | '_ ` _ \ / _` |/ _` |/ _ \ __| '__/ _ \/ _ \\
| | | | | | (_| |/ / ./ /__| | | | | | | (_| | (_| |  __/ |_| | |  __/  __/
|_| |_| |_|\__, /___|\_____/_|_| |_| |_|\__,_|\__, |\___|\__|_|  \___|\___|
            __/ |                              __/ |                       
           |___/                              |___/                        
  
                        Path-File MGZ labels filter

        Recursively walk down a directory tree and extract MGZ labels,
        creating image slices for each individual label preserving directory structure in output tree.

                             -- version """ + \
             Colors.YELLOW + str_version + Colors.CYAN + """ --

        'mgz2imagetree' is a customizable and friendly MGZ labels filter. 
         Input DICOM trees are reconstructed in an output
        directory, preserving directory structure. Each node tree contains
        label directories containing image slices (in png/jpeg format) on the corresponding output directory for each input subject.


""" + Colors.NO_COLOUR

def synopsis(ab_shortOnly = False):
    scriptName = os.path.basename(sys.argv[0])
    shortSynopsis =  '''
    NAME

	    pfdicom_tagExtract 
        - process DICOM file header information down a file system tree.

    SYNOPSIS

            pfdicom_tagExtract                                      \\
                     -I|--inputDir <inputDir>                       \\
                    [-i|--inputFile <inputFile>]                    \\
                     -O|--outputDir <outputDir>                     \\
                     -o|--output <outputFileStem>                   \\
                    [--outputLeafDir <outputLeafDirFormat>]
                    [-t|--outputFileType <outputFileType>           \\
                    [-v <verbosity>]                                \\
                    [--version]                                     \\
                    [-x|--man]                                      \\
                    [-y|--synopsis]

    '''

    description =  '''
    DESCRIPTION

        `mgz2imagetree` filters the labels in mgz files for each subject within 
        the inputdir tree structure and copies the resultant label directories containing
        the image slices in png/jpg format into the outputdir with a similar structure as inputdir.
         
        The script accepts an <inputDir>, and then from this point an os.walk
        is performed to extract all the subdirs. Each subdir is examined for
        MGZ files (in the simplest sense by a file extension mapping).

        An image conversion is performed on the mgz files using the library "mgz2imgslices"
        which creates individual label direcctories containing 256 png/jpg slices and 
        the whole volume too with all label values. The results are stored in a tree structure 
        similar to the inputdir.

    ARGS

        -I|--inputDir <inputDir>
        Input DICOM directory to examine. By default, the first file in this
        directory is examined for its tag information. There is an implicit
        assumption that each <inputDir> contains a single DICOM series.

        [-i|--inputFile <inputFile>]
        An optional <inputFile> specified relative to the <inputDir>. If 
        specified, then do not perform a directory walk, but convert only 
        this file.

        -O|--outputDir <outputDir>
        The output root directory that will contain a tree structure identical
        to the input directory, and each "leaf" node will contain the analysis
        results.

        [--outputLeafDir <outputLeafDirFormat>]
        If specified, will apply the <outputLeafDirFormat> to the output
        directories containing data. This is useful to blanket describe
        final output directories with some descriptive text, such as 
        'anon' or 'preview'. 

        This is a formatting spec, so 

            --outputLeafDir 'preview-%%s'

        where %%s is the original leaf directory node, will prefix each
        final directory containing output with the text 'preview-' which
        can be useful in describing some features of the output set.

        -o|--outputFileStem <outputFileStem>
        The output file stem to store data. This should *not* have a file
        extension, or rather, any "." in the name are considered part of 
        the stem and are *not* considered extensions.

        [-t|--outputFileType <outputFileType>]
        A comma specified list of output types. These can be:

            o <type>    <ext>       <desc>
            o raw       -raw.txt    the raw internal dcm structure to string
            o json      .json       a json representation
            o html      .html       an html representation with optional image
            o dict      -dict.txt   a python dictionary
            o col       -col.txt    a two-column text representation (tab sep)
            o csv       .csv        a csv representation

        Note that if not specified, a default type of 'raw' is assigned.

        [-x|--man]
        Show full help.

        [-y|--synopsis]
        Show brief help.

        [--version]
        If specified, print the version number and exit.

        [-v|--verbosity <level>]
        Set the app verbosity level. 

            0: No internal output;
            1: Run start / stop output notification;
            2: As with level '1' but with simpleProgress bar in 'pftree';
            3: As with level '2' but with list of input dirs/files in 'pftree';
            5: As with level '3' but with explicit file logging for
                    - read
                    - analyze
                    - write

    EXAMPLES

    Extract DICOM header info down an input tree and save reports
    to output tree:

        pfdicom_tagExtract                                      \\
                    -I /var/www/html/normsmall -e dcm           \\
                    -O /var/www/html/tag                        \\
                    -o '%_md5|6_PatientID-%PatientAge'          \\
                    -m 'm:%_nospc|-_ProtocolName.jpg'           \\
                    -s 3:none                                   \\
                    --useIndexhtml                              \\
                    -t raw,json,html,dict,col,csv               \\
                    --threads 0 -v 0 --json

        which will output only at script conclusion and will log a JSON 
        formatted string.

    '''
    if ab_shortOnly:
        return shortSynopsis
    else:
        return shortSynopsis + description


parser  = ArgumentParser(description = str_desc, formatter_class = RawTextHelpFormatter)

parser.add_argument("-I", "--inputDir",
                    help    = "input dir",
                    dest    = 'inputDir')
parser.add_argument("-i", "--inputFile",
                    help    = "input file",
                    dest    = 'inputFile',
                    default = '')
parser.add_argument("-o", "--outputFileStem",
                    help    = "output file stem",
                    default = "",
                    dest    = 'outputFileStem')
parser.add_argument("-O", "--outputDir",
                    help    = "output image directory",
                    dest    = 'outputDir',
                    default = '')
parser.add_argument("-t", "--outputFileType",
                    help    = "list of output report types",
                    dest    = 'outputFileType',
                    default = 'raw')
parser.add_argument("--feature",
                    help    = "name of mgz file with features (aparc+aseg)",
                    dest    = 'feature',
                    default = 'aparc+aseg.mgz')
parser.add_argument("--image",
                    help    = "name of entire image file (brain.mgz)",
                    dest    = 'image',
                    default = 'brain.mgz')
parser.add_argument('--label',
                    help='prefix a label to all the label directories',
                    dest='label',
                    default = 'label'
                    )
parser.add_argument('-n', '--normalize',
                    help='normalize the pixels of output image files',
                    dest='normalize',
                    default = False
                    )
parser.add_argument('-l', '--lookuptable',
                    help='file contain text string lookups for voxel values',
                    dest='lookuptable',
                    default = '__val__'
                    )
parser.add_argument('-s', '--skipLabelValueList',
                    help='Comma separated list of voxel values to skip',
                    dest='skipLabelValueList',
                    default = ''
                    )
parser.add_argument('-f', '--filterLabelValueList',
                    help='Comma separated list of voxel values to include',
                    dest='filterLabelValueList',
                    default = "-1"
                    )
parser.add_argument('-w', '--wholeVolume',
                    help='Converts entire mgz volume to png/jpg instead of individually masked labels',
                    dest='wholeVolume',
                    default = 'wholeVolume'
                    )
parser.add_argument("-x", "--man",
                    help    = "man",
                    dest    = 'man',
                    action  = 'store_true',
                    default = False)
parser.add_argument("-y", "--synopsis",
                    help    = "short synopsis",
                    dest    = 'synopsis',
                    action  = 'store_true',
                    default = False)
parser.add_argument("--outputLeafDir",
                    help    = "formatting spec for output leaf directory",
                    dest    = 'outputLeafDir',
                    default = "")
parser.add_argument("--printElapsedTime",
                    help    = "print program run time",
                    dest    = 'printElapsedTime',
                    action  = 'store_true',
                    default = False)
parser.add_argument("-v", "--verbosity",
                    help    = "verbosity level for app",
                    dest    = 'verbosity',
                    default = "0")
parser.add_argument('--version',
                    help    = 'if specified, print version number',
                    dest    = 'b_version',
                    action  = 'store_true',
                    default = False)

args = parser.parse_args()

for root, dirs, files in os.walk(args.inputDir):
    print(dirs)
    for file in files:
        if file==args.feature:
            print(os.path.join(root, file))
            # Create the object
            args.inputFile = file
            args.inputDir = root
            print(args.inputFile + " AND "+ args.inputDir)
            imgConverter    = mgz2imgslices.object_factoryCreate(args).C_convert
            print(imgConverter.str_inputFile)
            # And now run it!
            imgConverter.tic()
            imgConverter.run()





