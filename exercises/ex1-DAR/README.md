# INT260 - Data Classification with Python SDK and SAP AI Business Services

## Exercise 01

## Overview

This exercise introduces attendees to the Python Software Development Kit
for the Data Attribute Recommendation service.

## Requirements

To get started, we will first prepare two prerequisites:

* a valid SAP Cloud Platform trial account in the **Europe (Frankfurt) - AWS** region
* a Jupyter environment to execute the exercises

### SAP Cloud Platform trial account

If you have no trial account,
[you will need to create one first](markdown/create_trial_account.md).

If you already have a trial account,
[please check if it is setup correctly](markdown/check_existing_trial_account.md).

### Executing the Jupyter Notebook

You now have successfully set up a trial account on SAP Cloud Platform
in the **Europe (Frankfurt) - AWS** region.

We will now set up a Jupyter environment to execute the notebook
containing the exercises. There are two options: running the notebook
locally or running it on a cloud service.

#### Executing the Notebook directly in the browser

The easiest way to get started with Jupyter is to launch the
notebook directly in your browser via [mybinder.org].

[mybinder.org]: https://mybinder.org/v2/gh/SAP-samples/teched2020-INT260/main?filepath=exercises%2Fex1-DAR%2Fteched2020-INT260_Data_Attribute_Recommendation.ipynb

It may take up to five minutes to launch the notebook. Sessions on this free service
can be terminated after a [10 minutes of inactivity]. Make sure not to leave the
browser window for long periods of time and download your notebook once you
are done with the workshop for safekeeping.

[10 minutes of inactivity]: https://mybinder.readthedocs.io/en/latest/about/about.html#how-long-will-my-binder-session-last

If the main link above does not work for you and the notebook is not launching
even after five minutes, you can directly try one of the
[fallback options](https://binderhub.readthedocs.io/en/latest/federation/federation.html):
[Binderhub], [OVH] or [GESIS].

[Binderhub]: https://gke.mybinder.org/v2/gh/SAP-samples/teched2020-INT260/main?filepath=exercises%2Fteched2020-INT260_Data_Attribute_Recommendation.ipynb
[OVH]: https://ovh.mybinder.org/v2/gh/SAP-samples/teched2020-INT260/main?filepath=exercises%2Fteched2020-INT260_Data_Attribute_Recommendation.ipynb
[GESIS]: https://notebooks.gesis.org/binder/v2/gh/SAP-samples/teched2020-INT260/main?filepath=exercises%2Fteched2020-INT260_Data_Attribute_Recommendation.ipynb

If you prefer, the notebook is also available on [Google Colab] after prior login.

[Google Colab]: https://colab.research.google.com/github/SAP-samples/teched2020-INT260/blob/main/exercises/ex1-DAR/teched2020-INT260_Data_Attribute_Recommendation.ipynb

**Using the mybinder.org service or the Google Colab service is completely voluntary
and you are responsible for any information that you may add to mybinder.org. The
reference to the mybinder.org and Google Colab services are not an endorsement of
the respective offerings. You will be subject
to the terms and conditions and to the privacy policy of the respective offerings.**

Once you have launched the notebook, you are all set.
The remaining workshop content is located inside the notebook.

#### Executing the Notebook locally

If you prefer to run the notebook locally, we have a separate set of instructions
for a [Docker-based setup].

[Docker-based setup]: markdown/running_docker_locally.md

## How to obtain support

Support for the content in this repository is available during the actual time of the
online session for which this content has been designed. Otherwise, you may request
support via the [Issues](../../../../issues) tab.

## License

Copyright (c) 2020 SAP SE or an SAP affiliate company. All rights reserved.
This file is licensed under the Apache Software License, version 2.0 except
as noted otherwise in the [LICENSE](/LICENSES/Apache-2.0.txt) file.
