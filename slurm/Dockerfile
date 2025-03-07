ARG USERNAME=atomate

FROM --platform=linux/amd64 nathanhess/slurm:full
USER root

# Copy the SLURM startup script
COPY slurm/slurm_startup.sh /etc/startup.sh
HEALTHCHECK CMD sinfo || exit 1

# Install dependencies
RUN apt update && \
    apt install -y \
        openssh-server \
        sudo \
        python3.10-venv \
        python3-pip \
        gcc \
        g++ \
        make \
        dos2unix && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Configure SSH server
RUN sed -i 's/#PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config

# Create a user
ARG USERNAME
ENV USERNAME=${USERNAME}
RUN useradd -rm -d /home/${USERNAME} -s /bin/bash ${USERNAME} || exit 0 && \
    usermod -a -G sudo ${USERNAME}
RUN echo ${USERNAME}:${USERNAME} | chpasswd

# Give user sudo access to the startup script without password
RUN printf "${USERNAME} ALL=(root:root) NOPASSWD: /etc/startup.sh\n" >> /etc/sudoers.d/startup \
    && chmod 0440 /etc/sudoers.d/startup \
    && visudo -c

RUN mkdir -p /home/${USERNAME}/jobs

# Set up startup script and permissions
RUN chmod +x /etc/startup.sh && \
    dos2unix /etc/startup.sh
# RUN chown -R ${USERNAME} /home/${USERNAME} && \
#     chmod -R 755 /home/${USERNAME}

# Create an entrypoint script
RUN echo '#!/bin/bash\n\
sudo /etc/startup.sh\n\
# Keep container running\n\
tail -f /dev/null\n' > /entrypoint.sh && \
chmod +x /entrypoint.sh

USER ${USERNAME}

# Create a Python virtual environment and install the required packages
WORKDIR /home/${USERNAME}
RUN python3 -m venv /home/${USERNAME}/.venv && \
    /home/${USERNAME}/.venv/bin/pip install --no-cache-dir --upgrade pip && \
    /home/${USERNAME}/.venv/bin/pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    /home/${USERNAME}/.venv/bin/pip install --no-cache-dir atomate2[phonons,lobster,forcefields] jobflow-remote[gui]


ENTRYPOINT ["/entrypoint.sh"]