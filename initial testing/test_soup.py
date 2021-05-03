from bs4 import BeautifulSoup
#from test_tournament_html import test_tournament

html_tournament =  open("test_tournament_html.html")
html_pool =  open("test_pool.html")
    
pool_soup = BeautifulSoup(html_pool, 'html.parser')

athlete_list = []

for athlete in pool_soup.find_all('a'):
    link = athlete.get('href')
    link_pieces = link.split("/")
    print("Athlete Name: {name:<25} Athlete ID: {id}".format(name = athlete.get_text(), id=link_pieces[2]))
    athlete_list.append(athlete.get_text())


print(athlete_list)
pool_size = len(athlete_list)


for test in pool_soup.find_all('div',class_="Table-athlete"):
    print("Pool Row for ",end="")
    print(test.a.get_text())
    
    for score in test.find_all('div', class_="ResultsPool-score"):
        result = score.get_text()
        self = True if result else False
        if(score.get_text()):
            print("Score: {s}".format(s=score.get_text()))
        else:
            print("Score: ---")
