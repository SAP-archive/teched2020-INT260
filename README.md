# INT260 - Data Classification with Python SDK and SAP AI Business

## Description

This repository contains the material for the SAP TechEd 2020 session called
INT260 - Data Classification with Python SDK and SAP AI Business

## Overview

This session introduces attendees to the Python Software Development Kit
for the Data Attribute Recommendation service.

## Requirements

**You will need** to have a valid SAP Cloud Platform trial account in the
**Europe (Frankfurt) - AWS** region

See [this tutorial](https://developers.sap.com/tutorials/hcp-create-trial-account.html)
to learn how to create a Trial account. Note that regions other than
**Europe (Frankfurt) - AWS** are currently not supported.

**You will need** an environment where you can run Python code.
This workshop is available as a Jupyter notebook. We recommend that you use a Jupyter
environment to load the notebook and execute the exercises.

### Running Jupyter in Docker

There are several ways to run a Jupyter notebook.
Docker is a great way to quickly get an environment up and running.
For this workshop, we recommend the `jupyter/scipy-notebook` image.

To quickly bring up a Jupyter server inside Docker,
[run the following command](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/running.html):

```bash
$ docker run -p 8888:8888 jupyter/scipy-notebook:latest
```

This will print an URL which will point you to your running Jupyter environment.
There, you can upload this notebook file and execute it.

### Other options for Jupyter

If you cannot run Jupyter locally, there are several offerings available on the
internet. You can use any Jupiter Notebook environment of your choice. 

<!-- 
TODO: Add mybinder.org link and appropriate disclaimer
-->

## Exercises

Start the exercises
[here](exercises/teched2020-INT260_Data_Attribute_Recommendation.ipynb).

## How to obtain support

Support for the content in this repository is available during the actual time of the
online session for which this content has been designed. Otherwise, you may request
support via the [Issues](../../issues) tab.

## License

Copyright (c) 2020 SAP SE or an SAP affiliate company. All rights reserved.
This file is licensed under the Apache Software License, version 2.0 except as noted
otherwise in the [LICENSE](LICENSE) file.
