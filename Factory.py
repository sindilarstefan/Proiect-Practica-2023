from Siteuri import Siteuri, Emag, Altex

def factory(url):
    if "emag" in url:
        return Emag(url)
    else:
        if "altex" in url:
            return Altex(url)
