from os.path import abspath, dirname

from lxml.html import fromstring, tostring, Element

project_path = dirname(dirname(abspath(__file__)))

def read():
    """Return doc element for the input html"""
    with open(project_path + '/timeline.html', 'r') as f:
        return fromstring(f.read().decode('utf-8'))

def load_partial(partial):
    with open(project_path + '/csv/partials/' + partial) as f:
        return fromstring(f.read().decode('utf-8'))

def postprocess(doc):
    # put html lang
    doc.attrib['lang']='mk'

    # add meta charset
    doc.cssselect('head')[0].insert(0, Element('meta', attrib={'charset': 'utf-8'}))

    # add header
    header = load_partial('header.html')
    doc.cssselect('body')[0].insert(0, header)

    return doc

def write(doc):
    """Write document to index.html"""
    with open(project_path + '/index.html', 'w') as f:
        f.write(tostring(doc, encoding='utf-8'))

if __name__=='__main__':
    doc = read()
    doc = postprocess(doc)
    write(doc)
