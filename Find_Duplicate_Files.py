import path_handler
import os
import time
import csv_rank
import duplicate_search
import configparser
import pandas as pd

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
        path_handler.Get_File_List(item, filelist, path_filter)
    else:
        print('Invalid path or filter: \n\tPath-->',item, file='search.log')
print("All files are in the list!")
csv_rank.rank_by_filename(filelist, sorted_filelist)
print('All the files are range by their names acsendingly!')
duplicate_search.search_duplicate_file(sorted_filelist, result_list)
df = pd.read_csv(result_list, sep=',', encoding="utf-8", header=None)
df = df.sort_values(by=[1, 0], ascending=[1, 1])
df.to_csv(result_list, index=False, sep=',', header=None, encoding = 'utf-8')
print('Search finished!')
print ("Total time: %.2f minutes" %((time.clock()-start_time_s)/60.0))
