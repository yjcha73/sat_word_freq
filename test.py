from pdfminer.high_level import extract_pages, extract_text
import re
import pandas as pd
import glob
import string
import dev.attempt2 as juwon

def word_count_text(t):
    # ~ only text + space
    pattern1 = re.compile(r'[a-zA-Z]+\s{1}')
    # ~ empty df
    df = pd.DataFrame(columns = ['freq'])

    t = re.sub(pattern=r'[^\w]', repl=' ', string=t.lower())
    text = t.split()
    text = pattern1.findall(t.lower()) 
    
    for i in text:
        i = i.replace(' ','')
        if not i in list(df.index):
            df.loc[i,'freq']=1
        else:
            df.loc[df.index==i,'freq'] += 1

    df = df.sort_values(by='freq', ascending=True)
    return t, text, df

def word_count_pdf(fn):
    print(fn)
    t = extract_text(fn)
    return word_count_text(t)

if __name__ == '__main__':
    pic_file = r'pdfs\2021 March SAT QAS.pdf'
    # txt = juwon.get_full_text(pic_file)

    t, text, df = word_count_pdf(r'pdfs\April 2018 School Day SAT QAS Full Test.pdf')
    # t, text, df = word_count_text(pic_file)
    print(t[0:200])
    print(f'text: {text}')
    print(df.head())
    df.to_csv(r'freq.csv')