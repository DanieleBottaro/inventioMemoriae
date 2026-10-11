import lxml.etree as ET
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

# 1. Load the source files
dom = ET.parse('../xml_json_files/inMe_TEI.xml')
xslt = ET.parse('../xslt/inMe_XSLT.xslt')

# 2. Initialize the transformation engine
transform = ET.XSLT(xslt)
new_html = transform(dom)

raw_html = str(new_html)

soup = BeautifulSoup(raw_html, 'html.parser')
formatter = HTMLFormatter(indent=4)

indented_html = soup.prettify(formatter=formatter)

# 3. Write the static HTML file to disk
with open('../html_files/inMe_stylised_xml.html', 'wb') as f:
    f.write(indented_html.encode('utf-8'))