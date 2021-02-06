import pandas as pd
import requests
import bs4
import sys
from googlesearch import search 

rating=[]
phone_scores = []

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

review_sites = ["The Verge", "Techradar", "Tomsguide", "Android Authority","Whathifi", "Gsmarena", "Notebookcheck", "t3",
                "Phonearena",
                "Android Police", "Trustedreviews"]

test_sites = ["The Verge", "Techradar", "Tomsguide", "Android Authority","Whathifi", "Gsmarena", "Notebookcheck", "t3",
            "Phonearena"]

devices = ["S21 Ultra", "Note 20 Ultra", "Iphone 12 Pro Max", "Iphone 12", "Iphone SE",
           "Oneplus 8 Pro", "Google Pixel 5", "Google Pixel 4a"]

reviews = []

def main():
    for phone in devices:
        for site in test_sites:
            product = phone
            l = get_links(product, site)
            #print(l)
            k = check_links(product, site, l)
            #print(k)
            if k:
                x = get_score(k, site)
                rating.append(x)
                print(site + " " + str(x))
        if rating:
            total_sum = float(0)
            count = 0
            for value in rating:
                if value != 0:
                    total_sum = total_sum + value
                    count = count + 1
            if count != 0:
                avg_rating = total_sum/count
                phone_scores.append(avg_rating)
                print("%.2f" % avg_rating)
            else:
                print("Given sites have no rating for this product")
        else:
            print("No reviews were found for the product.")
        reviews.append([phone, avg_rating])
    sorted_reviews = sorted(reviews, key = lambda x : x[1], reverse = True)
    df = pd.DataFrame(sorted_reviews, columns = ["Smartphone", "Rating"])
    print(df)

def get_links(product, website):
    query = product + " " + "review" + " " + website 
    links = []
    for j in search(query, tld="co.in", num=3, stop=3, pause=5): 
        links.append(j)
    return links

def get_score(link, site):
    res = requests.get(link,headers=HEADERS)
    soup = bs4.BeautifulSoup(res.content, "html.parser")
    if site == "The Verge":
        score_txt = soup.find_all("span", {"class":"c-scorecard__score-number"})[0].get_text()
        score = float(score_txt.split(" ")[0])
        return score
    elif site == "Techradar" or  site == "Tomsguide" or site == "Whathifi":
        score_star = str(soup.find_all("span", {"class":"chunk rating"})[0])
        star = "icon icon-star"
        count_stars = score_star.count(star)
        count_half_stars = score_star.count("half")
        score = (float(count_stars) - float(count_half_stars)/2) * 2
        return score
    elif site ==  "Android Authority":
        score_star = soup.find_all("div", {"class":"moove-aa-star-rating-top-outer"})
        if not score_star:
            return 0
        else:
            score_txt = str(score_star[0])
            first = score_txt.split("style", 1)[1]
            second = first.split("%", 1)[0]
            score_txt = second.split(" ", 1)[1]
            score = float(score_txt) / 10
            return score
    elif site =="Gsmarena":
        score_txt = soup.find_all("span", {"class":"score"})[0].get_text()
        score = float(score_txt) * 2
        return score
    elif site =="Notebookcheck":
        score_txt = soup.find_all("tspan", {"id":"tspan4350"})[0].get_text()
        score = float(score_txt[-4:-2]) /10
        return score
    elif site == "t3":
        score_star = str(soup.find_all("span", {"class":"chunk rating"})[0])
        star = "rating__star"
        count_stars = score_star.count(star)
        count_empty_stars = score_star.count("empty") * 2
        count_half_stars = score_star.count("half") * 2
        score = (float(count_stars) - float(count_empty_stars) - float(count_half_stars)/2) * 2
        return score
    elif site == "Phonearena":
        score_txt = soup.find_all("div", {"class":"progress-wrap clearfix"})[0].get_text()
        first_int = score_txt.split(".", 1)[0][-1]
        second_int = score_txt.split(".", 1)[1][0]
        score = float(first_int + second_int) /10
        return score
        

def check_links(product, site, links):
    query = product + " " + site + " " + "review"
    right_link = ""
    words = query.split()
    for j in links:
        count = 0
        for word in words:
            if word.lower() in j.lower():
                count = count + 1
        if count == len(words):
            right_link = j
            break
    return right_link

if __name__ == "__main__":
    main()