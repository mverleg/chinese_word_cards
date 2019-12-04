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
    pages = []
    current_cards = []
    current_words = []
    for line in lines:
        if ';' not in line:
            continue
        current_words.append(line)
        if len(current_words) >= 6:
            current_cards.append(current_words)
            current_words = []
            if len(current_cards) >= 9:
                pages.append(current_cards)
                current_cards = []
    print(pages)
    html.append("</body></html>")


if __name__ == '__main__':
    main(set(argv[1:]))
