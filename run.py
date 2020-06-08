#!/usr/bin/env python3

from sys import path as sys_path
sys_path.insert(0, '/home/src')
from RetroPath2 import entrypoint as RetroPath2_entrypoint

from argparse import ArgumentParser as argparse_ArgParser
from shutil import copy as shutil_cp
from tempfile import TemporaryDirectory as tempfile_tempdir





# Wrapper for the RP2paths script that takes the same input (results.csv) as the original script but returns
# the out_paths.csv so as to be compliant with Galaxy




if __name__ == "__main__":
    parser = argparse_ArgParser('Python wrapper to run RetroPath2.0')
    parser.add_argument('-_file_sinkfile', type=str)
    parser.add_argument('-_file_sourcefile', type=str)
    parser.add_argument('-max_steps', type=int)
    parser.add_argument('-_file_rulesfile', type=str)
    parser.add_argument('-rulesfile_format', type=str)
    parser.add_argument('-topx', type=int, default=100)
    parser.add_argument('-dmin', type=int, default=0)
    parser.add_argument('-dmax', type=int, default=100)
    parser.add_argument('-mwmax_source', type=int, default=1000)
    parser.add_argument('-mwmax_cof', type=int, default=1000)
    parser.add_argument('-scope_csv', type=str)
    parser.add_argument('-timeout', type=int, default=30)
    params = parser.parse_args()
    if params.max_steps<=0:
        logging.error('Maximal number of steps cannot be less or equal to 0')
        exit(1)
    if params.topx<0:
        logging.error('Cannot have a topx value that is <0: '+str(params.topx))
        exit(1)
    if params.dmin<0:
        logging.error('Cannot have a dmin value that is <0: '+str(params.dmin))
        exit(1)
    if params.dmax<0:
        logging.error('Cannot have a dmax value that is <0: '+str(params.dmax))
        exit(1)
    if params.dmax>1000:
        logging.error('Cannot have a dmax valie that is >1000: '+str(params.dmax))
        exit(1)
    if params.dmax<params.dmin:
        logging.error('Cannot have dmin>dmax : dmin: '+str(params.dmin)+', dmax: '+str(params.dmax))
        exit(1)
    if 200<params.timeout or params.timeout<0:
        logging.error('Cannot have timeout less than 0 and more than 200: '+str(params.timeout))
        exit(1)

    # if params.rulesfile_format=="tar":
    #     rules_tar = tarfile.open(params._file_rulesfile)
    #     rules_tar.extract(params._file_rulesfile, './')
    #     rules_tar.close()

    with tempfile_tempdir() as tmpdirname:
        args = [
            '-sinkfile', params._file_sinkfile,
            '-sourcefile', params._file_sourcefile,
            '-max_steps', str(params.max_steps),
            '-rulesfile', params._file_rulesfile,
            '-topx', str(params.topx),
            '-dmin', str(params.dmin),
            '-dmax', str(params.dmax),
            '-mwmax_source', str(params.mwmax_source),
            '-mwmax_cof', str(params.mwmax_cof),
            '-timeout', str(params.timeout),
            '-outdir', tmpdirname,
            '-is_forward', 'False'
            ]
        RetroPath2_entrypoint(args)
        shutil_cp(tmpdirname+'/results.csv', params.scope_csv)
