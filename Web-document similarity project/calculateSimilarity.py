import sys
# sys.path.append("WebScrapping")
import extract_webpage as ew


if len(sys.argv) != 3:
    print("Run code as calculateSimilarity.py args1 args2 as ")
    sys.exit(1)

arg1 = sys.argv[1]
arg2 = sys.argv[2]

punctuation = ['.', ',', ':', ';',  '/', '\\', '!', '?', '(',')', '[', ']', '{', '}', '|', '&', '^', '%', '<', '>', '~', '#']
def remove_panctuation(original):
    cleaned_data = ""
    for i in original:
        if i not in punctuation:
            cleaned_data +=i
    return cleaned_data

def word_frequency(content):
    data = content.split()
    n = len(data)
    word_fre_dict = {}
    for word in range(n):
        ngram = " ".join(data[word:word+5])
        if word not in word_fre_dict:
            word_fre_dict[ngram] = 1
        else:
            word_fre_dict[ngram] += 1
    return word_fre_dict

def computeHashValue(word_dict):
    p = 53
    m = 2**64
    words_with_hash = {}
    for word in word_dict:
        hash = 0
        n=len(word)
        for j in range(n):
            ascii_value = ord(word[j])
            hash += ascii_value*(p**j)  # s[n-1].p^(n-1)
        hash = hash % m
        binary_string = bin(hash)[2:]
        padded_binary_string = binary_string.zfill(64)
        words_with_hash[word] = (word_dict[word],padded_binary_string)
    return words_with_hash

def computeSimHash(original_text):
    content = remove_panctuation(original_text)
    word_dict = word_frequency(content)
    hash64value = computeHashValue(word_dict)
    weight_sum_vector = []
    for i in range(64):
        weight = 0
        for j in hash64value:
            if hash64value[j][1][i] == "1":
                weight += hash64value[j][0]
            else:
                weight -= hash64value[j][0]
        weight_sum_vector.append(weight)
    fingerprint_vector = [1 if weight > 0 else 0 for weight in weight_sum_vector]
    return fingerprint_vector

def compareSimhashes(simhash1,simhash2):
    commonBits = 0
    for i in range(64):
        if simhash1[i] == simhash2[i]:
            commonBits+=1

    return f"The Common bits percentage in simhashes is : {100*commonBits/64} %"

if __name__ == "__main__":
    textcontent1 = ew.get_text_from_web(arg1)
    simhash1 = computeSimHash(textcontent1)
    textcontent2 = ew.get_text_from_web(arg2)
    simhash2 = computeSimHash(textcontent2)
    print(compareSimhashes(simhash1,simhash2))

