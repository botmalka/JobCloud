#TODO: import time and add a pause somewhere
from bs4 import BeautifulSoup 
import requests
import re 
import string
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def job_search(position, location):
    jobs, description, words = [], [], []
    #this section pulls data from indeed for the position/location for the pages in the range and extracts
    #the url from the clickable results for each job post, adding them to the 'jobs' list 
    for page in range(0,20,10): #15 items per page, but page in link iterates by 10 
        url = 'https://www.indeed.com/jobs?q={}&l={}&sort=date&start='.format(position, location)+str(page)
        result = requests.get(url)
        content = result.text
        soup = BeautifulSoup(content, 'html.parser')
        #searches the page for links in each post
        for tap_Items in soup.find_all(class_='tapItem'):
            for links in tap_Items.find_all('a', href=True):
                if ('fromjk=' in links['href']):
                    start = links['href'].find('fromjk=') + 4
                    stop = start + 19 #all the links so far have a set length of 19 characters as of 1/10/22
                    job_url = "https://www.indeed.com/viewjob?"+links['href'][start:stop]
                    jobs += [job_url]
    
    #grabs all text in the job description from every page found above and makes a dictionary of word counts
    for url in jobs:
        result = requests.get(url)
        content = result.text 
        soup = BeautifulSoup(content, 'html.parser')
        description = str(soup.text) #pulls the full text from each job 
        #this is a bunch of string manipulation to remove punctuation and split all the data into separate words
        words = words + re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', description)).translate(str.maketrans('','',string.punctuation)).split()
        frequency = [words.count(word) for word in words]
        word_count = dict(zip(words, frequency))
    return word_count

#runs a job search for data science and one for accounting, and generates a wordcloud from the data unique to the DS search
data_science = job_search('Data Science -analyst -engineer'.replace(' ', '%20'), '98108')
accounting = job_search('Accountant'.replace(' ', '%20'), '98108')
for key in accounting:
    if key in data_science:
        data_science.pop(key) #where x is in accounting
word_cloud = {key: value 
                for key, value in data_science.items()
                if value >= 15}
for remove_me in ["Data"]:
    word_cloud.pop(remove_me)
final_output_cloud = WordCloud(width = 1920, height = 1080).generate_from_frequencies(word_cloud)

#displays the wordcloud
plt.figure(figsize=(15,8))
plt.imshow(final_output_cloud)
print(word_cloud)
