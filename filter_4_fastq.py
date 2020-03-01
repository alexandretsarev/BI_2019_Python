import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--min_length', type=int, required=True)
parser.add_argument('--keep_filtered', action="store_true")
parser.add_argument('--gc_bounds', type=int, nargs='+', required=True)
parser.add_argument('--output_base_name', type=str, required=False)
parser.add_argument('fastq', type=str)

args = parser.parse_args()

assert args.min_length > 0, "min_length < 0. Так дела не делаются."
assert 1 <= len(args.gc_bounds) <= 2, 'Границ может быть либо две либо одна.'

gc_min = args.gc_bounds[0]
if len(args.gc_bounds) == 2:
    gc_max = args.gc_bounds[1]
else:
    gc_max = 100

if args.output_base_name is None:
    output_path = args.fastq[:args.fastq.rindex('.')]
else:
    output_path = args.output_base_name

with open(args.fastq, 'r') as file:
    fastq = file.readlines()


def filter(read, min_length, gc_min, gc_max):
    if len(read) < min_length:
        return 'bad'
    gc_content = len([i for i in read if i in "GC"]) * 100 / len(read)
    if gc_min <= gc_content <= gc_max:
        return 'good'
    else:
        'bad'


pass_path = output_path + '__passed.fastq'
fail_path = output_path + '__failed.fastq'
with open(pass_path, 'w') as passed, open(fail_path, 'w') as failed:
    for i in range(0, len(fastq), 4):
        if filter(fastq[i + 1], args.min_length, gc_min, gc_max) is 'good':
            passed.writelines(fastq[i: i + 4])
        else:
            failed.writelines(fastq[i: i + 4])