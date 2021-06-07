FROM jupyter/minimal-notebook

# LABEL="PDM Public Discourse Miner"

USER root

# clone the repository in the container 
RUN git clone https://github.com/Spirited666/PublicDiscourseMiner-COVID.git 

# Install python dependencies from the project
RUN cd PublicDiscourseMiner-COVID \ 
    && pip install --user -r requirements.txt

CMD cd PublicDiscourseMiner-COVID \ 
    && jupyter notebook --allow-root

