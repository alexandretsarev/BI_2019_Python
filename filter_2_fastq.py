#!/usr/bin/env python


def len_read(seq):
    return len(seq)


def gc_content_count(seq):
    if len(seq) != 0:
        gc_content = (seq.count("G") + seq.count("C")) / len(seq) * 100
        return gc_content
    else:
        return 0


def read_approval(seq, min_len, gc_min, gc_max):
    return True if len_read(seq) >= min_len and gc_min <= gc_content_count(seq) <= gc_max else False


if __name__ == '__main__':
    import argparse
    from os import path, remove

    parser = argparse.ArgumentParser(description="This programm can work with .fastq files, it can:\n"
                                                 "1) trimm reads by length\n"
                                                 "2) trimm reads by GC content (in %)\n"
                                                 "3) keep filtered and non-filtered reads")
    parser.add_argument('input', help="input fastq file")
    parser.add_argument('-ml', '--min_length', type=int, required=False, default=0,
                        help='filter by minimal length of the read')
    parser.add_argument('-gc', '--gc_bounds', nargs='+', required=False, type=int,
                        help='percent range of GC content (default: 0,100)', metavar='')
    parser.add_argument('-o', '--output_basename', nargs=1, required=False, type=str, metavar='')
    parser.add_argument('-kf', '--keep_filtered', action="store_true", help='flag which keeps filtered'
                                                                            ' reads in separate file')
    args = parser.parse_args()

    assert args.min_length >= 0, "Filter by length can't be less than zero"
    assert len(args.gc_bounds) in [1, 2], "GC% range has two restrictions: more and less than something" \
                                          " (e.g. -gc 10 50)"
    if len(args.gc_bounds) == 2:
        assert 0 <= (args.gc_bounds[0] and args.gc_bounds[1]) <= 100, "GC% range must be within 100 %"
    else:
        assert 0 <= args.gc_bounds[0] <= 100, "GC% range must be within 100 %"

    gc_min = args.gc_bounds[0] if len(args.gc_bounds) > 0 else 0
    gc_max = args.gc_bounds[1] if len(args.gc_bounds) > 1 else 100

    if args.output_basename is None:
        valid_path = args.input.replace(".fastq", "") + "__passed.fastq"
        non_valid_path = args.input.replace(".fastq", "") + "__failed.fastq"
    else:
        valid_path = args.output_basename[0] + "__passed.fastq"
        non_valid_path = args.output_basename[0] + "__failed.fastq"

    if path.exists(non_valid_path):
        remove(non_valid_path)

    with open(args.input, 'r') as fastq_data, open(valid_path, 'w') as valid_fq:
        for line in fastq_data:
            seq_id = line.strip()
            sequence = next(fastq_data).strip()
            description = next(fastq_data).strip()
            quality = next(fastq_data).strip()

            if read_approval(sequence, args.min_length, gc_min, gc_max):
                valid_fq.writelines([seq_id, '\n', sequence, '\n', description, '\n', quality, '\n'])
            else:
                if args.keep_filtered:
                    with open(non_valid_path, 'a') as non_valid_fq:
                        non_valid_fq.writelines([seq_id, '\n', sequence, '\n', description, '\n', quality, '\n'])
