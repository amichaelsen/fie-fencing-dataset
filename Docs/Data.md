# Data Descriptions 

This file contains more detailed descriptions of the data sources and output data for this project. 

## Data Source(s)
--- 

The International Fencing Federation (FIE) is recognized by the International Olympic Committee (IOC) as the world governing body of fencing, as such is charged with establishing the rules and implementation for international competition. 

While the FIE is not the only fencing results page (see [AskFRED](askfred.net)), it has the following advantages for this dataset: 
* *More Consistent Athlete List* - Since the FIE results represent only international competitions, as opposed to local/regional/national events, there is more continuity in the athlete community over the season(s). 
* *More Athlete Info* - Given the expexted athlete consistency, FIE maintains athelete bios which provides information about nationality, age, and handedness. 

However there were a couple of challenges with using this data source as well: 
* *No API/Data Conventions* - Unlike AskFRED, which has a [documented API](https://askfred.net/Info/webservices.php) for data access the FIE does not provide an API and data formating can be inconsistent across the website. Some data inconstency examples include: 
    * time formats for pools sometimes stored as either a date or a time.
    * fencer nationality itself is not stored on a fencer bio, only a tag for the internal flag code. 
    * competitions are stored with an `id` and a `competitionId` neither of which is unique across all seasons (neither is their combination) and only `competitionId` seems to be used 

* *Fewer Events* - Compared to AskFRED, which host most local and regional events in United States, the FIE tracks fewer competitions, and therefore fewer bouts. From Jan 1, 2021 to May 1, 2021, the FIE had only 11 tournaments, while AskFRED reports 347 tournaments (on both pages, a tournament may represent multiple divisions/events). 

* *No Mixed Events* - At the international level, all fencing events are a single gender (mens/womens) whereas in the US local/regional events typically have an 'open' category that is mixed gender. Data pulled from the FIE then will not contain any mixed gender bouts. 

The FIE website also maintains a list of competition results and fencer bios. The following pages were used to collect data: 

* **Results Search** 
    * Link: https://fie.org/competitions
    * search page for completed tournaments, used to extract urls for tournament pages 
* **Tournament Pages** 
    * Example link: https://fie.org/competitions/2021/1073
    * Contains results for a single event. Used to find pools results (under Results>Pools) as well as athelte info at the time (points & age) (under Athletes)
* **Athlete Bio Pages** 
    * Example link: https://fie.org/athletes/16779
    * Contains current athlete data like rank/points per division (division is determined by weapon, gender, and category/age group). Also indicates a fencer's handedness (left/right())


## Output Data
---

The output data, stored in `final_output/`, contains the following dataframes for each division collected (e.g. Women's Foil), each in their own CSV file within a division directory: 

* `Tournament Dataframe`
    * **Description**: Contains a list of tournaments in the division listed on the FIE competition results page. This contains information about the event itself, with the columns described below.
    * **Columns**: 
    ['competition_ID', 'season', 'name', 'category', 'country', 'start_date', 'end_date', 'weapon', 'gender', 'timezone', 'url', 'unique_ID','missing_results_flag']
        * `competition_ID` - the FIE competition_ID (used in the competition URL). *NOT* a unique identifier across seasons. 
        * `season` - the year in which the competition took place.
        * `unique_ID` - constructed from year and competition_ID to create a unique identifier for each event (matches ending of url).
        * `category` - the age division for the event, either 'cadet', 'junior', 'senior' or 'veteran'.
        * `missing_results_flag` - Bout results are inconsistently stored on the FIE website and many tournament pages do not have pools data. This flag indicates whether pools data was ommitted and why.

* `Bout Dataframe` 
    * **Description**: Contains a list of bouts from pools across all tournaments stored in the Tournament Dataframe. 
    * **Columns**: ['fencer_ID', 'opp_ID', 'fencer_age', 'opp_age', 'fencer_score', 'opp_score', 'winner_ID', 'fencer_curr_pts', 'opp_curr_pts', 'tournament_ID', 'pool_ID', 'upset', 'date']
        * `fencer`/`opp` - several data fields are stored for both fencers with the first in pool stored as `fencer_` and the latter stored as `opp_` (opponent).
        * `_ID` - the IDs for the two fencers in a match, used for lookups in the fencer data frames.
        * `_age`, `_curr_pts`- data about both fencers *at the time of the tournament*.
        * `winner_ID` - the ID for the fencer who won (needed in case of victories in overtime).
        * `upset` - indicates if the winner was an 'upset', if neither fencer has points this is `False`.

* `Fencer Bio Dataframe`
    * **Description**: Contains biographical information about each fencer stored by ID. 
    * **Columns**: ['id', 'name', 'country_code', 'country', 'hand', 'age', 'url', 'date_accessed']
        * `country_code`/`country` - The 3 letter code and full name of fencer's country
        * `Hand` - Fencer's handedness
        * `url` - webpage for the fencer
        * `date_accessed` - date when the fencer's data was pulled, since fields may change over time 

* `Fencer Rankings Dataframe`
    * **Description**: Contains historical data about the fencers rankings/points in each division (weapon/age category). The first 3 columns of the CSV file can be converted to a multiIndex as seen in `load_csv.py`
    * **Columns**: MultiIndex ['id', 'weapon', 'category', 'season'], Columns ['rank', 'points']
        * `id` - fencer's ID
        * `season` - the season in which the ranking/points were earned (e.g. 2014/2015)
        * `points` - points earned from competitions in this division (see FIE for more information about points)
        * `rank` - fencer's overall rank in the division (e.g. senior womens foil) based on points

