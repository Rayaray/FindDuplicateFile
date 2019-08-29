#!/usr/bin/env python
#-*-coding:utf-8-*-
import pandas as pd
def rank_by_filename(filelist,sorted_filelist):
    df = pd.read_csv(filelist, sep='\t', encoding="utf-8", header=None)
    df = df.sort_values(by=[0, 1], ascending=[1, 1])
    df.to_csv(sorted_filelist, index=False, sep='\t', header=None, encoding = 'utf-8')

        