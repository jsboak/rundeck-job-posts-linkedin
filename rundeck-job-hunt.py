import csv
import time
import requests
from bs4 import BeautifulSoup
import time, os

d="@data.last_mod@"
p='%Y-%m-%d %H:%M:%S'
file_size= os.path.getsize("/tmp/rundeck_jobs_dedupe.csv")

epoch = int(time.mktime(time.strptime(d,p)))

# # print(epoch)

now = int(time.time())

# print(epoch_time)

if now - epoch > 86400 or file_size == 0: #If data hasn't been updated in last 24hrs
    initial_list = ["Company", "Job Title", "State", "Full Location", "Job Description"]
    
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    
    with open('/tmp/rundeck_jobs.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(initial_list)
    
    geoIds = {
        'Alabama':'102240587',
        'Alaska':'100290991',
        'Arizona':'106032500',
        'Arkansas':'102790221',
        'California':'102095887',
        'Colorado':'105763813',
        'Connecticut':'106914527',
        'Delaware':'105375497',
        'Florida':'101318387',
        'Georgia':'103950076',
        'Hawaii':'105051999',
        'Idaho':'102560739',
        'Illinois':'101949407',
        'Indiana':'103336534',
        'Iowa':'103078544',
        'Kansas':'104403803',
        'Louisiana':'101822552',
        'Maine':'101102875',
        'Maryland':'100809221',
        'Massachusetts':'101098412',
        'Michigan':'103051080',
        'Minnesota':'103411167',
        'Mississippi':'106899551',
        'Missouri':'101486475',
        'Montana':'101758306',
        'Nebraska':'101197782',
        'Nevada':'101690912',
        'New Hampshire':'103532695',
        'New Jersey':'101651951',
        'New Mexico':'105048220',
        'New York':'105080838',
        'North Carolina':'103255397',
        'North Dakota':'104611396',
        'Ohio':'106981407',
        'Oklahoma':'101343299',
        'Oregon':'101685541',
        'Pennsylvania':'102986501',
        'Rhode Island':'104877241',
        'South Carolina':'102687171',
        'South Dakota':'100115110',
        'Tennessee':'104629187',
        'Texas':'102748797',
        'Utah':'104102239',
        'Vermont':'104453637',
        'Virginia':'101630962',
        'Washington':'103977389',
        'West Virginia':'106420769',
        'Wisconsin':'104454774',
        'Wyoming':'100658004',
        'Australia':'101452733',
        'New Zealand':'105490917',
        'England':'102299470',
        'Germany':'101282230'
    }
    
    for geoLabel,geoId in geoIds.items():
    
      for i in range(0, 25, 200):
        
        if i == 0:
          start = ""
        else:
          start = "&start=" + str(i)
    
        url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?geoId=" + geoId + "&keywords=rundeck&location=California%2C%20United%20States&position=0" + start
    
      # print(url)
    
        page = requests.get(url, headers=headers)
    
        results = BeautifulSoup(page.content, "html.parser")
    
        # print(results.prettify())
    
        job_elements = results.find_all("li")
        
        for job_element in job_elements:
    
          company_name = job_element.find("h4", class_="base-search-card__subtitle").text.strip()
    
          job_title = job_element.find("h3", class_="base-search-card__title").text.strip()
    
          #print(company_name + " " + job_title)
          location = job_element.find("span", class_="job-search-card__location").text.strip()
    
          links = job_element.find_all("a")
          for link in links:
            link_url = link["href"]
    
            if "?trk=public_" not in link_url: # and "anovaa" in link_url:      
    
              job_description = link_url
    
              time.sleep(0.5)
    
            with open('/tmp/rundeck_jobs.csv', 'a', newline='') as file:
    
              writer = csv.writer(file)
    
              writer.writerow([company_name, job_title, geoLabel, location, job_description])
    
    with open('/tmp/rundeck_jobs.csv','r') as in_file, open('/tmp/rundeck_jobs_dedupe.csv','w') as out_file:
        seen = set() # set for fast O(1) amortized lookup
        for line in in_file:
            if line in seen: continue # skip duplicate
    
            seen.add(line)
            out_file.write(line)
else:
    print("Data was updated in the last 24hrs, not rerunning webcrawler.")