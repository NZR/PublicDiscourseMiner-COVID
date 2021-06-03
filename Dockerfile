FROM jupyter/minimal-notebook

# LABEL="PDM Public Discourse Miner"

USER root

# Install Python 3 packages
RUN pip install \
    Scrapy \
    bs4 \
    tqdm \
    nltk \
    pytrends \
    matplotlib \
    pandas>=1.0 \
    searchtweets \
    searchtweets-v2 \
    knapsack \
    plotly \
    statsmodels \
    psutil \
    xlrd \
