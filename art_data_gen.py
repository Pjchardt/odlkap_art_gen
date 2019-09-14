import csv
import re
import random
import pandas as pd
#using a profanity check to filter results cuz the first installation is a public projection on a government run art building. don't care about the local government being offended/upsaet, but I don't want to cost the Art Director their job :)
from profanity_check import predict, predict_prob

class ArtDataGen(object):
    def __init__(self, data_path):
        self.load_art_data(data_path)

    def load_art_data(self, filename):
        self.my_csv = pd.read_csv(filename, usecols=['Title', 'Artist', 'Date'])

    def generate_art_data(self):

        generated_name = ""
        title_template = random.choice(self.my_csv.Title).split(" ")
        while title_template is None:
            title_template = random.choice(self.my_csv.Title).split(" ")
        for word in title_template:
            title_name = str(random.choice(self.my_csv.Title)).split(" ")
            generated_name += str(random.choice(title_name)) + " "
        title_list = generated_name.split()
        while len(title_list) > 8:
            del title_list[len(title_list)-1]
        generated_name = ' '.join(title_list)
        generated_name =  generated_name.replace("(", "").replace(")", "")

        #clean up title
        generated_name = self.cleanup_title(generated_name)

        generated_name = "\"" + generated_name + "\""

        name_template = str(random.choice(self.my_csv.Artist)).split(" ")
        while name_template is None:
            name_template = str(random.choice(self.my_csv.Artist)).split(" ")
        for name in name_template:
            artist_name = str(random.choice(self.my_csv.Artist)).split(" ")
            name = str(random.choice(artist_name))
            #while name is None or name == "nan": possible infinite loop if artist name is nan alone
            #    name = str(random.choice(artist_name))
            generated_name += " " + name

        date = str(random.choice(self.my_csv.Date))
        while date is None:
            date = str(random.choice(self.my_csv.Date))
        generated_name += ", " + date
        #predict_array = {generated_name}
        #offense_predict = predict(predict_array)
        #print (offense_predict)
        #if offense_predict > .5:
        #    return self.generate_art_data()
        #else:
            #return generated_name
        return generated_name


    def cleanup_title(self, title):
        stopwords = ['what','who','is','a','at','the','of','or','and','in', 'an', 'la', 'le', 'de', 'from']
        words = re.split("\W+",title)
        #words = title.split()
        if len(words) > 1:
            index = len(words)-1
            word = words[index].lower()
            #print(word)
            if word in stopwords or word is ',':
                #print(words[index])
                del words[index]
                title = self.cleanup_title(' '.join(words))
        return title
