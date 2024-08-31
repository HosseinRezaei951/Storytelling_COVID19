import functions as func
import data_frame as df
import plot as pt
import numpy as np
import country_converter as coco
cc = coco.CountryConverter()



############################################################
## Global variables
############################################################      
dateTime_format = '%Y-%m-%d %H:%M:%S'
covid19_confirmed_global_file_path = "Data/covid19_confirmed_global.csv"
covid19_deaths_global_file_path = "Data/covid19_deaths_global.csv"
cases_country_file_path = "Data/cases_country.csv"
cases_country_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv"




############################################################
## Pre_processing
############################################################      
def Pre_processing(data_frame,
                   dateTime_format = None, 
                   delete_columnName_list = None,
                   dateTime_columnName_list = None,
                   int_columnName_list = None,
                   float_columnName_list = None,
                   collection_columnName = None):

    result_data_frame = data_frame.copy_dataFrame()

    if delete_columnName_list != None:
        # delete some useless columns
        result_data_frame.delete_columns(delete_columnName_list)  

    if (dateTime_columnName_list != None) and (dateTime_format != None):
        # convert dateTime columns with string type to python dateTime type
        result_data_frame.convert_columns_to_dateTime(dateTime_columnName_list, dateTime_format)
        
    if int_columnName_list != None:
        # convert some columns with string type to int
        result_data_frame.convert_columns_to_int(int_columnName_list)

    if float_columnName_list != None:
        # convert some columns with string type to float
        result_data_frame.convert_columns_to_float(float_columnName_list)

    if collection_columnName != None:
        result_data_frame.collect_rows(collection_columnName)
        

    return result_data_frame


############################################################
## country_column_converter
############################################################   
def country_column_converter(data_frame, country_ColumnName, destinationType):
    result_data_frame = data_frame.copy_dataFrame()
    
    # get country columns ==> returns dictionary
    tmp_columnsValues = result_data_frame.get_columnsValues([country_ColumnName])
    country_ColumnValues = tmp_columnsValues[0]

    # convert country column to destinationType 
    new_country_ColumnValues = cc.convert(names = country_ColumnValues, to= destinationType)
    
    # change "not found" countries name to "Others"
    while "not found" in new_country_ColumnValues:
        new_country_ColumnValues = func.pop_and_insert_element_to_list(new_country_ColumnValues,
                                                                    "not found", "Others")

    # set new_country_column on result_data_frame
    result_data_frame.set_columnValues(country_ColumnName, new_country_ColumnValues)

    # change headers of result_data_frame
    result_data_frame.change_headers(country_ColumnName, destinationType)

    return result_data_frame



if __name__ == "__main__":

    ###############################################################
    ## MAKING AND READING FILES
    ###############################################################
    ### making cases_country_df DataFrame 
    cases_country_df = df.DataFrame()

    ### reading cases_country.csv file
    cases_country_df.read_csvFile(file_path = cases_country_file_path)
    
    ### reading cases_country.csv online
    # cases_country_df.read_csvOnline(cases_country_url)
    ###############################################################
    ## MAKING AND READING FILES
    ###############################################################
    


    ###############################################################
    ## Manipulation on cases_country_df
    ###############################################################
    ### initializing
    dateTime_columnName_list = ["Last_Update"]
    int_columnName_list = ["Confirmed", "Deaths", "Recovered", "Active"]
    float_columnName_list = ["Incident_Rate", "Mortality_Rate"]
    holdColumns = ["Country_Region", "Last_Update", "Confirmed", "Deaths",
                     "Recovered", "Active", "Incident_Rate", "Mortality_Rate"]
    delete_columnName_list = func.difference_two_list(cases_country_df.headers, holdColumns)

    ### pre processing
    cases_country_df = Pre_processing(data_frame= cases_country_df,
                                    dateTime_format= dateTime_format,    
                                    delete_columnName_list= delete_columnName_list,
                                    dateTime_columnName_list= dateTime_columnName_list,
                                    int_columnName_list= int_columnName_list, 
                                    float_columnName_list= float_columnName_list)
    
    
    #### printing info
    print("\n ===> this is cases_country_df: ")
    cases_country_df.print_info(numberOfRows=5) 

    ### writing file
    # cases_country_df.write_csvFile("Data/Produced Data/cases_country.csv")
    ###############################################################
    ## Manipulation cases_country_df
    ###############################################################
    

    ###############################################################
    ## Create cases_ISO2_df and manipulation on it
    ###############################################################
    ### converting countries names to ISO2
    cases_ISO2_df = country_column_converter(cases_country_df, "Country_Region", "ISO2")

    ### printing info
    print("\n ===> this is cases_ISO2_df: ")
    cases_ISO2_df.print_info(numberOfRows=5)


    ### writing file
    # cases_ISO2_df.write_csvFile("Data/Produced Data/cases_ISO2.csv")
    ################################################################
    ## Create cases_ISO2_df and manipulation on it
    ################################################################

    
    ################################################################
    ## Create cases_continent_df and manipulation on it
    ################################################################
    ### initializing
    holdColumns2 = ["Country_Region", "Confirmed", "Deaths",
                     "Recovered", "Active", "Incident_Rate", "Mortality_Rate"]
    delete_columnName_list2 = func.difference_two_list(cases_country_df.headers, holdColumns2)

    ### pre processing
    cases_continent_df = Pre_processing(data_frame= cases_country_df,
                                    delete_columnName_list= delete_columnName_list2)
                                                    

    ### converting countries names to continent name
    cases_continent_df = country_column_converter(cases_continent_df, "Country_Region", "Continent")

    
    ### collecting columns with same continent
    collection_index_column_name = "Continent"
    cases_continent_df.collect_rows(collection_index_column_name, float_columnName_list)
    
    ### adding total value of columns for total row (Total Global)
    cases_continent_df.add_total_values_of_columns("Continent", "Total Global", float_columnName_list)

    ### printing info
    print("\n ===> this is cases_continent_df: ")
    cases_continent_df.print_info()

    ### writing file
    # cases_continent_df.write_csvFile("Data/Produced Data/cases_Continent.csv")
    ################################################################
    ## Create cases_continent_df and manipulation on it
    ################################################################

    
    ################################################################
    ## Drawing plot of Global report
    ################################################################
    numberOfTops = cases_continent_df.nrows
    ignoredFirst = 1
    ignoredLast = len(cases_continent_df.headers)-2

    cases_continent_plot = pt.Plot()
    cases_continent_plot_labels = cases_continent_df.headers[ignoredFirst:ignoredLast]
    cases_continent_plot_values = np.array(cases_continent_df.get_rowsValues())[:numberOfTops,ignoredFirst:ignoredLast]
    cases_continent_plot_index_valuses = cases_continent_df.get_columnValues(cases_continent_df.index)[:numberOfTops]  
    
    cases_continent_plot.load_data(title="Global report «sorted by Confirmed»",
                    labels= cases_continent_plot_labels,
                    values= cases_continent_plot_values.tolist(),
                    index_values= cases_continent_plot_index_valuses)

    barsWidth = 1/(len(cases_continent_plot_index_valuses)*len(cases_continent_plot_labels)) * 1.5 
    cases_continent_plot.drow_groupedBarChart(barsWidth= barsWidth)
    ################################################################
    ## Drawing plot of Global report
    ################################################################


    ################################################################
    ## Drawing plot of Top 10 countries
    ################################################################
    ### sorting rows by "Confirmed"
    cases_country_df.sort_rows("Confirmed")

    numberOfTops = 10
    ignoredFirst = 2
    ignoredLast = len(cases_country_df.headers)-2

    cases_country_plot = pt.Plot()
    cases_country_plot_labels = cases_country_df.headers[ignoredFirst:ignoredLast]
    cases_country_plot_values = np.array(cases_country_df.get_rowsValues())[:numberOfTops,ignoredFirst:ignoredLast]
    cases_country_plot_index_valuses = cases_country_df.get_columnValues(cases_country_df.index)[:numberOfTops]
    
    cases_country_plot.load_data(title="Top 10 countries «sorted by Confirmed»",
                    labels= cases_country_plot_labels,
                    values= cases_country_plot_values.tolist(),
                    index_values= cases_country_plot_index_valuses)

    barsWidth = 1/(len(cases_country_plot_index_valuses)*len(cases_country_plot_labels)) * 3 
    cases_country_plot.drow_groupedBarChart(barsWidth= barsWidth)
    ################################################################
    ## Drawing plot of Top 10 countries
    ################################################################
    

    ###############################################################
    ## Calculate pearson correlation
    ###############################################################
    x = np.array(cases_country_df.get_rowsValues())[:,2:]
    y = np.array(cases_country_df.get_columnsValues())[2:,:]
    print(x)
    print(y)

    ### finished
    print("____finished____")

   