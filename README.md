# Automated ab initio workflows with Jobflow and Atomate2 - Cecam school

This repository contains a Docker compose setup for the hands-on sessions of the
Cecam school [Automated ab initio workflows with Jobflow and Atomate2](https://www.cecam.org/workshop-details/automated-ab-initio-workflows-with-jobflow-and-atomate2-1276) 
held in Lausanne from March 17, 2025 to March 20, 2025.


## Atomate2 + jobflow-remote Docker Setup

This Docker Compose setup provides three integrated containers:
- JupyterLab with atomate2 and jobflow-remote preconfigured for usage.
- SLURM with SSH access to simulate an HPC cluster.
- MongoDB database for workflow data storage.

## Directory Structure

```
.
├── docker-compose.yml
├── .env
├── slurm/
│   ├── Dockerfile
│   └── slurm_startup.sh
├── jupyter/
│   └── Dockerfile
├── config/
│   └── jfremote_template.yaml
├── notebooks/
│   └── (jupyter notebooks for the hands on sessions)
├── scripts/
│   └── (python scripts for the hands on sessions)
└── develop/
    └── (location for developing simple small jobs/flows)
```

## Configuration

Before building the services **a few values need to be set in the `.env` file** to properly
use the containers and the HPC cluster available during the hands-on sessions. Open the 
`.env` file with a text editor and set the following variables:

* `PROJECTNAME`: name of the jobflow-remote project. Used to also define the folder names.
  It should be a **unique name** to avoid clashes with other users on the HPC clusters.
  Preferably include your name and surname (e.g. `atomate2_john_doe`)
* `REMOTE_USER`: the username for the HPC cluster. **Will be communicated during the hands-on sessions**.
* `REMOTE_PASSWORD`: the password for the HPC cluster. **Will be communicated during the hands-on sessions**.

> [!NOTE]
> The container can be used for local tests even without access to the HPC cluster, thus only
> the `PROJECTNAME` variable is mandatory.

Some of the usernames and ports can be configured in the `.env` file, in case the default values
clash with some of your local services. 

## Usage

### Starting the Containers

To launch the environment, clone the repository, navigate to the project directory and run:

```bash
docker-compose up -d
```

Once the containers are running, verify their status with:

```bash
docker ps
```

If everything is set up correctly, you should see the containers listed (e.g., `atomate2_school-jupyter-1`, 
`atomate2_school-slurm-1`).


### Services

#### JupyterLab

Based on JupyterLab container, is the main entry point for the execution of workflows during the school. 
The base python environment includes `atomate2`, `jobflow`, `jobflow-remote` and all related 
packages required to execute the workflows. 
Jobflow-remote is already fully configured. 
Connect to http://localhost:8888 (or your custom `JUPYTER_PORT`) and use `atomate` as password.

Can also be accessed through a shell. Run
```bash
docker container list
```
to get the name of the container (similar to `atomate2_school-jupyter-1`) and launch a bash
session inside the container with 
```bash
docker exec -it <container-name> /bin/bash 
```

#### Local SLURM worker

A local worker with slurm to mimic the execution on an HPC cluster. Includes the same
python packages as in the jupyter container and can be accessed through ssh with
```bash
ssh -p 2222 atomate@localhost
```
(or your custom `SSH_PORT` and `SLURM_USERNAME`) from the local machine or with
```bash
ssh atomate@slurm
```
from the jupyter container.
The password is the same as the username.

#### MongoDB

The MongoDB is accessible on localhost:27018 (or your custom `MONGODB_PORT`) from the local 
machine and on mongodb:27017 from the jupyter container. There is no password protection
on the database.
It may be instructive to explore the content of the database with a GUI like
[MongoDB Compass](https://www.mongodb.com/products/tools/compass).

#### Jobflow-remote GUI

The jobflow-remote GUI can be started in the jupyter container running
```bash
jf gui
```
and can be accessed from the local machine connecting to http://localhost:50001 (or your custom `WEB_APP_PORT`).


### Notebooks and script

The local folders `notebooks` and `scripts` are mounted in the jupyter container, so that all their
content will be readily available.

### Develop folder

The `develop` folder is mounted in the container and added to the `PYTHONPATH` in the jobflow-remote
configuration, so that it can be used to store newly developed workflows that can be recognised from the
`local_shell` worker.

## Stopping the Containers

```bash
docker-compose down
```

To remove all data volumes:
```bash
docker-compose down -v
```
