# Environment setup without Docker

In case for any reason using the docker containers is not possible, this guide will help set up your system for the the hands-on sessions.
Note that this setup does not include a local Slurm service.

## 1. MongoDB

A MongoDB database is mandatory for the storage of the job states and outputs. You have two options to set up a MongoDB instance:

### Option 1: Install MongoDB Locally

To install MongoDB locally, you can follow the following steps:

- Download MongoDB Community Edition from the [official website](https://www.mongodb.com/try/download/community)
- Follow the installation instructions for your operating system:
  - [Windows Installation Guide](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/)
  - [MacOS Installation Guide](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/)
  - [Linux Installation Guide](https://www.mongodb.com/docs/manual/administration/install-on-linux/)
- Start the mongoDB according to the instructions provided in the previous steps. Setting up a password for
  the DB access is not needed for this tutorial.

### Option 2: Use MongoDB Atlas (Cloud)

MongoDB Atlas provides a free-tier M0 cluster for cloud-hosted MongoDB instances. This will be enough for the 
present tutorial. To use this option:

- Register for a free account at [MongoDB Atlas](https://www.mongodb.com/atlas/database)
- Create a free M0 cluster and follow the instructions to set it up
- Follow the [Atalas user guide](https://www.mongodb.com/docs/atlas/getting-started/) to configure it (Easier with "Atlas UI" option)
- On the cluster main page the `Connect` button will provide the connection details. Select the "drivers" section
  and look for the python code. Save the connection string for later. A connection string has the following format:
  ```
  mongodb+srv://<db_username>:<db_password>@cluster0.xxxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
  ```
  Username and password are those for the user that should have been configured in the previous step.

## 2. Local Python Environment

This section will provide instruction to set up a local virtual environment. If you already have a Python virtual 
environment (e.g., Conda or virtualenv) with Python >= 3.10, you can skip this section and just create an environment
for this tutorial (e.g. named `atomate`).

### Option 1: Conda

Conda is an open source package management system and environment management system. In this case we consider
using miniconda, which is a minimal Conda installer. To install:

- Download Miniconda from [here](https://www.anaconda.com/download/success)
- Follow the installation guide for your OS
- Create a new Conda environment:
  ```bash
  conda create -n atomate python=3.10
  conda activate atomate
  ```

Due to compatiblity issues among the different python packages, an additional conda environment
needs to be created in order to properly perform the tutorials on the [autoplex](https://autoatml.github.io/autoplex/index.html) package. To do this run:

```bash
  conda create -n autoplex python=3.11
  conda activate autoplex
```

#### Option 2: Using Virtualenv

If you prefer virtual environments with `venv`:

- Ensure you have Python 3.10+ installed from [python.org](https://www.python.org/downloads/)
- Create a virtual environment:
  ```bash
  python -m venv atomate
  source atomate/bin/activate  # On macOS/Linux
  atomate\Scripts\activate  # On Windows
  ```

  ```bash
  python -m venv autoplex
  source autoplex/bin/activate  # On macOS/Linux
  autoplex\Scripts\activate  # On Windows
  ```

### 3. Installing Required Packages

Once your `atomate` environment is activated, install the required Python packages:

```bash
pip install jupyterlab atomate2[phonons,lobster,forcefields] jobflow-remote[gui]
```

Similarly, for the `autoplex` environment:

```bash
pip install --no-cache-dir jupyterlab && pip install --no-cache-dir torch==2.2.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
pip install --no-cache-dir quippy-ase==0.9.14 autoplex[strict] jobflow-remote[gui]
```

### 4. Running JupyterLab

To start JupyterLab, in respective environment simply run:

```bash
jupyter lab
```

A browser window will usually open and bring you to the Jupyter Lab main page. Otherwise you will neede to access it 
from the address provided in the shell when starting Jupyter Lab (e.g. http://localhost:8888/lab?token=307489ea14c36c3536694f1f2610a8abbcc6238506aaxxxa).

### 5. Set up jobflow-remote

To properly use jobflow-remote during the hands-on sessions follow these steps:

* Create a `.jfremote` folder in your home
* Choose a name for the jobflow-remote project (referred from here on as `PROJECTNAME`). 
  Used to also define the folder names on the cluster. It should be a **unique name** 
  to avoid clashes with other users on the HPC clusters.
* Copy the `jfremote_template_no_docker.yaml` in the `.jfremote` folder and rename it to
  `{PROJECTNAME}.yaml` (replacing the value of your project name).
* Open `{PROJECTNAME}.yaml` with a text editor and set the following configuration options:
  * Replace all the occurrences of `${PROJECTNAME}` with the `PROJECTNAME` just chosen.
  * Replace all the occurrences of `${REMOTE_USER}` and `${REMOTE_PASSWORD}` with the values 
    of the username password for the HPC cluster that **will be communicated during the hands-on**.
  * Go to the `queue->store` section of the yaml and fill in the connection details depending
    on the chosen configuration, i.e. either the one based on the host or the URI. Remove the other.
    > [!WARNING]
    > Only one of the sections preceded by `==== LOCAL MONGODB ====` or `==== ATLAS MONGODB ====`
    > should remain in the file. The other should be removed!
  * Repeat the same for the DB details in the `jobstore->docs_store` and `jobstore->additional_stores->data`.

### 6. Test the setup

If everything is set up properly you should be able to run the command:

```bash
jf project check
```

In case the username and password for the HPC cluster have not been set yet you will get an
error when it attempts to connect to those resources, but the `local_shell` worker, `Jobstore`
and `Queue store` should all pass the checks.
