import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

def ptt(board, findpage, findlist):
    ptt_url = 'https://www.ptt.cc/bbs/'
    board_url = ptt_url + board + '/index.html'
    r = requests.get(board_url)

    # check if board exists
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')

        # get page num
        page_num = 0
        paging = soup.select('div.btn-group-paging a')
        for paging_btn in paging:
            if paging_btn.string == "‹ 上頁":
                last_page = paging_btn.get('href')
                last_page_index = last_page.split('/')[-1].replace('index','').replace('.html','')
                page_num = int(last_page_index) + 1
                break
        
        page_list = np.array(range(page_num, 0, -1))
        if findpage == "index":
            page_list = np.array(findlist)
        elif findpage == "new":
            page_list = np.array(range(page_num, page_num - findlist, -1))
        elif findpage == "old":
            page_list = np.array(range(1, page_list + 1))

        # get all posts by page
        for page_index in page_list:
            page_url = ptt_url + board + '/index' + str(page_index) + '.html'
            page_r = requests.get(page_url)

            # check if page exists
            if page_r.status_code == requests.codes.ok:
                print ("Page " + str(page_index))
                page_soup = BeautifulSoup(page_r.text, 'html.parser')
                post_divs = page_soup.select('div.r-ent')

                # get every single post in the page
                for div in post_divs:
                    div_soup = BeautifulSoup(str(div), 'html.parser')

                    # without post rule
                    post_mark = div_soup.select('div.meta div.mark')
                    if post_mark[0].string != 'M':

                        # get post url
                        a_tag = div_soup.select('div.title a')
                        # check if post exists
                        if a_tag:
                            post_url = a_tag[0].get('href')

                            # get post by url
                            post_dict = get_post(post_url)
                            if post_dict:
                                for key, value in post_dict.items():
                                    post_meta = str(key) + ': ' + str(value)
                                    print (post_meta)
            else:
                print ("Page" + str(page_index) + " isn't exist!")
            
    else:
        print ("Board isn't exist!")
        

def get_post(post_url):
    ptt_url = 'https://www.ptt.cc'
    post_url = ptt_url + post_url
    r = requests.get(post_url)

    post_dict = dict()
    #check if post url exists
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')

        # get board name
        board_name = soup.select('div.article-metaline-right span.article-meta-value')
        post_dict['Board'] = board_name[0].string

        # get meta data: author, title, date
        post_meta = soup.select('div.article-metaline')
        for meta in post_meta:
            meta_soup = BeautifulSoup(str(meta), 'html.parser')
            meta_tag = meta_soup.select('span.article-meta-tag')
            meta_value = meta_soup.select('span.article-meta-value')

            if meta_tag[0].string == '作者':
                post_dict['Author'] = meta_value[0].string
            elif meta_tag[0].string == '標題':
                post_dict['Title'] = meta_value[0].string
            elif meta_tag[0].string == '時間':
                post_dict['Date'] = meta_value[0].string

        # get post content
        post_content = str(soup.select('div#main-content')[0])
        # remove "board, meta data, push" from post to get content 
        board_tag = soup.select('div.article-metaline-right')
        meta_tag = soup.select('div.article-metaline')
        push_tag = soup.select('div.push')
        for remove in board_tag:
            post_content = post_content.replace(str(remove),'')
        for remove in meta_tag:
            post_content = post_content.replace(str(remove),'')
        for remove in push_tag:
            post_content = post_content.replace(str(remove),'')

        post_content = BeautifulSoup(post_content, 'html.parser')
        post_dict['Content'] = post_content.text
    
    return post_dict

ptt('movie','new',2)
#first parameter: board
#second parameter: find type(list(頁數), new(最新幾篇), old(最舊幾篇))
#third parameter: page number