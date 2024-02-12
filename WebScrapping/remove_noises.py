def remove_extra_spaces(text_content):
    cleaned_data=" "
    for i in range(len(text_content)):
        if (text_content[i] in ["\n","\r","\t"] and cleaned_data[-1] in ["\n","\r","\t"]):
            continue
        cleaned_data += text_content[i]
    return cleaned_data

def cleaned_data(text):
    data = ""
    i = 0
    while i < len(text)-1:
        if text[i] == "&" and text[i+1] == "#":
            t = text.find(";",i)
            i = t+1
            continue 
        data += text[i]
        i += 1
    return data 