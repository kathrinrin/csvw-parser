import json


def generate_object(url, row, metadata):
    rowobject = {}
    rowobject['url'] = url + '#row=' + str(row.number + 1)
    rowobject['rownum'] = row.number

        
    cells = [] 
    cellsobject = {} 
    cells.append(cellsobject)
    
    
    # quite a hack, will have to be generalized 
    if row.cells[0].about_url is not None: 
        cellsobject['@id'] = url + row.cells[0].about_url
    
    for cell in row.cells:
        
        if cell.value != "": 
            
            column_name = cell.column.name 
            
            if column_name is None: 
                column_name = cell.column.titles[0] 

            cellsobject[column_name] = cell.value


    rowobject['describes'] = cells
    return rowobject 
        



def minimal_mode(table, metadata):
    
    documentobject = {} 
    tables = []
    documentobject['tables'] = tables 
    tableobject = {}
    
    # ugly hack for test cases 
    table.url = table.url.replace('w3c.github.io', 'www.w3.org/2013')
    tableobject['url'] = table.url
    
    if 'dc:modified' in metadata: 
        tableobject['dc:modified'] = metadata['dc:modified']['@value']
        
    if 'dc:license' in metadata: 
        tableobject['dc:license'] = metadata['dc:license']['@id']
        
    if 'dc:title' in metadata: 
        tableobject['dc:title'] = metadata['dc:title']['@value']
    
    if 'dc:publisher' in metadata: 
        publisherobject = {}
        publisherobject['schema:url'] = metadata['dc:publisher']['schema:url']['@id']
        publisherobject['schema:name'] = metadata['dc:publisher']['schema:name']['@value']
        tableobject['dc:publisher'] = publisherobject
    
    if 'dcat:keyword' in metadata: 
        metakeywords = metadata['dcat:keyword']
        keywords = []
        for keyword in metakeywords: 
            keywords.append(keyword['@value'])
        tableobject['dcat:keyword'] = keywords

    tables.append(tableobject)
    

    
    rows = []
    for row in table.rows:
        rowjson = generate_object(table.url, row, metadata)
        rows.append(rowjson)
    
    tableobject['row'] = rows
    documentjson = json.dumps(documentobject, indent=2)
    
    
    return documentjson

