def counting(urls):
    file_dict = dict()
    for url in urls:
        url = url.replace('"','')
        split_url = url.split('/')
        url_file = split_url[-1]

        if file_dict.get(url_file, 0) > 0:
            file_dict[url_file] += 1 
        else:
            file_dict[url_file] = 1

    file_array = file_dict.items()
    file_array.sort(key=lambda x: (-x[1], x[0]))

    for i in range(3):
        print (file_array[i][0] + " " + str(file_array[i][1]))

urls = ["http://www.google.com/a.txt",
        "http://www.google.com.tw/a.txt",
        "http://www.google.com/download/c.jpg",
        "http://www.google.co.jp/a.txt",
        "http://www.google.com/b.txt",
        "https://facebook.com/movie/b.txt",
        "http://yahoo.com/123/000/c.jpg",
        "http://gliacloud.com/haha.png",
] 

counting(urls)