#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description="This programm can work with .fastq files, it can:\n"
                                             "1) trimm reads by length\n"
                                             "2) trimm reads by GC content (in %)\n"
                                             "3) keep filtered and non-filtered reads")
parser.add_argument('-i', '--input', metavar='', required=True, help='input fastq file')
parser.add_argument('-l', '--min_lenght', type=int, required=False, metavar='',
                    help='filter by minimal length of the read', default=0)
parser.add_argument('-gc', '--gc_bounds', nargs='+', required=False, type=int, default=[0, 100],
                    help='percent range of GC content (default: 0,100)', metavar='')
parser.add_argument('-o', '--output_basename', nargs=1, required=False, type=str, metavar='')
parser.add_argument('-kf', '--keep_filtered', action="store_true", help='flag which keeps filtered reads in separate '
                                                                        'file')

args = parser.parse_args()

assert args.min_lenght >= 0, "Filter by length can't be less than zero"
assert len(args.gc_bounds) in range(1, 3), "GC% range has two restrictions: more and less than something" \
                                           " (e.g. -gc 10 50)"
assert (args.gc_bounds[0] and args.gc_bounds[1]) <= 100, "GC% range cannot be more than 100%"
assert args.gc_bounds[0] >= 0, "GC% range cannot be more less than 0%"


def len_check(seq):
    if len(seq) > args.min_lenght:
        return True


def check_gc(seq):
    gc_min = args.gc_bounds[0] if len(args.gc_bounds) > 0 else 0
    gc_max = args.gc_bounds[1] if len(args.gc_bounds) > 1 else 100
    gc_content = (seq.count("G") + seq.count("C")) / len(seq) * 100
    if gc_content >= gc_min:
        return True
    elif gc_min <= gc_content <= gc_max:
        return True


if args.output_basename is None:
    valid_path = args.input.replace(".fastq", "") + "__passed.fastq"
    non_valid_path = args.input.replace(".fastq", "") + "__failed.fastq"
else:
    valid_path = args.output_basename[0] + "__passed.fastq"
    non_valid_path = args.output_basename[0] + "__failed.fastq"

with open(args.input, 'r') as fastq_data, \
        open(valid_path, 'w') as valid_fq:
    for line in fastq_data:
        seq_id = line.strip()
        sequence = next(fastq_data).strip()
        descript = next(fastq_data).strip()
        quality = next(fastq_data).strip()

        if len_check(sequence) and check_gc(sequence):
            valid_fq.writelines([seq_id, '\n', sequence, '\n', descript, '\n', quality, '\n'])
        else:
            if args.keep_filtered:
                with open(non_valid_path, 'a') as non_valid_fq:
                    non_valid_fq.writelines([seq_id, '\n', sequence, '\n', descript, '\n', quality, '\n'])