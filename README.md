# Description
This is the codebase for the article [Multi-label Classification with XGBoost for Metabolic Pathway Prediction](https://doi.org/10.1186/s12859-024-05666-0) published in BMC Bioinformatics.  
We are currently updating the source code and data.   
We want to thank the authors of [mlLGPR](https://github.com/hallamlab/mlLGPR) for open sourcing their code and data because this study would not have been possible without them.  

The project structure is based on the [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/) project structure.  
All tests were conducted on an Ubuntu 20.04.5 server with dual Intel Xeon CPU E5-2640 v4 and 94G ram.  
We used [miniconda](https://docs.conda.io/en/latest/miniconda.html) as our package and environment management system.  
After installing miniconda, use ``conda create -n mlxgpr python=3.9`` to create a python 3.9 environment called mlxgpr.  
Afterwards activate the environment with 
```bash
conda activate mlxgpr
```  
# Dependencies
The codebase is tested to work under Python 3.9.  
To install the necessary requirements, run the following commands:  
```bash
pip install -r requirements.txt
```
# Data and Model
The trained model and data can be downloaded [here](https://drive.google.com/drive/folders/1TZoHnmIqrYWkHoslFvwT4sKkH2OB5bZw?usp=sharing)  
-Unzip models.zip into the models directory.  
-Unzip evaluation.zip into the data/processed directory. The order of the PGDBs in gold_dataset_6_X.npy is AraCyc, EcoCyc, HumanCyc, LeishCyc, TrypanoCyc, YeastCyc.  
-Unzip Synset-2.zip into the data/processed directory.  
-Unzip biocyc205_tier23_9255.zip into the data/processed directory.  
# References
In the references directory there are two csv files that summarizes the index and corresponding pathway id/EC number.  
The order.txt file lists the order of the classifier chain.  
# Evaluate Model
You can evaluate the model with the files in the src/models directory.  
  
``python evaluate_pathologic.py`` will write a csv file into the directory with the results of PathoLogic without pruning on the six single organism T1 PGDBs as in Table 4. In line 315 of the file, if you change the data_path variable to the pruned directory and run the program you will get the results of PathoLogic with pruning. Or you can comment out line 315 and uncomment line 316.  
  
``python evaluate_mlxgpr.py`` will write a csv file into the directory with the results of mlXGPR+AB on the six single organism T1 PGDBs as in Table 4. If you want the results of mlXGPR+AB+RE comment lines 76-77 and uncomment lines 79-80.  
  
``python evaluate_chain.py`` will write a csv file into the directory with the results of mlXGPR+Chain on the six single organism T1 PGDBs as in Table 4. If you want the results of mlXGPR+RankChain change the model_name variable or comment line 13 and uncomment line 14.  
  
``python evaluate_cami.py`` will write a csv file into the directory with the results of mlXGPR+RankChain on the CAMI dataset as in Table 5. If you want the results of mlXGPR+RankChain (BioCyc) change the model_name variable or comment line 33 and uncomment line 34.  
# Train Model
You can train the models with the files in the src/models directory.    

``python train_mlxgpr.py`` will train a mlXGPR+AB model on the Synset-2 dataset. If you want to train a mlXGPR+AB+RE model comment lines 24-25 and uncomment lines 27-28. It takes about 30 minutes to train with n_jobs=35 on our server.  

``python train_classifierchain.py`` will train a mlXGPR+Chain model on the Synset-2 dataset. If you want to train a mlXGPR+RankChain model comment lines 30-31 and uncomment lines 33-36. If you want to train a mlXGPR+RankChain model on the BioCyc Tier 2/3 dataset comment lines 17-18 and 36 while uncommenting lines 19-20 and 37. It takes about an hour to train with n_jobs=35 on the Synset-2 dataset and 30 minutes for the BioCyc dataset on our server.  
# Determine Chain Order by Ranking  
You can determine the chain order by ranking with the file in the src/models directory. It is the code for Algorithm 3 in the article.  

``python determine_chain_order.py`` will load a trained model that will be used to determine the chain order. If you want to train a new model to determine the chain order, uncomment lines 47-56 and comment lines 58-59. The classifier chain order will be written into a text file in the references directory.  
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
# Data Source  
Information about the source for each dataset is in the data/raw directory.  
# Process Datasets
You can create the datasets with the files in the src/data directory.  

``python make_synset2.py`` will process the Synset2 dataset to be used for training. The resulting files will be created in the data/processed directory. Both X and y files take a few seconds to create.  
``python make_gold_dataset.py`` will process the golden dataset to be used for evaluation. The resulting files will be created in the data/processed directory.  
