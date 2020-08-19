import pickle


with open("toy/toy_hashed_data", "rb") as file:
    data = pickle.load(file)

with open("toy/toy_hashed_query", "rb") as file:
    query_hashes = pickle.load(file)

tmp = data + data
print(len(tmp))
with open('my_toy_hashed_data', 'wb') as f:
    pickle.dump(data + data, f)

