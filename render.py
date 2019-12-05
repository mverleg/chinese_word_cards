from sys import argv
from typing import List


class Word:
    def __init__(self, chars, pinyin):
        self.chars = chars
        self.pinyin = pinyin

    def __repr__(self):
        return self.chars


def read_words(filename: str) -> List[Word]:
    words = []
    with open(filename, 'r') as fh:
        lines = fh.read().splitlines()
    for line in lines:
        if not line.strip() or ';' not in line:
            continue
        chars, pinyin = line.split(';', maxsplit=2)
        words.append(Word(chars.strip(), pinyin.strip()))
    return words


def collect_pages(words: List[Word], word_per_card=8, card_per_row=3, row_per_page=4) -> List[List[List[List[Word]]]]:
    pages = []
    current_row = []
    current_cards = []
    current_words = []
    for word in words:
        current_words.append(word)
        if len(current_words) >= word_per_card:
            current_cards.append(current_words)
            current_words = []
            if len(current_cards) >= card_per_row:
                current_row.append(current_cards)
                current_cards = []
                if len(current_row) >= row_per_page:
                    pages.append(current_row)
                    current_row = []
    return pages


def to_html_cards(pages: List[List[List[List[Word]]]]) -> str:
    html = [
        '<!DOCTYPE html><html><head>',
        '<title>Chinese cards</title>',
        '<style>',
        '''@page {
           size: A4 portrait;
           margin: 0;
        }
        main {
            font-size: 60%;
            width: 8.2in;
            margin: 0 auto;
        }
        .page {
            page-break-after: always;
        }
        .row {
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
        }
        .card {
            border: 1px solid black;
            flex-basis: 30%;
            flex-grow: 1;
            text-align: center;
            margin: 1em;
            padding: 2em 0;
            display: flex;
        }
        .column {
            flex: 50%;
        }
        .word {
           margin-bottom: 2em;
        }
        .word:last-child {
            margin-bottom: 0;
        }
        .word h1, .word p {
            margin-bottom: 0;
            margin-top: 0;
        }
        ''',
        '</style>',
        '</head><body><main>',
    ]
    for page in pages:
        for row in page:
            html.append("<div class='row'>")
            for card in row:
                html.append("<article class='card'>")
                cols = [
                    ["<div class='column column1'>"],
                    ["<div class='column column2'>"]]
                for k, word in enumerate(card):
                    cols[k % len(cols)].append("<div class='word'>")
                    cols[k % len(cols)].append("<h1 id='chars'>{}</h1>".format(word.chars))
                    cols[k % len(cols)].append("<p id='pinyin'>{}</p>".format(word.pinyin))
                    cols[k % len(cols)].append("</div>")
                for col in cols:
                    html.extend(col)
                    html.append('</div>')
                html.append("</article>")
            html.append("</div>")
            html.append("<div class='page'>&nbsp;</div>")
    html.append("</main></body></html>")
    return '\n'.join(html)


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
    words = read_words('words.csv')
    pages = collect_pages(words)
    html = to_html_cards(pages)
    #outfile = mkstemp(suffix='.html')[1]
    outfile = '/tmp/chinese-cards.html'
    print(outfile)
    with open(outfile, 'w+') as fh:
        fh.write(html)


if __name__ == '__main__':
    main(set(argv[1:]))
