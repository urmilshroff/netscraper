import bs4
import requests
import operator
from halo import Halo

user_id = input("Enter the username of the GitHub profile:\n")
user_link = "https://github.com/" + user_id

spinner = Halo(text="Scraping info...", spinner="dots")
spinner.start()

res = requests.get(user_link)
soup = bs4.BeautifulSoup(res.text, "lxml")

name = soup.select(".p-name.vcard-fullname.d-block.overflow-hidden")
count = soup.select(".Counter")

try:
    contribs = soup.select(".f4.text-normal.mb-2")
    contribs = contribs[1].text
    contribs = contribs[:-38]
except IndexError:
    print("Error: missing or broken info!")

try:
    max_contribs = {}
    for item in soup.findAll("rect", {"class": "day"}):
        date = item.get("data-date")
        max_contribs[date] = int(item.get("data-count"))
    max_contribs = sorted(max_contribs.items(),
                          key=operator.itemgetter(1), reverse=True)
    max_num = max_contribs[0][1:]
    max_date = max_contribs[0][:1]
except IndexError:
    print("Error: missing or broken info!")

spinner.stop()

try:
    print("\nSummary for GitHub user {} (aka {}):".format(
        user_id, name[0].text))
except IndexError:
    print("Error: missing or broken info!")

try:
    print("\nNumber of repositories: {}".format(count[0].text.strip()))
    print("Number of projects: {}".format(count[1].text.strip()))
    print("Number of starred items: {}".format(count[2].text.strip()))
    print("Number of followers: {}".format(count[3].text.strip()))
    print("Number of following: {}".format(count[4].text.strip()))
except IndexError:
    print("Error: missing or broken info!")

try:
    print("\nMost contributions in a single day: {}".format(max_num[:2]))
    print("Date of most contributions in a day: {}".format(max_date[:3]))
    print("Total contributions in the last year: {}".format(contribs.strip()))
except IndexError:
    print("Error: missing or broken info!")