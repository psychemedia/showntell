FROM psychemedia/binder_maps


# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
