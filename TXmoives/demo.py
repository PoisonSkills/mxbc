import requests
from lxml import etree
import threading


class Spider(object):
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
        self.offset = 1

    def start_work(self, url):
        print("正在爬取第 %d 页......" % self.offset)
        self.offset += 1
        response = requests.get(url=url, headers=self.headers)
        html = response.content.decode()
        html = etree.HTML(html)

        video_src = html.xpath('//a[@class="jump-details pr-plugin-data"]/@href')
        new_video_src = []
        for item in video_src:
            v_resp = requests.get('http:' + item, headers=self.headers)
            h2 = v_resp.content.decode()
            h2 = etree.HTML(h2)
            v_src = h2.xpath('//div["img-wrap "]/img/@src')
            new_video_src.append(v_src[0])
        print(new_video_src)
        video_title = html.xpath('//img[@class="scrollLoading"]/@title')
        print(video_title)
        next_page = "http:" + html.xpath('//a[@class="next"]/@href')[0]
        # 爬取完毕...
        if next_page == "http:":
            return

        self.write_file(new_video_src, video_title)
        self.start_work(next_page)

    def write_file(self, video_src, video_title):
        for src, title in zip(video_src, video_title):
            response = requests.get("http:" + src, headers=self.headers)
            file_name = title + ".jpg"
            file_name = "".join(file_name.split("/"))
            print("正在抓取%s" % file_name)
            with open('/Users/lilonglong/Desktop/mp4/' + file_name, "wb") as f:
                f.write(response.content)


if __name__ == "__main__":
    spider = Spider()
    # t = threading.Thread(target=spider.start_work, args=('https://ibaotu.com/sucai/19613230.html',))
    # t.start()
    for i in range(0, 3):
        spider.start_work(url="https://ibaotu.com/guanggao/7-0-0-0-"+ str(i) +"-1.html")
        t = threading.Thread(target=spider.start_work,
                             args=("https://ibaotu.com/guanggao/7-0-0-0-" + str(i) + "-1.html",))
        # t = threading.Thread(target=spider.start_work,args=('https://ibaotu.com/sucai/19613230.html', ))
        t.start()