FROM --platform=linux/amd64 quay.io/jupyter/scipy-notebook:latest

ARG CREATE_AUTOPLEX_ENV=false

USER root

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
    "jobflow-remote[gui]" \
    "pymatviz"

# Optionally create an additional environment with autoplex
RUN if [ "$CREATE_AUTOPLEX_ENV" = "true" ]; then \
    conda create -n autoplex python=3.11 -y && \
    . /opt/conda/etc/profile.d/conda.sh && \
    conda activate autoplex && \
    pip install --no-cache-dir torch==2.2.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir quippy-ase==0.9.14 autoplex[strict] jobflow-remote && \
    pip install ipykernel && \
    # Register the environment as a Jupyter kernel
    python -m ipykernel install --user --name=autoplex --display-name="autoplex" && \
    conda deactivate; \
fi

WORKDIR "${HOME}"

EXPOSE 8888 5001

COPY config/jfremote_template.yaml /tmp/jfremote_template.yaml

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Add the CMD as it seem to not be recognized otherwise
CMD ["start-notebook.py"]
