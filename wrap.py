

from retropath2_wrapper import retropath2, build_args_parser
from os                 import path as os_path
from sys                import exit as sys_exit
from tempfile           import TemporaryDirectory
from shutil             import copyfile


def _cli():
    parser = build_args_parser()
    parser.add_argument('outfile', type=str)
    args  = parser.parse_args()

    with TemporaryDirectory() as temp_d:

        r_code, result = retropath2(args.sinkfile, args.sourcefile, args.rulesfile,
                                    temp_d,
                                    args.knime_exec,
                                    args.max_steps,
                                    args.topx,
                                    args.dmin, args.dmax,
                                    args.mwmax_source, args.mwmax_cof,
                                    args.timeout,
                                    args.forward)

    print()
    if r_code > 0:
        print('*** Error:')
        print('     ', result)
    else:
        copyfile(result, args.outfile)
    print()


if __name__ == '__main__':
    _cli()
