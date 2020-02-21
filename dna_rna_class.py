class nucl_acid:
    def __init__(self, seq):
        valid_nucl = ("A", "T", "G", "C", "U")
        seq = seq.upper()

        if all(nucl in valid_nucl for nucl in list(seq)):
            self.seq = seq
        else:
            raise Exception("your sequence contains inappropriate symbols")

    def gc_content(self):  # GC content in %
        gc_con = round((self.seq.count("G") + self.seq.count("C") / len(self.seq) * 100), ndigits=2)
        return gc_con

    def __eq__(self, other):
        return self.seq == other


class dna(nucl_acid):

    def reverse_complement(self):  # reverse DNA-DNA complement
        complement_dna_dna = {"A": "T", "T": "A", "G": "C", "C": "G"}
        if 'U' not in self.seq:
            revcomseq = ''.join(complement_dna_dna[nucl] for nucl in self.seq[::-1])
            return revcomseq
        else:
            raise Exception("your DNA has uridin, you cannot apply DNA methods this item")

    def transcribe(self):  # transcription from DNA(+)
        complement_dna_rna = {"A": "U", "T": "A", "G": "C", "C": "G"}
        if 'U' not in self.seq:
            rna_seq = ''.join(complement_dna_rna[nucl] for nucl in self.seq)
            return rna_seq
        else:
            raise Exception("your DNA has uridin, you cannot apply DNA methods this item")


class rna(dna):
    def reverse_complement(self):  # reverse transcription from RNA

        complement_rna_dna = {"A": "T", "U": "A", "G": "C", "C": "G"}
        if 'T' not in self.seq:
            revcomseq_dna = ''.join(complement_rna_dna[nucl] for nucl in self.seq[::-1])
            return revcomseq_dna
        else:
            raise Exception("your RNA has thymine, you cannot apply RNA methods this item")

