mgz2imagetree 1.0.2
===================

Quick Overview 
--------------

Recursively walk down a directory tree and extract ``MGZ`` labels,
creating image slices for each individual label preserving directory structure in output tree.

Overview
--------

``mgz2imagetree`` is a simple Python utility that recursively walks down an ``inputdir``, extracts all the ``mgz`` files, filters "labels" from ``mgz`` volume files and saves each label set as slices of (by default) ``png`` files (using the Python utility called ``mgz2imgslices``), organized into a series of directories, one per label set for each subject, and replicates the entire direcotry structure in the ``outputdir``.

This utility also allows to pass all the CLI arguments that are specific to ``mgz2imgslices``.

NOTE:

An ``mgz`` format file simply contains a 3D volume data structure of image values. Often these values are interpreted to be image intensities. Sometimes, however, they can be interpreted as label identifiers. Regardless of the interpretation, the volume image data is simply a number value in each voxel of the volume.

Dependencies
------------

Make sure that the following dependencies are installed on your host system (or even better, a ``python3`` virtual env):

``pfmisc`` : (a general miscellaneous module for color support, etc)

``nibabel`` : (to read NIfTI/MGZ files)

``numpy`` : (to support large, multidimensional arrays and matrices)

``imageio`` : (interface to read and write image data)

``pftree`` : Create a dictionary representation of a filesystem hierarchy.

Assumptions
-----------

This document assumes UNIX conventions and a ``bash`` shell. The script should work fine under Windows, but we have not actively tested on that platform -- our dev envs are Linux Ubuntu and macOS.

Installation
~~~~~~~~~~~~

Python module
~~~~~~~~~~~~~

One method of installing this script and all of its dependencies is by fetching it from `PyPI <https://pypi.org/project/mgz2imagetree/>`_.

.. code:: bash

        pip3 install mgz2imagetree

How to Use
----------

``mgz2imagetree`` needs at a minimum the following required command line arguments:

- ``[-I|--inputDir <inputDir>]`` : Input directory to examine. By default, the first file in this directory is examined for its tag information.

- ``[-O|--outputDir <outputDir>]`` : The output root directory that will contain a tree structure identical to the input directory, and each "leaf" node will contain the analysis results.

- ``[-o|--outputFileStem <outputFileStem>]`` : The output file stem to store data. This should *not* have a file extension, or rather, any "." in the name are considered part of the stem and are *not* considered extensions. 

- ``[--feature <MGZFileToConvertToLabelledSegments>]`` : The feature file containing the cortical strip which needs to be filtered into it constituent cortical segments using ``mgz2imgslices``

- ``[--image <MGZFileImageFile>]`` : The raw 3D mgz image file that needs to be split and stored as slices in the corresponding subject's output directory.

Examples
--------

First, let's create a directory, say ``devel`` wherever you feel like it. We will place some test data in this directory to process with this plugin.

.. code:: bash

    cd ~/
    mkdir devel
    cd devel
    export DEVEL=$(pwd)

Now, we need to fetch sample MGZ data.

Pull ``mgz`` data
~~~~~~~~~~~~~~~~~

- We provide a sample directory of a few ``.mgz`` volumes here. (https://github.com/FNNDSC/mgz_converter_dataset.git)

- Clone this repository (``mgz_converter_dataset``) to your local computer.

.. code:: bash

    git clone https://github.com/FNNDSC/mgz_converter_dataset.git

Make sure the ``mgz_converter_dataset`` directory is placed in the devel directory.

- Make sure your current working directory is ``devel``. At this juncture it should contain ``mgz_converter_dataset``.

- Create an output directory named ``results`` in ``devel``.

.. code:: bash

    mkdir results && chmod 777 results

EXAMPLE 1
^^^^^^^^^

- Run ``mgz2imgslices`` using the following command. Change the arguments according to your need.

.. code:: bash

    mgz2imagetree
        --inputDir ${DEVEL}/mgz_converter_dataset/                             \            
        --outputDir ${DEVEL}/results/                                          \ 
        --feature aparc.a2009s+aseg.mgz                                        \
        --image brain.mgz                                                      \
        --outputFileStem sample                                                \
        --outputFileType jpg                                                   \
        --label label                                                          \
        --wholeVolume FullVolume                                               \
        --rawDirName RawImageDirectory                                         \
        
- In the ``outputDir`` the directory structure of the ``inputDir`` will be replicated, and each subject directory will contain the labelled directoriescreated using ``mgz2imgslices``.

- For an input directory of a structure like the following:

.. code:: bash

        ${DEVEL}/mgz_converter_dataset/subject1/featureFile.mgz 
        ${DEVEL}/mgz_converter_dataset/subject2/featureFile.mgz    

        ....
        ....

        ${DEVEL}/mgz_converter_dataset/subjectN/featureFile.mgz

- The output will look something like this:

.. code:: bash

    
        results/subject1/label-001/sample-000.jpg ..... results/subject1/label-0012175/sample-000.jpg
        results/subject2/label-001/sample-000.jpg ..... results/subject2/label-0012175/sample-000.jpg

        ....
        ....

        results/subjectN/label-001/sample-000.jpg ..... results/subjectN/label-0012175/sample-000.jpg