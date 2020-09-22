import codecs
import os
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument('--file_path', default=r'../rudrec_markup/predicted_biobert.txt')
    parser.add_argument('--output_path', default='count_predicted_empty_lines.txt')
    args = parser.parse_args()
    file_path = args.file_path
    output_path = args.output_path
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and not output_dir == '':
        os.makedirs(output_dir)

    with codecs.open(file_path, 'r', encoding='utf-8') as inp_file:
        i = 0
        for j, line in enumerate(inp_file):
            line = line.strip()
            if line == "":
                i += 1
        with codecs.open(output_path, 'w+', encoding='utf-8') as output_file:
            output_file.write(f"empty lines: {i}\n"
                              f"all lines: {j + 1}\n")

if __name__ == '__main__':
    main()
