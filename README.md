# Microsoft Academic Paper Recommender User Study

The raw data and analysis code for the Microsoft Academic paper recommender system user study conducted in 2018. The results of this study were presented as part of the publication titled, "[A Scalable Hybrid Research Paper Recommender System for Microsoft Academic](https://dl.acm.org/citation.cfm?doid=3308558.3313700)", presented at The Web Conference, San Francisco - USA, May 2019.

To cite this dataset in academic works please use the following paper citation:

*bibtex*
```
@inproceedings{Kanakia2019scalable,
 author = {Kanakia, Anshul and Shen, Zhihong and Eide, Darrin and Wang, Kuansan},
 title = {A Scalable Hybrid Research Paper Recommender System for Microsoft Academic},
 booktitle = {The World Wide Web Conference},
 series = {WWW '19},
 year = {2019},
 isbn = {978-1-4503-6674-8},
 location = {San Francisco, CA, USA},
 pages = {2893--2899},
 numpages = {7},
 url = {http://doi.acm.org/10.1145/3308558.3313700},
 doi = {10.1145/3308558.3313700},
 acmid = {3313700},
 publisher = {ACM},
 address = {New York, NY, USA},
}
```

*ACM Reference*

Anshul Kanakia, Zhihong Shen, Darrin Eide, and Kuansan Wang. 2019. A Scalable Hybrid Research Paper Recommender System for Microsoft Academic. In Proceedings of the 2019 World Wide Web Conference (WWW '19), May 13–17, 2019, San Francisco, CA, USA.ACM, New York, NY, USA, Article 4, 7 pages. https://doi.org/10.1145/3308558.3313700

## Dataset Column Definitions

* `PaperId`: Id of original paper in the Microsoft Academic Graph (MAG) dataset as of October, 2018.
* `RecommendedPaperId`: Id of recommended paper in the MAG dataset as of October, 2018.
* `Method`: Refers to the recommendation method used to generate this paper recommendation pair. "Content" refers to content based embedding similarity, whereas "Behavior" refers to co-citation based similarity. In some cases, both methods presented the same paper recommendation pair. Such pairs are indicated by the word "Both" in this column. For such recommendation pairs, the higher of the two possible similarity values was used in the `Similarity` column.
* `StudyScore`: The score given by a user to this paper recommendation pair.
* `StudyRankByMethod`: The recommendation list order based on user score for this recommended paper compared to other recommendations generated using this method for this paper.
* `StudyRankGlobal`: The recommendation list order based on user score for this recommended paper compared to other recommendations generated using both methods combined, for this paper.
* `CooccurrenceCnt`: Only relevant for "Behavior" method based recommendations. The co-occurance count for this paper pair computed using the entire MAG citation network. For more information, see section 2.1 of the paper.
* `Similarity`: The combined recommendation similarity for this paper pair computed using the methods described in section 2.3 of the paper.
* `EmbSimilarity`: Only relevant for "Content" method based recommendations. The content embedding similarity for this paper pair computed using the methods described in section 2.2 of the paper.
* `TfIdfSimilarity`: Only relevant for "Content" method based recommendations. The TF-IDF based similarity for this paper pair.
* `ComputedRankByMethod`: The recommendation list order as computed by the MAG paper recommender system using this method for this paper.
* `ComputedRankGlobal`: The recommendation list order as computed by the MAG paper recommender system using both methods combined, for this paper.

## Running the Python script
### Requirements
* Python 3.xx
* Pandas python module

In a terminal, run the following command: `python ./user_study_analysis.py ./user_study_results.tsv`
