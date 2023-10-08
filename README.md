# olx-analysis
Originally developed for a high school competition.

Run `python .\scrape.py` to create a `.csv` file containing names of public offers of movies, their prices in PLN and their Filmweb rating.

To calculate the average Filmweb rating **`6.874429102496004`** (a value interesting in itself) the script `.\analyze.py` was ran, with the `database_path` variable to set to the directory in which I have downloaded and unzipped [the database of 20'000 polish movies](https://www.kaggle.com/datasets/michau96/descriptions-of-popular-movies-polish-language/).  

To visualize what people are selling you can run `python .\visualize.py` (after running webscraping for a while.)
