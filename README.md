# Storytelling COVID-19

## Project Overview

The **Storytelling COVID-19** project is designed to analyze and visualize COVID-19 data through the use of custom DataFrames, similar to those provided by the Pandas library. This project emphasizes the importance of data manipulation and visualization techniques to draw meaningful insights from complex datasets. The primary objective is to preprocess, transform, and visualize COVID-19 data at the country and continent levels, showcasing the impact and spread of the virus globally.

## Features

1. **Data Preprocessing**:
   - Cleaning and transforming raw COVID-19 data.
   - Handling missing values, data type conversions, and column manipulations.
   - Aggregating data at various levels (country, continent) for comprehensive analysis.

2. **DataFrame Implementation**:
   - Custom DataFrame class mimicking Pandas functionality.
   - Methods for reading, writing, copying, updating, and printing data.
   - Conversion functions for data types, including date-time, integer, and float conversions.
   - Aggregation and sorting functionalities for enhanced data analysis.

3. **Data Visualization**:
   - Creating grouped bar charts to visualize COVID-19 impact by country and continent.
   - Highlighting top 10 countries based on confirmed cases.
   - Visualizing global COVID-19 statistics, sorted by key metrics such as confirmed cases and mortality rate.

4. **Correlation Analysis**:
   - Calculating Pearson correlation coefficients to explore relationships between different COVID-19 metrics.

## Data Sources

The data used in this project is sourced from the [Johns Hopkins University COVID-19 repository](https://github.com/CSSEGISandData/COVID-19). The primary datasets include:
- `covid19_confirmed_global.csv`
- `covid19_deaths_global.csv`
- `cases_country.csv`

Additionally, processed data files are stored in the `Data/Produced Data` directory:
- `cases_Continent.csv`
- `cases_ISO2.csv`

## Project Structure

- **main.py**: The main script that orchestrates the data processing, transformation, and visualization tasks. It reads data, applies preprocessing steps, converts country names, and generates plots.
  
- **data_frame.py**: Implements a custom DataFrame class with methods for data manipulation, including reading/writing CSV files, data conversion, row/column operations, and sorting.

- **functions.py**: Contains utility functions for list and dictionary operations, including element removal, insertion, and key-value manipulations.

- **plot.py**: Defines a Plot class for generating grouped bar charts using Matplotlib. This class handles the setup and display of plots for different COVID-19 metrics.

## How to Use

1. **Data Preparation**:
   - Ensure the data files (`covid19_confirmed_global.csv`, `covid19_deaths_global.csv`, `cases_country.csv`) are placed in the `Data` directory.
   - Processed data files will be generated and saved in the `Data/Produced Data` directory.

2. **Running the Project**:
   - Execute `main.py` to process the COVID-19 data and generate visualizations.
   - The script performs the following steps:
     - Reads and preprocesses the `cases_country.csv` file.
     - Converts country names to ISO2 and continent names.
     - Aggregates data by continent and generates global statistics.
     - Visualizes the top 10 countries by confirmed cases and global statistics by continent.
     - Calculates and displays Pearson correlation coefficients for the COVID-19 metrics.

3. **Visualization**:
   - The generated plots will be displayed using Matplotlib, highlighting key insights from the data, such as the distribution of COVID-19 cases and deaths across different regions.

## Conclusion

The **Storytelling COVID-19** project demonstrates the importance of data preprocessing, transformation, and visualization in understanding the global impact of the COVID-19 pandemic. By leveraging custom DataFrame operations and visual tools, this project provides a comprehensive analysis of the pandemic's progression across countries and continents. This project serves as a valuable resource for learning how to manage and analyze large datasets, drawing meaningful conclusions through storytelling with data.
