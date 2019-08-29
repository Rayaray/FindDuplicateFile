import glob
import os
import csv
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
#                writer.writerow(os.path.split(resultpath))
#                record_file.write(os.path.basename(resultpath))
#                record_file.write('\t')
#                record_file.write(os.path.dirname(resultpath))
#                record_file.write('\n')