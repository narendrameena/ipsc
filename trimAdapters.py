#!/usr/bin/env python3
'''
@author: narumeena
@description: comprehensive quality profiling for both before and after filtering data (quality curves, base contents, KMER, Q20/Q30, 
GC Ratio, duplication, adapter contents...) filter out bad reads (too low quality, too short, or too many N...) cut low quality bases
for per read in its 5' and 3' by evaluating the mean quality from a sliding window (like Trimmomatic but faster). trim all reads in 
front and tail cut adapters. Adapter sequences can be automatically detected, which means you don't have to input the adapter sequences
to trim them. correct mismatched base pairs in overlapped regions of paired end reads, if one base is with high quality while the other 
is with ultra low quality trim polyG in 3' ends, which is commonly seen in NovaSeq/NextSeq data. Trim polyX in 3' ends to remove unwanted 
polyX tailing (i.e. polyA tailing for mRNA-Seq data) preprocess unique molecular identifier (UMI) enabled data, shift UMI to sequence name.
report JSON format result for further interpreting.

@study IPS cell lines 
'''

import sys,os
import errno,subprocess

'''
main variables 
'''
inputRnaDirName     = '/mnt/hdd1/narendra/cambridge/projects/inProgress/iPSCLinesProteogenomics/data/RNA/'
outputDirName       = '/mnt/hdd1/narendra/cambridge/projects/inProgress/iPSCLinesProteogenomics/analysis/trimAdapters/RNA/PRJEB7388/' 
inputForCommand     = '/mnt/hdd1/narendra/cambridge/projects/inProgress/iPSCLinesProteogenomics/data/RNA/PRJEB7388/'

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
    creating a folder if it doesn't exist
    '''
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def runFastP(fastq_path, output_dir, file_name,  options=[' ',]):
    """
    Run the fastqc program on a specified fastq file and return the output directory path.

    Parameters
    ----------
    fastq_path : str
        Path to the fastq file to analyze.
    output_dir : str
        Directory where output will be written. It will be created if it does not exist.
    filename : str
        prefix of fastq file to analyze
    options : list of str (optional)
        Command-line flags and options to fastqc. Default is --extract.

    Returns
    -------
    output_dir : str
        The path to the directory containing the detailed output for this fastq file.
        It will be a subdirectory of the specified output dir.
    """
    mkdir_p(output_dir + file_name)

    command = "fastp --unpaired1 --unpaired2 -w 20  -i "+fastq_path+file_name+"/"+file_name+ "_1.fastq.gz -o "+output_dir+file_name+"/"+file_name+"_trim_1.fastq.gz -I  "+fastq_path+file_name+"/"+file_name+"_2.fastq.gz -O "+output_dir+file_name+"/"+file_name+"_trim_2.fastq.gz".format(' '.join(options))
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
    [runFastP(inputForCommand, outputDirName , os.path.split(os.path.dirname(x))[1]) for x in listOfFiles]    
    #print(list(dict.fromkeys([os.path.split(os.path.dirname(x))[1] for x in listOfFiles])))

if __name__=="__main__":
    main()
 