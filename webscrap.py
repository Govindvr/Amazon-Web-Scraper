from bs4 import BeautifulSoup
import requests
import csv
import re



headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}

producct_details = []
def get_page(url):
    html_text = requests.get(url,headers=headers).text
    soup = BeautifulSoup(html_text, "lxml")
    return soup

def get_product_details(url):
    manufacturer = ""
    soup = get_page(url)
    description = soup.find("span", id="productTitle").text.strip()
    try:
        product_description = soup.find("div", id="productDescription")
        productDescription = product_description.find("p").text.strip()
    except:
        productDescription = ""

    try:
        deails = soup.find("div", id="detailBullets_feature_div")
        details = deails.find_all("li")
        for detail in details:
            if re.search("^Manufacturer",detail.text.strip()):
                manufacturer = detail.find("span", class_="").text.strip()
                break
    except:
        manufacturer = ""
    try:
        deails = soup.find("div", id="detailBullets_feature_div")
        details = deails.find_all("li")
        for detail in details:
            if re.search("^ASIN",detail.text.strip()):
                asin = detail.find("span", class_="").text.strip()
                break
    except:
        asin = ""
   
    return (description,asin,productDescription,manufacturer)

def get_record(item):
    try:
        item_name = item.find("span", class_="a-size-medium a-color-base a-text-normal").text
    except AttributeError:
        item_name = ""

    try:
        item_price = item.find("span", class_="a-price-whole").text
    except AttributeError:
        item_price = ""

    try:
        rating = item.find("span", class_="a-icon-alt").text
    except AttributeError:
        rating = ""
    
    try:
        review_count = item.find("span", class_="a-size-base s-underline-text").text
    except AttributeError:
        review_count = ""

    url = item.find("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal").get("href")
    url = "https://www.amazon.in" + url

   
    result = (url, item_name, item_price, rating, review_count)
    return result




if __name__ == "__main__":

    url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    records = []
    pno = 1
    
    for _ in range(20):
        print("Scraping page: " + str(pno))
        soup = get_page(url)
        items = soup.find_all("div", {"data-component-type": "s-search-result"})

        for item in items:
            record = get_record(item)
            if record:
                records.append(record)
        if pno != 20:
            next_link = soup.find("a", class_ = "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator").get("href")
            url = "https://www.amazon.in" + next_link
        pno += 1

    print("Scraping completed. Total records: " + str(len(records)))

    

    with open("amazonsearchresult.csv", "w", newline="", encoding="utf-8") as f:    
        writer = csv.writer(f)
        writer.writerow(["URL", "Name", "Price", "Rating", "Review Count"])
        writer.writerows(records)
    print("CSV file for search created successfully.")
    
    with open("amazonproductdetails.csv", "w", newline="", encoding="utf-8") as f:    
        writer = csv.writer(f)
        writer.writerow(["Description", "ASIN", "Product Description", "manufacturer"])
        i=0
        for record in records:
            product_details = get_product_details(record[0])
            writer.writerow(product_details)
            print("Product details for " + str(i) + " scraped successfully.")
            i+=1
    
    print("CSV file created successfully.")

   