import argparse
import requests
import pandas as pd
from typing import List, Dict
from Bio import Entrez
import xml.etree.ElementTree as ET
import os
from concurrent.futures import ThreadPoolExecutor

Entrez.email = "your_email@example.com"  # Replace with your email for API access

PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def fetch_pubmed_ids(query: str, max_results: int = 100) -> List[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    response.raise_for_status()
    return response.json().get("esearchresult", {}).get("idlist", [])

def fetch_paper_summaries(pubmed_ids: List[str]) -> List[Dict[str, str]]:
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "json"
    }
    response = requests.get(PUBMED_SUMMARY_URL, params=params)
    response.raise_for_status()
    data = response.json().get("result", {})
    return [
        {
            "PubmedID": paper_id,
            "Title": data.get(paper_id, {}).get("title", ""),
            "Publication Date": data.get(paper_id, {}).get("pubdate", "")
        }
        for paper_id in pubmed_ids
    ]
    
def save_to_csv_with_query_name(papers: List[Dict[str, str]], query: str, output_folder: str):
    """Save results to a CSV file using the query name."""
    sanitized_query = query.replace(" ", "_")
    filename = f"{sanitized_query}.csv"
    full_path = os.path.join(output_folder, filename)
    df = pd.DataFrame(papers)
    df.to_csv(full_path, index=False)
    return full_path


def fetch_paper_authors_batch(pubmed_ids: List[str]) -> Dict[str, List[Dict[str, str]]]:
    result = {}
    handle = Entrez.efetch(db="pubmed", id=",".join(pubmed_ids), rettype="xml", retmode="text")
    records = handle.read()
    root = ET.fromstring(records)

    for article in root.findall(".//PubmedArticle"):
        pmid = article.find(".//PMID").text
        authors_info = []
        for author in article.findall(".//AuthorList/Author"):
            last_name = author.find("LastName")
            fore_name = author.find("ForeName")
            if last_name is None or fore_name is None:
                continue
            author_name = f"{last_name.text} {fore_name.text}"
            affiliation = author.find("AffiliationInfo/Affiliation")
            email = None
            if affiliation is not None:
                affiliation = affiliation.text
                if "@" in affiliation:
                    email = affiliation.split()[-1]
            authors_info.append({
                "Author": author_name,
                "Affiliation": affiliation or "N/A",
                "Email": email
            })
        result[pmid] = authors_info
    return result

def save_to_csv(papers: List[Dict[str, str]], filename: str):
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers matching a query.")
    parser.add_argument("query", type=str, help="The search query.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV file name (optional).", default=None)
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    print(f"Fetching papers for query: {args.query}")

    pubmed_ids = fetch_pubmed_ids(args.query)
    
    with ThreadPoolExecutor() as executor:
        summaries_future = executor.submit(fetch_paper_summaries, pubmed_ids)
        authors_future = executor.submit(fetch_paper_authors_batch, pubmed_ids)
        summaries = summaries_future.result()
        authors_batch = authors_future.result()

    results = []
    for summary in summaries:
        pubmed_id = summary["PubmedID"]
        authors = authors_batch.get(pubmed_id, [])
        non_academic_authors = [a["Author"] for a in authors if "university" not in (a["Affiliation"] or "").lower()]
        affiliations = {a["Affiliation"] for a in authors}
        
        summary.update({
            "Non-academic Author(s)": ", ".join(non_academic_authors),
            "Affiliation(s)": ", ".join(affiliations),
            "Author Email": next((a["Email"] for a in authors if a["Email"]), "N/A")
        })
        results.append(summary)

    if args.file and os.path.isdir(args.file):
        output_folder = args.file
    else:
        sanitized_query = args.query.replace(" ", "_")
        output_folder = os.path.join(".", sanitized_query)
        os.makedirs(output_folder, exist_ok=True)
    
    # Save the CSV using the query name
    full_path = save_to_csv_with_query_name(results, args.query, output_folder)
    
    print(f"Results saved to: {full_path}")

if __name__ == "__main__":
    main()

