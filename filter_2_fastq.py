#!/usr/bin/env python

from collections import namedtuple
import argparse
from os import path, remove

# read and read report structures
Read = namedtuple('read', ['name', 'sequence', 'description', 'quality'])
ReadReport = namedtuple('read_report', ['read_valid', 'length_valid', 'gc_content_valid'])

# summary statistics of the whole fastq file in the beginning
fastq_statistics = {"n_total": 0,
                    "n_failed_by_length": 0,
                    "n_failed_by_gc_content": 0,
                    "n_failed": 0,
                    "n_valid": 0}


def length_read(input_read: Read) -> int:
    return len(input_read.sequence)


def gc_content_count(input_read: Read) -> int:
    return (input_read.sequence.count('G') + input_read.sequence.count('C')) / len(input_read.sequence) * 100 \
        if len(input_read.sequence) != 0 else 0


def crop(inputread: Read, threshold: int) -> Read:
    return Read(inputread.name, inputread.sequence[:threshold], inputread.description, inputread.quality[:threshold])


def headcrop(input_read: Read, threshold: int) -> Read:
    return Read(input_read.name, input_read.sequence[threshold:], input_read.description,
                input_read.quality[threshold:])


def quality_decipher(input_read: Read) -> list:
    return list(map(lambda ascii_symbol: ord(ascii_symbol) - 33, input_read.quality))


def trailing(input_read: Read, threshold: int) -> Read:
    read_quality = quality_decipher(input_read)
    cut_position = next((idx for idx, nucl_quality in enumerate(read_quality) if nucl_quality < threshold), None)
    return crop(input_read, cut_position)


def leading(input_read: Read, threshold: int) -> Read:
    read_quality = quality_decipher(input_read)
    cut_position = length_read(input_read) - next((idx + 1 for idx, nucl_quality in enumerate(read_quality[::-1])
                                                   if nucl_quality < threshold), None)
    return headcrop(input_read, cut_position)


def sliding_window(input_read: Read, threshold: int, window_size: int) -> Read:
    read_quality = quality_decipher(input_read)
    cut_position = next(
        (idx for idx in range(len(read_quality) - window_size + 1) if
         sum(read_quality[idx:idx + window_size]) / window_size < threshold), None)
    return crop(input_read, cut_position)


def read_approval_report(input_read: Read, min_length: int, gc_min: int, gc_max: int) -> ReadReport:
    length_not_valid = length_read(input_read) < min_length
    gc_content_not_valid = gc_min > gc_content_count(input_read) < gc_max
    read_valid = not length_not_valid and not gc_content_not_valid
    return ReadReport(read_valid, length_not_valid, gc_content_not_valid)


def update_statistics_per_read(statistics_dict: dict, one_read_report: ReadReport) -> dict:
    statistics_dict['n_total'] += 1
    statistics_dict['n_failed_by_length'] += one_read_report.length_valid
    statistics_dict['n_failed_by_gc_content'] += one_read_report.gc_content_valid
    statistics_dict['n_valid'] += 1 if one_read_report.read_valid else 0
    statistics_dict['n_failed'] += 1 if not one_read_report.read_valid else 0
    return statistics_dict


def generate_statistics_summary(statistics_dict: dict) -> str:
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

    parser = argparse.ArgumentParser(
        usage='./filter_2_fastq.py example.fastq --min_length 20 --gc_bounds 12 95 --slidingwindow 20 5 --headcrop 5 '
              '--crop 25 --keep_filtered --stat_summary  --output_basename ./path_to_directory/processed_file',
        description='it works only with phred33 quality!', )
    parser.add_argument('input', help="input fastq file")
    parser.add_argument('--min_length', type=int, default=0, metavar='', help='minimal length')
    parser.add_argument('--gc_bounds', nargs='+', type=int, metavar='', help='percent range of GC '
                                                                             'content')
    parser.add_argument('--output_basename', type=str, help='path to output file', metavar='')
    parser.add_argument('--keep_filtered', action="store_true", help='keep filtered reads in a separate file')
    parser.add_argument('--stat_summary', action="store_true", help='keep summary statistics in file')
    parser.add_argument('--crop', nargs=1, type=int, metavar='',
                        help='cut the read to a specified length by removing bases from the end')
    parser.add_argument('--headcrop', nargs=1, type=int, metavar='',
                        help='cut the specified number of bases from the start of the read')
    parser.add_argument('--trailing', nargs=1, type=int, metavar='',
                        help='cut bases off the end of a read, if below a threshold quality')
    parser.add_argument('--leading', nargs=1, type=int, metavar='',
                        help='cut bases off the start of a read, if below a threshold quality')
    parser.add_argument('--slidingwindow', nargs=2, type=int, metavar='',
                        help='it takes 2 arguments quality and window size and performs a sliding window trimming '
                             'approach. It starts scanning at the 5-prime end and clips the read once the average '
                             'quality within the window falls below a threshold')
    args = parser.parse_args()

    # assertion block
    assert args.min_length >= 0, "Filter by length can't be less than zero"

    if args.gc_bounds:
        assert len(args.gc_bounds) <= 2, "GC% range has two restrictions: more and less than something e.g. 10 50)"
        gc_min = args.gc_bounds[0]
        if len(args.gc_bounds) == 2:
            gc_max = args.gc_bounds[1]
            assert 0 <= (gc_min and gc_max) <= 100, "GC% range must be within 100 %"
        else:
            assert 0 <= gc_min <= 100, "GC% range must be within 100 %"
    else:
        gc_min, gc_max = 0, 100

    if args.slidingwindow:
        assert args.slidingwindow[1] >= 1, "window in slidingwindow cannot be less that 1 nucleotide"
    if args.trailing:
        assert args.trailing[0] > 0, "sequence quality cannot be less than 1"
    if args.leading:
        assert args.leading[0] > 0, "sequence quality cannot be less than 1"

    # block which creates pathways for output files
    if args.output_basename is None:
        basename = path.splitext(path.basename(args.input))[0]
    else:
        basename = args.output_basename
    valid_path = basename + "__passed.fastq"
    non_valid_path = basename + "__failed.fastq"
    stat_summary_path = basename + "__statistics.txt"

    remove(non_valid_path) if path.exists(non_valid_path) else None
    # I do that because non_valid_path file is open with 'a' mode

    with open(args.input, 'r') as fastq_data, open(valid_path, 'w') as valid_fq:

        for line in fastq_data:
            read = Read(line.strip(), next(fastq_data).strip(), next(fastq_data).strip(), next(fastq_data).strip())

            # statistics update block
            read_report = read_approval_report(read, args.min_length, gc_min, gc_max)
            fastq_statistics = update_statistics_per_read(fastq_statistics, read_report)

            # trimmomatic block
            if args.crop:
                read = crop(read, args.crop[0])
            if args.headcrop:
                read = headcrop(read, args.crop[0])
            if args.trailing:
                read = trailing(read, args.trailing[0])
            if args.leading:
                read = leading(read, args.leading[0])
            if args.slidingwindow:
                read = sliding_window(read, args.slidingwindow[0], args.slidingwindow[1])

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
