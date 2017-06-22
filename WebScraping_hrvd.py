from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
import os
import json

def multifind(string, value, start = 0, stop = None):
    values = []
    while True:
        found = string.find(value, start, stop)
        if found == -1:
            break
        values.append(found)
        start = found + 1
    return values

driver=webdriver.Chrome()
driver.get("https://connects.catalyst.harvard.edu/Profiles/search/")


elem=driver.find_element_by_id("ctl00_ContentMain_rptMain_ctl00_ctl00_txtFname")
elem.clear()
elem.send_keys("x")
elem.send_keys(Keys.RETURN)


# get page #

no_of_pages=driver.find_element_by_xpath(".//*[@id='ctl00_divProfilesContentMain']/div[7]/div/table/tbody/tr/td[2]")

pages=no_of_pages.text

pos1= pages.index("of ")
pages= pages[pos1+3:]
 
contentPage=webdriver.Chrome()

def extract_content():
    dict={}
    links=driver.find_elements_by_xpath(".//*[@id='tblSearchResults']/tbody/tr[*]/td[*]")
    for link in links:
        dict["name"]=link.text
        data=link.find_element_by_tag_name("a")
        linkName= data.get_attribute("href")
        contentPage.get(linkName)
        profileNumber=contentPage.current_url.split("/")
        # print(profileNumber[-1])
        
        profileList=contentPage.find_elements_by_xpath(".//*[@id='ctl00_divProfilesContentMain']/div[7]/table/tbody/tr/td[1]/div/table/tbody/tr/td/div/table/tbody/tr[*]")
        
        
        dict["identifier"]=profileNumber[-1]
        email=""
        for profile in profileList:
            if profile.text.find("Email") !=-1:
                #download image
                elem = profile.find_element_by_tag_name("img")
                src=elem.get_attribute("src")
                urllib.urlretrieve(src, "c:/temppython/email.png")
                #call tessearct ocr and generate ouput.txt
                os.system("C:\Progra~2/Tesser~1/tesseract.exe c:/temppython/email.png c:/temppython/output")
                #read output.txt and get data
                try:
                    email = next(open("c:/temppython/output.txt"))
                except StopIteration:
                    email=""
                if email !="":
                    email = email.replace(" ",".")
                    email = email.replace("/n","").rstrip()
                    dict["email"]=email
            else:
                #get all other data and construct json
                if profile.text.find(" ")==-1:
                    dict[profile.text.lower()]=""
                else:
                    arr=profile.text.split(" ",1)
                    dict[arr[0].lower()]=arr[1]
        
        
        pmIds=contentPage.find_element_by_tag_name("body")
      
        pmids_search=pmIds.text
        
        #pmids_search=mystring
        positions=multifind(pmids_search,"PMID: ")
       
    
        ##TODO need to add array of PMIDs to dictionary
        
        pmids_list=[]
        for pos in positions:
             index=pmids_search.index(".",pos)
             
    
             pmid=pmids_search[(pos+5) : index]
             pmid=pmid.strip()
             
             try:
                 index=pmid.index(";")
                 pmid=pmid[:index]
                 pmid=pmid.strip()
             except ValueError:
                 print('not found')
             
             
             pmids_list.append(pmid)
             #print(pmids_list)
    
        dict["pmids"]=pmids_list
        print(pmids_list)
        json_data=json.dumps(dict)
        f = open("c:/temppython/output/"+ profileNumber[-1]  + ".json","w") #opens file with name of "test.txt"
    
        f.write(json_data)
        f.close()


for i in range(1,int(pages)+1):
    extract_content()
    next_elem=driver.find_element_by_xpath(".//*[@id='ctl00_divProfilesContentMain']/div[7]/div/table/tbody/tr/td[3]/a[2]")
    next_elem.click()    
    i=i+1

   
#contentPage.close()
#driver.close()


