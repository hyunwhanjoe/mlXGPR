# Description
This is the codebase for the manuscript "Multi-label Classification with XGBoost for Metabolic Pathway Prediction".  
We are currently updating the source code and data to match the revision to the manuscript submitted on 23/12/13.  

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
# References
In the references directory there are two csv files that summarizes the index and corresponding pathway id/EC number.  
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
# Creating a PGDB with PathoLogic  
-We used PathoLogic version 22 to generate the PGDBs. All PGDBs for the manuscript were created on a Windows 10 pc.  
-First apply for a license to download Pathway Tools [here](https://biocyc.org/download.shtml)  
-After you installed Pathway Tools, open it and on the Tools tab click on PathoLogic.  
-When the the PathoLogic window opens on the Database tab, click on Create New.  
-After naming the PGDB, choose the Organism taxonomic class. For example the class for AraCyc is Arabidopsis thaliana.  
-Create the PGDB afterwards by pressing ok. 
-Press No to skip the replicon editor.  
-Put the relevant 0.pf and genetic-elements.dat files (located in the pathologic directory in evaluation.zip) in the input directory where your PGDB is stored. For example on Windows the input directory path is Documents\Pathway Tools\ptools-local\pgdbs\user\aracyc\1.0\input  
-Go to the Build tabs on the PathoLogic window and select Trial Parse to see if there is any issues. If there aren't, select Automated Build.  
-For the Pathway Scoring Parameters, we selected No for Generate Cellular Overview and Prepare Blast databases. If you get a warning that blastp.exe wasn't found you can dismiss it. Press okay to create your PGDB and close the PathoLogic window after it is created.   
-Select the PGDB that you created and afterwards on the File tab, Export, Entire DB to attribute value and BioPAX files.  
-In the data directory where your PGDB is stored, copy the pathways.col and pathways.dat files into the relevant PGDB directory in data/processed/pathologic. For example on Windows the data directory path is Documents\Pathway Tools\ptools-local\pgdbs\user\aracyc\1.0\data  
