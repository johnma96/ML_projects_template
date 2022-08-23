This repository proposes a structure for the development of machine learning projects. Feel free to modify the structure according to your own criteria and needs.

This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/) and [reproducible-model](https://github.com/cmawer/reproducible-model) repository.

Check this [post](https://www.jeremyjordan.me/ml-projects-guide/) by Jeremy Jordan for get guidelines on managing ML projects.

## Repo structure 

```
├── README.md                         <- You are here
│
├── LICENSE
│
├── credentials/
│   ├── __init__.py                   <- File to work with python packages
|   ├── data_paths.py                 <- File to get absolute paths from credentials files.
│
├── data                              <- Folder that contains data used or generated. Please be careful with files you're going to track as they may contain sensitive information.
│   ├── archive/                      <- Place to put archive data is no longer usabled. Not synced with git. 
│   ├── processed/                    <- Data sets for modeling.
│   ├── raw/                          <- The original, immutable data dump
│   ├── __init__.py                   <- File to work with python packages
|   ├── data_paths.py                 <- File to get absolute paths from files sotred within archive, processed or raw folder
│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries. You could also have an archive folder
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others. 
│   ├── archive                       <- Develop notebooks no longer being used. 
│
├── reports                           <- Generated analysis as HTML, PDF, LaTeX, etc.
│   ├── figures                       <- Generated graphics and figures to be used in reporting
│
├── src                               <- Source code for use in this project 
│   ├── __init__.py                   <- File to work with python packages
│   ├── archive/                      <- No longer current scripts. 
│   ├── sql/                          <- SQL source code. Consider ignoring files that may be inside this folder as they contain sensitive code and information
│   ├── ingest_data.py                <- Script for ingesting data from different sources 
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── train_model.py                <- Script for training machine learning model(s)
│   ├── score_model.py                <- Script for scoring new predictions using a trained model.
│   ├── postprocess.py                <- Script for postprocessing predictions and model results
│   ├── evaluate_model.py             <- Script for evaluating model performance 
│
├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── requirements.txt                  <- Python package dependencies 
```