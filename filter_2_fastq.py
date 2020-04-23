#!/usr/bin/env python

from collections import namedtuple

# read and read report structures
Read = namedtuple('read', ['name', 'sequence', 'description', 'quality'])
Read_report = namedtuple('read_report', ['read_valid', 'length_valid', 'gc_content_valid'])

# summary statistics of the whole fastq file in the beginning
fastq_statistics = {"n_total": 0,
                    "n_failed_by_length": 0,
                    "n_failed_by_gc_content": 0,
                    "n_failed": 0,
                    "n_valid": 0}


def length_read(input_read: Read):
    return len(input_read.sequence)


def gc_content_count(input_read: Read):
    return (input_read.sequence.count("G") + input_read.sequence.count("C")) / len(input_read.sequence) * 100 \
        if len(input_read.sequence) != 0 else 0


def crop(inputread: Read, threshold: int):
    return Read(inputread.name, inputread.sequence[:threshold], inputread.description, inputread.quality[:threshold])


def headcrop(input_read: Read, threshold: int):
    return Read(input_read.name, input_read.sequence[threshold:], input_read.description,
                input_read.quality[threshold:])


def quality_decipher(input_read: Read):
    return list(map(lambda ascii_symbol: ord(ascii_symbol) - 33, input_read.quality))


def trailing(input_read: Read, threshold: int):
    read_quality = quality_decipher(input_read)
    cut_position = next((idx for idx, nucl_quality in enumerate(read_quality) if nucl_quality < threshold), None)
    return Read(input_read.name,
                input_read.sequence[:cut_position],
                input_read.description,
                input_read.quality[:cut_position])


def leading(input_read: Read, threshold: int):
    read_quality = quality_decipher(input_read)
    cut_position = next((idx for idx, nucl_quality in reversed(list(enumerate(read_quality)))
                         if nucl_quality < threshold), None)
    return Read(input_read.name,
                input_read.sequence[cut_position:],
                input_read.description,
                input_read.quality[cut_position:])


def sliding_window(input_read: Read, threshold: int, window: int):
    read_quality = quality_decipher(input_read)
    cut_position = next(
        (idx for idx in range(len(read_quality) - window + 1) if
         sum(read_quality[idx:idx + window]) / window < threshold), None)
    return Read(input_read.name,
                input_read.sequence[:cut_position],
                input_read.description,
                input_read.quality[:cut_position])


def read_approval_report(input_read: Read, min_length: int, gc_min: int, gc_max: int):
    length_not_valid = 0 if length_read(input_read) >= min_length else 1
    gc_content_not_valid = 0 if gc_min <= gc_content_count(input_read) <= gc_max else 1
    read_valid = True if length_not_valid == 0 and gc_content_not_valid == 0 else False
    return Read_report(read_valid, length_not_valid, gc_content_not_valid)


def update_statistics_per_read(statistics_dict: dict, one_read_report: Read_report):
    statistics_dict['n_total'] += 1
    statistics_dict['n_failed_by_length'] += one_read_report.length_valid
    statistics_dict['n_failed_by_gc_content'] += one_read_report.gc_content_valid
    statistics_dict['n_valid'] += 1 if one_read_report.read_valid else 0
    statistics_dict['n_failed'] += 1 if not one_read_report.read_valid else 0
    return statistics_dict


def generate_statistics_summary(statistics_dict: dict):
    proportion_valid = round(statistics_dict["n_valid"] / statistics_dict["n_total"] * 100, 3)
    proportion_failed = round(statistics_dict["n_failed"] / statistics_dict["n_total"] * 100, 3)
    failed_by_length_part = round(
        statistics_dict["n_failed_by_length"] / statistics_dict["n_total"] * 100, 3)
    failed_by_gc_part = round(
        statistics_dict["n_failed_by_gc_content"] / statistics_dict["n_total"] * 100, 3)

    return "\n".join(["FILTER STATISTICS:", f"Total number of reads {statistics_dict['n_total']}",
                      f"Total valid reads {statistics_dict['n_valid']} ({proportion_valid}%)",
                      f"Total failed reads {statistics_dict['n_failed']} ({proportion_failed}%)",
                      f"Failed by length reads {statistics_dict['n_failed_by_length']} ({failed_by_length_part}%)",
                      f"Failed by GC-content reads {statistics_dict['n_failed_by_gc_content']} ({failed_by_gc_part}%)"])


if __name__ == '__main__':
    import argparse
    from os import path, remove

    parser = argparse.ArgumentParser(
        usage='./filter_2_fastq.py example.fastq -ml 20 -gc 12 95 -sw 20 5 -hc 5 -c 25 -kf -stat -o '
              './path_to_directory/processed_file')
    parser.add_argument('input', help="input fastq file")
    parser.add_argument('-ml', '--min_length', type=int, required=False, default=0,
                        help='filter by minimal length of the read')
    parser.add_argument('-gc', '--gc_bounds', nargs='+', required=False, type=int,
                        help='percent range of GC content', metavar='')
    parser.add_argument('-o', '--output_basename', nargs=1, required=False, type=str, metavar='',
                        help='path to output file')
    parser.add_argument('-kf', '--keep_filtered', action="store_true", help='keep filtered reads in a separate file')
    parser.add_argument('-stat', '--stat_summary', action="store_true", help='keep summary statistics in file')
    parser.add_argument('-c', '--CROP', nargs=1, required=False, type=int, metavar='',
                        help='cut the read to a specified length by removing bases from the end')
    parser.add_argument('-hc', '--HEADCROP', nargs=1, required=False, type=int, metavar='',
                        help='cut the specified number of bases from the start of the read')
    parser.add_argument('-t', '--TRAILING', nargs=1, required=False, type=int, metavar='',
                        help='cut bases off the end of a read, if below a threshold quality')
    parser.add_argument('-l', '--LEADING', nargs=1, required=False, type=int, metavar='',
                        help='cut bases off the start of a read, if below a threshold quality')
    parser.add_argument('-sw', '--SLIDINGWINDOW', nargs=2, required=False, type=int, metavar='',
                        help='it takes 2 arguments quality and window size and performs a sliding window trimming '
                             'approach. It starts scanning at the 5-prime end and clips the read once the average '
                             'quality within the window falls below a threshold')
    args = parser.parse_args()

    # assertion block
    assert args.min_length >= 0, "Filter by length can't be less than zero"
    assert len(args.gc_bounds) <= 2, "GC% range has two restrictions: more and less than something" \
                                     " (e.g. -gc 10 50)"
    if len(args.gc_bounds) == 2:
        assert 0 <= (args.gc_bounds[0] and args.gc_bounds[1]) <= 100, "GC% range must be within 100 %"
    else:
        assert 0 <= args.gc_bounds[0] <= 100, "GC% range must be within 100 %"

    gc_min = args.gc_bounds[0] if len(args.gc_bounds) > 0 else 0
    gc_max = args.gc_bounds[1] if len(args.gc_bounds) > 1 else 100

    if args.SLIDINGWINDOW:
        assert args.SLIDINGWINDOW[1] >= 1, "window in SLIDINGWINDOW cannot be less that 1 nucleotide"
    if args.TRAILING:
        assert args.TRAILING[0] > 0, "sequence quality cannot be less than 1"
    if args.LEADING:
        assert args.LEADING[0] > 0, "sequence quality cannot be less than 1"

    # block which creates pathways for output files
    if args.output_basename is None:
        valid_path = args.input.replace(".fastq", "") + "__passed.fastq"
        non_valid_path = args.input.replace(".fastq", "") + "__failed.fastq"
        stat_summary_path = args.input.replace(".fastq", "") + "__statistics.txt"
    else:
        valid_path = args.output_basename[0] + "__passed.fastq"
        non_valid_path = args.output_basename[0] + "__failed.fastq"
        stat_summary_path = args.output_basename[0] + "__statistics.txt"

    remove(non_valid_path) if path.exists(non_valid_path) else None

    with open(args.input, 'r') as fastq_data, open(valid_path, 'w') as valid_fq:

        for line in fastq_data:
            read = Read(line.strip(), next(fastq_data).strip(), next(fastq_data).strip(), next(fastq_data).strip())

            # statistics update block
            read_report = read_approval_report(read, args.min_length, gc_min, gc_max)
            fastq_statistics = update_statistics_per_read(fastq_statistics, read_report)

            # trimmomatic block
            if args.CROP:
                read = crop(read, args.CROP[0])
            if args.HEADCROP:
                read = headcrop(read, args.HEADCROP[0])
            if args.TRAILING:
                read = trailing(read, args.TRAILING[0])
            if args.LEADING:
                read = leading(read, args.LEADING[0])
            if args.SLIDINGWINDOW:
                read = sliding_window(read, args.SLIDINGWINDOW[0], args.SLIDINGWINDOW[1])

            # read filtering and writing block
            if read_report.read_valid:
                valid_fq.writelines([read.name, '\n', read.sequence, '\n', read.description, '\n', read.quality, '\n'])
            else:
                if args.keep_filtered:
                    with open(non_valid_path, 'a') as non_valid_fq:
                        non_valid_fq.writelines(
                            [read.name, '\n', read.sequence, '\n', read.description, '\n', read.quality, '\n'])
        # statistics summary block
        if args.stat_summary:
            with open(stat_summary_path, 'w') as summary_statistics:
                summary_statistics.writelines(generate_statistics_summary(fastq_statistics))

        print(generate_statistics_summary(fastq_statistics))
