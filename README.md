PubMed Paper Fetcher README
Output
The script generates CSV files containing:

PubmedID: Unique identifier for each paper.
Title: Title of the research paper.
Publication Date: Date the paper was published.
Non-academic Authors: List of authors not affiliated with universities.
Affiliations: All affiliations associated with the authors.
Author Email: Email address of any author, if available.
Overview
The PubMed Paper Fetcher is a Python tool designed to simplify the retrieval of research papers and author information from PubMed. Leveraging the Entrez API and concurrent programming, this script helps users search for papers, extract metadata, and store the results in organized CSV files for further analysis.

Features
Search PubMed: Search for research papers based on a user-defined query.
Retrieve Metadata: Fetch detailed metadata, including titles, publication dates, and authorship information.
Author Information: Extract author affiliations, emails (when available), and identify non-academic authors.
Customizable Output: Save results to dynamically named CSV files using the query name.
Concurrent Fetching: Use threading for efficient data retrieval.
Debugging Support: Optional debugging mode for enhanced logging.
Requirements
Python 3.7+
Libraries:
argparse
requests
pandas
Bio (from biopython)
xml.etree.ElementTree
concurrent.futures
Install dependencies using:

bash
Copy code
pip install requests pandas biopython
Usage
Run the script from the command line:

bash
Copy code
python fetch.py <query> [options]
Arguments
<query>: The PubMed search query (e.g., "machine learning in healthcare").
Options
-f, --file: Specify an output folder for CSV results. If omitted, results are saved to a folder named after the query.
-d, --debug: Enable debug mode for detailed logs.
Example
bash
Copy code
python fetch.py "deep learning in medicine" -f ./results -d
