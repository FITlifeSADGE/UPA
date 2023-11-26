from bs4 import BeautifulSoup
import sys
import asyncio
import aiohttp

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
                        
                        url = url.strip()
                        
                        publisher_info = publisher_info.text.strip() if publisher_info else None
                        publisher_info = publisher_info.replace("Publisher:", "")
                        
                        ISBN_info = ISBN_info.text.strip() if ISBN_info else None
                        ISBN_info = ISBN_info.replace("ISBN:", "")
                        
                        format_info = format_info.text.strip() if format_info else None
                        format_info = format_info.replace("Format:", "")
                        
                        book_name = book_name.text.strip() if book_name else None
                        price = price.text.strip() if price else None
                        
                        print(f"{url}\t", end='')
                        print(f"{book_name}\t", end='')
                        print(f"{price}\t", end='')
                        print(f"{publisher_info}\t", end='')
                        print(f"{ISBN_info}\t", end='')
                        print(f"{format_info}")  
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
                        
                            # format_info = product_info_div.find('li', class_='format')       
                            # publisher_info = product_info_div.find('li', class_='publisher')
                            # ISBN_info = product_info_div.find('li', class_='EAN')
                            
                            # url = url.strip()
                            
                            # publisher_info = publisher_info.text.strip() if publisher_info else None
                            # publisher_info = publisher_info.replace("Publisher:", "")
                            
                            # ISBN_info = ISBN_info.text.strip() if ISBN_info else None
                            # ISBN_info = ISBN_info.replace("ISBN:", "")
                            
                            # format_info = format_info.text.strip() if format_info else None
                            # format_info = format_info.replace("Format:", "")
                            
                            # book_name = book_name.text.strip() if book_name else None
                            # price = price.text.strip() if price else None
                            
                            # print(f"{url}\t", end='')
                            # print(f"{price}\t", end='')
                            # print(f"{book_name}\t", end='')
                            # print(f"{publisher_info}\t", end='')
                            # print(f"{ISBN_info}\t", end='')
                            # print(f"{format_info}")  
#     except Exception as e:
#         print(f"Error processing URL {url}: {e}")
#         return None, None, None, None, None

# 30 at a time
# async def run(selected_product_urls):
#         semaphore = asyncio.Semaphore(30)
#         tasks = list()
#         for domain in selected_product_urls:
#             #await urlQ.put(i)
#             task = asyncio.create_task(extract_data(domain, semaphore))
#             tasks.append(task) 
#         await asyncio.gather(*tasks)
        
async def run(selected_product_urls, max_lines = None):
        tasks = list()
        for i, domain in enumerate(selected_product_urls):
            if max_lines is not None and i >= max_lines:
                break
            task = asyncio.create_task(extract_data(domain))
            tasks.append(task) 
        await asyncio.gather(*tasks)

  
def main(lines, max_lines = None):
        with open (lines, "r") as myfile:
            urls = myfile.readlines()
            asyncio.run(run(urls, max_lines))

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], int(sys.argv[2]))
    else:
        main(sys.argv[1])
