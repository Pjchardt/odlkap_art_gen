# odlkap_art_gen
image generator for ODLKAP [online database of lesser known american painters] project

Project pulls images from firebase database and applies neural style transfer--courtesy of https://github.com/cysmith/neural-style-tf --by selecting a random style from a database of images scraped from Wikiart. Image data (Title, Artist, and date) is generated using the Moma repo https://github.com/MuseumofModernArt/collection 

Note: A forked version of neural-style is a submodule of the repo. Not sure how that works with a public repo as I only used submodules in one previous project with no collaborators :) 
