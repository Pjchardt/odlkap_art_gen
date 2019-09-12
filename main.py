from os import listdir
from os.path import isfile, isdir, join
import random
import time

import neural_style_tf.neural_style as ns
import art_data_gen as dg
import database as db

#STYLEPATH = './neural_style_tf/styles/'
STYLEPATH = './image_scraping/output'
CONTENTPATH = './images/content/'
CONTENTNAME = 'content.jpg'
GENERATEDIMAGEPATH = './image_output/result/result.png'

class Main(object):
    def __init__(self):
        self.db = db.PyrebaseDatabase()
        self.art_data = dg.ArtDataGen('./data/Artworks.csv')

    def start(self):
        self.run()
        #self.test_data_gen()

    def run(self):
        self.run_loop = True
        while self.run_loop:
            result, url = self.db.download_image("{0}{1}".format(CONTENTPATH, CONTENTNAME))
            if result is True:
                style_dir, style_name = self.get_style()
                print(style_name)
                args = ['--content_img', CONTENTNAME, '--content_img_dir', CONTENTPATH, '--style_imgs', style_name, '--style_imgs_dir', style_dir, '--model_weights', './neural_style_tf/imagenet-vgg-verydeep-19.mat' ]
                ns.main(args)
                image_data = self.art_data.generate_art_data()
                print(image_data)
                self.db.push_data(GENERATEDIMAGEPATH, image_data)
                time.sleep(10)
            else:
                time.sleep(1)

    def test_data_gen(self):
        while True:
            print(self.art_data.generate_art_data())
            time.sleep(1)

    def get_style(self):
        dirs = [d for d in listdir(STYLEPATH) if isdir(join(STYLEPATH, d))]
        style_dir = join(STYLEPATH, random.choice(dirs))
        print("Style directory: " + style_dir)
        styles = [f for f in listdir(style_dir) if isfile(join(style_dir, f))]
        print(styles)
        return style_dir, random.choice(styles)


m = Main()
m.start()
