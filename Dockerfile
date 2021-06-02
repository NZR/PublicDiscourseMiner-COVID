FROM jupyter/minimal-notebook

LABEL ="PDM Public Discourse Miner"

USER root

# Install Python 3 packages
RUN conda install --quite --yes \
    'tqdm' \
    'nltk' \
    'pytrends' \
    'pandas=1.0*' \
    'searchtweets' \
    'knapsack' \
    'plotly' \
    'beautifulsoup4=4.9.*' \
    'conda-forge::blas=*=openblas' \
    'h5py=3.2.*' \
    'ipympl=0.7.*'\
    'ipywidgets=7.6.*' \
    'matplotlib-base=3.4.*' \
    'pandas=1.2.*' \
    'scipy=1.6.*' \
    'seaborn=0.11.*' \
    'xlrd=2.0.*' && \
    conda clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"
