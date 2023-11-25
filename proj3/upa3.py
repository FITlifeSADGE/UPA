import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp

def scrape_product_urls(url, max_items=100):
    all_product_urls = []

    # Function to extract product URLs from a page
    def extract_product_urls(soup):
        product_urls = []

        # Find all div elements with class="card-body"
        card_body_divs = soup.find_all('div', class_='search-item__name')

        for card_body_div in card_body_divs:
            # Check if both h3 and a elements are present in the card-body div
            card_title_h3 = card_body_div.find('h3', class_='search-item__title')
            anchor_tag_a = card_title_h3.find('a', href=True)

            if card_title_h3 and anchor_tag_a:
                product_urls.append('https://www.hive.co.uk' + anchor_tag_a['href'])

        return product_urls

    # Iterate through pages
    page_number = 1
    while len(all_product_urls) < max_items:
        page_url = f'{url}&pg={page_number}' if page_number > 1 else url
        response = requests.get(page_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_urls = extract_product_urls(soup)

            # Break the loop if no more product URLs are found
            if not product_urls:
                break

            # Add product URLs to the list, ensuring not to exceed max_items
            remaining_items = max_items - len(all_product_urls)
            all_product_urls.extend(product_urls[:remaining_items])
            page_number += 1
        else:
            print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
            break

    # Shuffle the collected product URLs

    return all_product_urls[:max_items]

async def extract_data(url):
    try:
        # Fetch the HTML content of the URL
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=10) as r:
                html = await r.text()
                if r.ok: #if return code is under 400 go on
                    if html != "":
                        soup = BeautifulSoup(html, 'html.parser')
        
                        price = soup.find('p', class_="sitePrice")
                        book_name = soup.find('h1', itemprop="name")
                        
                        if book_name:
                                for span in book_name.find_all('span'):
                                    span.decompose()
                                    
                        product_info_div = soup.find('div', class_='productInfo')
                        
                        format_info = product_info_div.find('li', class_='format')       
                        publisher_info = product_info_div.find('li', class_='publisher')
                        ISBN_info = product_info_div.find('li', class_='EAN')
                        
                        publisher_info = publisher_info.text.strip() if publisher_info else None
                        ISBN_info = ISBN_info.text.strip() if ISBN_info else None
                        format_info = format_info.text.strip() if format_info else None
                        book_name = book_name.text.strip() if book_name else None
                        price = price.text.strip() if price else None
                        
                        print(f"URL: {url}")
                        print(f"Price paid: {price}")
                        print(f"Book name: {book_name}")
                        print(f"{publisher_info}")
                        print(f"{ISBN_info}")
                        print(f"{format_info}")
                        print("----")     
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None, None, None, None, None

# 30 requests at a time
# async def extract_data(url, semaphore):
#     try:
#         async with semaphore:
#             # Fetch the HTML content of the URL
#             async with aiohttp.ClientSession() as s:
#                 async with s.get(url, timeout=10) as r:
#                     html = await r.text()
#                     if r.ok: #if return code is under 400 go on
#                         if html != "":
#                             soup = BeautifulSoup(html, 'html.parser')
            
#                             price = soup.find('p', class_="sitePrice")
#                             book_name = soup.find('h1', itemprop="name")
                            
#                             if book_name:
#                                     for span in book_name.find_all('span'):
#                                         span.decompose()
                                        
#                             product_info_div = soup.find('div', class_='productInfo')
                            
#                             format_info = product_info_div.find('li', class_='format')       
#                             publisher_info = product_info_div.find('li', class_='publisher')
#                             ISBN_info = product_info_div.find('li', class_='EAN')
                            
#                             publisher_info = publisher_info.text.strip() if publisher_info else None
#                             ISBN_info = ISBN_info.text.strip() if ISBN_info else None
#                             format_info = format_info.text.strip() if format_info else None
#                             book_name = book_name.text.strip() if book_name else None
#                             price = price.text.strip() if price else None
                            
#                             print(f"URL: {url}")
#                             print(f"Price paid: {price}")
#                             print(f"Book name: {book_name}")
#                             print(f"{publisher_info}")
#                             print(f"{ISBN_info}")
#                             print(f"{format_info}")
#                             print("----")     
#     except Exception as e:
#         print(f"Error processing URL {url}: {e}")
#         return None, None, None, None, None


# Specify the URL of the first page
url = 'https://www.hive.co.uk/Search/eBooks/Fiction?fq=01124-121934'

selected_product_urls = scrape_product_urls(url, max_items=100)


# 30 at a time
# async def run(selected_product_urls):
#         semaphore = asyncio.Semaphore(30)
#         tasks = list()
#         for domain in selected_product_urls:
#             #await urlQ.put(i)
#             task = asyncio.create_task(extract_data(domain, semaphore))
#             tasks.append(task) 
#         await asyncio.gather(*tasks)
        
async def run(selected_product_urls):
        tasks = list()
        for domain in selected_product_urls:
            task = asyncio.create_task(extract_data(domain))
            tasks.append(task) 
        await asyncio.gather(*tasks)

asyncio.run(run(selected_product_urls))


