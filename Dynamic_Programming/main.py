import argparse
from .alignment import global_align

def parse_input(path):
    with open(path, 'r') as f:
        seq = f.readline().strip()
    return seq

def main():
    parser = argparse.ArgumentParser()
    align_group = parser.add_mutually_exclusive_group()
    align_group.add_argument('--global_alignment', '-g', action='store_true')
    align_group.add_argument('--local_alignment', '-l', action='store_true')

    parser.add_argument('--read', '-r', required=True, type=parse_input)
    parser.add_argument('--template', '-t', required=True, type=parse_input)
    
    args = parser.parse_args()

    if args.global_alignment:
        forward, trace_back = global_align(args.read, args.template)
        print(forward)

if __name__ == '__main__':
    main()