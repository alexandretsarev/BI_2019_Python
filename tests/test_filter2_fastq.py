#!/usr/bin/env python

import unittest

from ..filter_2_fastq import length_read, gc_content_count, quality_decipher, crop, headcrop, trailing, leading, \
    sliding_window, read_approval_report, update_statistics_per_read, generate_statistics_summary
from collections import namedtuple

# named tuples for testing
Read = namedtuple('read', ['name', 'sequence', 'description', 'quality'])
Read_report = namedtuple('read_report', ['read_valid', 'length_valid', 'gc_content_valid'])

# test reads
test_read_1 = Read("@SRR521461.17063732",
                   "AGAGCATTTTAAGAGGTGCAGCCTCTGGAAGTGGATCAAACTAGAACTCATATGCCATACTAGATATGTTTGTCAA",
                   "+", "GGGGGGGGGFGGGGGGGFGGEGGGGGGGGGFFGGGGGFGGGGGGFGGFGGGGFFEEGGGBDDDBEEFEEEDEE=ED")
test_read_2 = Read("@SRR521461.17063732", "", "+", "")
test_read_3 = Read("@SRR521461.17063732", "GGGGAAAATTTTCCCC", "+", "GGGGGGGGGGGG")


class FilterTest(unittest.TestCase):

    def test_len_sequence(self):
        self.assertEqual(length_read(test_read_1), 76)

    def test_len_sequence_zero(self):
        self.assertEqual(length_read(test_read_2), 0)

    def test_gc_content_count(self):
        self.assertEqual(gc_content_count(test_read_3), 50)

    def test_gc_content_count_zero(self):
        self.assertEqual(gc_content_count(test_read_2), 0)

    def test_gc_quality_decipher(self):
        self.assertEqual(quality_decipher(test_read_3), [38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38])

    def test_crop_sequence(self):
        self.assertEqual(crop(test_read_1, 35).sequence, "AGAGCATTTTAAGAGGTGCAGCCTCTGGAAGTGGA")

    def test_crop_sequence_2(self):
        self.assertEqual(crop(test_read_1, 1).sequence, "A")

    def test_crop_quality(self):
        self.assertEqual(crop(test_read_1, 35).quality, "GGGGGGGGGFGGGGGGGFGGEGGGGGGGGGFFGGG")

    def test_crop_quality_2(self):
        self.assertEqual(crop(test_read_1, 1).quality, "G")

    def test_headcrop_sequence(self):
        self.assertEqual(headcrop(test_read_1, 35).sequence, "TCAAACTAGAACTCATATGCCATACTAGATATGTTTGTCAA")

    def test_headcrop_quality(self):
        self.assertEqual(headcrop(test_read_1, 35).quality, "GGFGGGGGGFGGFGGGGFFEEGGGBDDDBEEFEEEDEE=ED")

    def test_trailing_sequence(self):
        self.assertEqual(trailing(test_read_1, 37).sequence, "AGAGCATTTTAAGAGGTGCA")

    def test_trailing_quality(self):
        self.assertEqual(trailing(test_read_1, 37).quality, "GGGGGGGGGFGGGGGGGFGG")

    def test_leading_sequence(self):
        self.assertEqual(leading(test_read_1, 35).sequence, "CAA")

    def test_leading_quality(self):
        self.assertEqual(leading(test_read_1, 35).quality, "=ED")

    def test_sliding_window_sequence(self):
        self.assertEqual(sliding_window(test_read_1, 38, 5).sequence, "AGAGC")

    def test_sliding_window_quality(self):
        self.assertEqual(sliding_window(test_read_1, 38, 5).quality, "GGGGG")

    def test_read_approval_report_1(self):
        self.assertEqual(read_approval_report(test_read_1, 3, 1, 50), Read_report(False, True, True))

    def test_read_approval_report_2(self):
        self.assertEqual(read_approval_report(test_read_2, 3, 1, 50), Read_report(True, False, False))

    def test_update_statistics_per_read_1(self):
        self.assertEqual(update_statistics_per_read({"n_total": 0,
                                                     "n_failed_by_length": 0,
                                                     "n_failed_by_gc_content": 0,
                                                     "n_failed": 0,
                                                     "n_valid": 0}, Read_report(True, 0, 0)),
                         {'n_total': 1, 'n_failed_by_length': 0, 'n_failed_by_gc_content': 0, 'n_failed': 0,
                          'n_valid': 1})

    def test_update_statistics_per_read_2(self):
        self.assertEqual(update_statistics_per_read({"n_total": 0,
                                                     "n_failed_by_length": 0,
                                                     "n_failed_by_gc_content": 0,
                                                     "n_failed": 0,
                                                     "n_valid": 0},
                                                    Read_report(True, 1, 0)),
                         {'n_total': 1, 'n_failed_by_length': 1, 'n_failed_by_gc_content': 0, 'n_failed': 0,
                          'n_valid': 1})

    def test_update_statistics_per_read_3(self):
        self.assertEqual(update_statistics_per_read({"n_total": 0,
                                                     "n_failed_by_length": 0,
                                                     "n_failed_by_gc_content": 0,
                                                     "n_failed": 0,
                                                     "n_valid": 0},
                                                    Read_report(True, 1, 1)),
                         {'n_total': 1, 'n_failed_by_length': 1, 'n_failed_by_gc_content': 1, 'n_failed': 0,
                          'n_valid': 1})

if __name__ == '__main__':
    unittest.main()
