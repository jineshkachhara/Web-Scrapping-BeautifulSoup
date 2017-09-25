from bs4 import BeautifulSoup
import re
import time
import requests


def run(url):

    pageNum=2 # number of pages to collect

    fw=open('reviews.txt','w') # output file
	
    for p in range(1,pageNum+1): # for each page 

        print ('page',p)
        html=None

        if p==1: pageLink=url # url for page 1
        else: pageLink=url+'?page='+str(p)+'&sort=' # make the page url
		
        for i in range(5): # try 5 times
            try:
                #use the browser to access the url
                response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content # get the html
                break # we got the file, break the loop
            except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                print ('failed attempt',i)
                time.sleep(2) # wait 2 secs
				
		
        if not html:continue # couldnt get the page, ignore
        
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml') # parse the html 

        reviews=soup.findAll('div', {'class':re.compile('review_table_row')}) # get all the review divs

        for review in reviews:

            critic= (getCritic(review))
            text= (getRating(review))
            datee= (getSource(review))
            source= (getDate(review))
            TextLen= (getTextLen(review))
                            
            fw.write(critic+'\t'+text+'\t'+datee+'\t'+source+'\t'+TextLen+'\t'+'\n') # write to file 
	
    fw.close()

    

def getCritic(review):
    critic='NA'
    criticChunk=review.find('a',{'href':re.compile('/critic/')})
    if criticChunk: 
        critic=criticChunk.text
    return critic#.encode('ascii','ignore')
        
def getRating(review):
    rating='NA'
    rating_rot=review.find('div',{'class':'review_icon icon small rotten'})
    if rating_rot: 
        rating= 'rotten'
        #.encode('ascii','ignore')
                
    rating_rot1=review.find('div',{'class':'review_icon icon small fresh'})
    if rating_rot1: 
        rating = 'fresh'#.encode('ascii','ignore')
    return rating
        
def getSource(review):
    source='NA'
    sourceChunk=review.find('em',{'class':'subtle'})
    if sourceChunk: 
        source= sourceChunk.text#.encode('ascii','ignore')
    return source

def getDate(review):
    date='NA' 
    Gdate=review.find('div',{'class':'review_date'})
    if Gdate: 
        date=Gdate.text#.encode('ascii','ignore')
    return date

def getTextLen(review):
    text='NA'
    textChunk=review.find('div',{'class':'the_review'})
    if textChunk: 
        text=textChunk.text#.encode('ascii','ignore')
    return str(len(text))
            
        
if __name__=='__main__':
    url='https://www.rottentomatoes.com/m/space_jam/reviews/'
    run(url)