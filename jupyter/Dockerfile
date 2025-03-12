FROM quay.io/jupyter/scipy-notebook:latest

ARG NB_UID=1001
ARG NB_GID=1001

USER root

RUN usermod -u $NB_UID jovyan && groupmod -g $NB_GID users \
    && chown -R jovyan:users /home/jovyan

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        make \
        cmake \
        libfftw3-dev \
        libopenblas-dev \
        liblapack-dev \
        libhdf5-dev \
        gettext-base \
        sshpass \
        rsync \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Create an entrypoint script to handle config file processing
COPY jupyter/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

USER ${NB_UID}

# install pytorch separately to avoid installing nvidia dependence.
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install atomate2 and jobflow-remote in the base python environment
RUN pip install --no-cache-dir \
    "atomate2[phonons,lobster,forcefields]" \
    "jobflow-remote[gui]"

WORKDIR "${HOME}"

EXPOSE 8888 5001

COPY config/jfremote_template.yaml /tmp/jfremote_template.yaml

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Add the CMD as it seem to not be recognized otherwise
CMD ["start-notebook.py"]