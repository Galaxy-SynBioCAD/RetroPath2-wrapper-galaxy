

from retropath2_wrapper import (
    retropath2,
    build_args_parser,
    parse_and_check_args
)
from sys                import exit as sys_exit
from tempfile           import TemporaryDirectory
from shutil             import copyfile


def _cli():
    parser = build_args_parser()
    parser.add_argument('outfile', type=str)
    args = parse_and_check_args(parser)

    with TemporaryDirectory() as temp_d:

        r_code, result = retropath2(
            sink_file = args.sink_file,
            source_file = args.source_file,
            rules_file = args.rules_file,
            outdir = temp_d,
            kexec = None,
            workflow = None,
            max_steps = args.max_steps,
            topx = args.topx,
            dmin = args.dmin,
            dmax = args.dmax,
            mwmax_source = args.mwmax_source,
            mwmax_cof = args.mwmax_cof,
            timeout = args.timeout,
            is_forward = args.forward
        )

    if r_code == 'OK' or r_code == 'TimeLimit':
        logger.info('{attr1}Results{attr2}'.format(attr1=attr('bold'), attr2=attr('reset')))
        logger.info('   |- Checking... ')
        r_code = check_results(result_files, logger)
        logger.info('   |--path: '+args.outdir)
    else:
        logger.error('Exiting...')

    return __ERROR_CODES__[r_code]


if __name__ == '__main__':
    sys_exit(_cli())
