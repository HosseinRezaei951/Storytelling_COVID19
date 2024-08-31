import csv, os, datetime, copy, requests
import functions as func
from contextlib import closing
from tabulate import tabulate
import numpy as np  

############################################################
## DataFrame Class
############################################################
class DataFrame(str):

    def __init__(self):
        self.file_path = None
        self.headers = []
        self.rows = []
        self.index = None
        self.ncols = None
        self.nrows = None

   

    ################################################################
    ## READ, WRITE, COPY, UPDATE, PRINT METHODS
    ################################################################
    def read_csvOnline(self, url):
        with closing(requests.get(url, stream=True)) as r:
            f = (line.decode('utf-8') for line in r.iter_lines())
            reader = csv.DictReader(f, delimiter=',', quotechar='"')
            for row in reader:
                self.rows.append(row)            
        
        self.headers = [key for key, value in self.rows[0].items()]
        self.index = self.headers[0] 
        self.ncols = len(self.headers)
        self.nrows = len(self.rows) 

        for i in range(self.nrows):
            for key, value in self.rows[i].items():
                if value == "":
                    self.rows[i][key] = "NONE"


    def read_csvFile(self, file_path):
        self.file_path = file_path
        with open(self.file_path, mode='r' ,newline='') as csvfile:
            reader = csv.DictReader(csvfile) 
            for row in reader:
                self.rows.append(row)

       
        self.headers = [key for key, value in self.rows[0].items()]
        self.index = self.headers[0] 
        self.ncols = len(self.headers)
        self.nrows = len(self.rows)      

        for i in range(self.nrows):
            for key, value in self.rows[i].items():
                if value == "":
                    self.rows[i][key] = "NONE"


    def write_csvFile(self, file_path):
        self.file_path = file_path

        if os.path.exists(self.file_path):
            raise Exception("File already exists!")

        csvfile = os.popen("gzip > %s" % self.file_path, mode='w', newline='')\
        if self.file_path.endswith('.gz') else open(self.file_path, mode='w', newline='')

        with csvfile:
            writer = csv.DictWriter(csvfile, self.headers)       
            writer.writeheader()  
            writer.writerows(self.rows)  
   

    def copy_dataFrame(self):
        new_DataFrame = DataFrame()
        new_DataFrame = copy.deepcopy(self)
        return new_DataFrame


    def update_info(self):
        self.nrows = len(self.rows)
        self.ncols = len(self.headers)


    def print_info(self, numberOfRows=None):

        if numberOfRows != None:
            rowsValues = self.get_rowsValues(rowIndexValue_list=[self.rows[i][self.index] for i in range(numberOfRows)])

        else:
            rowsValues = self.get_rowsValues(rowIndexValue_list=[self.rows[i][self.index] for i in range(self.nrows)])

        tableHeaders = self.headers       
        table = tabulate(tabular_data=rowsValues, headers=tableHeaders, tablefmt='orgtbl')

        print("\n")
        print(" ====================start Dataframe inof====================\n")
        print("file path: %s\n" %(self.file_path)) 
        print("headers: %s\n" %(self.headers))
        print("index column: %s\n" %(self.index))
        print("number of cols: %d\n" %(self.ncols))
        print("number of rows: %d\n" %(self.nrows))
        print("five first rows: \n") 
        print(table,"\n")
        print(" =====================end Dataframe inof=====================")
        print("\n")
    
    
    
    ################################################################
    ## CONVERT METHODS
    ################################################################
    def convert_columns_to_int(self, columnName_list):
        for column in columnName_list:
            for i in range(self.nrows):
                if self.rows[i][column] == "NONE":
                    self.rows[i][column] = int(0)
                else:
                    self.rows[i][column] = int(float(self.rows[i][column]))


    def convert_columns_to_float(self, columnName_list):
        for column in columnName_list:
            for i in range(self.nrows):
                if self.rows[i][column] == "NONE":
                    self.rows[i][column] = int(0)
                else:
                    self.rows[i][column] = float(self.rows[i][column])


    def convert_columns_to_dateTime(self, columnName_list, dateTime_format):
        for column in columnName_list:
            for i in range(self.nrows):
                self.rows[i][column] = datetime.datetime.strptime(self.rows[i][column], dateTime_format)


    
    ################################################################
    ## GET METHODS
    ################################################################
    def set_index(self, index):
        self.index = index

   
    def get_rows(self, rowIndexValue_list=None):
        rows = []
        # get all rows
        if rowIndexValue_list == None:    
            rows = self.rows
            return rows
        # get rows with rowIndexValue in rowIndexValue_list
        else:
            for row in self.rows:
                if row[self.index] in rowIndexValue_list:
                    rows.append(row)                
        return rows


    def get_rowsValues(self, rowIndexValue_list=None):
        rowsValues = []
        # get all rowsValues
        if rowIndexValue_list == None:    
            for row in self.rows:
                rowValues = list(row.values())
                rowsValues.append(rowValues)
        # get rowsValues with rowIndexValue in rowIndexValue_list
        else:
            for row in self.rows:
                if row[self.index] in rowIndexValue_list:
                    rowValues = list(row.values())
                    rowsValues.append(rowValues)
        return rowsValues


    def get_columnValues(self, columnHeader):
        columnValues = []
        for row in self.rows:
            columnValues.append(row[columnHeader])
        return columnValues


    def get_columnsValues(self, columnHeader_list=None):
        columnsValues = []
        # get all columns values
        if columnHeader_list == None:    
            for column in self.headers:
                columnValues = self.get_columnValues(column)
                columnsValues.append(columnValues)
        # get columns values with header in columnHeader_list
        else:
            for column in columnHeader_list:
                columnValues = self.get_columnValues(column)
                columnsValues.append(columnValues)
        return columnsValues

    def set_columnValues(self, columnName, columnValues):
        for i in range(self.nrows):
            self.rows[i][columnName] = columnValues[i]

    
    ################################################################
    ## ADD, DELETE, CHANGE METHODS
    ################################################################
    def add_header(self, header, headerIndex=None):
        # add header to end of self.headers
        if headerIndex == None:
            self.headers.append(header)
        # insert header into index of self.headers    
        else:
            self.headers.insert(headerIndex, header)
        self.update_info()


    def add_row(self, row, rowIndex=None):
        # row is dictionary {header_name:culomn_value, header_name:culomn_value, ...}
        # add row to end of self.rows
        if rowIndex == None:  
            self.rows.append(row) 
        # insert row into index of self.rows 
        else:
            self.rows.insert(rowIndex, row)
        self.update_info()


    def add_column(self, columnName, columnValues, columnIndex=None):
        # add header to end of self.headers
        if columnIndex == None:
            self.add_header(columnName)
        # insert header into columnIndex of self.headers
        else:
            self.add_header(columnName, columnIndex)
        for i in range(self.nrows):
            self.rows[i][columnName] = culomnValues[i]
        self.update_info()


    def delete_header(self, header):
        self.headers.remove(header)

   
    def delete_columns(self, columnName_list):
        # delete all headers columnName_list in from self.headers
        for column in columnName_list:
            self.delete_header(column)
        # delete all columns from self.rows
        for i in range(self.nrows):
            self.rows[i] = func.delete_elements_from_dictionary(self.rows[i], columnName_list)
        self.update_info()
              

    def change_headers(self, oldHeader, newHeadr):
        self.headers = func.pop_and_insert_element_to_list(self.headers,
                                                            oldHeader,
                                                            newHeadr)
        if oldHeader == self.index:
            self.set_index(newHeadr)
        for i in range(self.nrows):
            self.rows[i] = func.change_key_of_dictionary(self.rows[i], oldHeader, newHeadr)



    ################################################################
    ## OTHER USEFUL METHODS
    ################################################################
    def find_all_rows_with_same_columnValue(self, columnName, goalValue):
        result = []
        for row in self.rows:
            if row[columnName] == goalValue :
                result.append(row)
        return result

    
    def collect_columnsValues_of_rows(self, indexColumn, rows_list, average_ColumnName_list):
        result_row = {}
        for column in self.headers:
            tmp_value = 0
            for row in rows_list:
                if column == indexColumn:
                    result_row[column] = row[column]
                else:
                    tmp_value += row[column]
                    result_row[column] = tmp_value
        if average_ColumnName_list != None:
            for column in average_ColumnName_list:
                result_row[column] = result_row[column] / len(rows_list)
        return result_row


    def collect_rows(self, indexColumn, average_ColumnName_list=None):
        new_rows = []
        for row in self.rows:
            if new_rows:
                
                new_row_flag = True
                for new_row in new_rows:
                    if new_row[indexColumn] == row[indexColumn]: 
                        new_row_flag = False 
                        break
                
                if new_row_flag == True:
                    tmp_rows_list = self.find_all_rows_with_same_columnValue(indexColumn, row[indexColumn])
                    tmp_row = self.collect_columnsValues_of_rows(indexColumn, tmp_rows_list, average_ColumnName_list)
                    new_rows.append(tmp_row)
                    
            else:
                tmp_rows_list = self.find_all_rows_with_same_columnValue(indexColumn, row[indexColumn])
                tmp_row = self.collect_columnsValues_of_rows(indexColumn, tmp_rows_list, average_ColumnName_list)
                new_rows.append(tmp_row)
        self.rows = new_rows
        self.update_info()      
        

    def add_total_values_of_columns(self, indexColumn, totalRowName, average_ColumnName_list=None):
        total_row = {}
        total_row[indexColumn] = totalRowName
        for column in self.headers:
            if column != indexColumn:
                column_total_value = 0
                for row in self.rows:
                    column_total_value += row[column]
                total_row[column] = column_total_value
        if average_ColumnName_list != None:
            for column in average_ColumnName_list:
                total_row[column] = total_row[column] / len(self.rows) 
        self.rows.append(total_row)
        self.update_info()
    

    def rowValues_to_rowDict(self, rowValues):
        rowDict = {}
        for i in range(len(rowValues)):
            rowDict[self.headers[i]] = rowValues[i]
        return rowDict


    def sort_rows(self, indexColumn_name):
        new_rows = []
        tmp_rowsValues = self.get_rowsValues()
        index = func.get_index_in_list(self.headers, indexColumn_name)
        sorted_rowsValues = sorted(tmp_rowsValues,key=lambda x: x[index], reverse=True)
        
        for row in sorted_rowsValues:
            new_rows.append(self.rowValues_to_rowDict(row))
        
        self.rows = new_rows
        self.update_info()
