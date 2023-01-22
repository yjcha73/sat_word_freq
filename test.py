from pdfminer.high_level import extract_pages, extract_text
import re
import pandas as pd
import glob

# ~ only text + space
pattern1 = re.compile(r'[a-zA-Z]+\s{1}')
# ~ only text +  punctuation
pattern2 = re.compile(r'[a-zA-Z]+^[a-zA-Z0-9]{1}')
# ~ empty df
df = pd.DataFrame(columns = ['freq'])

for fn in glob.glob(r'./pdfs/*.pdf'):
# ~ for fn in glob.glob(r'.\pdfs\*.pdf'):
    print(fn)
    t = extract_text(fn)
    text = pattern1.findall(t.lower()) + pattern2.findall(t.lower())
    for i in text:
        i = i.replace(' ','').replace('\n','').replace('.','').replace(',','').replace('?','').replace('!','')
        if not i in list(df.index):
            df.loc[i,'freq']=1
        else:
            df.loc[df.index==i,'freq'] += 1

df = df.sort_values(by='freq', ascending=False)
df.to_csv('sat_word_freq.csv')

# ~ hi
