#!/usr/bin/env python

import unittest

from ..filter_2_fastq import len_read, gc_content_count, read_approval


class FilterTest(unittest.TestCase):

    def test_len_sequence(self):
        self.assertEqual(len_read("GCAT"), 4)

    def test_len_sequence_zero_length(self):
        self.assertEqual(len_read(""), 0)

    def test_gc_content_count(self):
        self.assertEqual(gc_content_count("GCAT"), 50)

    def test_gc_content_count_zero_GC(self):
        self.assertEqual(gc_content_count("ATATATATA"), 0)

    def test_gc_content_read_approval_no_thresholds(self):
        self.assertEqual(read_approval("AGATA", 0, 0, 100), True)

    def test_gc_content_read_approval_length_filter(self):
        self.assertEqual(read_approval("ATATGCGC", 20, 1, 100), False)

    def test_gc_content_read_approval_gc_filter(self):
        self.assertEqual(read_approval("ATATGCGC", 0, 70, 100), False)

    def test_gc_content_read_approval_length_gc_filter(self):
        self.assertEqual(read_approval("ATATGCGC", 50, 70, 100), False)


if __name__ == '__main__':
    unittest.main()
