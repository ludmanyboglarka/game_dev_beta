# importing packages
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import warnings
import dplython as dpy 

raw_data = pd.read_csv("data/edge1.1.csv")
# print(raw_data.head())

#' ------------------------------------------------
#' 0. DATA PREPARATION
#' removing unnecessary variables, creating `PercentByAuthor`
#' main source: multiverse_gamedev2.Rmd 
#' ((( since i am translating R code to Python (and therefore using R logic instead of python logic), code might be sloppy )))
#' ------------------------------------------------

dropped_cols = raw_data.loc[:, "Order":"Number.Characters"].columns
raw_data = (
    raw_data
    .drop(columns=dropped_cols)
)

group_keys = ["ThreadId", "Id"] #grouping colnames

slice_cols = raw_data.loc[:, "Type":"ContributionsbyAuthor"].columns #in order for slice_cols to be a list -> this can be cut out
grouped_cols = slice_cols.difference(group_keys, sort=False) #in tidyverse terms: select(Type:ContributionsbyAuthor, -ThreadId, -Id)

summary = (
    raw_data
    .groupby(group_keys)[grouped_cols]
    .agg(lambda s: "; ".join(s.fillna("NA").astype(str).unique()))
    .reset_index() # note to self: turns grouping variables back to cols
)

print(raw_data.columns)

