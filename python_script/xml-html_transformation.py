import lxml.etree as ET

# 1. Load the source files
dom = ET.parse('../xml_json_files/inMe_TEI.xml')
xslt = ET.parse('../xslt/inMe_XSLT.xslt')

# 2. Initialize the transformation engine
transform = ET.XSLT(xslt)
new_html = transform(dom)

# 3. Write the static HTML file to disk
with open('../html_files/inMe_stylised_xml.html', 'wb') as f:
    f.write(ET.tostring(new_html, pretty_print=True, method="html"))