# Data Sweeper

Data Sweeper is a Streamlit-based web application that allows users to upload, clean, visualize, and convert data files (CSV, Excel) with an intuitive interface.

## Features

- **File Upload**: Support for CSV and Excel files (both .xlsx and .xls)
- **Data Cleaning**: Remove duplicates, handle missing values with various strategies
- **Column Selection**: Interactive selection of columns to keep
- **Data Visualization**: Multiple chart types (histograms, box plots, scatter plots, line charts)
- **File Conversion**: Export cleaned data in CSV or Excel format

## Project Structure

```
data_sweeper/
│
├── app.py                  # Main Streamlit app that runs everything
├── requirements.txt        # Dependencies (pandas, streamlit, openpyxl, etc.)
├── README.md               # Project overview, instructions
│
├── modules/                # Core app functionality broken into modules
│   ├── __init__.py
│   ├── uploader.py         # Handles file uploads
│   ├── cleaner.py          # Handles data cleaning
│   ├── selector.py         # Handles column selection
│   ├── visualizer.py       # Handles visualizations
│   └── converter.py        # Handles file conversion and download
│
├── utils/                  # Helper functions and utilities
│   ├── __init__.py
│   └── file_utils.py       # File handling utilities (extensions, MIME types, etc.)
│
└── assets/                 # Optional folder for images, icons, or styling files
```

## Setup and Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Upload Files**: Use the file uploader to select one or more CSV or Excel files
2. **Preview Data**: View a sample of your uploaded data
3. **Clean Data**: Remove duplicates and handle missing values
4. **Select Columns**: Choose which columns to keep in the final dataset
5. **Visualize Data**: Create charts to explore your data
6. **Convert & Download**: Export your cleaned data in your preferred format

## Modules

### uploader.py
Handles file uploads with validation for supported file types (CSV, Excel).

### cleaner.py
Provides options to remove duplicates and handle missing values in multiple ways:
- Drop rows with missing values
- Fill with zeros
- Forward fill
- Backward fill

### selector.py
Allows users to select which columns to keep from their datasets.

### visualizer.py
Creates various types of visualizations using Plotly:
- Histograms
- Box plots
- Scatter plots
- Line charts

### converter.py
Converts cleaned dataframes to CSV or Excel format for download.

### file_utils.py
Contains utility functions for file validation, extension detection, and filename sanitization.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.