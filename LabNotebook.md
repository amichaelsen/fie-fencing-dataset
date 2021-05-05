# Lab Notebook

Inspired by Abhishek Gupta's [talk](https://zenodo.org/record/4737535#.YJGjZn1KhN0) on Lab Notebooks at [csv,conf,v6](https://csvconf.com/), I have decided to maintain a lab notebook as part of this project to track more detailed, unfiltered notes. The aim of this notebook is not to be a polished presentation of the final product, but a history of its development including half-baked ideas and failed experiments/implementations. Entries will be ordered reverse-chronologically, with the most recent ones appearing at the top. 

# Entries 

### 05/05/2021 

**File Structure/Types**

* Spending time exploring BeautifulSoup and maybe save "exploring_..." files to show that process to help myself retrace my steps or adapt them later to other goals 

**JSON vs HTML Parsing**

 * existing script for HTML pools but tournament page data contains JSON (not direct HTML) for the pools data so need to recontruct processing to handle json objects 

**Data Scoping**
* (for now) arbitrary (personal familiarity) focus on Womens Foil.
* what data to include about the fencers themselves? goal to compare collab filter "features" with known features like height, weight, handedness, country?, etc  

**Tournament page scraping Update** 

* add description of current status once done parsing JSON ...

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
