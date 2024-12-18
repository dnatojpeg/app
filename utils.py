## This file contains utility functions that are used in the main application code.
def parse_fasta(content: str) -> str:
    lines = content.strip().split('\n')
    seq_lines = [line.strip() for line in lines if not line.startswith('>')]
    return ''.join(seq_lines)
