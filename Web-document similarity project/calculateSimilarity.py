import sys
import extract_webpage as ew

if len(sys.argv) != 3:
    print("Run code as calculateSimilarity.py args1 args2 as ")
    sys.exit(1)

arg1 = sys.argv[1]
arg2 = sys.argv[2]
ngram = int(input("Enter the n gram value: "))
n_overlapping = int(input("Enter the number of overlapping value: "))
if ngram <= n_overlapping:
    raise ValueError("overlapping value must be less than n gram value!")


punctuation = ['.', ',', ':', ';',  '-','/', '\\', '\'','!', '?', '(',')', '+','[', ']', '{', '}', '|', '&', '^', '%', '<', '>', '~', '#']
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
    for word in range(0, n, ngram - n_overlapping):   # steping with ngram - n_overlapping steps for n overlapping
        ngram_data = " ".join(data[word:word+ngram])  # n gram collector
        if ngram_data not in word_fre_dict:
            word_fre_dict[ngram_data] = 1
        else:
            word_fre_dict[ngram_data] += 1
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
            hash += ascii_value*(p**j)  # hash(s) = s[0] + s[1].p  + s[2].p^2   + ..... + s[n-1].p^(n-1)
        hash = hash % m
        binary_string = bin(hash)[2:]  # converting hash into binary value  
        binary_string_64_bit = binary_string.zfill(64) # (Zerofill) making the binary value with 64 bit by filling the extra 0 in front
        words_with_hash[word] = (word_dict[word], binary_string_64_bit)
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
    simhash1 = computeSimHash(textcontent1.lower())
    textcontent2 = ew.get_text_from_web(arg2)
    simhash2 = computeSimHash(textcontent2.lower())
    print(compareSimhashes(simhash1,simhash2))