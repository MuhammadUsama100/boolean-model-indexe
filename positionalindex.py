import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
import pickle

# file read

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


# breaking the value to tokens add position to the document
def preprocessing(sentence):
    sentence = sentence.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(sentence)

    return tokens


def preprocessing_all(tokens):
     # stem_tokens = []
    # for token in tokens:
    #     stem_tokens.append(ps.stem(token))
    token_with_position = []
    for i in range(0, len(tokens)):
        token_with_position.append({"token": tokens[i], "position": i})
    filtered_tokens = [
        word_with_position for word_with_position in token_with_position if not word_with_position["token"] in stopwords]
    return filtered_tokens


# function use to sort the data
def get_token(index):
    return index.get('token')


processed_array = []
for doc in array:
    processed_doc = []
    all_tokens = []
    for lines in doc:
        all_tokens.extend(preprocessing(lines))
    processed_doc.extend(preprocessing_all(all_tokens))

    processed_doc.sort(key=get_token)
    processed_array.append(processed_doc)


print(len(processed_array))


positional_index = {}

for index in range(1, len(processed_array)+1):
    for word_with_position in processed_array[index-1]:
        if (word_with_position["token"] not in positional_index):
            positional_index[word_with_position["token"]] = [{}]

        if word_with_position["token"] in positional_index:
            if str(index) not in positional_index[word_with_position["token"]][0]:
                positional_index[word_with_position["token"]][0][str(index)] = {
                    word_with_position["position"]}
            else:
                positional_index[word_with_position["token"]][0][str(
                    index)].add(word_with_position["position"])

for key in positional_index:
    positional_index[key].insert(0, len(positional_index[key][0]))


#inverted_index = collections.OrderedDict(sorted(inverted_index.items()))
f = open("positional-index.txt", "w")
f.write(str(positional_index))
f.close()

# store in file as binary
with open('positional-index.p', 'wb') as fp:
    pickle.dump(positional_index, fp, protocol=pickle.HIGHEST_PROTOCOL)
