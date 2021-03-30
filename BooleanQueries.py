import re
from flask import Flask, request
from flask_cors import CORS, cross_origin
import pickle

# read inverted and positional index using binary file read
data = ""
with open('inverted-index.p', 'rb') as fp:
    data = pickle.load(fp)

data2 = ""
with open('positional-index.p', 'rb') as fp:
    data2 = pickle.load(fp)

# priority operator
operators = {
    "or": 1,
    "and": 2,
    "/": 0
}
proximity_operator = [
    "/"
]
# calculate postfix with priority map


def postfix(infix_tokens):
    output = []
    operator_stack = []

    # creating postfix expression
    for token in infix_tokens:
        if (token in operators):
            if (operator_stack):
                current_operator = operator_stack[-1]
            while (operator_stack and operators[current_operator] > operators[token]):
                output.append(operator_stack.pop())
                if (operator_stack):
                    current_operator = operator_stack[-1]
            operator_stack.append(token)
        else:
            output.append(token.lower())

    while (operator_stack):
        output.append(operator_stack.pop())
    return output

# processing boolean queries
# input inverted index we could have used positional but to make things easy we used inverted index
# created an universal set to handel quries like : not A which have only one value with operator
# processed query with processed query array which cantain and array of input query in token form
# then query is solve with that processed query that have postfix tokens sorted with priority
# thet result is stored in an selected_index array


def process_query(processed_quries, dictionary_inverted):
    universal = set()
    for i in range(1, 51):
        universal.add(i)
    selected_index = []
    for index in range(0, len(processed_quries)):
        print(processed_quries[index])
        if(processed_quries[index] == "and"):
            selected_index[0] = selected_index[0].intersection(
                selected_index[1])
            selected_index.remove(selected_index[1])
        elif (processed_quries[index] == "or"):
            selected_index[0] = selected_index[0].union(
                selected_index[1])
            selected_index.remove(selected_index[1])
        elif (processed_quries[index] == "not"):
            if len(selected_index) == 0:
                try:
                    selected_index.append(universal.difference(
                        dictionary_inverted[processed_quries[index+1]][0]))
                except:
                    selected_index.append(universal)
                index = index + 2
            elif (len(processed_quries)-1 < index + 2):
                continue
            elif ((processed_quries[index+2] != "and" or processed_quries[index+2] != "or")):
                try:
                    selected_index.append(universal.difference(
                        dictionary_inverted[processed_quries[index+1]][0]))
                except:
                    selected_index.append(universal)
                index = index + 2
        else:
            try:
                selected_index.append(
                    dictionary_inverted[processed_quries[index]][0])
            except:
                selected_index.append(set())
    return selected_index[0]

# proximity search have query and positional index as parameters
# we have first extracted first value and second value from then positional index
# the term with / operator is assigned to jump operator
# know we have found the relavent position for words and then add the jump to that value and compared to other value


def proximity_search(proximity_query, positional_index):
    first_value = positional_index[proximity_query[0]][1]
    secound_value = positional_index[proximity_query[1]][1]
    jump = int(proximity_query[2].split("/")[-1])
    x = set()
    for key, value in first_value.items():
        for key2, value2 in secound_value.items():
            if (key == key2):
                for val in value:
                    for val2 in value2:
                        if(int(val)+(int(jump)+1) == int(val2) or int(val)-(int(jump)+1) == int(val2)):
                            x.add(key)
    return x


app = Flask(__name__)
CORS(app)

# this is a flask route which takes a query and returns a value that is used in the frontend to display the user the result
@app.route('/process-query', methods=['POST'])
@cross_origin()
def process():
    try:
        if request.method == 'POST':
            q = str(request.get_json()["query"]).lower().strip()
            print(q)
            result = ""
            if(re.search("/[0-9]", q)):
                result = proximity_search(q.split(" "), data2)
            else:
                print(postfix(q.split(" ")))
                result = process_query(postfix(q.split(" ")), data)
            return {"resultset": list(result).sort()}
    except:
        return {"err": str("ERROR DUE TO INVALID QUERY")}
