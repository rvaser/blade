# Blade
Tool for automatic processing of a large amount of sequencing data.

## Description
Blade was implemented to automatically run any executable on a large amount of sequencing data. The used executable must accept sequencing data in FASTA/FASTQ format (with support for compression via gzip) as positional argument. For tools which have different interfaces, a simple encapsulation script can be used instead. If a reference genome is present, it will be passed as the second positional argument to the used executable.

## Dependencies
1. python 2.x or python 3.x
2. cmake 3.2+

## Instalation
To install Blade run the following commands:

```bash
git clone https://github.com/rvaser/blade.git blade
cd blade
mkdir build
cd build
cmake ..
make
```

After successful installation, an executable name `blade` will appear in `build/bin`.

## Usage
Usage of `blade` is as following:

    blade [options ...] executable path [path ...]

        <executable>
            executable which takes reads in FASTA/FASTQ format (with gzip support)
            as positional argument; if present, a file with the reference genome
            in FASTA format will be passed as the second positional argument
            (supported file names are those that contain the word reference)
        <path>
            path to directory which somewhere in its directory tree contains
            compressed/uncompressed sequencing data in FASTA/FASTQ format
            (supported file extensions are .fa, .fasta, .fq, .fastq, .fa.gz,
            .fasta.gz, .fq.gz and .fastq.gz)

        options:
            -r, --reference-required
                ignore data sets without reference genomes
            -h, --help
                prints the usage

## Contact information
For additional information, help and bug reports please send an email to: robert.vaser@fer.hr.

## Acknowledgement
This work has been supported in part by Croatian Science Foundation under the project UIP-11-2013-7353.
