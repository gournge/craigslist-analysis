from googlesearch import search
import requests
from bs4 import BeautifulSoup
import time

def find_data(url, tofind = 'links', containing = None) -> list[str]:

    extracted = []

    # Send an HTTP GET request to the URL
    response = requests.get(url, headers={'User-agent': 'your bot 0.1'})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        links = None
        if tofind == 'links':

            # Use BeautifulSoup to extract the information you need from the HTML
            # For example, let's extract all the links (anchor tags) on the page:
            links = soup.find_all('a')

            # Print the extracted links
            for link in links:
                ending = link.get('href')
                extracted.append(ending)

        elif tofind == 'h3 and spans':
            h3s = soup.find_all('h3')
            spans = soup.find_all('span')

            for h3 in h3s:
                h3_text = str(h3)
                first_sign = h3_text.find('>') + 1
                second_sign = h3_text.find('<', 1)
                extracted.append(h3_text[first_sign:second_sign])

            for span in spans:
                span_text = str(span)
                first_sign = span_text.find('>') + 1
                second_sign = span_text.find('<', 1)
                extracted.append(span_text[first_sign:second_sign])

        elif tofind == 'span':
            spans = soup.find_all('span')

            if containing is None:
                for span in spans:

                    extracted.append(str(span))
            else:
                for span in spans:

                    if all([phrase in str(span) for phrase in containing]):
                        extracted.append(str(span))
                        break
        else:
            raise NotImplementedError()
        
    else:
        print(' - - - ')
        print("\tFailed to retrieve the webpage. Status code:", response.status_code, '\t\nWebpage:', url)

    return extracted

def movie_offer_links(howmany):

    links = []

    for i in range(6, 25):

        # time.sleep(2)        
        # print('lol')

        url = f'https://www.olx.pl/muzyka-edukacja/filmy/?page={i}'
        extracted = find_data(url)

        for ending in extracted:
            if str(ending).startswith('/d/oferta'):
                links.append('https://www.olx.pl' + ending)

    return links

def get_movie_info(movielink):

    price, views = None, None
    extracted = find_data(movielink, tofind='h3 and spans')

    for ext in extracted:

        if price is not None and views is not None: break

        if price is None and 'zł' in ext:
            p = str(ext).replace(',', '.')
            price = float(p[:-3].replace(' ', ''))
        
        if views is None and 'Wyświetlenia:' in ext:
            views = int(ext[13:]) 

    return price, views

def get_movie_rating(name: str):

    try:
        search_results = search('filmweb ' + name, num_results=5, sleep_interval=1)
    except:
        print('http error occured. (probably too many requests)')
        return None

    for r in search_results:
        if 'filmweb' in r and ('film' in r[23:] or 'serial' in r):
            extracted = find_data(r, tofind='span')
            for ext in extracted:
                if 'filmRating__rateValue' in ext:
                    comma = ext.find(',')
                    start = comma - 1
                    end = comma + 2
                    value = ext[start:end].replace(',', '.')
                    return float(value)


    return None

def movie_data(howmany):

    data = []

    links = movie_offer_links(howmany)

    for link in links:


        name = str(link)[28:-20].replace('-', ' ')

        if 'viaplay' in name: continue
        if 'zestaw' in name: continue

        # print("Looking for the movie", name)

        rating = get_movie_rating(name)
        if rating is None: continue

        price, offerviews = get_movie_info(link)

        print(name, price, rating)
        data.append((name, price, rating))

    return data

if __name__ == '__main__':

    import csv

    data = movie_data(25)
    
    csv_file_path = 'movie_data.csv'

    with open(csv_file_path, mode="w", newline="") as file:
        # Create a CSV writer object
        csv_writer = csv.writer(file)

        csv_writer.writerow(["Name", "Price", "Rating"])

        # Write the data to the CSV file
        for row in data:
            csv_writer.writerow(row)