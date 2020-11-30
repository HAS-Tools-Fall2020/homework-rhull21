--
### Evaluation of GitHub Repo(s)
### FAIR data
Quinn Hull
Week 14
11/25/2020

--

## Overview:
  * I decided to try two different styles of repo on this assignment to maximize the probability of 'success', and compare FAIRly.

    1. A 'canned' GitHub repo created for reproducibility and not necessarily associated with a journal article.
      * 'Time Series Prediction Using LSTM in PyTorch'
      * https://github.com/spdin/time-series-prediction-lstm-pytorch

    2. A 'research' GitHub repo tied to an article.
      * Jianfeng Zhang, Yan Zhu, Xiaoping Zhang, Ming Ye, Jinzhong Yang, Developing a Long Short-Term Memory (LSTM) based model for predicting water table depth in agricultural areas, Journal of Hydrology, Volume 561, 2018, Pages 918-929, ISSN 0022-1694, https://doi.org/10.1016/j.jhydrol.2018.04.065.
      * Article: https://www.sciencedirect.com/science/article/pii/S0022169418303184
      * Repo: https://github.com/jfzhang95/Water-Table-Depth-Prediction-PyTorch

    * Henceforth the projects/repos will be referred to as **(1)** and **(2)**


## Reflection
### (1) 'Time Series Prediction Using LSTM in PyTorch'

  1. What is the paper or project you picked? Include a title, a link the the paper and a 1-2 sentence summary of what its about.
    * https://github.com/spdin/time-series-prediction-lstm-pytorch
    * Control System Engineer playing Deep Learning
    * This is a public repo that is exclusively designed for learning about python deep learning
    * This repo isn't technically associated with a journal article. The publisher is mostly concerned with his own learning and facilitating the learning of others (runs a tutorial website for programmers)
    * This could be thought of as a 'base case' against which to compare code associated with research

  2. What codes and/or data are associated with this paper? Provide any link to the codes and datasets and a 1-2 sentence summary of what was included with the paper (i.e. was it a github repo? A python package?A database? Where was it stored and how?)
    * The codes and description were hosted on a simple GitHub repo with documentation of data sources and workflow etc...
    * A jupyter notebook that can be run locally or on Google Colab:
      * https://github.com/spdin/time-series-prediction-lstm-pytorch/blob/master/Time_Series_Prediction_with_LSTM_Using_PyTorch.ipynb
    * Datasets: publically available airline passenger data hosted on GitHub
    * I ran this script on Google Colab, which means the needed libraries are stored on the cloud  

            import numpy as np
            import matplotlib.pyplot as plt
            import pandas as pd
            import torch
            import torch.nn as nn
            from torch.autograd import Variable
            from sklearn.preprocessing import MinMaxScaler

  3. Summarize your experience trying to understand the repo: Was their readme helpful? How was their organization? What about documentation within the code itself?
    * The readme pointed the user towards relevant resources outside of the document, as well as demonstrated the results of the python workflow. It was sparse, but that worked out fine.

  4. Summarize your experience trying to work with their repo: What happened? Were you successful? Why or why not?
    * Super easy. I didn't even need to download the repo itself. I just downloaded the ipynb and brought it into google colab.

  5. Summarize your experience working with the data associated with this research. Could you access the data? Where was it? Did it have a DOI? What format was it in?
    * The research was publicly available and simple, hosted on github for its programmability. No issues at all accessing it.
      * https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv

  6. Did this experience teach you anything about your own repo or projects? Things you might start or stop doing?
    * I think that the combination of publicly available (web-accessible) data, web-hosted repositories of code and data (like github), and collaborative programming interactive editors that are web-hosted (like colab) significantly improve the success rate of FAIR research objectives. Researchers could take a page from industry professionals in using these platforms more often and efficiently.

### (2) 'Developing a Long Short-Term Memory (LSTM) based model for predicting water table depth in agricultural areas'

  1. What is the paper or project you picked? Include a title, a link the the paper and a 1-2 sentence summary of what its about.
    * Article: https://www.sciencedirect.com/science/article/pii/S0022169418303184
    * This article seems to be one of the most-referenced LSTM-related articles in hydrologic sciences (~300 refs on Scholar). The main thrust of this paper is to use ML networks (like LSTM) to predict water table depths in a data-sparse and complex groundwater system. An explicit goal is to make the data and workflow publicly available, and the method generalizable.

  2. What codes and/or data are associated with this paper? Provide any link to the codes and datasets and a 1-2 sentence summary of what was included with the paper (i.e. was it a github repo? A python package?A database? Where was it stored and how?)
      * Repo: https://github.com/jfzhang95/Water-Table-Depth-Prediction-PyTorch
      * There are two repos, one containing an LSTM model built in PyTorch, and another built using base python.
      * Both are just demos, meaning they demonstrate how to use the model on a 'fake' data. Neither contain the elements needed to duplicate the results from the paper. I.E. - they include the method (using the LSTM model in Python), but no way to verify precisely the results (because the raw data are not included)
      * It is an older paper, which means that some of the python implementations are a bit dated and the code (as I found out) could not be run out of the box. But it was well documented and simple enough figure out without much fiddling.
      * Packages needed:

            Python3.x
            pytorch>=0.4.0
            numpy>=1.14.0
            pandas>=0.22.0
            scikit-learn>=0.14

  3. Summarize your experience trying to understand the repo: Was their readme helpful? How was their organization? What about documentation within the code itself?
    * The readme was super well documented and stepped through what python and packages to have, how to clone the repo, how to run the script, and what the output should look like
    * The documentation within the code was sufficiently detailed. i.e. it basic overview of what was happening within the code without being overly descriptive, or more descriptive than necessary.
    * For me personally, it was necessary to break up the code to see exactly what was happening within each chunk of code, but I think I tend to over-comment

  4. Summarize your experience trying to work with their repo: What happened? Where  you successful? Why or why not?
    * It went well. Because the repo is a bit old, it used now depricated processes that caused the script not to run at first attempt.
    * For example: Unable to run python demo.py via command line becaue pd.DataFrame.as_matrix() is depricated. Reran the script using .values() instead of as_matrix(). It worked like a charm.

  5. Summarize your experience working with the data associated with this research. Could you access the data? Where was it? Did it have a DOI? What format was it in?
    * The data itself wasn't available through github. That complicates my conclusion a little bit. If you document the process, but not the source data itself, are you really doing 'FAIR' science?
    * The method itself did not have a DOI. It was managed in a simple github repo with python scripts, readmes, and source data.

  6. Did this experience teach you anything about your own repo or projects? Things you might start or stop doing?
    * I think the success of this article (100s of citations) was / is a function of it being one of the first of its kind in Hydrology to document a referencable LSTM model that could essentially be taken out of the box and employed on any other multitude of problems. Lots of people have taken this as a starting point for their own research without having to go on too many goose chases. = POWERFUL.
    * I wish that the repo had included the tools to replicate precisely the results of this study, but in doing so it might have made the repo so complicated that it would deter users looking for a simpler implementation.
    * I am surprised that after just a few years, there are problems with the code (i.e. issues due to the aging of conventions within python packages like pandas). This really goes to show that in order for 'FAIR' to really work, there needs to be a long-term commitment to sustaining the integrity of the data and workflows. It's not a matter of throwing something on GitHub and walking away. It takes continuous cultivation.
