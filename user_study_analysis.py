import sys
import csv
import math
import pandas as pd

delta = 1e-15
study_score_range = range(1, 6) # 1 = least relevent, 5 = most relevent

def read_dataset (ds_file):
  df = pd.read_csv(ds_file, sep='\t')
  return df.to_dict(orient='records')


def get_dataset_for_method (ds, method):
  dsm = ds
  if method != "All":
    dsm = [r for r in ds if r["Method"] == method or r["Method"] == "Both"]
  return dsm


def compute_precision (ds, method, minUserScore, rank_col):
  dsm = get_dataset_for_method(ds, method)

  dsma = dsm
  if rank_col == "ComputedRankGlobal":
    dsma = ds

  dsm_ranked = [r for r in dsma if not math.isnan(r[rank_col])]
  dsm_ranked_p = [r for r in dsm if (not math.isnan(r[rank_col])) and r["StudyScore"] >= minUserScore]

  return len(dsm_ranked_p) / len(dsm_ranked)


def compute_ndcg (ds, method, rank_col):
  dsm = get_dataset_for_method(ds, method)
  queries = list(set([dsm_i["PaperId"] for dsm_i in dsm]))

  # takes a list of tuples of the form: (score, rank)
  def _get_dcg (tup):
    return sum([(2**t[0] - 1) / math.log(t[1] + 1, 2) for t in tup])

  ndcg = 0
  i = 0
  for q in queries:
    qdsm = [r for r in dsm if r["PaperId"] == q and not math.isnan(r[rank_col])]
    dcg_ranks = [(r["StudyScore"], r[rank_col]) for r in qdsm]
    dcg = _get_dcg(dcg_ranks)

    scores = [r["StudyScore"] for r in qdsm]
    scores.sort(reverse=True)
    idcg_ranks = [(scores[i], i+1) for i in range(len(scores))]
    idcg = _get_dcg(idcg_ranks)
    if (not math.isnan(idcg)) and idcg > 0:
      ndcg += (dcg / idcg)
      i += 1
  return ndcg / i

def bin_simiarty_with_score (ds, method, bin_col):
  dsm = get_dataset_for_method(ds, method)
  
  bins = [[0,0,0,0,0] for _ in study_score_range]
  for score in study_score_range:
    dsm_for_score = [dsm_i[bin_col] for dsm_i in dsm if dsm_i["StudyScore"] == score]
    for v in dsm_for_score:
      if 0.6 <= v < 0.7:
        bins[score - 1][0] += 1
      elif 0.7 <= v < 0.75:
        bins[score - 1][1] += 1
      elif 0.75 <= v < 0.8:
        bins[score - 1][2] += 1
      elif 0.8 <= v < 0.9:
        bins[score - 1][3] += 1
      elif 0.9 <= v:
        bins[score - 1][4] += 1
  return bins


def print_survey_stats (ds):
  dsm = [r for r in ds if (not math.isnan(r["StudyScore"])) and r["StudyScore"] > 0]
  dsm_b = [r for r in dsm if r["Method"] == "Behavior"]
  dsm_c = [r for r in dsm if r["Method"] == "Content"]
  dsm_t = [r for r in dsm if r["Method"] == "Both"]
  print (f'Method: All, Recommendation Pairs = {len(dsm)}')
  print (f'Method: Behavior, Recommendation Pairs = {len(dsm_b)}')
  print (f'Method: Content, Recommendation Pairs = {len(dsm_c)}')
  print (f'Method: Both, Recommendation Pairs = {len(dsm_t)}')

def print_bin_stats (bins, method, bin_col):
  for score in study_score_range:
    print ( '\nUser Score Bins ------------------------------------------- ')
    print (f'  Method: {method} | Binning column: {bin_col}')
    print (f'  User generated score = {score}\n')
    print (f'  [0.6, 0.7) = {bins[score - 1][0]}')
    print (f'  [0.7, 0.75) = {bins[score - 1][1]}')
    print (f'  [0.75, 0.8) = {bins[score - 1][2]}')
    print (f'  [0.8, 0.9) = {bins[score - 1][3]}')
    print (f'  [0.9, 1)   = {bins[score - 1][4]}')
    print ( ' -----------------------------------------------------------\n')

def print_precision_stats (precisionAt10, method, minUserScore, rank_col):
  print ( '\nPrecision@10 ---------------------------------------------- ')
  print (f'  Method: {method} | Min. User Score: {minUserScore} | Rank Column: {rank_col}')
  print (f'  Precision@10 = {precisionAt10}')
  print ( ' -----------------------------------------------------------\n')

def print_ndcg_stats (ndcg, method, rank_col):
  print ( '\nAverage nDCG --------------------------------------------- ')
  print (f'  Method: {method} | Rank Column: {rank_col} ')
  print (f'  nDCG = {ndcg}')
  print ( ' -----------------------------------------------------------\n')

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print ("Usage: python ./BinSimilarityWithScore.py <result_dataset.tsv> (Results should be tab separated)")

  ds = read_dataset(sys.argv[1])

  print_survey_stats(ds)

  bin_params_list = [
    {"method": "Content", "bin_col":"Similarity"},
    {"method": "Content", "bin_col":"EmbSimilarity"},
    {"method": "Content", "bin_col":"TfIdfSimilarity"},
    {"method": "Behavior", "bin_col":"Similarity"},
    {"method": "All", "bin_col":"Similarity"} ]
  
  for bin_params in bin_params_list:
    bins = bin_simiarty_with_score(ds, **bin_params)
    print_bin_stats(bins, **bin_params)

  precision_params_list = [
    {"method": "Content", "minUserScore": 3, "rank_col": "ComputedRankByMethod"},
    {"method": "Behavior", "minUserScore": 3, "rank_col": "ComputedRankByMethod"},
    {"method": "All", "minUserScore": 3, "rank_col": "ComputedRankGlobal"},
    {"method": "Content", "minUserScore": 3, "rank_col": "ComputedRankGlobal"},
    {"method": "Behavior", "minUserScore": 3, "rank_col": "ComputedRankGlobal"},
    {"method": "Content", "minUserScore": 4, "rank_col": "ComputedRankByMethod"},
    {"method": "Behavior", "minUserScore": 4, "rank_col": "ComputedRankByMethod"},
    {"method": "All", "minUserScore": 4, "rank_col": "ComputedRankGlobal"},
    {"method": "Content", "minUserScore": 4, "rank_col": "ComputedRankGlobal"},
    {"method": "Behavior", "minUserScore": 4, "rank_col": "ComputedRankGlobal"},
  ]

  for precision_params in precision_params_list:
    precisionAt10 = compute_precision(ds, **precision_params)
    print_precision_stats(precisionAt10, **precision_params)


  ndcg_params_list = [
    {"method": "Content", "rank_col": "ComputedRankByMethod" },
    {"method": "Behavior", "rank_col": "ComputedRankByMethod" },
    {"method": "All", "rank_col": "ComputedRankGlobal" },
    {"method": "Content", "rank_col": "ComputedRankGlobal" },
    {"method": "Behavior", "rank_col": "ComputedRankGlobal" },
  ]

  for ndcg_params in ndcg_params_list:
    ndcg = compute_ndcg(ds, **ndcg_params)
    print_ndcg_stats(ndcg, **ndcg_params)