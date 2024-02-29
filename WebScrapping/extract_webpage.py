import requests

def fetch_html_content(url):
    try:
        response = requests.get(url)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content: {e}")
        return None

def extract_title(html_content):
    start = html_content.find("<title")
    end = html_content.find("</title")
    return html_content[start+7:end]

def extract_body(html_content):
    start = html_content.find("<body")
    end = html_content.find("</body")
    return html_content[start:end]

def extract_main_content(html_content):
    is_tag = False
    is_script = False
    is_style = False
    is_span = False
    text_content = ""

    for i in range(len(html_content)):

        if html_content[i] == '<':
            is_tag = True
            if html_content[i:i+6].lower() == '<style':
                is_style = True
            elif html_content[i] == '<' and html_content[i:i+7].lower() == '</style':
                is_style = False
            if html_content[i:i+7].lower() == '<script':
                is_script = True
            elif html_content[i] == '<' and html_content[i:i+8].lower() == '</script':
                is_script = False
            if html_content[i:i+5].lower() == '<span':
                is_span = True
            elif html_content[i] == '<' and html_content[i:i+6].lower() == '</span':
                is_span = False

        elif html_content[i] == '>':
            is_tag = False
            continue

        if not is_tag and not is_script and not is_style and not is_span:
            text_content += html_content[i]
    return text_content

def remove_extra_spaces(text_content):
    cleaned_data=" "
    for i in range(len(text_content)):
        if (text_content[i] in ["\n","\r","\t"] and cleaned_data[-1] in ["\n","\r","\t"]):
            continue
        cleaned_data += text_content[i]
    return cleaned_data

def checkLinks(tag):
    start = tag.find('<a href')
    link = tag.find('http',start+7,start+21)
    isLink =  link != -1
    if start != -1 and isLink :
        first_quatation = tag.find('"',start+6)
        second_quatation = tag.find('"',first_quatation+1 )
        print(tag[first_quatation +1 :second_quatation])

def extract_link(html_content):
    tag = ""
    i = 0
    while i < len(html_content):
        if html_content[i] == '<':
            isTagOpen = True

        elif html_content[i] == '>':
            isTagOpen = False

        if isTagOpen :
            tag += html_content[i]

        elif not isTagOpen :
            checkLinks(tag)
            tag = ""
        i = i+1

def get_text_from_web(url):
    html_content = fetch_html_content(url)
    body_content = extract_body(html_content)
    text_content = extract_main_content(body_content)
    textdata = extract_title(html_content) +"\n"+ remove_extra_spaces(text_content)
    processed_text = ""
    i = 0
    while i < len(textdata)-1:
        if textdata[i] == "&" and textdata[i+1] == "#":
            t = textdata.find(";",i)
            i = t+1
            continue 
        processed_text += textdata[i]
        i += 1
    return processed_text 

# if __name__ == "__main__":
#     print(get_text_from_web("https://sitare.org/univ/"))

