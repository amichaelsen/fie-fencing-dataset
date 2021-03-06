# Lab Notebook

Inspired by Abhishek Gupta's [talk](https://zenodo.org/record/4737535#.YJGjZn1KhN0) on Lab Notebooks at [csv,conf,v6](https://csvconf.com/), I have decided to maintain a lab notebook as part of this project to track more detailed, unfiltered notes. The aim of this notebook is not to be a polished presentation of the final product, but a history of its development including half-baked ideas and failed experiments/implementations. Entries will be ordered reverse-chronologically, with the most recent ones appearing at the top. 

# Entries 
<!-- -------------------------------------------------------------------- -->


### 05/13/2021 

**Data Processing Pipeline**

* add a basic flowchart for process? or just image from notability drawing? Should first go through and flag public/private methods 

**Denornamlized Dataframe?** Also maybe a single bout full data frame or script that compiles all 3 data frames into a single one that contains *all* the information for each bout in its row (this is redundant but easier to process for some analyses) 


**Points for Cadet?**

* Examples of seeming missing points data for cadet events:
    * https://fie.org/athletes/28086
    * https://fie.org/athletes/36225


### 05/12/2021

**Lesson Learned:**

In converting cached data, process takes a while from url calls and may not run in one go, so have batched saves every 50 fencers to make sure progress is made even if the program gets terminated early or runs into an error 

**More data inconsistencies**

* Fencer ID: 1414 appears in https://fie.org/competitions/2015/1105 for the fencer HENNIG Bonnie but the athlete page is almost empty with the name AGUERO Es and the original Bonnie fencer does not exist in the database anymore...

**Caching HTML Requests** 

* Added code to cache the req.content to a file and load that for the tournaments always if possible and for the fencers depending on a cache flag. If no such file exists, it makes the URL request as normal and saves the content to a file. 

### 05/11/2021

**Fencer Nationality Improvement**

* Using the fie athlete search page, I was able to construct a dictionary that takes the flag code (which can be pulled from a fencers bio page) and converts to a country code and then a country name. Implementing this now saves better nationality for fencers.
* Need to figure out how to handle previously cached fencer data, obviously it could be deleted and refetched as needed... or perhaps I could write a script to find the ones that dont have nationality data (either empty of just the country code) and run a special script to fill the data??

**Dropdowns in Markdown?**

<details>
<summary> 

   `big method name` 
</summary>
<br> 

 * `Added` detail about method implementation
</details>

**Results Search Processing**
 
* steps added to the pipeline:
    * `get_results_for_division(-)` takes search parameters 
        * `get_search_params(-)` generates search params for http request
        * `get_url_list_from_seach(-)` creates list of tournament urls for processing
        * `get_dataframes_from_tournament_url_list(-)` reads URL list and gets tournament data
            * `process_tournament_data_from_urls(-)` gets tournament/bout data and fencer ID list
            * `get_fencer_dataframes_from_ID_list(-)` loads fencer info from ID list
            * `cleanup_dataframes(-)` performs pandas dataframe processing


**Error Handling?** 

* In building the pipeline, I keep running into issues where it will throw a soup error (something is being called/passed incorrectly) and then to trouble shoot I end up added print statements everywhere. Maybe try something like this for all(?) soup requests:
    ``` 
    # fencers/fencer_scraping.py
    #   -> get_fencer_bio_from_soup(soup, fencer_ID)
    try: 
        # make a soup request here
        name_tag = soup.find('h1', class_='AthleteHero-fencerName')
        fencer_name = name_tag.get_text()
    except:
        # print current state for debugging
        print("Failed to read name from name_tag for fencer: {}".format(fencer_ID))

    ```

**Missing Fencer IDs!?** 

* For at least one tournament (ex https://fie.org/competitions/2016/941) all fencers have 'id' 0 which will not load an athlete bio page. Also makes it hard to keep track of them. Upon inspection, these athletes likely *do* have IDs and pages, they just weren't stored with this event for some reason. 
    * Can maybe use https://fie.org/athletes to search for them by name in the atheletes index? 
    * Can also use this page to get a dict for translating nationalities... 
    * ACTUALLY, this has hand info... maybe use this instead? well, maybe, but doesnt have historical rankings data... so probably a hybrid of the two, but could use this one first to find the IDs? 
    * Ah! Could also maybe extract a dict for converting flag to nationality ... 

* Some (older?) tournaments have different formats/data 
    * Example: no pools data (https://fie.org/competitions/1999/239)
    * Example: no details, only overview (https://fie.org/competitions/2004/377, https://fie.org/competitions/2020/767)
    * Example: Pools data but fencer id is always 0  (https://fie.org/competitions/2016/941)
* For now:
    * If no pools data, skip tournament by passing NoneType for TournamentData
    * If 0 in fencer ID list (probably means list - [0]) then skip tournament by passing NoneType for TournamentData

* Also seems like there may be some inconsistencies with points data? Specifically, https://fie.org/athletes/36225 has a ranking of 1 for 2014/2015 but with 0 points. Hard to verify because the athlete search page only searches by senior and junior... May only be an issue for cadet, make not in final doc that cadet points data seems unreliable 

### 05/10/2021

**Multi-Weapon Fencer Data**

* Implemented a method for pulling rankings/points for each weapon when reading a fencer's data. 
* Couldn't figure out a way to tell what the "default" weapon is that loads with the fencer url (no '?weapon=') tag 

**Code Cleanup** 

* Pulled out some helper functions.
* Still need to convert df.append loops to list creation loops and then convert to df at the end 

**Making HTTPS Web Requests to FIE.org** 

* figuring out how to get the tournament results list by search
* Explore the Google "Networks" tab and a 'search' request that appears when changing the check boxes in the search bar. From there, pull the url, POST, and search params dict to pass as `data` to the python `requests` call. 
* See `initial_testing/results.html` for example of results page on fie 
* See `initial_testing/request_reponse/json` for a sample POST response 
* Note: need all the fields even if most are blank! 
* Note: to get all seasons instead of leaving "season" blank ("") need to pass "-1" (this can be seen when viewing the search params on an FIE search http request.)



### 05/07/2021

**Fencer Ranking/Points by Weapon** 

* Assume that handedness does not change by weapon -> store in the fencer bio dataframe 
* on a page, there is a drop down menu for weapon 
    ```
    <select class="ProfileInfo-weaponDropdown js-athlete-dropdown-weapon" name="weapon">
        <option value="F">foil</option>
        <option value="S" selected>sabre</option>
    </select>
    ```
    and for each "option value", need to make a url call to "../athletes/ID?weapon={}" where {}=F,E,S for each weapon option. 

    Note: if a fencer has only one weapon, making this URL call is not a problem but creates redundant calls so should be avoided. 

### 05/06/2021

**Fencer Data Pages** 

* Nationality by itself is not stored on the fencer's page, only the tag for the flag. Should probably pull nationality out from competition then... Note, found many fencers have a "window._tabOpponent" in which their own fencer data (like in tournament pages) was listed and could pull nationality from there but for fencers with so few results, this fails from an empty list... have created logic in the get_fencer_data_from_ID to  leave nationality empty in this case 

* Some fencers have multiple weapons (not many), right now this saves their weapon as 'sabrefoil' for example, however accessing their ranking/points for their non-dominant weapon doesn't even seem possible on the FIE website (see https://fie.org/athletes/34656?weapon=F)

**GAHHHH Inconsistent Pool "Time"** 

* Some pools have 'time' as a date string, others as an actual time string. To get around this, will use the "start_date" of tournament as the date for the bout 
* Also pandas can store as a Datetime and must include "time" (00:00:00 in our case) or can convert to date only `['date'].dt.date` but this reverts to `object` type. Since sorting by date may be useful, I will leave these in datetime for now. Since it is easy to convert between them this may change later.

**Fixing Imports Notes** 

* Do the following in terminal to make sure that paths work: 
    ```
    echo $PYTHONPATH
    vim ~/.bash_profile
    ```
    Insert the following into ~/.bash_profile
    ```     
    export PYTHONPATH="$PYTHONPATH:/path/to/directory/fie-fencing-dataset"    
    ``` 
    Save `./bash_profile` and restart Terminal 
    ```
    echo $PYTHONPATH
    ```
    should now return a strong containing `/path/to/directory/fie-fencing-dataset`



**Single Data Generation vs Iterable** 

* iterable allows adding new events without rerunning old data (reduces computation time and redundancy) 

* iterable introduces complications in storing fencer "overall" data since newer lookups will have different overall rankings/points than previously called fencers... 
    * basically iteration is fine for old pools and tournament data but creates inconsistencies in the fencer data frame --> maybe allow iteration but re-run the fencer data frame every time new data is added? 
    * if iterating, maybe have option to pass dataframes (if none, create fresh) and for each tournament check if the tournament is already in the data frame and if so skip it. so everytime reset fencers data to a dict or whatever internal structure I'm using (adding known fencers from pools) and then adding as events are processed and then always performing the lookup at the end? 
        * case: performing "new" lookup but no new events, should we still refresh fencer rankings/points? they should not have changed... ah but age could change for example and that may be interesting... ah maybe age at event time is important too and should be stored with the tournament/bout data... so actually unless points expire (which they might but does that affect the collected data?) it may not be necessary to refresh the fencer dataframe (is there value to having it be 'up to date' though? )

* updating the fencer dataframe is costly becuase it involves many requests calls, so thats another argument for not refreshing, but then definitely need to keep track of *when* that fencers data was pulled, which might be reason enough to refresh it every time 

**Fencer Ranking/Points**

* flexible value that changes over time, probably want to store fencer rankings with each bout... 
* for unrated fencers the order is randomized (see FIE Rules in `initial_testing/README.me`) so measuring "upsets" by event ranking is not significant but could be interesting when at least one fencer has points. 

**Tournament 'IDs'** 

* has 2 IDs specified and neither is unique (across seasons) ... [verified using Grand Prix results for 2020 and 2017, both have same id and compId but different season ] 
* storing IDs as ints/str? especially if int will be year-id (e.g. 2020-771) where 2020771 doesn't obviously communicate the use of the date in the ID 
* loads "fake" competition if season-id combo does not exists


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
