import requests
from bs4 import BeautifulSoup as bs
import cred

def get_links(url):
    login_url = "https://elitesgrid.com/login"
    login_post_url = "https://elitesgrid.com/post/login"

    head = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'origin': 'https://elitesgrid.com', 'referer': 'https://elitesgrid.com/login'
    }
    s = requests.session()
    t = s.get(login_url)
    doc = bs(t.text, "html.parser")
    token = doc.find("input")["value"]

    login_payload = {
        'email': cred.email,
        'password': cred.password,
        '_token': token
    }

    login_req = s.post(login_post_url, headers=head, data=login_payload)

    varc = s.get(url)
    soup = bs(varc.text, "html.parser")
    tbody = soup.find_all('tbody')

    downloads = {}

    for team in tbody:
        rows = team.find_all('tr')
        for row in rows:
            lists = row.find_all('td')
            name = lists[1].string
            link = row.find('a', class_="btn btn-primary")["href"]
            downloads[name] = link
    
    path = cred.download_dir_path + "/"

    for item in downloads:
        req = s.get(downloads[item])
        file = open(f"{path + item}.pdf", "wb")
        file.write(req.content)
        file.close()
        print(f"{item} completed.....")

    return "\nYour Downloads are complete\n\n---------Thanks for visiting---------\n\n"

if __name__ == "__main__":
    downloads = get_links(cred.url)
    print(downloads)


