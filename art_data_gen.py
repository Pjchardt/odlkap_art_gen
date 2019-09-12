import csv
import random
import pandas as pd

class ArtDataGen(object):
    def __init__(self, data_path):
        self.load_art_data(data_path)

    def load_art_data(self, filename):
        self.my_csv = pd.read_csv(filename, usecols=['Title', 'Artist', 'Date'])

    def generate_art_data(self):
        generated_name = "\""

        title_template = random.choice(self.my_csv.Title).split(" ")
        for word in title_template:
            title_name = str(random.choice(self.my_csv.Title)).split(" ")
            generated_name += str(random.choice(title_name)) + " "
        generated_name = (generated_name[:-1] + "\"").replace("(", "").replace(")", "")

        name_template = random.choice(self.my_csv.Artist).split(" ")
        for name in name_template:
            artist_name = str(random.choice(self.my_csv.Artist)).split(" ")
            name = str(random.choice(artist_name))
            while name is None:
                name = str(random.choice(artist_name))
            generated_name += " " + name

        date = str(random.choice(self.my_csv.Date))
        while date is None:
            date = str(random.choice(self.my_csv.Date))
        generated_name += ", " + date

        return generated_name
