def scrape():
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    import requests as r
    from splinter import Browser

    nasa_info = {}

    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

    url_1 = 'https://mars.nasa.gov/news/'
    response = r.get(url_1)
    soup = bs(response.text, "html.parser")
    title = soup.find('div', class_="content_title").text.strip()
    #print(title)
    paras = soup.find('div', class_="rollover_description_inner").text.strip()
    #print(paras)
    nasa_info["news_title"] = title
    nasa_info["news_text"] = paras 

    #mars_space_images
    #executable_path = {'executable_path': 'chromedriver.exe'}
    #browser = Browser('chrome', **executable_path, headless=False)
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)
    html = browser.html
    soup = bs(html, 'html.parser')
    img = soup.find('article', class_="carousel_item")['style']
    img_url = img.replace("background-image: url('", "").replace("');", "")
    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + img_url
    #print(featured_image_url)
    nasa_info["featured_image_link"] = featured_image_url  
    
    #scraping mars_weather
    url_3 = "https://twitter.com/marswxreport?lang=en"
    response = r.get(url_3)
    soup = bs(response.text, "html.parser")
    #print(soup.prettify())
    tweet = soup.find('div', class_="js-tweet-text-container").text.strip()
    #print(tweet)    
    nasa_info["tweet"] = tweet
    
    #scraping mars_facts
    url_4 = 'https://space-facts.com/mars/'
    df = pd.read_html(url_4)
    mars_df = df[0]
    mars_renamed_df = mars_df.rename(columns={0: 'Parameter', 1: 'Value'})
    mars_renamed_df
    html_string = mars_renamed_df.to_html(classes='string')
    print(html_string)
    nasa_info["mars_facts"] = html_string
    
    #scraping mars_hems
    url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = r.get(url_5)
    soup = bs(response.text, "html.parser")
    #print(soup.prettify())
    images = soup.find_all('a', class_= "itemLink product-item")
    #print(images)
    for image in images:
        title = image.text
        img = image['href']
        main_url = 'https://astrogeology.usgs.gov'
        main_img_url = main_url + img
        #print(main_img_url)
        response = r.get(main_img_url)
        soup = bs(response.text, "html.parser")
        img_url_raw = soup.find('img', class_="wide-image")['src']
        img_url = main_url + img_url_raw
        #print(img_url)   
        
        nasa_info["img_title"] = title
        nasa_info["img_url"] = img_url

    return nasa_info
