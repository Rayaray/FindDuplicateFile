#!/usr/bin/env python
#-*-coding:utf-8-*-

import os
import glob
import time
import pandas as pd
import csv
import configparser


def Get_File_List(search_root, record_file, filter_pattern):
    filter_pass = True
    search_path = search_root + '\**'
    with open(record_file, 'a', newline='', encoding='utf-8') as filelist:
        writer = csv.writer(filelist, delimiter='\t')
        for resultpath in glob.glob(search_path,recursive=True):
            for item in filter_pattern:
                if item in resultpath:
                    filter_pass = False
                    break
                else:
                    filter_pass = True
            
            if filter_pass and os.path.isfile(resultpath):
                split_path=os.path.split(resultpath)
                writer.writerow([split_path[1], split_path[0]])

                
def rank_by_filename(filelist,sorted_filelist, set_mark = '\t'):
    df = pd.read_csv(filelist, sep=set_mark, encoding="utf-8", header=None)
    df = df.sort_values(by=[0, 1], ascending=[1, 1])
    df.to_csv(sorted_filelist, index=False, sep='\t', header=None, encoding = 'utf-8')

def search_duplicate_file(inputlist, outputlist = 'search_result.csv'):
    with open(inputlist, newline='', encoding='utf-8') as fpin, open (outputlist, 'w', newline='', encoding='utf-8') as fpout:
        in_list = csv.reader(fpin, dialect='excel-tab')
        out_list = csv.writer(fpout)
        buffer_line = ['','']
        for row in in_list:
            if row[0] == buffer_line[0]:
                out_list.writerow([row[0],row[1],buffer_line[1]])
            buffer_line = row


cfg = configparser.ConfigParser()
cfg.read('config.ini')
search_root = cfg['search']['Search_Root'].split(',\n')
path_filter = cfg['search']['Filter'].split(',\n')

if not cfg['Result']['Output'].strip():
    outputfile = 'search_result.csv'
else:
    outputfile = cfg['Result']['Output']


current_path = os.getcwd()
filelist = os.path.join(current_path, 'filelist.csv')
sorted_filelist = os.path.join(current_path, 'filelist_sorted.csv')
result_list = os.path.join(current_path, outputfile)

if os.path.isfile(filelist):
    os.remove(filelist)

if os.path.isfile(sorted_filelist):
    os.remove(sorted_filelist)

if os.path.isfile(result_list):
    os.remove(result_list)

start_time_s = time.clock()
print("Start to search, please be patient...")
for item in search_root:
    if os.path.isdir(item):
        Get_File_List(item, filelist, path_filter)
    else:
        print('Invalid path or filter: \n\tPath-->',item, file='search.log')
print("All files are in the list!")
rank_by_filename(filelist, sorted_filelist)
print('All the files are range by their names acsendingly!')
search_duplicate_file(sorted_filelist, result_list)
df = pd.read_csv(result_list, sep=',', encoding="utf-8", header=None)
df = df.sort_values(by=[1, 0], ascending=[1, 1])
df.to_csv(result_list, index=False, sep=',', header=None, encoding = 'utf-8')
print('Search finished!')
print ("Total time: %.2f minutes" %((time.clock()-start_time_s)/60.0))
