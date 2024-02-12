import requests
import sys
import getlink
import gettitle
import remove_noises as ns

url = sys.argv[1]

def fetch_html_content(url):
    try:
        response = requests.get(url)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content: {e}")
        return None

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



html_content = fetch_html_content(url)
print("################################################## Title ###################################################")
print("\n")
print(gettitle.extract_title(html_content))
print("\n")

body_content = extract_body(html_content)
text_content = extract_main_content(body_content)
print("################################################# Body Content #################################################")
print("\n")
print(ns.cleaned_data(ns.remove_extra_spaces(text_content)))
print("\n")
print("################################################ Links ################################################")
print("\n")
getlink.extract_link(html_content)

