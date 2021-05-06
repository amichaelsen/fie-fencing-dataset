# Lab Notebook

Inspired by Abhishek Gupta's [talk](https://zenodo.org/record/4737535#.YJGjZn1KhN0) on Lab Notebooks at [csv,conf,v6](https://csvconf.com/), I have decided to maintain a lab notebook as part of this project to track more detailed, unfiltered notes. The aim of this notebook is not to be a polished presentation of the final product, but a history of its development including half-baked ideas and failed experiments/implementations. Entries will be ordered reverse-chronologically, with the most recent ones appearing at the top. 

# Entries 

### 05/05/2021 

**JSON vs HTML Parsing**

Having built a method that takes the full HTML representation of a pool and extracts the data, I then started exploring making https requests to systematically get the desired HTML to feed into this method. It was then that I realized that the source code for the tournament page is *not* the fully compiled HTML but gets compiled from Javascript. This meant that the pools data was stored in a JSON object rather than  HTML. So I scrapped my html version (well it still exists because it may be useful for future me figuring out HTML parsing) and created a new pool scraping method that now takes the dictionary extracted from the JSON. 

Given the nested set up for the pools dictionary, I created a generator (`extract_matches`) to iterate over the squares in the pools grid. 


**File Structure/Types**

Given the time I spent exploring the tournament page structure using requests and BeautifulSoup and the lessons learned there that didn't make it into the final implementation I wanted to save that code and its comments somewhere for potential future reading. However not wanting to clutter up the working files, I have decided to use `exploring_[topic].py` files to keep track of this work. This pairs nicely with the `testing_[module].py` files which I use to import and run the code in each module. 

**Data Scoping**

In thinking about representation and overall goals for this dataset, I realized that to date I have only been handling "womens foil" for personal familiarity/nostalgia reasons. Once I have the machinery in place to scrape all the pool data for all currently listed women's foil (individual) events I will work to expand this to handle other weapons (epee/saber) and genders (men's). 

I also realized that in comparing fencer's performance some demographic data on the fencers themselves will be useful and should be included for completeness's sake. From the pool data I can easily extract their nationality, name, and ID. From the ID I can find the athlete webpage (e.g. https://fie.org/athletes/42286) which contains further information such as handedness and age along with historical results and over rank and points which can be used as a proxy for general skill level. Not included (for privacy or because such data could change) are height and weight which could have been interesting statistics (particularly height) to examine. 

**Tournament page scraping Update** 

Now that the code has been updated to handle JSON parsing the updates are as follows: 

* **`pool_scraping.py`** (updated) contains a method `get_pool_data_from_dict` which takes a dictionary representation of a pool and returns a list of fencers, represented by dicts, and  a `poolData` class object with the data of the pool. It also contains the old method `get_pool_data_from_html` which takes a string with the file location for the html of a single pool and returns a `poolData` class object with the data of the pool 
* **`testing_pool_scraping.py`** (updated) tests both `pool_data.py` and both methods from `pool_scraping.py` by making several calls to each and printing the results. 
*  **`exploring_json_extraction.py`** (new) contains the exploratory code for navigating the HTML of a tournament website with the goal of extracting the list of dicts for pool results. 
* **`tournament_scraping.py`** (new) has a single method `get_pool_list_from_url` which takes a string of the tournament url (e.g. 'https://fie.org/competitions/2020/771') and returns a list of pools, each represented by a dict that can be fed in `get_pool_data_from_dict`. 
* **`testing_tournament_scraping.py`** (new) tests the process of pulling the pools from a url and parsing them into pool data and a fencer list. 


### 05/04/2021

**Pipeline planning**

Ultimately, I would like to scope the data to be gathered (e.g. "womens foil", only individual data for now), create a script to make the https requests to pull a list of relevant tournament results, parse that into link for the specific results pages, call those pages and store the resulting html to be parsed. Parsing a tournament result page will involve first finding and splitting out each pool, processing the pool data, and then recompiling all the bout information along with tournament data (location, date, tournament id/link). 

**Data Format Ideas**

Pools are currently being stored as 2 lists (fencer names and IDs) and two arrays (winners and scores). My current plan for the end goal is to store all bouts in a single dataframe with the following information for each row: 
* fencer1 name, fencer2 name (alphabetically stored?)
* fencer1 ID, fencer 2 ID
* score for each
* winner
* tournament id/link
* pool number 
* tournament location 
* date 

I initially considered storing each bout twice once from each "perspective" but this results in more complex queries to put the data together or storing duplicate data. One consideration will be to make sure the two fencers do not get mixed, for example if "winner" column was an indicator of victory then I would want to label the fencers in uneven naming (eg "fencer" and "opponent") to make clear who the indicator applied to. 

I am still considering whether to store fencer names in the dataframe or to split out into a separate lookup dataframe with names and IDs. 

**Pools Scraping Update**

The first goal of the project was to create a method that could take as input the html for a single pool and read out from it the fencers names and IDs and array representation(s) of the scores. The pool summary statistics (which are used for rankings going into DEs) will be ignored. 

So far, the following files are complete and functional: 
* `pool_data.py` contains a dataclass class for storing pool information which includes the attributes: `pool_size`, `fencer_names`, `fencer_IDs`, `winners`, and `scores`. 
* `pool_scraping.py` contains a method `get_pool_data` which takes a string with the file location for the html of a single pool and returns a `poolData` class object with the data of the pool
* `testing_pool_scraping.py` tests both `pool_data.py` and `pool_scraping.py` by making several calls to each and printing the results. 


### 05/03/2021

**What is the 'why'?** 

Fencing is a beautiful sport, often called "physical chess" for its combination of atheleticism and mental analysis. As a former fencer, I have both a love for and understanding of the sport. Given its lack of prominence in mainstream sports attention, fencing is a ripe area for study in almost any field. Furthermore, it is an individual closed sport, wherein opponents compete directly with each other, rather than against a clock. This increases the complexity in predicting competition performance by introducing the many variables of the opponent in addition to parameters of the fencer themselves. 

**Data sources** 

The two main data sources I considered were the FIE [results page](https://fie.org/competitions), which records international fencing tournaments, and AskFRED.net, which records local and regional tournaments in the US. The former provides more consistency in its data as well as more persistence in the athlete pool however the latter has altogether more data as well as mixed gender events which opens other avenues for analysis. Given the consistency benefits, I chose to follow the FIE route for now but hope in the future to explore the AskFRED data (some helpful resources for that are [here](https://sites.google.com/a/countersix.com/fred-rest-api/)). 

**Pools vs DEs Data** 

In pools, a group of 5 to 7 fencers will all fence each other for a short time (3 min) to a low score (5 points) as compared to Direct Elimination (DE) where they fence in an elimination tableau for longer (3 x 3 min) and to a higher score (15 points). In pools a fencer is guaranteed to fence 4-6 people, whereas a fencer who loses their first DE bout will only fence 1 DE bout for that competition. Thus pools data provides the most consistent bouts per person and most data points for comparison between fencers, thus generating a rich dataset for analyzing fencers comparable performance. Since fencer's strategies can differ dramatically between pools and DEs it should be noted that comclusion made from pools data are unlikely to be applicable to DEs. 
