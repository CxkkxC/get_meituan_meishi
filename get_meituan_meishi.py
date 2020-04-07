import sqlite3
def meituan_opendb():
    conn = sqlite3.connect("meituan_date.db")
    cur = conn.execute("""create table if not exists meishi_info
    (id integer PRIMARY KEY autoincrement,
    poiId varchar(30),infourl varchar(126),
    name varchar(256),avgScore varchar(30),address varchar(256),
    allCommentNum varchar(30),avgPrice varchar(30))""")
    return cur,conn

#  往数据库中添加内容
def meituan_insertData(poiId,infourl,name,avgScore,address,allCommentNum,avgPrice):
        hel = meituan_opendb()
        hel[1].execute("insert into meishi_info(poiId,infourl,name,avgScore,address,allCommentNum,avgPrice) values ('%s','%s','%s','%s','%s','%s','%s')"%(poiId,infourl,name,avgScore,address,allCommentNum,avgPrice))
        hel[1].commit()
        hel[1].close()

# 查询用户全部信息
def meituan_showAll():
    hel = meituan_opendb()
    cur = hel[1].cursor()
    cur.execute("select * from meishi_info")
    res = cur.fetchall()
    cur.close()
    return res

def url_list(url):  # 构建页地址列表
    get_url_list = []
    for i in range(1, 68):
        get_url_list.append(url+'%s/'%str(i))
    return get_url_list
# url_list(url)
def get_url(url):  # 解析美食页，获取美食的名字，平均价格，平均分数, 评论数
    response = requests.get(url)
    html = response.content.decode()
    soup = BeautifulSoup(html, 'lxml')
    soup = soup.find_all('script')
    print(soup)
    text = soup[14].get_text().strip()
#         print(text)
    text = text[19:-1]
    result = json.loads(text)
#         print(result)
    results = result['poiLists']
    count=results['totalCounts']
    print('火锅店总数为：%s'%count)
    results = results['poiInfos']
    allinfo=[]
    for i in results:
        allinfo.append([i['poiId'],"https://gz.meituan.com/meishi/"+str(i['poiId']),i['title'], i['avgScore'], i['address'], i['allCommentNum'], i['avgPrice']])
    return allinfo  # 获取的原数据

def main(urls):
    for url in url_list(urls):
        a = get_url(url)
#         print(a)
        for i in a:
            meituan_insertData(str(i[0]),str(i[1]),str(i[2]),str(i[3]),str(i[4]),str(i[5]),str(i[6]))
        print(url+'-----该页完成！')
        time.sleep(5)
        
urls='https://gz.meituan.com/meishi/c17/pn'
main(urls)
