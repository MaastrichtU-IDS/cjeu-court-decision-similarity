#!/usr/bin/env python
# coding: utf-8

# # EUR-LEX Case Similarity Notebook: Doc2Vec

# ### Abstract: 
# #### This notebook implements Doc2Vec document similarity measures (based on Word2Vec) on EUR-LEX judgements and orders

# ### Step 1. Import data & resources

# #### I.e. import full texts of cases from file, define a mapping to case IDs so we can lookup Doc2Vec similarity values by caseID, import stopwords file

# In[ ]:


from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import os
import pickle
import nltk
from nltk.corpus import stopwords
import time

start = time.time()

print("Doc2Vec document similarity analyser")
print("------------------------------------")
print()

print("* Building index of documents...")

# List all documents in directory
path = "../inputdata/full_texts_all_cases/"

# Import stopwords           
stopwordsfile = "../script_resources/stopwords.pickle"
stopwords_full = []
with open(stopwordsfile, "rb") as f:
    tmp = pickle.load(f)
    stopwords_full.extend(list(tmp))
    stopwords_full.extend(stopwords.words('english'))
    
stopwords_full = list(set(stopwords_full))

#print(stopwords_full)

# Only keep celex number from filename
def cleanfilename(name):
    result = ""
    result = name.replace("full_text_","")
    result = result.replace(".txt","")
    return result

def remove_stopwords(text):
    global stopwords_full
    for item in stopwords_full:
        text = text.replace(str(item),'')
    return text

# Import files and define mapping between case IDS and full texts   
files = []
index_to_celex = {}
datafortraining = []
index = 0
for r, d, f in os.walk(path):
    for file in f:
        if '.txt' in file:
            files.append(os.path.join(r, file))
            celexnum = cleanfilename(os.path.basename(file))
            with open (path+file, "r", encoding="utf-8" ) as myfile:
                data = myfile.read().replace('\n', '')
                data = remove_stopwords(data)
                datafortraining.append(data)
                index_to_celex[index] = file
                index += 1

documents = [TaggedDocument(file, [i]) for i, file in enumerate(datafortraining)]

print(" Index successfully built!")
print()


# ### Step 2. Train Doc2Vec model on input case texts

# In[ ]:


import os.path
from gensim.test.utils import get_tmpfile

print("* Loading / training Doc2Vec models...")

model_32 = None
model_64 = None
model_128 = None
model_256 = None

fname_32 = None
fname_64 = None
fname_128 = None
fname_256 = None

print()
print("* Vector size 32")
print()

if os.path.exists(os.path.join(os.path.join(os.path.realpath('..'), "script_resources"), "doc2vec_32.model")):
    print(" loading model from file...")
    fname_32 = get_tmpfile(os.path.join(os.path.join(os.path.realpath('..'), "script_resources"), "doc2vec_32.model"))
    model_32 = Doc2Vec.load(fname_32)
    print(" successfully loaded model!")
else:
    print(" training model...")
    model_32 = Doc2Vec(documents, vector_size=32, window=5, min_count=1, workers=4)
    model_32.train(documents, total_examples=model_32.corpus_count,epochs=20)
    print(" successfully trained model!")
    print(" saving model to file...")
    fname_32 = get_tmpfile(os.path.join(os.path.join(os.path.realpath('..'), "script_resources"), "doc2vec_32.model"))
    model_32.save(fname_32)
    print(" successfully saved model!")
    
print()

print("* Vector size 64")
if os.path.exists(os.path.join(os.path.join(os.path.realpath('..'), "script_resources"), "doc2vec_64.model")):
    print(" loading model from file...")
    fname_64 = get_tmpfile(os.path.join(os.path.join(os.path.realpath('..'), "script_resources"), "doc2vec_64.model"))
    model_64 = Doc2Vec.load(fname_64)
    print(" successfully loaded model!")
else:
    print(" training model...")
    model_64 = Doc2Vec(documents, vector_size=64, window=5, min_count=1, workers=4)
    model_64.train(documents, total_examples=model_64.corpus_count,epochs=20)
    print(" successfully trained model!")
    print(" saving model to file...")
    fname_64 = get_tmpfile(os.path.join(os.path.join(os.path.realpath('..'), "script_resources"), "doc2vec_64.model"))
    model_64.save(fname_64)
    print(" successfully saved model!")
    
print()

print("* Vector size 128")
if os.path.exists(os.path.join(os.path.join(os.path.realpath('..'), "script_resources"), "doc2vec_128.model")):
    print(" loading model from file...")
    fname_128 = get_tmpfile(os.path.join(os.path.join(os.path.realpath('..'), "script_resources"), "doc2vec_128.model"))
    model_128 = Doc2Vec.load(fname_128)
    print(" successfully loaded model!")
else:
    print(" training model...")
    model_128 = Doc2Vec(documents, vector_size=128, window=5, min_count=1, workers=4)
    model_128.train(documents, total_examples=model_128.corpus_count,epochs=20)
    print(" successfully trained model!")
    print(" saving model to file...")
    fname_128 = get_tmpfile(os.path.join(os.path.join(os.path.realpath('..'), "script_resources"), "doc2vec_128.model"))
    model_128.save(fname_128)
    print(" successfully saved model!")

print()
    
print("* Vector size 256")
if os.path.exists(os.path.join(os.path.join(os.path.realpath('..'), "script_resources"), "doc2vec_256.model")):
    print(" loading model from file...")
    fname_256 = get_tmpfile(os.path.join(os.path.join(os.path.realpath('..'), "script_resources"), "doc2vec_256.model"))
    model_256 = Doc2Vec.load(fname_256)
    print(" successfully loaded model!")
else:
    print(" training model...")
    model_256 = Doc2Vec(documents, vector_size=256, window=5, min_count=1, workers=4)
    model_256.train(documents, total_examples=model_256.corpus_count,epochs=20)
    print(" successfully trained model!")
    print(" saving model to file...")
    fname_256 = get_tmpfile(os.path.join(os.path.join(os.path.realpath('..'), "script_resources"), "doc2vec_256.model"))
    model_256.save(fname_256)
    print(" successfully saved model!")
print()


# ### Step 3. Import sample cases

# In[ ]:


path = "../inputdata/full_texts_all_cases/"

def getfile(celexnumber):
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if celexnumber in file:
                return file
    return None

def celex_to_index(celexnumber):
    file = getfile(celexnumber)
    for k, v in index_to_celex.items():
        if v == file:
            return k
    return -1

import pandas as pd

print("* Importing sample cases...")
# Fetch sample cases from file
def get_sample_cases(topic):
    data = pd.read_csv("../inputdata/sampled_cases.csv")
    relevant_rows = data[data['topic'] == topic]
    return relevant_rows['source'].tolist()

# Celex numbers of reference cases
publichealth = get_sample_cases('public health')
socialpolicy = get_sample_cases('social policy')
dataprotection = get_sample_cases('data protection')

publichealth_indices = []
socialpolicy_indices = []
dataprotection_indices = []
sample_cases_indices = []

for item in publichealth:
    sample_cases_indices.append(celex_to_index(item))

for item in socialpolicy:
    sample_cases_indices.append(celex_to_index(item))

for item in dataprotection:
    sample_cases_indices.append(celex_to_index(item))

print(" Successfully imported sample cases!")
print()


# ### Step 4. Define functions mapping between case ID, filename, and associated full text (references to same document)

# In[ ]:


# Function to convert entire similarity results to case ID references
def convert_to_case_references(doc2vec_result):
    global index_to_celex
    result = []
    for item in doc2vec_result:
        case_reference = cleanfilename(index_to_celex[item[0]]) # convert to case reference
        similarity_value = item[1]
        result.append((case_reference,similarity_value))
    return result


# ### Step 5. Define functions to look up citations for a given case, and to check if there is a citation link between two cases

# In[ ]:


print("* Import citations for cases...")
citations = pd.read_csv('../inputdata/all_cases_citations.csv')
print(" Successfully imported citations!")
print()

def find_cited_cases(celexnumber):
    global citations
    relevantsource = citations[citations['source'] == celexnumber]
    return relevantsource['target'].tolist()

def exists_citation_link_between(celexnumber1,celexnumber2):
    global citations
    relevantsource1 = citations[citations['source'] == celexnumber1]
    relevantsource2 = citations[citations['source'] == celexnumber2]
    if celexnumber2 in relevantsource1['target'].tolist() or celexnumber1 in relevantsource2['target'].tolist():
        return True
    return False


# ### Step 6. Look up top n similar cases per sample case

# In[ ]:


results = []

def lookup_similar_cases(sample_cases, n, topic, model, modelfilename):
    global results

    for item in sample_cases:
        similar_cases = model.docvecs.most_similar(celex_to_index(item), topn=n)
        similar_cases_references = convert_to_case_references(similar_cases)
        for reference in similar_cases_references:
            method = modelfilename[-17:]
            method = method.replace(".model","")
            method = method.replace('\\',"")
            method = method + str("_default")
            results.append([item,reference[0],reference[1],method,exists_citation_link_between(item,reference[0]),topic])


# In[ ]:


print("* Computing similar cases...")

lookup_similar_cases(publichealth,20,'public health', model_32, fname_32)
lookup_similar_cases(publichealth,20,'public health', model_64, fname_64)
lookup_similar_cases(publichealth,20,'public health', model_128, fname_128)
lookup_similar_cases(publichealth,20,'public health', model_256, fname_256)

lookup_similar_cases(socialpolicy,20,'social policy', model_32, fname_32)
lookup_similar_cases(socialpolicy,20,'social policy', model_64, fname_64)
lookup_similar_cases(socialpolicy,20,'social policy', model_128, fname_128)
lookup_similar_cases(socialpolicy,20,'social policy', model_256, fname_256)

lookup_similar_cases(dataprotection,20,'data protection', model_32, fname_32)
lookup_similar_cases(dataprotection,20,'data protection', model_64, fname_64)
lookup_similar_cases(dataprotection,20,'data protection', model_128, fname_128)
lookup_similar_cases(dataprotection,20,'data protection', model_256, fname_256)

print(" Successfully computed similar cases!")
print()


# ### Step 7. Write results to file

# In[ ]:


print("* Writing results to file...")
import csv
import os.path

if os.path.exists('../outputdata/results.csv') == False:
    results.insert(0,['source_case','similar_case','similarity_score','method','citation_link','source_case_topic'])
    
with open('../outputdata/results.csv', 'a', newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerows(results)
    
end = time.time()

print(" Successfully wrote files to file!")
print()
print(" Done!")
print()
print("* Time taken:",(end-start),"s")
