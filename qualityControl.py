#!/usr/bin/env python3
'''
@author: narumeena
@description: doing quality check of all RNA samples
@study IPS cell lines 
'''

import sys,os
import errno,subprocess

'''
main variables 
'''
inputRnaDirName     = '/mnt/hdd1/narendra/cambridge/projects/inProgress/iPSCLinesProteogenomics/data/RNA/'
outputDirName       = '/mnt/hdd1/narendra/cambridge/projects/inProgress/iPSCLinesProteogenomics/analysis/qualityControl/RNA/PRJEB7388/' 



def getListOfFiles(dirName):
    '''
    For the given path, get the List of all files in the directory tree 
    '''
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles


def mkdir_p(path):
    '''
    creating a folder if doesn't exist
    '''
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def runFastQc(fastq_path, output_dir, options=['--extract -t 10',]):
    """
    Run the fastqc program on a specified fastq file and return the output directory path.

    Parameters
    ----------
    fastq_path : str
        Path to the fastq file to analyze.
    output_dir : str
        Directory where output will be written. It will be created if it does not exist.
    options : list of str (optional)
        Command-line flags and options to fastqc. Default is --extract.

    Returns
    -------
    output_dir : str
        The path to the directory containing the detailed output for this fastq file.
        It will be a subdirectory of the specified output dir.
    """
    mkdir_p(output_dir)

    command = "fastqc {} -o {} {}".format(' '.join(options), output_dir, fastq_path)
    subprocess.check_call(command, shell=True)

    # Fastqc creates a directory derived from the basename
    fastq_dir = os.path.basename(fastq_path)
    if fastq_dir.endswith(".gz"):
        fastq_dir = fastq_dir[0:-3]
    if fastq_dir.endswith(".fq"):
        fastq_dir = fastq_dir[0:-3]
    if fastq_dir.endswith(".fastq"):
        fastq_dir = fastq_dir[0:-6]
    fastq_dir = fastq_dir + "_fastqc"

    # Delete the zip file and keep the uncompressed directory
    zip_file = os.path.join(output_dir, fastq_dir + ".zip")
    os.remove(zip_file)

    output_dir = os.path.join(output_dir, fastq_dir)
    return output_dir

def main():
    # Get the list of all files in directory tree at given path
    listOfFiles = getListOfFiles(inputRnaDirName)

    # filter fastq files 
    listOfFiles = [x for x in listOfFiles if 'fastq.gz' in x]

    #running fastqc 
    [runFastQc(x, outputDirName + os.path.split(os.path.dirname(x))[1]) for x in listOfFiles]    


if __name__=="__main__":
    main()
 
