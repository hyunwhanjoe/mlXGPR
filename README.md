# Description
This is the codebase for the manuscript "Multi-label Classification with XGBoost for Metabolic Pathway Prediction".  
The project structure is based on the [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/) project structure.  
All tests were conducted on an Ubuntu 20.04.5 server with dual Intel Xeon CPU E5-2640 v4 and 94G ram.  
We used [miniconda](https://docs.conda.io/en/latest/miniconda.html) as our package and environment management system.  
After installing miniconda, use ``conda create -n mlxgpr python=3.9`` to create a python 3.9 environment called mlxgpr.  
Afterwards activate the environment with ``conda activate mlxgpr``  
# Dependencies
The codebase is tested to work under Python 3.9.  
To install the necessary requirements, run the following commands:  
``pip install -r requirements.txt``
# Data and Model
The trained model and data can be downloaded [here](https://drive.google.com/drive/folders/1TZoHnmIqrYWkHoslFvwT4sKkH2OB5bZw?usp=sharing)  
Unzip model.zip into the models directory.  
Unzip evaluation.zip into the data/processed directory.  
The order of the PGDBs in gold_dataset_6_X.npy is AraCyc, EcoCyc, HumanCyc, LeishCyc, TrypanoCyc, YeastCyc.  
Unzip Synset-2.zip into the data/processed directory.
# Evaluate Model
You can evaluate the model with the files in the src/models directory.  
``python evaluate_biocyc.py`` will write a csv file into the directory with the results of mlXGPR on the six single organism T1 PGDBs as in Table 4.  
``python evaluate_pathologic.py`` will write a csv file into the directory with the results of PathoLogic using taxonomic pruning on the six single organism T1 PGDBs as in Table 4.  
``python evaluate_cami.py`` will write a csv file into the directory with the results of mlXGPR on the CAMI dataset as in Table 5.
# Train Model
You can train a model with the files in the src/models directory.  
``python train_model.py`` will train and save a model 'model.json' into the models directory.  
It takes about 28.5 minutes to train a model from our server with n_jobs=35.  
It takes about 32 minutes to train a model from our server with n_jobs=10.  
# References
In the references directory there are two csv files that summarizes the index and corresponding pathway id/EC number.
