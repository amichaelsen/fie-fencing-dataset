# Project Overview

The goal of this project is to generate a dataset of fencing matches pulled from the International Fencing Federation (FIE) [website](fie.org).

## Data Source(s)

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

* tournament dataframe 

* bout dataframe 

* fencer dataframe

 -> all exported into CSVs with date pulled in the filename 

**Denornamlized Dataframe?** Also maybe a single bout full data frame or script that compiles all 3 data frames into a single one that contains *all* the information for each bout in its row (this is redundant but easier to process for some analyses) 


# Directory Structure

Webpage processing used pythons [`requests`](https://docs.python-requests.org/en/latest/user/quickstart/) package and the [`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) package. 