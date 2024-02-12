def extract_title(html_content):
    start = html_content.find("<title")
    end = html_content.find("</title")
    return html_content[start+7:end]
