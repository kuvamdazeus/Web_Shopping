from bs4 import BeautifulSoup
import requests, os, sys, json
os.system("clear")

def get_and_search_page(query):
    # convert query from normal string to a searchable string in order to make successful get requests
    search = query.strip().replace(" ", "+")
    print("Searching...")
    URL = "https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY".format(search)
    response = requests.get(URL)
    print(response.status_code)
    if response.status_code == 503:
        print("Its not working...")
        sys.exit(1)
    elif response.status_code == 408:
        print("Please make sure you have a fast internet")
        sys.exit(1)
    soup = BeautifulSoup(response.content, "html.parser")
    header_elems = soup.find_all("div", class_ = "_3wU53n")
    span_elems = soup.find_all("div", class_ = "_1vC4OE _2rQ-NK")
    ratings = soup.find_all("div", class_ = "hGSR34")
    item_list = []
    total_prices = 0
    for header_elem, span_elem, rating in zip(header_elems, span_elems, ratings):
        dict = {}
        dict["Name"] = header_elem.text
        dict["Price"] = span_elem.text[1:]
        dict["Ratings"] = rating.text
        total_prices += int(span_elem.text[1:].replace(",", "_"))
        item_list.append(dict)
    if len(item_list) == 0:
        page_content = requests.get(URL).content
        new_soup = BeautifulSoup(page_content, "html.parser")
        items = new_soup.find_all("a", class_ = "_2cLu-l")
        prices = new_soup.find_all("div", class_ = "_1vC4OE")
        ratings = new_soup.find_all("div", class_ = "hGSR34")
        for item, price, rating in zip(items, prices, ratings):
            dict = {}
            dict["Name"] = item.get("title")
            dict["Price"] = price.text[1:]
            dict["Ratings"] = rating.text
            total_prices += int(price.text[1:].replace(",", "_"))
            item_list.append(dict)
    # final steps
    json.dump(item_list, open("items.json", "w"), indent = 4)
    print("Done, check the json file")
    print("-"*45 + "ITEMS.JSON" + "-"*45)
    if os.path.exists("items.json"):
        os.system("cat items.json")
        os.system("echo")
        print("\nAverage Price: {}\n".format(total_prices/len(item_list)))
    print("-"*45 + "ITEMS.JSON" + "-"*45)

if __name__ == "__main__":
    while True:
        try:
            query = input("\nEnter item to search on flipkart: ").strip()
            get_and_search_page(query)
        except KeyboardInterrupt:
            os.system("echo")
            sys.exit(0)