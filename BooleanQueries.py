import re
from flask import Flask, request
from flask_cors import CORS, cross_origin
import pickle
from nltk.stem import PorterStemmer

data = ""
with open('inverted-index.p', 'rb') as fp:
    data = pickle.load(fp)

data2 = ""
with open('positional-index.p', 'rb') as fp:
    data2 = pickle.load(fp)


# print(type(data))

operators = {
    "or": 1,
    "and": 2,
    "not": 3,
    "/": 0
}
proximity_operator = [
    "/"
]


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

    # while staack is not empty appending
    while (operator_stack):
        output.append(operator_stack.pop())
    return output


ps = PorterStemmer()


def process_query(processed_quries, dictionary_inverted):
    selected_index = []
    for quries in processed_quries:
        if(quries == "and"):
            selected_index[0] = selected_index[0].intersection(
                selected_index[1])
            selected_index.remove(selected_index[1])
        elif (quries == "or"):
            selected_index[0] = selected_index[0].union(
                selected_index[1])
            selected_index.remove(selected_index[1])
        elif (quries == "not"):
            selected_index[0] = selected_index[0].difference(
                selected_index[1])
            selected_index.remove(selected_index[1])
        else:
            selected_index.append(dictionary_inverted[quries][0])
    return selected_index[0]


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
                        if(int(val)+(int(jump)+1) == int(val2)):
                            x.add(key)
    return x


app = Flask(__name__)
# cors = CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)


@app.route('/process-query', methods=['POST'])
@cross_origin()
def process():
    try:
        if request.method == 'POST':
            q = request.get_json()["query"]
            print(q)

            result = ""
            if(re.search("/[0-9]", q)):
                result = proximity_search(q.split(" "), data2)
            else:
                result = process_query(postfix(q.split(" ")), data)
            return {"resultset": list(result)}
    except:
        return {"err": str("ERROR DUE TO INVALID QUERY")}


if __name__ == '__main__':
    app.run()
