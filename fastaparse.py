import re
from pathlib import Path
from typing import Dict, List

mass_table = {
    "A": 71.03711,
    "C": 103.00919,
    "D": 115.02694,
    "E": 129.04259,
    "F": 147.06841,
    "G": 57.02146,
    "H": 137.05891,
    "I": 113.08406,
    "K": 128.09496,
    "L": 113.08406,
    "M": 131.04049,
    "N": 114.04293,
    "P": 97.05276,
    "Q": 128.05858,
    "R": 156.10111,
    "S": 87.03203,
    "T": 101.04768,
    "V": 99.06841,
    "W": 186.07931,
    "Y": 163.06333,
}

rna_codon_table = {
    "UUU": "F",
    "UUC": "F",
    "UUA": "L",
    "UUG": "L",
    "UCU": "S",
    "UCC": "S",
    "UCA": "S",
    "UCG": "S",
    "UAU": "Y",
    "UAC": "Y",
    "UAA": "STOP",
    "UAG": "STOP",
    "UGU": "C",
    "UGC": "C",
    "UGA": "STOP",
    "UGG": "W",
    "CUU": "L",
    "CUC": "L",
    "CUA": "L",
    "CUG": "L",
    "CCU": "P",
    "CCC": "P",
    "CCA": "P",
    "CCG": "P",
    "CAU": "H",
    "CAC": "H",
    "CAA": "Q",
    "CAG": "Q",
    "CGU": "R",
    "CGC": "R",
    "CGA": "R",
    "CGG": "R",
    "AUU": "I",
    "AUC": "I",
    "AUA": "I",
    "AUG": "M",
    "ACU": "T",
    "ACC": "T",
    "ACA": "T",
    "ACG": "T",
    "AAU": "N",
    "AAC": "N",
    "AAA": "K",
    "AAG": "K",
    "AGU": "S",
    "AGC": "S",
    "AGA": "R",
    "AGG": "R",
    "GUU": "V",
    "GUC": "V",
    "GUA": "V",
    "GUG": "V",
    "GCU": "A",
    "GCC": "A",
    "GCA": "A",
    "GCG": "A",
    "GAU": "D",
    "GAC": "D",
    "GAA": "E",
    "GAG": "E",
    "GGU": "G",
    "GGC": "G",
    "GGA": "G",
    "GGG": "G",
}


def parse(path_to_file: str) -> Dict:
    resulting_dict = {}
    path = Path(path_to_file)
    seq = []
    seq_id = ""
    if not path.is_file():
        print("Error, such file doesn't exist")
        return resulting_dict
    with path.open() as file:
        for line in file:
            if line.startswith(">"):
                if seq_id:
                    resulting_dict[seq_id] = "".join(seq)
                seq_id = line.strip()[1::]
                seq = []
            else:
                seq.append(line.strip())
            resulting_dict[seq_id] = "".join(seq)

    return resulting_dict


def translate(rna_seq: str) -> str:
    prot = []
    start = rna_seq.find("AUG")
    for i in range(start + 3, len(rna_seq), 3):
        base = rna_seq[i:i + 3]
        if base in ["UAA", "UAG", "UGA"]:
            return "".join(prot)
        else:
            prot.append(rna_codon_table[base])


def calc_mass(protein: str) -> float:
    mass = 0
    for aa in protein:
        mass += mass_table[aa]
    return mass


def orf(rna_seq: str) -> List:
    prots = []
    starts = [m.start() for m in re.finditer("AUG", rna_seq)]
    for start in starts:
        prot = []
        for i in range(start, [m.start() for m in re.finditer(r"UAA|UAG|UGA", rna_seq)][-1] + 1, 3):
            base = rna_seq[i:i + 3]
            if base in ["UAA", "UAG", "UGA"]:
                prots.append(prot)
                break
            else:
                prot.append(rna_codon_table[base])
    return sorted(["".join(i) for i in prots])
