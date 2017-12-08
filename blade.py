#!/usr/bin/env python

import os, sys, time, shutil, tarfile, argparse, subprocess

#*******************************************************************************

class Runner:

    __work_directory = os.path.dirname(os.path.realpath(__file__)) +\
        '/replicant_list'

    def __init__(self, executable, *args):

        if (not (os.path.isfile(executable) and os.access(executable, os.X_OK))):
            print('blade::Runner:: error: '
                '{} is not an executable!'.format(executable))
            sys.exit(1)

        self.executable = os.path.abspath(executable)
        self.path_dictionary = {}

        for path in args:
            if (not os.path.isdir(path)):
                print('blade::Runner:: warning: '
                    '{} is not a directory!'.format(path))
                continue

            for directory_name, _, data_names in os.walk(path):
                directory_path = os.path.abspath(directory_name)
                if (directory_path not in self.path_dictionary):
                    self.path_dictionary[directory_path] = (set(), set(), set())
                for data_name in data_names:
                    data_path = os.path.join(directory_path, data_name)
                    if (data_name.endswith(('.fa', '.fasta', '.fq', '.fastq'))):
                        if ('reference' in data_name):
                            self.path_dictionary[directory_path][0].add(data_path)
                        else:
                            self.path_dictionary[directory_path][1].add(data_path)
                    elif (data_name.endswith(('.tar.gz', '.tgz'))):
                        self.path_dictionary[directory_path][2].add(data_path)

    def reload(self, executable, *args):
        __init__(executetable, *args)

    def execute(self):

        try:
            os.makedirs(Runner.__work_directory)
        except OSError:
            if (not os.path.isdir(Runner.__work_directory)):
                print('blade::Runner::execute error: '
                    'unable to create work directory!')
                sys.exit(1)

        runner_report = open(os.path.join(Runner.__work_directory,\
            'blade_runner_report_' + str(time.time()) + '.txt'), "w")

        for directory_path, data_paths in self.path_dictionary.items():
            if (sum([len(paths) for paths in data_paths]) == 0):
                continue
            print('Processing directory {}'.format(directory_path))

            reference_paths, uncompressed_data_paths, compressed_data_paths = data_paths

            reference_path = next(iter(reference_paths))\
                if (len(reference_paths) != 0) else ""

            for data_path in uncompressed_data_paths:

                print('--> {} {} {}'.format(\
                    os.path.basename(self.executable),\
                    os.path.basename(data_path),\
                    os.path.basename(reference_path)))

                p = subprocess.Popen([self.executable, data_path, reference_path],\
                    stdout=runner_report, stderr=runner_report)
                p.communicate()

            for compressed_data_path in compressed_data_paths:
                print('--[ extracting {}'.format(\
                    os.path.basename(compressed_data_path)))

                shutil.copy(compressed_data_path, Runner.__work_directory)

                tar_path = os.path.join(Runner.__work_directory,\
                    os.path.basename(compressed_data_path))
                tar = tarfile.open(tar_path)

                data_paths = [os.path.join(Runner.__work_directory, data_path)\
                    for data_path in tar.getnames()]

                tar.extractall(Runner.__work_directory)
                tar.close()
                os.remove(tar_path)

                for data_path in data_paths:

                    print('    --> {} {} {}'.format(\
                        os.path.basename(self.executable),\
                        os.path.basename(data_path),\
                        os.path.basename(reference_path)))

                    p = subprocess.Popen([self.executable, data_path, reference_path],\
                        stdout=runner_report, stderr=runner_report)
                    p.communicate()

                    os.remove(data_path)

        runner_report.close()

#*******************************************************************************

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='''Run any executable which has
        the form \'executable reads [reference]\' on a large amount of
        sequencing data.''')
    parser.add_argument('executable', help='''executable which takes reads in
        FASTA or FASTQ format as positional argument; if present, a reference
        file in FASTA format (containing the word reference in name) will be
        passed as second argument''')
    parser.add_argument('path', nargs='+', help='''path to folder which contains
        compressed (.tar.gz or .tgz) or uncompressed sequencing data in FASTA or
        FASTQ format (supported file extensions are .fa, .fasta, .fq and
        .fastq)''')
    args = parser.parse_args()

    runner = Runner(args.executable, *args.path)
    runner.execute()
