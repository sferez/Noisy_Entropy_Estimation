#!/usr/bin/env python
# coding: utf-8

# Class:
# 1 - Personality
# 2 - News and Media
# 3 - Company
# 

# In[1]:


from dataAquisition.scraping import scraping, init_driver


# In[4]:


scrape_accounts = [
    # Personality
    # {
    #     "user": "elonmusk",
    #     "dates": [
    #         ["2010-01-01", "2011-01-01"],
    #         ["2011-01-01", "2012-01-01"],
    #         ["2012-01-01", "2013-01-01"],
    #         ["2013-01-01", "2014-01-01"],
    #         ["2014-01-01", "2015-01-01"],
    #         ["2015-01-01", "2016-01-01"],
    #         ["2016-01-01", "2017-01-01"],
    #         ["2017-01-01", "2018-01-01"],
    #         ["2018-01-01", "2019-01-01"],
    #         ["2019-01-01", "2020-01-01"],
    #         ["2020-01-01", "2021-01-01"],
    #         ["2021-01-01", "2022-01-01"],
    #         ["2022-01-01", "2023-01-01"],
    #     ],
    #     "class": '1'
    # },
    # {
    #     "user": "billgates",
    #     "dates": [
    #         ["2009-01-01", "2010-01-01"],
    #         ["2010-01-01", "2011-01-01"],
    #         ["2011-01-01", "2012-01-01"],
    #         ["2012-01-01", "2013-01-01"],
    #         ["2013-01-01", "2014-01-01"],
    #         ["2014-01-01", "2015-01-01"],
    #         ["2015-01-01", "2016-01-01"],
    #         ["2016-01-01", "2017-01-01"],
    #         ["2017-01-01", "2018-01-01"],
    #         ["2018-01-01", "2019-01-01"],
    #         ["2019-01-01", "2020-01-01"],
    #         ["2020-01-01", "2021-01-01"],
    #         ["2021-01-01", "2022-01-01"],
    #         ["2022-01-01", "2023-01-01"]
    #     ],
    #     "class": '1'
    # },
    # {
    #     "user": "barackobama",
    #     "dates": [
    #         ["2007-01-01", "2008-01-01"],
    #         ["2008-01-01", "2009-01-01"],
    #         ["2009-01-01", "2010-01-01"],
    #         ["2010-01-01", "2011-01-01"],
    #         ["2011-01-01", "2012-01-01"],
    #         ["2012-01-01", "2013-01-01"],
    #         ["2013-01-01", "2014-01-01"],
    #         ["2014-01-01", "2015-01-01"],
    #         ["2015-01-01", "2016-01-01"],
    #         ["2016-01-01", "2017-01-01"],
    #         ["2017-01-01", "2018-01-01"],
    #         ["2018-01-01", "2019-01-01"],
    #         ["2019-01-01", "2020-01-01"],
    #         ["2020-01-01", "2021-01-01"],
    #         ["2021-01-01", "2022-01-01"],
    #         ["2022-01-01", "2023-01-01"]
    #     ],
    #     "class": '1'
    # },
    # {
    #     "user": "emmanuelmacron",
    #     "dates": [
    #         ["2013-01-01", "2014-01-01"],
    #         ["2014-01-01", "2015-01-01"],
    #         ["2015-01-01", "2016-01-01"],
    #         ["2016-01-01", "2017-01-01"],
    #         ["2017-01-01", "2018-01-01"],
    #         ["2018-01-01", "2019-01-01"],
    #         ["2019-01-01", "2020-01-01"],
    #         ["2020-01-01", "2021-01-01"],
    #         ["2021-01-01", "2022-01-01"],
    #         ["2022-01-01", "2023-01-01"]
    #     ],
    #     "class": '1'
    # },
    # {
    #     "user": "sanchezcastejon",
    #     "dates": [
    #         ["2009-01-01", "2010-01-01"],
    #         ["2010-01-01", "2011-01-01"],
    #         ["2011-01-01", "2012-01-01"],
    #         ["2012-01-01", "2013-01-01"],
    #         ["2013-01-01", "2014-01-01"],
    #         ["2014-01-01", "2015-01-01"],
    #         ["2015-01-01", "2016-01-01"],
    #         ["2016-01-01", "2017-01-01"],
    #         ["2017-01-01", "2018-01-01"],
    #         ["2018-01-01", "2019-01-01"],
    #         ["2019-01-01", "2020-01-01"],
    #         ["2020-01-01", "2021-01-01"],
    #         ["2021-01-01", "2022-01-01"],
    #         ["2022-01-01", "2023-01-01"]
    #     ],
    #     "class": '1'
    # },
    # Press EN
    # {
    #     "user": "BBCNews",
    #     "dates": [
    #         ["2007-01-01", "2008-01-01"],
    #         ["2008-01-01", "2009-01-01"],
    #         ["2009-01-01", "2010-01-01"],
    #         ["2010-01-01", "2011-01-01"],
    #         ["2011-01-01", "2012-01-01"],
    #         ["2012-01-01", "2013-01-01"],
    #         ["2013-01-01", "2014-01-01"],
    #         ["2014-01-01", "2015-01-01"],
    #         ["2015-01-01", "2016-01-01"],
    #         ["2016-01-01", "2017-01-01"],
    #         ["2017-01-01", "2018-01-01"],
    #         ["2018-01-01", "2019-01-01"],
    #         ["2019-01-01", "2020-01-01"],
    #         ["2020-01-01", "2021-01-01"],
    #         ["2021-01-01", "2022-01-01"],
    #         ["2022-01-01", "2023-01-01"]
    #     ],
    #     "class": '2'
    # },
    # {
    #     "user": "CNN",
    #     "dates": [
    #         ["2007-01-01", "2008-01-01"],
    #         ["2008-01-01", "2009-01-01"],
    #         ["2009-01-01", "2010-01-01"],
    #         ["2010-01-01", "2011-01-01"],
    #         ["2011-01-01", "2012-01-01"],
    #         ["2012-01-01", "2013-01-01"],
    #         ["2013-01-01", "2014-01-01"],
    #         ["2014-01-01", "2015-01-01"],
    #         ["2015-01-01", "2016-01-01"],
    #         ["2016-01-01", "2017-01-01"],
    #         ["2017-01-01", "2018-01-01"],
    #         ["2018-01-01", "2019-01-01"],
    #         ["2019-01-01", "2020-01-01"],
    #         ["2020-01-01", "2021-01-01"],
    #         ["2021-01-01", "2022-01-01"],
    #         ["2022-01-01", "2023-01-01"]
    #     ],
    #     "class": '2'
    # },
    # {
    #     "user": "nytimes",
    #     "dates": [
    #         ["2007-01-01", "2008-01-01"],
    #         ["2008-01-01", "2009-01-01"],
    #         ["2009-01-01", "2010-01-01"],
    #         ["2010-01-01", "2011-01-01"],
    #         ["2011-01-01", "2012-01-01"],
    #         ["2012-01-01", "2013-01-01"],
    #         ["2013-01-01", "2014-01-01"],
    #         ["2014-01-01", "2015-01-01"],
    #         ["2015-01-01", "2016-01-01"],
    #         ["2016-01-01", "2017-01-01"],
    #         ["2017-01-01", "2018-01-01"],
    #         ["2018-01-01", "2019-01-01"],
    #         ["2019-01-01", "2020-01-01"],
    #         ["2020-01-01", "2021-01-01"],
    #         ["2021-01-01", "2022-01-01"],
    #         ["2022-01-01", "2023-01-01"]
    #     ],
    #     "class": '2'
    # },
    # {
    #     "user": "guardian",
    #     "dates": [
    #         ["2009-01-01", "2010-01-01"],
    #         ["2010-01-01", "2011-01-01"],
    #         ["2011-01-01", "2012-01-01"],
    #         ["2012-01-01", "2013-01-01"],
    #         ["2013-01-01", "2014-01-01"],
    #         ["2014-01-01", "2015-01-01"],
    #         ["2015-01-01", "2016-01-01"],
    #         ["2016-01-01", "2017-01-01"],
    #         ["2017-01-01", "2018-01-01"],
    #         ["2018-01-01", "2019-01-01"],
    #         ["2019-01-01", "2020-01-01"],
    #         ["2020-01-01", "2021-01-01"],
    #         ["2021-01-01", "2022-01-01"],
    #         ["2022-01-01", "2023-01-01"]
    #     ],
    #     "class": '2'
    # },
    # {
    #     "user": "Reuters",
    #     "dates": [
    #         ["2007-01-01", "2008-01-01"],
    #         ["2008-01-01", "2009-01-01"],
    #         ["2009-01-01", "2010-01-01"],
    #         ["2010-01-01", "2011-01-01"],
    #         ["2011-01-01", "2012-01-01"],
    #         ["2012-01-01", "2013-01-01"],
    #         ["2013-01-01", "2014-01-01"],
    #         ["2014-01-01", "2015-01-01"],
    #         ["2015-01-01", "2016-01-01"],
    #         ["2016-01-01", "2017-01-01"],
    #         ["2017-01-01", "2018-01-01"],
    #         ["2018-01-01", "2019-01-01"],
    #         ["2019-01-01", "2020-01-01"],
    #         ["2020-01-01", "2021-01-01"],
    #         ["2021-01-01", "2022-01-01"],
    #         ["2022-01-01", "2023-01-01"]
    #     ],
    #     "class": '2'
    # },
    # Press FR


]


# In[ ]:


for scrape in scrape_accounts:
    for date in scrape["dates"]:
        print(f'Scraping from {date[0]} to {date[1]} for {scrape["user"]}')
        driver = init_driver(headless=False, show_images=False, env=".env")
        data = scraping(date[0], until=date[1], interval=1, from_account=scrape["user"], save_dir=f"../data/raw/{scrape['user']}", driver=driver, env=".env", headless=False, only_id=False, Class=scrape["class"])


# In[5]:



# In[ ]:



