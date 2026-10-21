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

particip_data_duplicates = (
    raw_data
    .groupby(group_keys)[grouped_cols]
    .agg(lambda s: "; ".join(s.fillna("NA").astype(str).unique()))
    .reset_index() # note to self: turns grouping variables back to cols
)

particip_data_filt = (
    particip_data_duplicates
    .loc[lambda df: df[grouped_cols].apply(lambda col: col.str.contains(";", regex=False)).any(axis=1)] 
    .reset_index(drop=True)
)

# HERE: ANTI_JOIN 
# first: flag where the raw_data cols and rows don't match the ones in particip_data_filt, then: drop those rows
raw_data = (
    raw_data
    .merge(right=particip_data_filt[["ThreadId", "Id"]].drop_duplicates(), on=["ThreadId", "Id"], how="left", indicator=True)
    .loc[lambda df: df["_merge"] == "left_only"]
    .drop(columns="_merge")
)

# TODO: 
# PERCENT_BY_AUTHOR 
raw_data = (
    raw_data
    .assign(lambda df)
)

particip_data_clean = (
    raw_data
    # .drop(columns=dropped_cols)
    .groupby(group_keys)[grouped_cols]
    .agg(lambda s: list(s.unique()))
    .reset_index()
)

raw_data_n = raw_data.drop(columns="Live")
agg_cols = (raw_data.loc[:, "Type":"UniqueFemaleParticipation"].columns
            .difference(group_keys, sort=False))

raw_data_n = (
    raw_data
    .groupby(group_keys)[agg_cols]
    .agg(lambda s: list(s.unique()))
    .reset_index()
)

print(raw_data.columns)

