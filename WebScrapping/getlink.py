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