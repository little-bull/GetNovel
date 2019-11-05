import re
import urllib.request
import urllib.error
import sys

sys.setrecursionlimit(3000)


def getNovel(novel_url, next_cp):
    html = getHtml(novel_url)
    index = 2
    if html != "":
        title = getTitle(html)
        # print(title)

        text1 = getText(html)
        text2 = ''
        page_text, page_html = getNextPage(novel_url, index)
        index = index + 1
        while page_text != '':
            text2 = text2 + page_text
            page_text, page_html = getNextPage(novel_url, index)
            index = index + 1

        write2file(title + "\n\n" + text1 + text2)

        # print(text1 + text2)

        if text2 != '':
            next_chapter_url = getNextChapterUrl3(page_html, novel_url)
        else:
            next_chapter_url = getNextChapterUrl3(html, novel_url)

        print(novel_url)
        print(next_chapter_url)
        if next_chapter_url and next_cp:
            # print(next_chapter_url)
            getNovel(next_chapter_url, next_cp)

    print("finish Get")


def getHtml(novel_url):
    html = ""
    try:
        req = urllib.request.Request(novel_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/62.0.3202.62 Safari/537.36')
        html = urllib.request.urlopen(req).read()
        html = html.decode("gbk")
    except urllib.error.HTTPError as e:
        print(e.reason)

    return html


def getTitle(html):
    # 匹配规则1
    # title_reg = r'class=\"zhangj\"\>([\u4e00-\u9fa5]*\d*[\u4e00-\u9fa5]*)'
    # print(html)
    # 匹配规则2
    title = ''
    title_reg = '<h1>[a-zA-Z0-9\u4e00-\u9fa5\s]+</h1>'
    title_reg = re.compile(title_reg)

    title_match = title_reg.search(html)
    if title_match:
        title = title_match.group()
        title = title.replace('<h1>', ':)  ')
        title = title.replace('</h1>', '  (:')
        title = title + '\n' + "要开心哦~"

    # 每记录一章计数器加一
    global chapter_count
    chapter_count = chapter_count + 1

    return title or "find NoTitle"


def getText(html):
    # 匹配规则1
    # str_reg = "<p>([\u4e00-\u9fa5]+[（）《》——；，。“”<>！])+"

    # 匹配规则2
    str_reg = "&nbsp;([《》“”])?([\u4e00-\u9fa5]+[（）《》——；，。“”<>！])+([《》“”])?"

    str_reg = re.compile(str_reg)  # 可添加可不添加，增加效率
    str_list = str_reg.finditer(html)

    all_str = ""
    for k in str_list:
        all_str = all_str + k.group().replace("&nbsp;", "") + "\n"
    return all_str


def getNextChapterUrl(html):
    str_reg = "href=\".*\.html\"\>[\u4e00-\u9fa5]{3}"
    str_reg = re.compile(str_reg)  # 可添加可不添加，增加效率
    str_list = str_reg.finditer(html)

    all_str = ""
    for k in str_list:
        temp = k.group().replace("href=\"", "https://www.ertongtuku.com")
        temp = temp[0:-5]
        all_str = "" + temp
    # print(all_str)
    return all_str


def getNextChapterUrl2(last_url):
    next_url = ""
    chapter_id = 0

    chapter_id_reg = '[0-9]+.html'
    chapter_id_reg = re.compile(chapter_id_reg)

    chapter_id_match = chapter_id_reg.search(last_url)
    chapter_id = chapter_id_match.group()
    # repalec_start_pos = chapter_id_match.start()
    # repalec_end_pos = chapter_id_match.end()

    chapter_id = chapter_id.replace(".html", "")
    chapter_id = int(chapter_id)

    next_chapter_id = chapter_id + 1
    next_chapter_id = str(next_chapter_id)
    chapter_id = str(chapter_id)

    next_url = last_url.replace(chapter_id, next_chapter_id)

    return next_url


def getNextChapterUrl3(html, last_url):
    next_url = ''
    next_url_reg = '<a\shref=.*[0-9]+.html">[\u4e00-\u9fa5]+</a>'
    next_url_reg = re.compile(next_url_reg)

    next_url_matchs = next_url_reg.finditer(html)

    for math in next_url_matchs:
        next_url = math.group()
        if next_url.find('下一章') >= 0:
            break

    next_url = next_url.replace('<a href="', '')
    next_url = next_url.replace('">下一章</a>', '')
    next_url = re.sub('[0-9]+.html', next_url,last_url)

    return next_url


def getNextPage(last_url, index):
    text = ""
    page_url = ""
    replace_str = str.format('_{}.html', str(index))
    if last_url:
        page_url = re.sub('_?.html', replace_str, last_url)
        # page_url = last_url.replace(".html", "_2.html")
        html = getHtml(page_url)
        text = getText(html)
        return text, html


def write2file(text):
    text = text + "\n温馨提示：本章结束喽\n\n"
    with open("D:\\abc.txt", mode="a", encoding="UTF-8") as text_file:
        print("openfile", chapter_count)
        text_file.write(text)


# def funTest():
#     string = "abcdefg  acbdgef  abcdgfe  cadbgfe"
#
#     # 带括号与不带括号的区别
#     # 不带括号
#     regex = re.compile("((\w+)\s+\w+)")
#     print(regex.findall(string))


url1 = "https://www.ertongtuku.com/novel/477570/1" \
       "/aHR0cDovL3d3dy5lcnRvbmd0dWt1LmNvbS9kL2ZpbGUvMjAxOTA5LzI2L3Z6dHBrMHhkY2thLnBuZw==.html"

url2 = "https://www.xinshubao.net/14/14436/30673304.html"

next_chapter = True

chapter_count = 0

getNovel(url2, next_chapter)
# print(getHtml(url2))


# s_reg = '[0-9]+.html'
# s_reg = re.compile(s_reg)
# title = s_reg.search(url2).group()
# print(s_reg.search(url2))
# print(s_reg.search(url2).start())
# print(s_reg.search(url2).end())
# print(s_reg.search(url2).span())
#
#
# title = title.replace(".html", "")
# title = int(title)
# #
# print(title)
# #

# stra = '<a href="30366863.html">下一章</a>'
# print(stra.find('下一章'))
# print(stra.replace('<a href=\"', ''))
#
# print(str.format('{}', '8'))