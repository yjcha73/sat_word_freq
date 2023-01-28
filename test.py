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
    # text = t.split()
    text = pattern1.findall(t) 
    
    for i in text:
        i = i.replace(' ','')
        if not i in list(df.index):
            df.loc[i,'freq']=1
        else:
            df.loc[df.index==i,'freq'] += 1

    df = df.sort_values(by='freq', ascending=False)
    return t, text, df

def word_count_pdf(fn):
    t = juwon.get_full_text(fn)
    return word_count_text(t)

def merge_freq(df1, df2):
    df1 = df1.rename(columns = {'freq':'freq1'})
    df2 = df2.rename(columns = {'freq':'freq2'})

    df = df1.join(df2, how = 'outer')
    df = df.fillna(0)
    df['freq'] = df.freq1 + df.freq2
    df = df[['freq']]
    return df
    

if __name__ == '__main__':
   
    files = [r'pdfs\2021 March SAT QAS.pdf',r'pdfs\April 2018 School Day SAT QAS Full Test.pdf']
    t = []
    text = []
    df = []
    for file in files:
        print(file)
        temp_t, temp_text, temp_df = word_count_pdf(file)
        # temp_t, temp_text, temp_df = word_count_text(file)
        t.append(temp_t)
        text.append(temp_text)
        df.append(temp_df)
    df_final = merge_freq(df[0], df[1])
    # print(f'df[0]: {df[0]}')
    # print(f'df[1]: {df[1]}')
    # print(f'df_final: {df_final}')
    
    
    df_final.to_excel('text.xlsx', sheet_name = 'df_final')
    with pd.ExcelWriter('text.xlsx', mode='a') as writer:
        df[0].to_excel(writer, sheet_name = 'df0')
        df[1].to_excel(writer, sheet_name = 'df1')
    