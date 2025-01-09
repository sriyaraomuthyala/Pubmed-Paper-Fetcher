***PubMed Research Paper Fetcher***
This project fetches research papers from PubMed based on a user-defined query. It retrieves the paper details, including the title, publication date, and author information (affiliations and emails). The results are saved as a CSV file.

**Features :**
Fetch PubMed research papers using a custom search query.
Extract and store the following details for each paper:
PubMed ID
Title
Publication Date
Non-academic Authors
Affiliation(s)
Author Email
Save results as a CSV file in a user-defined or automatically created folder named after the query.

**Dependencies :**
This project uses the following libraries:
*requests:* For making API calls to PubMed.
*pandas:* For saving data to a CSV file.
*Bio.Entrez from biopython:* For fetching detailed author information.
*concurrent.futures:* For parallel data fetching.
*argparse:* For handling command-line arguments.
*xml.etree.ElementTree:* For parsing XML data.

**Install dependencies:**
pip install -r requirements.txt
Usage
**Run the script from the command line:**
python command_line_interface.py "<search_query>" [-f <output_directory>] [-d]
**Arguments**
<search_query>: The PubMed search query (e.g., "brain tumor").
-f, --file <output_directory>: (Optional) The directory to save the CSV file. If not provided, the CSV will be saved in a folder named after the query.
-d, --debug: (Optional) Prints additional debug information.
Examples
**Save results for the query "diabetes management" in the default folder:**
*python command_line_interface.py "diabetes management"*
Saves diabetes_management.csv in the current working directory.

**Save results for "lung cancer research" in a custom folder:**
* python command_line_interface.py "lung cancer research" -f "C:\Users\YourName\Documents\Research" *
Saves the file as lung_cancer_research.csv in the specified directory.

**Customization:**
Email: Set Entrez.email in command_line_interface.py to your email address for API access:
Entrez.email = "your_email@example.com"
**Error Handling:**
No Results: If no papers are found, the script will complete without saving any files.
Invalid Directory: If the provided path in -f is not valid, the script creates a folder with the query name in the current working directory.
