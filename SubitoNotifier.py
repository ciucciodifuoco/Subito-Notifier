from bs4 import BeautifulSoup
import requests
import time
import beepy
import re
import animation
semaphore = True


def getitems():
    objects = []
    req = requests.get(main_url)
    soup = BeautifulSoup(req.text, "html.parser")
    product_list_items = soup.find_all('div', class_=re.compile(r'item-key-data'))
    for product in product_list_items:
        title = product.find('h2').string

        try:
            price = product.find('div', class_=re.compile(r'price')).string
        except:
            price = None

        link = product.parent.parent.parent.parent.get('href')
        location = product.find('span', re.compile(r'town')).string + product.find('span', re.compile(r'city')).string
        try:
            date = product.find('span', class_=re.compile(r'date')).string
        except:
            date = None

        if title and price and location and date and link:
            objects.append([title,price,location,date,link])

    return objects



def update_list(seconds, semaphore):
    wait.start()
    while semaphore:

        newlist = getitems()
        if any(items not in itemslist for items in newlist):
            wait.stop()
            print("\n/////////New item(s) is(are) being added////////////\n")
            beepy.beep()

            for elements in newlist:
                if elements not in itemslist:
                    itemslist.append(elements)
                    print("-------------------------\n")
                    print(elements[0])
                    print(elements[2] + " * " + elements[3])
                    print(elements[1])
                    print(elements[4])
            semaphore = False

        else:
            time.sleep(seconds)

    return 0



if __name__ == "__main__":
    while (True):
        try:
            main_url = str(input("Insert URL from subito.it:"))
            if "https://" not in main_url:
                main_url = "https://" + main_url

            break
        except:
            print("URL is not correct, retry")
            pass

    while (True):
        try:
            updateseconds = int(input("How often you want to search for new items (in seconds)? (Leave blank for every 120 seconds):"))
            break
        except:
            print("ERROR: Please insert a numeric value expressed in seconds")
            pass
    wait = animation.Wait()


    # POPULATE LIST WITH FIRST PAGE RESULTS
    #Array element [i][0] is title
    # Array element [i][1] is price
    # Array element [i][2] is location
    # Array element [i][3] is date
    # Array element [i][4] is URL
    itemslist = getitems()
    for i in range(len(itemslist)):
        print("-------------------------\n")
        print(itemslist[i][0])
        print(itemslist[i][2] + " * " + itemslist[i][3])
        print(itemslist[i][1])
        print(itemslist[i][4])








while True:
    update_list(updateseconds, semaphore)
    #update_list() sets semaphore = False after finding new items, re-set it to True to make it loop or do not and break to other stuff
    semaphore = True




