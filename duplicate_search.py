#!/use/bin/env python
#-*-coding:utf-8-*-
import csv
def search_duplicate_file(inputlist, outputlist = 'search_result.csv'):
    with open(inputlist, newline='', encoding='utf-8') as fpin, open (outputlist, 'w', newline='', encoding='utf-8') as fpout:
        in_list = csv.reader(fpin, dialect='excel-tab')
        out_list = csv.writer(fpout)
        buffer_line = ['','']
        for row in in_list:
            if row[0] == buffer_line[0]:
                out_list.writerow([row[0],row[1],buffer_line[1]])
            buffer_line = row