#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:34:37 2022

@author: oscarmejias
"""
#%%
import pandas as pd
import db

#%%
df = pd.DataFrame.from_records(db.data.find())


#%%

#df1 = pd.DataFrame(list(zip(a, b)))

class WrappedDataFrame:
    def __init__(self, df):
        self._df = df
        self._update_computed_columns()

    def _update_computed_columns(self):
        # Define all your computed columns
        self._df['densidad'] = self._df['masa'] / self._df['volumen']

    @property
    def df(self):
        self._update_computed_columns()
        return self._df
    
df1 = WrappedDataFrame(df)
# %%
