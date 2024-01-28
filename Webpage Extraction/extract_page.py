import requests

url = input("Enter the url to extract links, title and body : ")


def fetch_html_content(url):
    try:
        response = requests.get(url)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content: {e}")
        return None


def extract_webpage(data):
    result = ""
    tag = ""
    isTitle = False
    isBody = False
    isTagOpen = False
    
    for i in range(len(data)):
        if data[i] == '<':
            isTagOpen = True
            
        elif data[i] == '>':
            isTagOpen = False

        if isTagOpen :
            tag += data[i]
            
        elif not isTagOpen:
            checkLinks(tag)
            # if tag != "":
            #     print(tag)
            if tag == '<title':
                isTitle = True
            elif tag == '</title':
                isTitle = False
            elif tag == "<body":
                isBody = True
            elif tag == '</body':
                isBody = False
                
            if isBody or isTitle :
                ### uncomment it for better look
                # if not (data[i] == " " and result[-1] == " "):
                #     if data[i] not in ['>']:
                #         result = result + data[i]
                
                if data[i] not in ['\r','\n','>']:
                    result = result + data[i]
            tag = ""
    
    return result

def checkLinks(tag):
    start = tag.find('<a href')
    isLink = tag.find('http', start+7) != -1
    if start != -1 and isLink :
        first_quatation = tag.find('"',start+6)
        second_quatation = tag.find('"',first_quatation+1 )
        print(tag[first_quatation +1 :second_quatation])

if __name__ == '__main__':
    print(extract_webpage(fetch_html_content(url)))