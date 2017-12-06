FROM psychemedia/binder_maps

# Make sure the contents of our repo are in ${HOME}
USER root
COPY . ${HOME}

#Run any catch-up stuff
#Should this be running as another user?
RUN ${HOME}/postBuild

#Check that ${NB_USER} owns their notebook files and is the group
RUN chown -R ${NB_USER}:${NB_USER} ${HOME}


#Revert to the notebook user for the session
USER ${NB_USER}