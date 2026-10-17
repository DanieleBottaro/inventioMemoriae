import lxml.etree as ET
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

#load the source files
dom = ET.parse('../xml_json_files/inMe_TEI.xml')
xslt = ET.parse('../xslt/inMe_XSLT.xslt')

#initialize the transformation engine
transform = ET.XSLT(xslt)
new_html = transform(dom)

raw_html = str(new_html)

#beautify the HTML output using BeautifulSoup and the HTMLFormatter to indent the HTML code for better readability
soup = BeautifulSoup(raw_html, 'html.parser')
formatter = HTMLFormatter(indent=4)

indented_html = soup.prettify(formatter=formatter)

#write the static HTML file to disk
with open('../html_files/inMe_stylised_xml.html', 'wb') as f:
    f.write(indented_html.encode('utf-8'))