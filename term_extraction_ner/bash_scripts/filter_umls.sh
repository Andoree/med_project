#!/bin/bash

MRCONSO_PATH=/home/tlenusik/DATA/medical_vocabs_and_ontologies/UMLS/UMLS2019AB/MRCONSO.RRF
MRSTY_PATH=/home/tlenusik/DATA/medical_vocabs_and_ontologies/UMLS/2020AA/META/MRSTY.RRF
ONTOLOGY=MDRRUS
SAVE_FULL_DICTIONARY_PATH=umls_filtering/full_vocabs/full_umls_mdrrus.txt
LANG=RUS

UMLS_GROUPS_FILE=umls_filtering/SemGroups.txt
FILTERED_VOCAB_PATH=umls_filtering/vocabs_filtered_columns/ru_meddra_vocab.tsv
KEEP_COLUMNS_FILE=umls_filtering/rename_maps/rename_mdrrus_map.txt

LANG=C.UTF-8 LC_ALL=C.UTF-8 python filter_umls.py \
--mrconso $MRCONSO \
--mrsty $MRSTY_PATH \
--save_to $SAVE_FULL_DICTIONARY_PATH \
--save_all \
--ontology $ONTOLOGY \
--join_mrconso_mrsty \
--lang $LANG &

LANG=C.UTF-8 LC_ALL=C.UTF-8 python umls_filtering/code/merge_umls_files.py \
--groups_file $UMLS_GROUPS_FILE\
--vocab_path $SAVE_FULL_DICTIONARY_PATH \
--keep_columns_file $KEEP_COLUMNS_FILE \
--output_path $FILTERED_VOCAB_PATH



