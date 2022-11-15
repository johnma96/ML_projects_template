This repository proposes a structure for the development of machine learning projects. Feel free to modify the structure according to your own criteria and needs.

This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/) and [reproducible-model](https://github.com/cmawer/reproducible-model) repository.

Check this [post](https://www.jeremyjordan.me/ml-projects-guide/) by Jeremy Jordan for get guidelines on managing ML projects.

Other resources.
- Books
    - [Clean Machine Learning Code](https://leanpub.com/cleanmachinelearningcode)

## Repo structure 

```
├── README.md                         <- You are here
│
├── LICENSE
│
├── credentials
│   ├── __init__.py                   <- Script to work with python packages
|   ├── data_paths.py                 <- Script to get absolute paths from credentials files.
│
├── data                              <- Folder that contains data used or generated. Please be careful with files you're going to track
│                                        as they may contain sensitive information.
│   ├── archive/                      <- Place to put archive data is no longer usabled. Not synced with git. 
│   ├── processed/                    <- Data sets for modeling.
│   ├── raw/                          <- The original, immutable data dump
│   ├── __init__.py                   <- Script to work with python packages
|   ├── data_paths.py                 <- Script to get absolute paths from files sotred within archive, processed or raw folder
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
├── references                        <- Data dictionaries, manuals, and all other explanatory materials. Consider ignoring some files 
│                                        when they are binary or large   
│
├── reports                           <- Generated analysis as HTML, PDF, LaTeX, etc.
│   ├── figures                       <- Generated graphics and figures to be used in reporting
│
├── src                               <- Source code for use in this project 
│   ├── archive/                      <- No longer current scripts. 
│   ├── sql/                          <- SQL source code. Consider ignoring files that may be inside this folder as they contain sensitive 
│                                        code and information
│   ├── __init__.py                   <- Script to work with python packages
│   ├── evaluate_model.py             <- Script for evaluating model performance
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── load_data.py                  <- Script for ingesting data from different sources 
│   ├── postprocess.py                <- Script for postprocessing predictions and model results 
│   ├── score_model.py                <- Script for scoring new predictions using a trained model.
│   ├── train_model.py                <- Script for training machine learning model(s)
│
├── main.py                           <- Simplifies the execution of one or more of the src scripts 
├── requirements.txt                  <- Python package dependencies 
├── .gitignore                        <- Script with some templates to ignore by git 

```

references folder: Place here pdf files or other bibliographic sources that have allowed to reach the selection of the model or the understanding of some algorithm that you want to keep.

Consider ignoring some files when they are binary or large

noteboosk folder: This folder is intended to store all the notebooks you create to explore, test, train, etc. models and code in general. Naming convention is the suggest by [Cookiecutter](https://drivendata.github.io/cookiecutter-data-science/#directory-structure): 
- A number (for ordering), the creator's initials, and a short `-` delimited description, e.g. `1.0-jqp-initial-data-exploration`.

models folder: Trained and serialized models, model predictions, or model summaries

docs folder: A default Sphinx project; see sphinx-doc.org for details.

data folder: Use this folder to store your data. Here there's a python's file for get absolute path of this folder.
Currently there are 5 folders for store data: raw (for raw data from the company), interim (for data with some modification but not completly), processed (for manipulated data in final version) and external(data from third parties).