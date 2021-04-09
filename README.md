# Inter-IIT Tech Meet 9.0
# IITB: Bridgei2i Automated Headline and Sentiment Generator
## Problem Statement:

### Task 1: Domain Classification
- **Approach**: Our approach for this task involves matching words in the given text with a hand crafted bag of words to determine if the tweet/article is relevant to mobile technology. We use fuzzy string matching to account for spelling errors 
- **Steps to run**: After moving the data file ``evaluation_data.csv`` in the root folder, run the commant ``python3 rule_based.py``. The output file will be generated in the root folder with the name ``eval_preds_mob_tech.csv`` 
- **Performance**: The code takes around 10seconds to run on a 4 core Intel(R) Core(TM) i5CPU @ 2.50GHz machine  

### Task 2: Brand Identification and Sentiment Generator
<p align="center">
  <img src="https://user-images.githubusercontent.com/34444901/114154997-9d3d6280-993e-11eb-9d8a-7675b542c6b2.png" alt="task2"/>
</p>

- **Approach**: In this task we focused on leveraging the essentially finite set of companies. We already know from problem description that we expect to find only real-world mobile tech and mobile accessory companies in the tweets and the articles. So it makes sense to construct a similar robust set of companies for which our model will look for, in the documents. Upon brand identification we categorize a tweet/article into one of two categories:&nbsp;

      i.	Having a single brand present in the tweet/article
      ii.	Having multiple brands present in a given tweet/article
    If a given tweet/article falls into the first category then we pass it through a sentiment analysis model to identify the associated sentiment value.
    
- **Steps to run**: For the company extraction part, the experiments can be run directly using the bash script - ``bash extract_companies.sh`` in the ``Task 2 folder``. An example run has been shown where evaluation happens on the evaluation dataset released. All the data files have also been added to the submission folder. Commented bash commands can be uncommented to run similar experiments on tweets and articles. The output of the evaluation is dumped in a JSON file in the following format:
    ```javascript
    {
      {
        "doc_id": ~~~~,
        "raw_text": ~~~~,
        "text": ~~~~,
        "companies": <list of gold companies if there in data, otherwise empty>,
        "company_extractions": {
          <company name>: [
            [
              <company instance>,
              [
                <sentences with context containing that instance>
              ]
            ]
          ]
        }
      },
    ...
    }
    ```
    For reference see ``data/evaluation_data.jsons.``
- **Performance**: The code takes around 4min. 10seconds to run on a 4 core Intel® Core™ i7CPU @ 2.30GHz machine


This JSON file is then used to make predictions, this is done by passing the tokenized paragraphs (into sentences) with the brand names to the fine tuned **m-BERT** model (trained as described in preliminary submission doc.) which then generates one out of three possible outcomes; we combine the list of all predictions made for a given brand (ex:[1,0,1,1], negative for this brand if the brand is mentioned 4 times), we then take the brand sentiment to be negative or positive depending on the number of number of occurrences of the positive or negative class (whichever appears more is taken to be the overall sentiment). If neither positive nor negative sentence is present then we take the brand sentiment to be neutral.
Trained on kaggle using GPU: the code is in the file ``Task2/subtask-2_sentiment_prediction.ipynb``
- Training time: 40 min for the complete dataset
- Inference time: 90 sec for the complete dataset  

### Task 3: Headline Generation/ Summarisation 
<p align="center">
  <img src="https://user-images.githubusercontent.com/34444901/114154939-90207380-993e-11eb-88ff-e75e0da2ab4a.png" alt="task3"/>
</p>

- **Approach**: We begin with a thorough examination of the dataset. The dataset has a lot of variability in the sensethat we could find all 4 kinds of translated/transliterated articles between the English and Hindi Languagei.e. Hindi and English written in both devanagari as well as roman scripts. Quite naturally, this implies that the problem would be more tractable if we get it all in one setting (roman). This would also vastly increase the scalability and robustness of the solution as then we can use this for articles in any languagerather than hinging on just english-hindi ones. Moreover, this would open the doors to the plethora ofexcellent pretrained models available for the english language. 
    We clean the dataset and translate it using a widely available free python API ``translator``.  This uses translation interfaces of Google, Yandex, Microsoft(Bing), Baidu, Alibaba etc to output decent englishtranslations of the input article.
    Then we finetuned the dataset on **distilBART**, a distilled (lighter) version of BART, denoising autoencoders for pretraining sequence-to-sequence models. For fine tuning on the given dataset, we use all the articles at the initial stages and not just the domain ones. We divide the articles into train and validation splits. For every tenth article we add it to the val dataset. Hence, the training set has 3600 pairs while the validation one has 400. We finetune it for 5000 steps. 
- **Steps to run**: For preprocessing: run ``bash translate.sh`` with the ``evaluation_data.csv``  in the same path. It generates a ``test.source`` file. All relevant preprocessed data available at: https://drive.google.com/drive/folders/1IIWsGj8aLcSr8NLev4rAooOxpkIrhJQ7?usp=sharing
For model training and evaluation:
Run ``Train_and_eval.ipynb``  notebook. Note that paths need to be changed. Please note to make this change: at line 118 replace ``self.sharded_dpp`` by ``false`` in ``seq2seq_trainer.py`` after installation of ``transformer`` library.
The trained model is available at https://drive.google.com/drive/folders/13IurxI9KMti9QFtEw57XsPxZVEwBhUo3?usp=sharing
For training as well as evaluation, you will need to run different parts of the code in the notebook.
- **Performance**: Preprocessing takes around 30-40 seconds per article. Inference using the model takes 1 second per article. Total Training Time:Around 2.5 hours for 5000 steps on Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz

----- 
## Team Members

- Pragyanshu Singh
- Pranav
- Yash Gupta
- Yash Jain
- Aishwarya Agarwal  
- Aman Kansal
- Anshul Nasery
- Deepti Mittal
- Siddhesh P Pawar
- Shubham Mishra

The contingent won Bronze Medal 🥉 in the Bridgei2i Automated Headline and Sentiment Generator challenge.

