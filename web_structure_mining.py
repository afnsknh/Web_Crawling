import requests
from bs4 import BeautifulSoup

import pandas as pd

import networkx as nx
import matplotlib.pyplot as plt


def simplifiedURL(url):
    
    if "www." in url:
        ind = url.index("www.")+4
        url = "http://"+url[ind:]

    if url[-1] == "/":
        url = url[:-1]

    parts = url.split("/")
    url = ''
    for i in range(3):
        url += parts[i] + "/"
    return url

def crawl(url, max_deep,  show=False, deep=0, done=[]):
    global edgelist
    
    url = simplifiedURL(url)
    deep += 1

    if not url in done:
        links = getLink(url)
        done.append(url)
        if show:
            if deep == 1:
                print(url)
            else:
                print("|", end="")
                for i in range(deep-1): print("--", end="")
                print("(%d)%s" %(len(links),url))

        for link in links:
            link = simplifiedURL(link)
            edge = (url,link)
            if not edge in edgelist:
                edgelist.append(edge)
            if (deep != max_deep):
                crawl(link, max_deep, show, deep)

def getLink(src):
    try:
        page = requests.get(src)
        soup = BeautifulSoup(page.content, 'html.parser')

        a = soup.findAll('a')
        temp = []
        for i in a :
            try:
                link = i['href']
                if not link in temp and 'http' in link :
                    temp.append(link)
                
            except KeyError:
                pass
        return temp
        print(temp)
    except:
        return list()

                
root = "https://www.codepolitan.com/articles"
edgelist = []
nodelist = [root]

tampil = True
crawl(root, 3, show=tampil)
edgeListFrame = pd.DataFrame(edgelist, None, ("From", "To"))

g = nx.from_pandas_edgelist(edgeListFrame, "From", "To", None, nx.DiGraph())
pos = nx.spring_layout(g)

# hitung pagerank
damping = 0.1
max_iterr = 100
error_toleransi = 0.01
pr = nx.pagerank(g, alpha = damping, max_iter = max_iterr, tol = error_toleransi)

print("\n keterangan node:")
nodelist = g.nodes
label= {}
data = []
for i, key in enumerate(nodelist):
    data.append((pr[key], key))
    label[key]=i

urut = data.copy()
for x in range(len(urut)):
    for y in range(len(urut)):
        if urut[x][0] > urut[y][0]:
            urut[x], urut[y] = urut[y], urut[x]
            
urut = pd.DataFrame(data, None, ("Pagerank", "Node"))
print(urut)

plt.title('graph codepolitan')
nx.draw(g, pos)
nx.draw_networkx_labels(g, pos, label, font_color="w")

plt.axis("off")
plt.show()
