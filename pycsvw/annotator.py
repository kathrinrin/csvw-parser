import re
import datetime

# first steps towards annotated table   

def annotate_table(table, metadata): 
    
    tableSchema = metadata.json()['tables'][0]['tableSchema']
    if 'primaryKey' in tableSchema: 
            primaryKey = metadata.json()['tables'][0]['tableSchema']['primaryKey']
            
    if 'aboutUrl' in tableSchema:    
        aboutURL = metadata.json()['tables'][0]['tableSchema']['aboutUrl']
        aboutColumn = re.search('%s(.*)%s' % ('{', '}'), aboutURL).group(1)
    
        
    for column in table.columns:
        
        index = int(str(column)[-1:]) - 1    
        metacolumn = metadata.json()['tables'][0]['tableSchema']['columns'][index]  
        
        if 'titles' in metacolumn: 
            titles = metacolumn['titles']
            for key, value in titles.items():
                for title in value: 
                    column.titles.append(title)
        
        if 'name' in metacolumn: 
            column.name = metacolumn['name']
        
        
        if (column.name != None) and (column.name == primaryKey):
            for row in table.rows: 
                row.primary_key = row.cells[index]
 
        
        if (column.name != None) and (str(column.name) == str(aboutColumn)):
            for row in table.rows: 
                for cell in row.cells: 
                    cell.about_url = aboutURL.replace('{' + aboutColumn + '}', row.cells[index].value)


        if 'datatype' in metacolumn: 
            
            datatype = metacolumn['datatype']
            column_datatype = datatype
            
            
            if 'base' in datatype: 
                column_datatype = {} 
                column_datatype["base"] = datatype['base']
                column_datatype["format"] = datatype['format']
                
                if column_datatype["base"] == "date": 
                    for cell in column.cells: 
                        if column_datatype["format"] == "M/d/yyyy": 
                            parsed_date = datetime.datetime.strptime(cell.value, '%m/%d/%Y').date()
                            cell.value = str(parsed_date)
    # 
            column.datatype = column_datatype
    
    return table, metadata 
        