#!/usr/bin/env python

from __future__ import print_function
import os, sys, time, shutil, tarfile, argparse, subprocess

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

#*******************************************************************************

class Runner:

    def __init__(self, executable, reference_required, *args):

        if (not (os.path.isfile(executable) and os.access(executable, os.X_OK))):
            eprint('Blade::Runner::__init__ error: '
                '{} is not an executable!'.format(executable))
            sys.exit(1)

        self.executable = os.path.abspath(executable)
        self.reference_required = reference_required
        self.path_dictionary = {}

        for path in args:
            if (not os.path.isdir(path)):
                eprint('Blade::Runner::__init__ warning: '
                    '{} is not a directory!'.format(path))
                continue

            for directory_name, _, data_names in os.walk(path):
                directory_path = os.path.abspath(directory_name)
                if (directory_path not in self.path_dictionary):
                    self.path_dictionary[directory_path] = (set(), set())
                for data_name in data_names:
                    data_path = os.path.join(directory_path, data_name)
                    if (data_name.endswith(('.fa', '.fasta', '.fq', '.fastq', '.fa.gz', '.fasta.gz', '.fq.gz', '.fastq.gz'))):
                        if ('reference' in data_name):
                            self.path_dictionary[directory_path][0].add(data_path)
                        else:
                            self.path_dictionary[directory_path][1].add(data_path)

        self.work_directory = os.getcwd() + '/replicant_list'

    def __enter__(self):
        try:
            os.makedirs(self.work_directory)
        except OSError:
            if (not os.path.isdir(self.work_directory)):
                eprint('Blade::Runner::__enter__ error: unable to create work directory!')
                sys.exit(1)

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def execute(self):

        runner_report = open(os.path.join(self.work_directory,\
            'blade_runner_report_' + str(time.time()) + '.txt'), 'w')

        for directory_path, data_paths in self.path_dictionary.items():
            if (sum([len(paths) for paths in data_paths]) == 0):
                continue

            reference_paths, sequencing_data_paths = data_paths

            reference_path = next(iter(reference_paths))\
                if (len(reference_paths) != 0) else ''

            if self.reference_required and not reference_path:
                continue

            eprint('Blade::Runner::execute processing directory {}'.format(directory_path))

            for data_path in sequencing_data_paths:

                eprint('--> {} {} {}'.format(\
                    os.path.basename(self.executable),\
                    os.path.basename(data_path),\
                    os.path.basename(reference_path)))

                p = subprocess.Popen([self.executable, data_path, reference_path],\
                    stdout=runner_report, stderr=runner_report)
                p.communicate()

        runner_report.close()

#*******************************************************************************

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='''Run any executable which has
        the form \'executable reads [reference]\' on a large amount of
        sequencing data.''')
    parser.add_argument('executable', help='''executable which takes reads in
        FASTA/FASTQ format (with gzip support) as positional argument; if present,
        a file with the reference genome in FASTA format will be passed as the
        second positional argument (supported file names are those that contain
        the word reference)''')
    parser.add_argument('path', nargs='+', help='''path to directory which
        somewhere in its directory tree contains compressed/uncompressed sequencing
        data in FASTA/FASTQ format (supported file extensions are .fa, .fasta,
        .fq, .fastq, .fa.gz, .fasta.gz, .fq.gz and .fastq.gz)''')
    parser.add_argument('-r', '--reference-required', action='store_true',
        help='''ignore data sets without a reference genome''')

    args = parser.parse_args()

    runner = Runner(args.executable, args.reference_required, *args.path)

    with runner:
        runner.execute()
