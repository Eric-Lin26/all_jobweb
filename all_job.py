from bs4 import BeautifulSoup
import requests
import time
import random
i = 1
job = [] # 抓取到的最後資料放這

# 104
print('正在爬104求職網')
for page in range(5): # 看要爬幾頁
    url = 'https://www.104.com.tw/jobs/search/?ro=0&jobcatExpansionType=0&area=6001007001%2C6001007002&order=11&asc=0&sctp=M&scmin=30000&scstrict=1&scneg=0&page='+str(i)+'&mode=s&jobsource=2018indexpoc'
    domain = 'https:'
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }
        
    rep = requests.get(url, headers=headers)
    
    if rep.status_code == 200: # 測試有無錯誤
        print('連結成功')
    else:
        print('URL連結錯誤：', url)

    soup = BeautifulSoup(rep.text, 'html5lib')
    link = soup.findAll('a',{'class':'js-job-link'})# 單純先看有幾筆資料
    print('共有 ' + str(len(link)) + ' 筆資料') 

    # 這邊直接先抓取整個欄位
    data = soup.findAll('article', {'class':'b-block--top-bord job-list-item b-clearfix js-job-item'})

    time.sleep(1)
    for ts in data: # 下面再從欄位中, 一個個取出
        title = ts.find('a',{'class':'js-job-link'}).text
        salary = ts.find('span',{'class':'b-tag--default'}).text.strip()
        url = ts.find('a',{'class':'js-job-link'}).attrs['href']
        date = ts.find('span', {'class':'b-tit__date'}).text.strip()
        company = ts.find('ul', {'class':'b-list-inline b-clearfix'}).find('a').text.strip()
        job.append(date + '｜' + title + '｜' + company + '｜' + salary + '｜' + domain + url) # 使用｜, 是方便存成csv編碼, 自動讓他切割欄位
    i += 1
    print('正在跑第', i, '頁')
    time.sleep(random.randint(1, 6))

# 1111
print('正在爬1111求職網')
i = 1
for page in range(5):
    url = 'https://www.1111.com.tw/search/job?c0=100802%2C100801&st=1&sa0=30000*&fs=1&page='
    domain = 'https://www.1111.com.tw'
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }
        
    rep = requests.get(url+str(i), headers=headers)
    
    if rep.status_code == 200: # 測試有無錯誤
        print('連結成功')
    else:
        print('URL連結錯誤：', url)

    soup = BeautifulSoup(rep.text, 'html5lib')

    link = soup.findAll('a',{'class':'text-truncate position0Link mobileItemClick'})# 單純先看有幾筆資料
    print('共有 ' + str(len(link)) + ' 筆資料') 

    # 這邊直接先抓取整個欄位
    data = soup.findAll('ul', {'class':'row no-gutters si-item si-1 digest'})
    
    time.sleep(1)
    for ts in data: # 下面再從欄位中, 一個個取出
        title = ts.find('a',{'class':'text-truncate position0Link mobileItemClick'}).text
        salary = ts.find('span',{'style':'color:#dd7926;'}).text.strip()
        url = ts.find('a',{'class':'text-truncate position0Link mobileItemClick'}).attrs['href']
        company = ts.find('div', {'class':'d-none d-md-flex'}).find('a').text
        date = ts.find('div', {'class':'date'}).text
        job.append(date[5:15] + '｜' +title + '｜' + company + '｜' + salary + '｜' + domain + url) # 使用｜, 是方便存成csv編碼, 自動讓他切割欄位
    i += 1
    print('正在跑第', i, '頁')
    time.sleep(random.randint(1, 6))

# 518
print('正在爬518求職網')
i = 1
for page in range(5):
    url = 'https://www.518.com.tw/job-index-P-'+str(i)+'.html?i=1&am=1&aa=3001012002,3001012004,&ai=0&ai=0'
    rep = requests.get(url)
    rep_text = rep.text
    soup = BeautifulSoup(rep_text, 'html5lib')
    all_job_hover = soup.findAll('ul', {'class':'all_job_hover'})
    
    for line in all_job_hover:
        title = line.find('h2').text
        date = line.find('li', {'class':'date'}).text.strip()
        salary = line.find('p', {'class':'jobdesc'}).text
        company = line.find('li', {'class':'company'}).text.strip('\n').strip('\t')
        url = line.find('a',{'target':'_blank'}).attrs['href']
        job.append(date + '｜' + title + '｜' + company + '｜' + salary + '｜' + url)
    i += 1
    print('正在跑第', i, '頁')
    time.sleep(random.randint(1, 6))

print('共抓完', i, '頁')
print('寫入檔案')
with open('0616all_jobs.csv', 'w', encoding='utf-8') as f:
    f.write('日期｜職缺｜公司｜薪水｜網址\n') # 先寫入這三個欄位
    for line in job:
        f.write(line + '\n')
print('已完成爬蟲')