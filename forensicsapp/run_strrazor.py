#!/usr/bin/env python
"""
STRaitRazor pipeline

Authors: Cameron Jack & Bob Buckley
ANU Bioinformatics Consultancy,
John Curtin School of Medical Research,
Australian National University
18/5/2016

This code is part os the Forensics project.
"""


import os
import time
import modpipe as px
import modcommon as com


def strrazor(itrfce, progress=None):
    """
        Pipeline for running STRaitRazor script

        Define a hardcoded pipeline that gets its optional command strings
        from Bob's interface code.

        itrfce is a dictionary of dictionaries, with each top level key
        being a pipeline stage and each second level key being the
        argument and the value being the value of said argument.

        progress is an optional progress bar object we can update
    """
    strrazor_home = '/home/bobb/Downloads/STRaitRazorv2.5/Newest_STRait_Razor'
    # Note: STRaitRazor needs its own configuration ...
    # it's modified to process FASTQ .gz file
    # and to find it's agrep program

    for sect in ['Shared', 'Trimmomatic', 'strrazor']: 
        if not sect in itrfce:
            print sect, "is not present in the interface dictionary :("
            return False

    home, destdir = com.forensicsenv

    fqs, bn, cmds, wkdir, logger = com.prepare(itrfce, 'STRaitRazor', progress)

    # target directory must not be present
    # cmd = [ 'test', '-d', wkdir, '&&', 'rm', '-rf', wkdir, ';', 'true' ]
    # cmds.append((cmd, 'bsh'))

    # run STRaitRazor
    cmd = [ 'cd', strrazor_home, ';', 
             # "PPSS_DIR="+os.path.join(destdir, 'ppss_dir'), # this would not work well
             'perl', './STRaitRazor.pl', '-dir', wkdir,
          ] + [ x for f in fqs for x in [ '-fastq', f ]] + [
             '-sampleNum', itrfce['strrazor']['workdir'],
             '-typeselection', itrfce['strrazor']['opt'],
          ]
    cmds.append((cmd, 'bsh'))

    success = px.run_pipeline(cmds, logger=logger, progress=progress)

    return success

if __name__ == '__main__':
    """ Run a Mpileup or Freebayes SNP calling pipeline """
    import sys
    import dummypb
    # define dummy interface output so we can get started
    interface = {
        'Shared': {
            'r1': '/home/cam/projects/forensics/forensics_data/MiSeq_DFSC/R701-A506_S5_L001_R1_001.fastq.gz',
            'single': 'single-end',
            'threads': '3',
        },
        'Trimmomatic': {'a': '', 'c': 0, 'd': 0, 'm': '20', 'q': '20', 's': 1, 'w': '4'}, 
        'strrazor': {
            'sample': 'S5',
            'opt' : 'ALL',	# choice of X, Y, AUTOSOMAL, ALL
        },
    }

    # parameters for paired end testing
    if 0:	# set paired end values
        interface['Shared']['r1'] = '/home/cam/projects/forensics/forensics_data/MiSeq_DFSC/R701-A506_S5_L001_R1_001.fastq.gz'


    if 1:
        interface['Shared']['single'] = 'auto-detect'

    if len(sys.argv) == 2:
        interface['Shared']['r1'] = sys.argv[1]

    success = strrazor(interface, progress=dummypb.StatusProgress())
    if success:
        print 'STRaitRazor pipeline completed successfully'
    else:
        print 'STRaitRazor pipeline failed'
