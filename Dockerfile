FROM psychemedia/binder_maps

# Make sure the contents of our repo are in ${HOME}
USER root
COPY . ${HOME}

RUN chown -R ${NB_USER} ${HOME}

USER ${NB_USER}