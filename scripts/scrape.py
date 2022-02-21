# functions for scraping

# importing libs
import requests
from bs4 import BeautifulSoup
import pandas as pd

# defining functions
def collect_tag_links():
    '''
    collects all complete links to different intership category pages such as:
    internships in Delhi, Finance internships, Tech internships, internships in chandigarh etc.
    
    OUPUT:
    tag_links - returns all links to different present on www.letsintern.com 
    '''
    tag_links = []
    
    url = requests.get('https://www.letsintern.com/')
    data = url.text
    soup = BeautifulSoup(data,'lxml')
    
    tags = soup.find_all('li',attrs = {'class':'col-sm-4'})
    for i in tags:
        hrefs = i.find_all('a')
        hrefs = ['http://letsintern.com' + j['href'] for j in hrefs]
        tag_links.extend(hrefs)
        
    return tag_links

def find_links_main(links_list):
    '''
    finds links to specific internship pages from pages where different internship profiles are listed. 
    Eg : www.letsintern.com/interships/IT-internships
    
    INPUT:
    links_list - a list of complete links that refer to different categorial pages
    
    OUPUT:
    collected_links - a list of collected links from all the pages in links_list 
    '''
    collected_links = []
    n = 1
    print('Progress(completes when = 1):')
    for link in links_list:
        url = requests.get(link)
        data = url.text
        soup = BeautifulSoup(data,'lxml')
        
        links = soup.find_all('div', attrs = {'class':'job-title'})
        
        collected_links.extend(['http://letsintern.com' + i.a['href'] for i in links if 'letsintern' not in i.a['href']])
        
        print(n/len(links_list))
        n+= 1
    collected_links = list(set(collected_links))
    return collected_links

def find_links_internship(links_list):
    '''
    finds the links present on an internship profile page. These links point to a company 
    page where more links are posted. 
    Also, the links collected will be similar to the internship on that page as these themselves are the 
    recommendations by letsintern.
    
    INPUT:
    links_list - a list of complete links that refer to specific internship pages
    
    OUTPUT:
    collected_links - a list of collected links from all the pages in links_list after removing the 
                      links in the input links_list(ensuring we aren't returning duplicates).
                      
    '''
    collected_links = []
    n = 1
    print('Progress(completes when = 1):')
    for link in links_list:
        url = requests.get(link)
        data = url.text
        soup = BeautifulSoup(data, 'lxml')
        
        links = soup.find_all('div',attrs={'class':"col-sm-9 col-xs-9"})
        
        collected_links.extend(['http://letsintern.com' + i.a['href'] for i in links])
        
        print(n/len(links_list))
        n+= 1
    collected_links = list(set(collected_links))
    return collected_links

def find_links_company(links_list):
    '''
    finds the links to different internship profiles present on an internship company page. 
    
    INPUT:
    links_list - a list of complete links that refer to specific company pages
    
    OUTPUT:
    collected_links - a list of collected links from all the pages in links_list after removing the 
                      links in links_list.
    '''
    collected_links = []
    n = 1
    print('Progress(completes when = 1):')                      
    for link in links_list:
        url = requests.get(link)
        data = url.text
        soup = BeautifulSoup(data, 'lxml')
                           
        links = soup.find_all('div',attrs = {'class':'job-title'})
                           
        for i in links:
            try:
                collected_links.append('http://letsintern.com'+ i.a['href'])
            except:
                print('link not found:')
                print(i.a)
                continue
        print(n/len(links_list))
        n+= 1
    return list(set(collected_links))

def extract_data(links_list):
    '''
    extracts all the relevant data needed from each of the links and returns and saves a 
    dataframe containing all that information.
    
    INPUT:
    links_list - a list of complete links that refer to specific internship pages
    
    OUTPUT:
    df - a dataframe with the rows as the links and the columns as the information extracted
    
    '''
    job_title = []
    company_name = []
    job_loc = []
    details = []
    category = []
    compensation =[]
    start = []
    end = []
    skills = []
    hrefs = []
    n = 1
    
    for link in links_list:
        url = requests.get(link)
        data = url.text
        soup = BeautifulSoup(data,'lxml') 

        try :
            # many job titles were not given as the pages didn't exist themselves
            job_title.append(soup.find_all('div',attrs={'class':'job-title'})[0].text)
        except:
            print(link)
            links_list.remove(link)
            continue # continue breaks the current iteration of the loop and jumps to the next one
        try:                 
            company_name.append(soup.find_all('div', attrs ={'class':'company-name'})[0].text)
        except:
            print(soup.find_all('div', attrs ={'class':'company-name'}))
            company_name.append('no company found')
        try:
            job_loc.append(soup.find_all('div', attrs ={'class':'job-locations'})[0].text)
        except:
            print(soup.find_all('div', attrs ={'class':'job-locations'}))
            job_loc.append('no job location found')
        try:
            details.append(soup.find_all('div', attrs ={'class':'details-section fixht'})[0].text)
        except:
            print(soup.find_all('div', attrs ={'class':'details-section fixht'}))
            details.append('no details found')
        try:  
            category.append(soup.find_all('a', attrs= {'title':'Internship Category'})[0].text)
        except:
            print(soup.find_all('a', attrs= {'title':'Internship Category'}))
            category.append('no category found')
        try:
            compensation.append(soup.find_all('a', attrs= {'title':'Compensation Type'})[0].text)
        except: 
            print(soup.find_all('a', attrs= {'title':'Compensation Type'}))
            compensation.append('no compensation found')
        try:
            start.append(soup.find_all('li', attrs = {'title':'Start Date'})[0].text)
        except:
            print(soup.find_all('li', attrs = {'title':'Start Date'}))
            start.append('no start date found')
        try:    
            end.append(soup.find_all('li', attrs = {'title':'End Date'})[0].text)
        except:
            print(soup.find_all('li', attrs = {'title':'End Date'}))
            end.append('no end date found')
        try:
            skills.append(soup.find_all('div', attrs = {'id':'skills-required'})[0].text)
        except: 
            print(soup.find_all('div', attrs = {'id':'skills-required'}))
            skills.append('no skills found')
        hrefs.append(link)
        print(n/len(links_list))
        n+=1
       

    df = pd.DataFrame({'href':hrefs, 'job_title':job_title, 'company_name':company_name, 'job_loc':job_loc
                      ,'details':details, 'category':category, 'compensation':compensation, 'start':start
                      ,'end':end, 'skills':skills})

    return df


def scrape():
	'''
	runs all the above functions and returns a dataframe containing all the information
	
	OUTPUT:
	df - dataframe that contains the scraped data

	'''
	print('collecting links to categories on landing page')
	tag_links = collect_tag_links()
	print('collecting specific internship profile links - 1 ')
	saved_links = find_links_main(tag_links)
	print('collecting company page links from above internship pages')
	saved_links_1 = find_links_internship(saved_links)
	print('collecting specific internship profile links -2')
	saved_links_2 = find_links_company(saved_links_1)
	final_links = list(set(saved_links_2) | set(saved_links))
	print('collecting data from all internship profile links')
	df = extract_data(final_links)

	return df


