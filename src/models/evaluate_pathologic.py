import os
import os.path
from collections import OrderedDict
import csv

import numpy as np
from sklearn.metrics import f1_score, precision_score,\
                            recall_score, hamming_loss
import sys
sys.path.append('../utility')
from utility import load_csvindex

# https://github.com/arbasher/prepBioCyc/blob/master/src/preprocess/pathway.py
class Pathway(object):
    def __init__(self, pathway_dat_file_name='pathways.dat', pathway_col_file_name='pathways.col'):
        """ Initialization
        :param ptwFnameLinks:
        :type pathway_dat_file_name: str
        :param pathway_dat_file_name: file name for the pathway
        """
        self.pathway_dat_file_name = pathway_dat_file_name
        self.pathway_col_file_name = pathway_col_file_name
        self.super_pathways = list()
        self.pathway_info = OrderedDict()

    def process_pathways(self, pathway_idx_list_ids, list_ids, data_path, header: bool = False):
        self.__process_pathways(pathway_idx_list_ids=pathway_idx_list_ids, list_ids=list_ids, data_path=data_path)
        self.__process_pathways_col(pathway_idx_list_ids=pathway_idx_list_ids, list_ids=list_ids, data_path=data_path,
                                    header=header)

    
    def __process_pathways(self, pathway_idx_list_ids, list_ids, data_path):
        file = os.path.join(data_path, self.pathway_dat_file_name)
        if os.path.isfile(file):
            print('\t\t\t--> Prepossessing pathways from: {0}'.format(file.split('/')[-1]))
            with open(file, errors='ignore') as f:
                for text in f:
                    if not str(text).startswith('#'):
                        ls = text.strip().split()
                        if ls:
                            if ls[0] == 'UNIQUE-ID':
                                pathway_id = ' '.join(ls[2:])
                                pathway_name = ''
                                lst_pathway_types = list()
                                lst_pathways_links = list()
                                lst_predecessors = list()
                                lst_reactions = list()
                                lst_reactions_layout = list()
                                lst_key_reactions = list()
                                lst_synonyms = list()
                                lst_species = list()
                                lst_taxonomic_range = list()
                                lst_sup_pathways = list()
                                lst_sub_pathways = list()
                            elif ls[0] == 'COMMON-NAME':
                                pathway_name = ' '.join(ls[2:])
                            elif ls[0] == 'TYPES':
                                lst_pathway_types.append(' '.join(ls[2:]))
                            elif ls[0] == 'PATHWAY-LINKS':
                                lst_pathways_links.append(' '.join(ls[2:]))
                            elif ls[0] == 'PREDECESSORS':
                                lst_predecessors.append(' '.join(ls[2:]))
                            elif ls[0] == 'REACTION-LIST':
                                lst_reactions.append(' '.join(ls[2:]))
                            elif ls[0] == 'REACTION-LAYOUT':
                                lst_reactions_layout.append(' '.join(ls[2:]))
                            elif ls[0] == 'KEY-REACTIONS':
                                lst_key_reactions.append(' '.join(ls[2:]))
                            elif ls[0] == 'SYNONYMS':
                                lst_synonyms.append(' '.join(ls[2:]))
                            elif ls[0] == 'SPECIES':
                                lst_species.append(' '.join(ls[2:]))
                            elif ls[0] == 'TAXONOMIC-RANGE':
                                lst_taxonomic_range.append(' '.join(ls[2:]))
                            elif ls[0] == 'SUPER-PATHWAYS':
                                lst_sup_pathways.append(' '.join(ls[2:]))
                            elif ls[0] == 'SUB-PATHWAYS':
                                lst_sub_pathways.append(' '.join(ls[2:]))
                            elif ls[0] == '//':
                                if 'Super-Pathways' in lst_pathway_types:
                                    self.super_pathways.append(pathway_id)
                                    continue
                                if pathway_id not in list_ids[pathway_idx_list_ids]:
                                    list_ids[pathway_idx_list_ids].update(
                                        {pathway_id: len(list_ids[pathway_idx_list_ids])})

                                if pathway_id not in self.pathway_info:
                                    # datum is comprised of {UNIQUE-ID: (COMMON-NAME, TYPES, PATHWAY-LINKS, PREDECESSORS,
                                    # REACTION-LIST, REACTION-LAYOUT, SYNONYMS, SPECIES, TAXONOMIC-RANGE, SUPER-PATHWAYS,
                                    # SUB-PATHWAYS)}
                                    datum = {pathway_id: (['COMMON-NAME', pathway_name],
                                                          ['TYPES', lst_pathway_types],
                                                          ['PATHWAY-LINKS', lst_pathways_links],
                                                          ['PREDECESSORS', lst_predecessors],
                                                          ['REACTION-LIST', lst_reactions],
                                                          ['REACTION-LAYOUT', lst_reactions_layout],
                                                          ['KEY-REACTIONS', lst_key_reactions],
                                                          ['SYNONYMS', lst_synonyms],
                                                          ['SPECIES', lst_species],
                                                          ['TAXONOMIC-RANGE', lst_taxonomic_range],
                                                          ['SUPER-PATHWAYS', lst_sup_pathways],
                                                          ['SUB-PATHWAYS', lst_sub_pathways])}
                                    self.pathway_info.update(datum)

    def __process_pathways_col(self, pathway_idx_list_ids, list_ids, data_path, header=False):
        file = os.path.join(data_path, self.pathway_col_file_name)
        if os.path.isfile(file):
            print('\t\t\t--> Prepossessing pathways from: {0}'.format(file.split('/')[-1]))
            with open(file, errors='ignore') as f:
                for text in f:
                    if not str(text).startswith('#'):
                        ls = text.strip().split('\t')
                        if ls:
                            if not header:
                                if ls[0] == 'UNIQUE-ID':
                                    header = True
                                    lst_g_name_idx = list()
                                    lst_g_idx = list()
                                    for (i, item) in enumerate(ls):
                                        if item == 'UNIQUE-ID':
                                            pathway_idx = i
                                        elif item == 'NAME':
                                            pathway_name_idx = i
                                        elif item == 'GENE-NAME':
                                            lst_g_name_idx.append(i)
                                        elif item == 'GENE-ID':
                                            lst_g_idx.append(i)
                            else:
                                if ls[pathway_idx] in self.super_pathways:
                                    continue
                                if ls[pathway_idx] not in list_ids[pathway_idx_list_ids]:
                                    list_ids[pathway_idx_list_ids].update(
                                        {ls[pathway_idx]: len(list_ids[pathway_idx_list_ids])})

                                if ls[pathway_idx] in self.pathway_info:
                                    (pathway_name, lst_pathway_types, lst_pathways_links, lst_predecessors,
                                     lst_reactions, lst_reactions_layout, lst_key_reactions, lst_synonyms, lst_species,
                                     lst_taxonomic_range, lst_sup_pathways, lst_sub_pathways) = self.pathway_info[
                                        ls[pathway_idx]]

                                lst_genes_names = ls[pathway_name_idx + 1: lst_g_name_idx[-1] + 1]
                                lst_genes_ids = ls[lst_g_name_idx[-1] + 1:]
                                lst_genes_names = [gn for gn in lst_genes_names if gn]
                                lst_genes_ids = [gid for gid in lst_genes_ids if gid]

                                # datum is comprised of {UNIQUE-ID: (COMMON-NAME, TYPES, PATHWAY-LINKS, PREDECESSORS,
                                # REACTION-LIST, REACTION-LAYOUT, SYNONYMS, SPECIES, TAXONOMIC-RANGE, SUPER-PATHWAYS,
                                # SUB-PATHWAYS, GENES-NAME, GENES-ID)}
                                datum = {ls[pathway_idx]: (pathway_name,
                                                           lst_pathway_types,
                                                           lst_pathways_links,
                                                           lst_predecessors,
                                                           lst_reactions,
                                                           lst_reactions_layout,
                                                           lst_key_reactions,
                                                           lst_synonyms,
                                                           lst_species,
                                                           lst_taxonomic_range,
                                                           lst_sup_pathways,
                                                           lst_sub_pathways,
                                                           ['GENES-NAME', lst_genes_names],
                                                           ['GENES-ID', lst_genes_ids])}
                                self.pathway_info.update(datum)

    def add_reaction_info(self, reactions_info, ec_position_idx, in_pathway_position_idx, orphan_position_idx,
                          spontaneous_position_idx):
        print('\t\t\t--> Include enzymatic reactions to pathways')
        for (p_id, p_item) in self.pathway_info.items():
            (pathway_name, lst_pathway_types, lst_pathways_links, lst_predecessors, lst_reactions,
             lst_reactions_layout, lst_key_reactions, lst_synonyms, lst_species, lst_taxonomic_range, lst_sup_pathways,
             lst_sub_pathways,
             lst_genes_names, lst_genes_ids) = p_item
            spontaneous = 0
            orphans = 0
            lst_ec = list()
            lst_unique_rxns = list()
            for r_id in lst_reactions[1]:
                if r_id in reactions_info:
                    ec_lst = reactions_info[r_id][ec_position_idx][1]
                    for ec in ec_lst:
                        lst_ec.append(ec)
                    if reactions_info[r_id][spontaneous_position_idx][1]:
                        spontaneous += 1
                    if reactions_info[r_id][orphan_position_idx][1]:
                        orphans += 1
                    if len(reactions_info[r_id][in_pathway_position_idx][1]) == 1:
                        if p_id in reactions_info[r_id][in_pathway_position_idx][1]:
                            lst_unique_rxns.append(r_id)

            # datum is comprised of {UNIQUE-ID: (COMMON-NAME, TYPES, PATHWAY-LINKS, PREDECESSORS,
            # REACTION-LIST, REACTION-LAYOUT, SPECIES, TAXONOMIC-RANGE, SUPER-PATHWAYS, SUB-PATHWAYS,
            # GENES-NAME, GENES-ID, ORPHANS, SPONTANEOUS, EC, UNIQUE REACTIONS)}
            datum = {p_id: (pathway_name,
                            lst_pathway_types,
                            lst_pathways_links,
                            lst_predecessors,
                            lst_reactions,
                            lst_reactions_layout,
                            lst_key_reactions,
                            lst_synonyms,
                            lst_species,
                            lst_taxonomic_range,
                            lst_sup_pathways,
                            lst_sub_pathways,
                            lst_genes_names,
                            lst_genes_ids,
                            ['ORPHANS', orphans],
                            ['SPONTANEOUS', spontaneous],
                            ['EC', lst_ec],
                            ['UNIQUE REACTIONS', lst_unique_rxns])}
            self.pathway_info.update(datum)


# https://github.com/arbasher/prepBioCyc/blob/master/src/biocyc.py"
class BioCyc(object):
    def __init__(self):
        self.list_kb_paths = list()
        self.processed_kb = OrderedDict()

        # List of ids
        self.protein_id = OrderedDict()
        self.gene_id = OrderedDict()
        self.enzyme_id = OrderedDict()
        self.compound_id = OrderedDict()
        self.reaction_id = OrderedDict()
        self.pathway_id = OrderedDict()
        self.ec_id = OrderedDict()
        self.gene_name_id = OrderedDict()
        self.go_id = OrderedDict()
        self.product_id = OrderedDict()
            
    def extract_info_from_database(self, db_path):
        pathway = Pathway()
        list_ids = [self.protein_id, self.go_id, self.gene_id, self.gene_name_id,
                            self.product_id, self.enzyme_id, self.reaction_id, self.ec_id,
                            self.pathway_id, self.compound_id]

        pathway.process_pathways(pathway_idx_list_ids=8, list_ids=list_ids, data_path=db_path, header=False)


def transform_predictions(pwlabel_idx, n_pws, biocyc):
    y_hat = np.zeros((n_pws), dtype=np.int8)
    missing_pws = []

    for pw in biocyc.pathway_id.keys():
        if pw in pwlabel_idx:
            y_hat[int(pwlabel_idx[pw])] = 1
        else:
            missing_pws.append(pw)
    print(f'missing {missing_pws}') # MetaCyc 22
    
    return y_hat

def evaluate_pathologic(pwlabel_idx, n_pws):
    gold_pgdbs = ['aracyc', 'ecocyc', 'humancyc', 'leishcyc', 'trypanocyc', 'yeastcyc']
    order = ['ecocyc', 'humancyc', 'aracyc', 'yeastcyc', 'leishcyc', 'trypanocyc']
    hamms=[]
    precs = []
    recalls = []
    f1s = []
    
    data_path='../../data/processed/pathologic/'
    y = '../../data/processed/gold_dataset_6_y.npy'
    with open(y, 'rb') as y_file:
        gold_y = np.load(y_file, allow_pickle=False)
        for i, pgdb in enumerate(gold_pgdbs):
            y = gold_y[i]
            
            biocyc = BioCyc()
            biocyc.extract_info_from_database(db_path=data_path+pgdb)
            print(pgdb)
            y_hat=transform_predictions(pwlabel_idx, n_pws, biocyc)
            
            hamms.append(round(hamming_loss(y, y_hat),4))
            precs.append(round(precision_score(y, y_hat),4))
            recalls.append(round(recall_score(y, y_hat),4))
            f1s.append(round(f1_score(y, y_hat),4))
        
        def reorder():
            pgdb_map = {pgdb:i for i, pgdb in enumerate(gold_pgdbs)}
            
            reordered_hamms = [hamms[pgdb_map[pgdb]] for pgdb in order]
            reordered_precs = [precs[pgdb_map[pgdb]] for pgdb in order]
            reordered_recalls = [recalls[pgdb_map[pgdb]] for pgdb in order]
            reordered_f1s = [f1s[pgdb_map[pgdb]] for pgdb in order]
            
            return reordered_hamms, reordered_precs,\
                    reordered_recalls, reordered_f1s
                
        def write_results(reordered_hamms, reordered_precs,\
                        reordered_recalls, reordered_f1s):
            with open('pathologic.csv', 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', 
                                        quoting=csv.QUOTE_MINIMAL)
                
                order.insert(0,'metrics')
                reordered_hamms.insert(0,'hamming')
                reordered_precs.insert(0,'prec')
                reordered_recalls.insert(0,'recall')
                reordered_f1s.insert(0,'f1')
                
                csvwriter.writerow(order)
                csvwriter.writerow(reordered_hamms)
                csvwriter.writerow(reordered_precs)
                csvwriter.writerow(reordered_recalls)
                csvwriter.writerow(reordered_f1s)
        
    reordered_hamms, reordered_precs, reordered_recalls, reordered_f1s=reorder()
    write_results(reordered_hamms, reordered_precs, reordered_recalls, reordered_f1s)

csv_file = '../../references/idx_pw.csv'
pwlabel_idx = load_csvindex(csv_file, 'Pathway', 'index')
n_pws = len(pwlabel_idx)

evaluate_pathologic(pwlabel_idx, n_pws)