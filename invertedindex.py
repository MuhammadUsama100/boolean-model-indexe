import nltk
from nltk.tokenize import RegexpTokenizer
#from nltk.stem import PorterStemmer
from pattern.en import singularize
import pickle

array = []
for i in range(1, 51):
    file1 = open(
        "G:/University/SEMESTER/SIXSEMESTER/IR/assignment/ass1/dataset/ShortStories/" + str(i) + ".txt", 'r',  encoding='utf8')
    Lines = file1.readlines()
    array.append(Lines)

# read stopwords
file2 = open(
    "G:/University/SEMESTER/SIXSEMESTER/IR/assignment/ass1/dataset/Stopword-List.txt", 'r',  encoding='utf8')
lines = file2.readlines()

# creating a list of stop word each word is strip before adding to stop word list
stopwords = []
for i in lines:
    if(i.rstrip("\n") != ""):
        stopwords.append(i.rstrip("\n").strip())
print(stopwords)


#ps = PorterStemmer()

# breaking the value to tokens


def preprocessing(sentence):
    sentence = sentence.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(sentence)
    stem_tokens = []
    # for token in tokens:
    #     stem_tokens.append(ps.stem(token))
    for token in tokens:
        stem_tokens.append(singularize(token))
    filtered_tokens = [word for word in stem_tokens if not word in stopwords]
    return filtered_tokens


processed_array = []
for doc in array:
    processed_doc = []
    for lines in doc:
        processed_doc.extend(preprocessing(lines))
    processed_doc.sort()
    processed_array.append(processed_doc)

print(len(processed_array))

# used data structure in inverted index list dic/maps set
inverted_index = {}

for index in range(1, len(processed_array)+1):
    for word in processed_array[index-1]:
        if word not in inverted_index:
            inverted_index[word] = [set()]

        if word in inverted_index:
            inverted_index[word][0].add(index)

for key in inverted_index:
    inverted_index[key].append(len(inverted_index[key][0]))

#inverted_index = collections.OrderedDict(sorted(inverted_index.items()))
# f = open("inverted-index.txt", "w")
# f.write(str(inverted_index))
# f.close()

# store is file a binary object
with open('inverted-index.p', 'wb') as fp:
    pickle.dump(inverted_index, fp, protocol=pickle.HIGHEST_PROTOCOL)
