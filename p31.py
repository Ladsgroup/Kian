import wikipedia
import codecs
base_dir = '/data/project/dexbot/pywikipedia-git/'
f = codecs.open('%skian_res.txt' % base_dir, 'r', 'utf-8')
a = f.read().split('\n')
f.close()
site = wikipedia.getSite('nl')
for name in a:
    if not name.strip():
        continue
    page = wikipedia.Page(site, name)
    try:
        page.get()
    except:
        continue
    try:
        data = wikipedia.DataPage(page)
        data.get()
    except:
        data.createitem()
    else:
        continue
    page2 = wikipedia.Page(site, name)
    try:
        data = wikipedia.DataPage(page2)
        data.get()
        data.editclaim(31, 5, refs={(143, 10000)})
    except:
        pass
