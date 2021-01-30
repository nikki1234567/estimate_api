# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 14:05:02 2021

@author: nikhi
"""


import json

configuration = {}

configuration['dataframe_paths'] = {'LabelFeatures':['Forum comment dataframe','label_features.csv'],
                                    'relation':['Contains mapping of feature keyword,synonyms and actual feature','relation-v2 (1).csv'],
                                    'labeltask':['Task dataframe with billable,non-billable & work hours','label_task.csv'],
                                    'LabelFeatureAdded': ['Forum comment dataframe with added extracted features and their extractors','label_features_added.csv'],
                                    'LabelTaskAdded':['Task dataframe with added extracted features and their extractors','label_task_added.csv'],
                                    'FeatureAddonlist':['Actual feature file','Featrues-Addon-list.csv']
                                    }

configuration['hyperparameters'] = { 'init':'random',
                                      'n_init':10,
                                      'max_iter':300,
                                      'random_state':42
                                    }

configuration['project_default'] = {'Push to staging':4,
                                    'Push to production':5,
                                    'QA':20,
                                    'Hosting and environment setup(local and production)':10,
                                    'Planning and analysis':10
                                    }

with open('configuration.txt', 'w') as outfile:
    json.dump(configuration, outfile)


