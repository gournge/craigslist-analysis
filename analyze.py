import csv

filmweb_database_path = r''
movie_data_path = 'movie_data_cleaned.csv'

allratings = []

# Open the CSV file
with open(filmweb_database_path, 'r', encoding="utf8") as csvfile:
    # Create a CSV reader object
    csvreader = csv.reader(csvfile)
    
    # Iterate through each row in the CSV file
    for row in csvreader:
        # Check if there are at least two columns in the row
        if len(row) >= 2:
            try:
                # Convert the second column to a float and add it to the total
                value = float(row[1])
                allratings.append(value)
            except ValueError:
                # Handle cases where the second column is not a valid number
                pass

prices, ratings = [], []
with open(movie_data_path, 'r') as f:
    csvreader = csv.reader(f)

    for i, row in enumerate(csvreader):
        if i == 0: continue
        price = float(row[1])
        rating = float(row[2])
        prices.append(price)
        ratings.append(rating)

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

import numpy as np
avg = np.mean(allratings)
ax1.hist(allratings, bins = 20, color='skyblue', alpha=0.5, label='Rozkład ocen na Filmweb')
ax1.axvline(avg, color='skyblue', linestyle='--', label=f'Średnia ocena na Filmweb = {avg:.2f}')
ax1.set_ylabel('Ilość ocen na Filmweb')
ax2.set_ylabel('Cena oferty')
ax1.set_xlabel('Ocena filmu')

ax2.axvline(np.mean(ratings), color='red', linestyle='--', label='Średnie oceny filmów z OLX')

ax2.scatter(ratings, prices, color='red', label = 'Oferty wystawione na OLX')
ax1.legend(loc='upper left')
ax2.legend(loc='lower left')

plt.show()