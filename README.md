# Amazon Website scraper

python program to scrape a amazon page for products and save them on a csv file

## Installation
```bash
pip install -r requirements.txt
```

## Usage
Scrape atleast 20 pages of product listing pages
Items to scrape
    • Product URL
    • Product Name
    • Product Price
    • Rating
    • Number of reviews

These items will be saved on a amazonsearchresult.csv file

With the Product URL received in the above case, hit each URL, and add below items:
    • Description
    • ASIN
    • Product Description
    • Manufacturer

These items will be saved on a amazonproductdetails.csv file