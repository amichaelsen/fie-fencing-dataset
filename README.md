# Project Overview

The goal of this project is to generate a dataset of fencing matches pulled from the International Fencing Federation (FIE) [website](fie.org).

## Data Source(s)

The International Fencing Federation (FIE) is recognized by the International Olympic Committee (IOC) as the world governing body of fencing, as such is charged with establishing the rules and implementation for international competition. 

While the FIE is not the only fencing results page (see [AskFRED](askfred.net) or [USFA](https://www.usafencing.org/natresults)), it has several advantages to other sources considered. To read more about the source comparisons, check out the 'Data Source(s)' section of [`docs/Data.md`](https://github.com/amichaelsen/fie-fencing-dataset/blob/main/docs/Data.md) 


The FIE website maintains a list of competition results and fencer bios. The following pages were used to collect data: 

* **[Results Search](https://fie.org/competitions)** 
* **[Tournament Pages](https://fie.org/competitions/2021/1073)** 
* **[Athlete Bio Pages](https://fie.org/athletes/16779)** 
   
## Output Data

The output data, stored in `final_output/`, contains the following dataframes for each division collected (e.g. Women's Foil), each in their own CSV file within a division directory: 

### `Tournament Dataframe` (\*\_tournament_data\_\*.csv)
List of tournaments in the division listed on the FIE competition results page. 

| variable | type | description |
|:-------  |:---: | :-------|
|competition_ID| int| FIE competition ID| 
|season | int | start year of competition season|
|name | string | Name of tournament | 
|category | string | age category for event (Cadet/Junior/Senior/Veterans)|
| country | string | host country for tournament| 
| start_date | date | first day of event | 
| end_date | date | last day of event | 
| weapon | string | foil/epee/saber  |
|gender | string | event gender (Mens/Womens)| 
|timezone| string | timezone where the event took place|
|url | string | FIE url for event page|
|missing_results_flag | string | specifies missing (pools) results|

Sample of Dataframe (not all columns shown):

|    |   season | name                   | category   | country       | start_date   | weapon   | gender   | competition+ID   |
|---:|---------:|:-----------------------|:-----------|:--------------|:-------------|:---------|:---------|:------------|
|  0 |     2015 | Memorial de Martinengo | Junior     | SLOVAKIA      | 2014-11-21   | Foil     | Womens   | 37     |
|  1 |     2004 | Trophée Federico II    | Junior     | ITALY         | 2003-11-29   | Foil     | Womens   | 36     |
| 2 |     2011 | Coupe du Monde         | Junior     | SERBIA        | 2011-03-06   | Foil     | Womens   | 35     |
<!-- |  3 |     2007 | Tournoi Carl Schwende  | Junior     | CANADA        | 2007-01-20   | Foil     | Womens   | 40     |
|  4 |     2006 | Cole Cup               | Senior     | GREAT BRITAIN | 2006-06-17   | Foil     | Womens   | 555    | -->

### `Bout Dataframe`  (\*\_bout_data\_\*.csv)
List of bouts from pools across all tournaments stored in the Tournament Dataframe.

| variable | type | description |
|:-------  |:---: | :-------|
|fencer_id | int | ID of of fencer in the bout |
|opp_ID    | int | ID of the opponent in the bout| 
|fencer_age| int | age of fencer at the time of the event|
|opp_age   | int | age of opponent at the time of the event|
| fencer_score| int | points scored in bout for fencer| 
| opp_score| int | points scored in bout for opponent | 
| winner_ID| int | ID matching the fencer who won |
|fencer_curr_pts | double | fencer's points in the division at the start of the event | 
|opp_curr_pts    | double |opponents's points in the division at the start of the event  | 
|tournament_ID   |string| tournament the pool occured in |
|upset |boolean | True if fencer with fewer points won|
|date |date | date of the pool | 

Bouts are not double count, so `fencer_ID` corresponds to the fencer with the lower number in the pools table ordering. If both fencers have no points, then `upset` is `False`. `winner_ID` is included in the case of ties, where the scores will match. 


Sample of Dataframe (not all columns shown):

|    |   fencer_ID |   opp_ID |   fencer_age |   fencer_score |   opp_score |   winner_ID |   fencer_curr_pts | tournament_ID   |   pool_ID | upset   | date       |
|---:|------------:|---------:|-------------:|---------------:|------------:|------------:|------------------:|:----------------|----------:|:--------|:-----------|
|  0 |       29240 |    27947 |           24 |              2 |           5 |       27947 |                 0 | 2015-37         |         1 | False   | 2014-11-21 |
|  1 |       29240 |    35149 |           24 |              5 |           3 |       29240 |                 0 | 2015-37         |         1 | False   | 2014-11-21 |
|  2 |       29240 |    28025 |           24 |              0 |           5 |       28025 |                 0 | 2015-37         |         1 | False   | 2014-11-21 |
<!--|  3 |       29240 |    23626 |           24 |              1 |           5 |       23626 |                 0 | 2015-37         |         1 | False   | 2014-11-21 |
|  4 |       29240 |    33989 |           24 |              5 |           4 |       29240 |                 0 | 2015-37         |         1 | True    | 2014-11-21 |-->
    
### `Fencer Bio Dataframe`  (\*\_fencer_bio_data\_\*.csv)
Biographical information about each fencer stored by ID. 
| variable | type | description |
|:-------  |:---: | :-------|
|id |int| FIE ID number for fencer|
| name  |string| Fencer's full name|
| country  |string| Fencer's country (when data was accessed)|
|  hand |string|whether the fencer is left or right handed|
| age  |int| Fencer's age (when data was accessed)|
| date_accessed  |datetime| Date and time when data was accessed |

Sample of Dataframe:

|    |    id | name                | country   | hand   |   age | date_accessed       |
|---:|------:|:--------------------|:----------|:-------|------:|:--------------------|
|  0 | 20482 | YANAOKA Haruka      | JAPAN     | Right  |    26 | 2021-05-11 18:15:32 |
|  1 | 28701 | CIPRESSA Erica      | ITALY     | Right  |    24 | 2021-05-11 18:15:44 |
|  2 | 33865 | TANGHERLINI Elena   | ITALY     | Left   |    23 | 2021-05-11 18:16:12 |
<!--|  3 | 30818 | BIANCHIN Elisabetta | ITALY     | Right  |    24 | 2021-05-11 12:05:47 |
|  4 | 36458 | POSGAY Zsofia       | GERMANY   | Left   |    22 | 2021-05-11 12:05:52 |-->
        

### `Fencer Rankings Dataframe`  (\*\_fencer_rankings_data\_\*.csv)
Historical data about the fencers rankings/points in each division (weapon/age category). 

| variable | type | description |
|:-------  |:---: | :-------|
|id|int|Fencer's FIE ID|
|weapon|string|foil/epee/saber |
|category|string|Age category of ranking (Cadet/Junior/Senior/Veterans)|
|season|string| season for ranking in format YYYY/YYYY|
|rank|int|ranking within division (weapon and category) for the given season|
|points|double| points earned in the division (weapon and category) for the given season |


Sample of Dataframe (rendered with MultiIndex):

|    id | weapon   | category   | season    |   rank |   points |
|------:|:---------|:-----------|:----------|-------:|---------:|
| 32192 | Foil     | Junior     | 2013/2014 |    20|        2 |
|  |      |      | 2014/2015 |    180 |        4 |
|  |      |      | 2015/2016 |    296 |        0 |
|  |      |      | 2016/2017 |    226 |        4 |
|  |      |      | 2017/2018 |     73 |       22 |
|  |      | Senior     | 2016/2017 |    433 |        0 |
|  |      |      | 2018/2019 |    312 |        0 |
        

## Generating & Loading New Data

To generate new division data, use the following steps: 

1. Fork this repo to obtain a local copy 
2. Edit the following lines in `main.py` to specify the division parameters:
    ```
    #f=foil, #e=epee, s=sabre
    weapon = 'f' 
    # f=womens, m=mens
    gender = 'f'
    # c=cadet, j=junior, 
    # s=senior, v=veteran
    category = ''
    ```
3. Add the path to `fie-fencing-dataset` to $PYTHONPATH (instructions below from [here](https://stackoverflow.com/questions/3402168/permanently-add-a-directory-to-pythonpath))
    * Open up Terminal
    * Type `open .bash_profile`
    * In the text file that pops up, add this line at the end: 
    `export PYTHONPATH=$PYTHONPATH: [path goes here].../fie-fencing-dataset`
    * Save the file, restart the Terminal
    * Type `echo $PYTHONPATH` and check that the path to `fie-fencing-dataset` is there.
4. From the terminal run `main.py` using python
    ```
    ...$ python3 main.py 
    ```
5. The script will save the four dataframes into four CSV files. These files will be saved in a subdirectory of `output` with the date the script was run (e.g. `output/May-13-2021/`). 

6. To load and work with the dataframes you have created, run the following command in python or an interactive notebook like Jupyter:
    ```
    from load_csv import tournament_df, bout_df, fencer_bio_df, fencer_rankings_df
    ```

# Directory Structure

## Main Directories/Files: 

### Files to Create/Load Data: 

* main
* load_csv 

### Directories:

* /docs 
    <!-- * Data
    * ExternalLinks
    * LabNotebook -->
* /fencers
    <!-- * fencer_scraping
    * generate_flag_dict -->
* /pools 
    <!-- * pool_data
    * pool_scrapings -->
* /tournaments
    <!-- * tournament_data
    * tournamnet_scraping -->
* /final_output
    <!-- * all_mens_foil
    * all_womens_foil  -->
* /helper
    <!-- * get_results
    * caching_methods
    * dataframe_columns
    * soup_scraping -->

## Other Directories/Files: 

### Files:

* demo 

### Directories: 

* initial_testing
* output 

# Other 

Webpage processing used pythons [`requests`](https://docs.python-requests.org/en/latest/user/quickstart/) package and the [`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) package. 

