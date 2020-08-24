Insilico ner
---

Overview: This repository contains code for named entity recognition and medical concept 
normalization


Data 
---
   1. CDR data -- located in ~/DATA/CDR_Data/insilico_ner_test
         ```
         |--l2r_training # contains data for learning to rank algorithm training
         |--mesh_vocab.txt # possibly unneeded ?
         |--train_val_data # data for training max-margin loss (not presented in repository)
         |--train_val_data_mesh_data_num_candidates_20 # same as train_val_data
        ```
   2. trials data  -- located ~/DATA/insilico_ner/
        ```
          |--all_entities # all extracted entities from trial.json
          ...
        ```
        
   3. Mesh mapping vocabs. Located in ~/DATA/UMLS/UMLS2016AA/
```
        |--mesh_filered.txt # mesh vocab restricted to cdr codes
        |--mesh_filered_embeddings.txt # biobert embeddings of mesh vocab 
        |--mesh_full.txt # full mesh 
        |--mesh_full_embeddings.txt #  full mesh vocab embeddings
```
        
Data processing pipeline
---
1. Extract entities. Input file must contain json formatted lines, 
    each line must contain "text" key (Entities will be extracted from 
    "text" column and  saved to  "entity_text" column) 
    Results  will be saved in json formatted file (each line is json). 
    Note that the script preserves all initial columns
    
    ```bash
    python extract_entities.py --jsonl  path/to/input/json --save_to path/to/save/json --trials [if trials are used as input]
    ```
2. Vocab vectorization
    
    ```bash
       python data_processing_uttils/vectorize_vocab.py --vocab_path /path/to/mapping/vocab  \
                                                     --save_to path/to/save/embeddings \
                                                     --bert_config_file path/to/bert/config_file \
                                                     --init_checkpoint path/to/ckpt \
                                                     --vocab_file path/to/bert/bpevocab
    ```

3. Entities vectorization
    
    ```bash
    python data_processing_uttils/vectorize_interventions.py --jsonl /path/to/input/json  \
                                                     --save_to path/to/save/json \
                                                     --bert_config_file path/to/bert/config_file \
                                                     --init_checkpoint path/to/ckpt \
                                                     --vocab_file path/to/bert/bpevocab
                                                     
    ```

4. Candidates generation
    
    ```bash
    python generate_candidates.py --jsonl path/to/input/jsonl \
                              --save_to path/to/save/json \
                              --config_path path/to/configuration/file \
                              --mapper ranking or es_mapper
    ```

    * es_mapper is elastic search mapper
        configuratio for es_mapper should contain: \
        1. vocab_path: /root/DATA/UMLS/UMLS2016AA/mesh_filered.txt -- path to vocabulary
        2. index_name: mesh_index  -- index name in elastic search engine
    * ranking is embeddings based mapper
        configuratio for es_mapper should contain: \
       1. concept_embeddings_path: /root/DATA/UMLS/UMLS2016AA/mesh_filered_embeddings.txt -- path to vocabulary embeddings file
       2. vocab_path: /root/DATA/UMLS/UMLS2016AA/mesh_filered.txt -- path to vocabulary
  
    Some default configurations are located in config file
    * ranking_mesh.yml is configuration for mapping to mesh vocabulary(restricted) using
      biobert embeddings
    * mesh_mapper_config.yml is configuration for mapping to mesh vocabulary(restricted) using
      elastic search
      
    **Note** to run the elastic mapper you need running elastic engine and indexes must be created. To create indexes run
    commands bellow:
    ```bash
     python  data_processing_utils/populate_es.py --index_name name --documents_file path/to/vocab \
                                                  --index_config_file path/to/index/config # example in configs/es_index_config.cfg
                                                    
    ```
     
    **Preprocessed data could be downloaded (generated candidates):**

    ```bash
     wget https://yadi.sk/d/xiGz3tPVE2n0rw # ncbi data
     wget https://yadi.sk/d/oHe-0XTW4xQV3w # med mentions data 
    ```
     
5. Combining the generated candidates:

    ```bash
    python data_processing_utils/combine_candidates.py --input_files paths/to/input/files \
                                                       --save_to path/to/save/combined/json
 
    ```
    
6. Add correct candidate ids to json file

    ```bash
    python data_processing_utils/prepare_train_data.py --jsonl path/input/json  \
                                                       --save_to path/to/save/json
    ```
7. Convert json to libsvm formatted file

    ```bash
       python data_processin_utils/to_libsvm_format.py --jsonl path/input/json  \
                                                       --save_to path/to/save/json \
                                                       --entity_embeddings path/to/vocab/embedding \
                                                       --vocab_file path/to/mapping/vocab
    ```
    
8. Train and predict learning to rank algorithm
    ```bash
       python tf_ranking_libsvm.py --train_path path/to/train/data \
                                   --vali_path path/to/validation/data \
                                   --test_path path/to/test/data \
                                   --output_dir path/to/directory/for/model/saving \
                                   --num_features number_of_features \
                                   --save_results_to path/to/store/predicitons/on/test \
                                   --train whether to train or not \
                                   --predict whether to predict or not 
    ```
    
9. Evaluation results

    ```bash
    python eval.py --jsonl path/to/gold/data \
                   --predicted_data path/to/prediction
    ```
    evaluate baselines
    ```bash
    python evaluation/evaluate_baselines.py --output path/to/file/with/candidates
    ```
