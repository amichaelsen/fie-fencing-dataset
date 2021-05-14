# Project Overview

The goal of this project is to generate a dataset of fencing matches pulled from the International Fencing Federation (FIE) [website](fie.org).

## Data Source(s)

The International Fencing Federation (FIE) is recognized by the International Olympic Committee (IOC) as the world governing body of fencing, as such is charged with establishing the rules and implementation for international competition. 

While the FIE is not the only fencing results page (see [AskFRED](askfred.net) or [USFA](https://www.usafencing.org/natresults)), it has several advantages to other sources considered. To read more about the source comparisons, check out the 'Data Source(s)' section of [`Docs/Data.md`](https://github.com/amichaelsen/fie-fencing-dataset/blob/main/Docs/Data.md) 


The FIE website maintains a list of competition results and fencer bios. The following pages were used to collect data: 

* **[Results Search](https://fie.org/competitions)** 
* **[Tournament Pages](https://fie.org/competitions/2021/1073)** 
* **[Athlete Bio Pages](https://fie.org/athletes/16779)** 
   
## Output Data

The output data, stored in `final_output/`, contains the following dataframes for each division collected (e.g. Women's Foil), each in their own CSV file within a division directory: 

* `Tournament Dataframe`
    * List of tournaments in the division listed on the FIE competition results page. Below is an example of a subset of the dataframe:


        |    |   season | name                   | category   | country       | start_date   | weapon   | gender   | unique_ID   |
        |---:|---------:|:-----------------------|:-----------|:--------------|:-------------|:---------|:---------|:------------|
        |  0 |     2015 | Memorial de Martinengo | Junior     | SLOVAKIA      | 2014-11-21   | Foil     | Womens   | 2015-37     |
        |  1 |     2004 | Trophée Federico II    | Junior     | ITALY         | 2003-11-29   | Foil     | Womens   | 2004-36     |
        |  2 |     2011 | Coupe du Monde         | Junior     | SERBIA        | 2011-03-06   | Foil     | Womens   | 2011-35     |
        |  3 |     2007 | Tournoi Carl Schwende  | Junior     | CANADA        | 2007-01-20   | Foil     | Womens   | 2007-40     |
        |  4 |     2006 | Cole Cup               | Senior     | GREAT BRITAIN | 2006-06-17   | Foil     | Womens   | 2006-555    |

* `Bout Dataframe` 
    * List of bouts from pools across all tournaments stored in the Tournament Dataframe. 

        |    |   fencer_ID |   opp_ID |   fencer_age |   fencer_score |   opp_score |   winner_ID |   fencer_curr_pts | tournament_ID   |   pool_ID | upset   | date       |
        |---:|------------:|---------:|-------------:|---------------:|------------:|------------:|------------------:|:----------------|----------:|:--------|:-----------|
        |  0 |       29240 |    27947 |           24 |              2 |           5 |       27947 |                 0 | 2015-37         |         1 | False   | 2014-11-21 |
        |  1 |       29240 |    35149 |           24 |              5 |           3 |       29240 |                 0 | 2015-37         |         1 | False   | 2014-11-21 |
        |  2 |       29240 |    28025 |           24 |              0 |           5 |       28025 |                 0 | 2015-37         |         1 | False   | 2014-11-21 |
        |  3 |       29240 |    23626 |           24 |              1 |           5 |       23626 |                 0 | 2015-37         |         1 | False   | 2014-11-21 |
        |  4 |       29240 |    33989 |           24 |              5 |           4 |       29240 |                 0 | 2015-37         |         1 | True    | 2014-11-21 |
    
* `Fencer Bio Dataframe`
    * Biographical information about each fencer stored by ID. 

        |    |    id | name                | country   | hand   |   age | date_accessed       |
        |---:|------:|:--------------------|:----------|:-------|------:|:--------------------|
        |  0 | 20482 | YANAOKA Haruka      | JAPAN     | Right  |    26 | 2021-05-11 18:15:32 |
        |  1 | 28701 | CIPRESSA Erica      | ITALY     | Right  |    24 | 2021-05-11 18:15:44 |
        |  2 | 33865 | TANGHERLINI Elena   | ITALY     | Left   |    23 | 2021-05-11 18:16:12 |
        |  3 | 30818 | BIANCHIN Elisabetta | ITALY     | Right  |    24 | 2021-05-11 12:05:47 |
        |  4 | 36458 | POSGAY Zsofia       | GERMANY   | Left   |    22 | 2021-05-11 12:05:52 |
        

* `Fencer Rankings Dataframe`
    * Historical data about the fencers rankings/points in each division (weapon/age category). 

        |    id | weapon   | category   | season    |   rank |   points |
        |------:|:---------|:-----------|:----------|-------:|---------:|
        | 32192 | Foil     | Junior     | 2013/2014 |    201 |        2 |
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

