from sys import argv


def main(args):
    pinyin = None
    if 'pinyin' in args:
        pinyin = True
    elif 'nopinyin' in args:
        pinyin = False
    else:
        raise Exception("provide either 'pinyin' or 'nopinyin' as argument")
    with open('words.csv', 'r') as fh:
        lines = fh.read().splitlines()
    html = ["<!DOCTYPE html><html><body>"]
    word_blocks = []
    current_block = []
    for line in lines:
        if ';' not in line:
            continue
        current_block.append(line)
        if len(current_block) >= 6:
            word_blocks.append(current_block)
            current_block = []
    print(word_blocks)
    html.append("</body></html>")


if __name__ == '__main__':
    main(set(argv[1:]))
