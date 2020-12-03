

from retropath2_wrapper import retropath2, build_args_parser
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

        print(r_code)
        print(result)

        print()
        if r_code > 0:
            print('*** Error:')
            print('     ', result)
        else:
            copyfile(result, args.outfile)
        print()

    return r_code


if __name__ == '__main__':
    sys_exit(_cli())
