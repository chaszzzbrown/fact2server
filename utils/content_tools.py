'''
import xlrd

FNAME = 'content_tracking_cb.xls'

book = xlrd.open_workbook(FNAME)
sheet = book.sheets()[1]
'''

content = []

'''
def capture_to_dict():

    rows = (sheet.row(rn) for rn in range(4, sheet.nrows) if sheet.cell(rn,0).value)

    for row in rows:
        content.append( {
            'headline': row[1].value,
            'source_URL': row[2].value,
            'full_text': row[3].value,
            'additional_info': row[4].value,
            } )
'''

import json
import os
import re

try:
    from articles.models import Article
except ImportError:
    pass

def parse_full_text(article):
    body = article['full_text'].strip()

    if '//' in body:
        ptype = 'slashed'
        chunks = body.split('//')
    elif '\n\n' in body:
        ptype = 'double n'
        chunks = body.split('\n\n')
    elif '\n' in body:
        ptype = 'single n'
        chunks = body.split('\n')
    else:
        ptype = 'none'
        chunks = (body.replace('. ', '.\n\n').replace(u'.\u201d', u'.\u201d\n\n')).split('\n\n')

    chunks = [chunk.strip() for chunk in chunks]
    
    chunk1 = chunks[0]
    if len(chunks)==2:
        chunk2 = chunks[1]
        chunk3 = ''
    else :
        ix = (len(chunks)-1)/2 + 1
        chunk2 = '\n\n'.join(chunks[1:ix])
        chunk3 = '\n\n'.join(chunks[ix:])

    article['chunk1'] = chunk1
    article['chunk2'] = chunk2
    article['chunk3'] = chunk3
    
    article['ptype'] = ptype    
        
def split_info(article):
    tags = {
        'source': 'Source:',
        'references': 'Named sources or checkable facts:',
        'author': 'Author:',
        'tone': 'Tone:',
        }

    def index_(pat,s):
        try:
            return s.index(pat)
        except ValueError:
            return len(s)

    info = article['additional_info']

    items = []
    for k, pat in tags.items():
        items.append((index_(pat, info), k, pat))
    items = sorted(items, cmp=lambda a,b: a[0]-b[0])

    res = {}
    for ix, item in enumerate(items):
        try:
            span = info[item[0]+len(item[2]):items[ix+1][0]]
        except IndexError:
            span = info[item[0]+len(item[2]):]
        res[item[1]] = span.strip()

    pat = re.compile(r'\s*\(.+?\)')
    match = pat.match(res['tone'])
    if match:
        res['tone'] = (res['tone'][match.end():]).strip()

    article.update(res)

    return res

def collect_tones():

    tones = set()
    for article in content:
        tones.add(article['tone'])
    return tones

def create_articles():
    
    for article_info in content:
        article = Article()
        for key in article_info:
            try:
                setattr(article, key, article_info[key])
            except AttributeError:
                pass
        article.save()

if __name__=='__main__':
    with open('content.json', 'r') as f:
        content = json.load(f)
else:
    with open('utils/content.json', 'r') as f:
        content = json.load(f)
    




    
