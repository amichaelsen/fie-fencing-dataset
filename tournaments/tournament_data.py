from dataclasses import dataclass
from pools.pool_data import poolData
import numpy as np


@dataclass
class tournamentData:
    '''
    A dataclass to represent data from a single tournament

    Attributes:
    -----------
    
    '''
    unique_ID : str # this will be season-competition_id, e.g. "2020-771"
    season : int
    competition_id : int
    weapon : str # make this an enum eventually 
    gender : str # make this an enum eventually 
    category : str # make this an enum eventually 
    level : str  # make this an enum eventually 
    start_date : str
    end_date : str
    name : str 
    country : str
    timezone : str  # make this an enum eventually ??
    url : str 

    pools_list : list[poolData]
    fencers_dict : dict

    def __str__(self):
        str_rep = "\nTournament Information:\n"
        str_rep +=   "-----------------------\n"
        str_rep += "   Name:  {:<25} (unique ID {:<10})\n".format(self.name, self.unique_ID)
        str_rep += "   Season:  {:<10}  Competition ID:  {:<5}\n".format(self.season, self.competition_id)
        str_rep += "   Weapon:  {:<10}  Gender:          {:<5}\n".format(self.weapon, self.gender)
        str_rep += "   Country: {:<10}  TimeZone:        {:<5}\n".format(self.country, self.timezone)
        str_rep += "   Start:   {:<10}  End:             {:<5}\n".format(self.start_date, self.end_date)
        str_rep += "   Website:   {} \n\n\n".format(self.url)


        str_rep += "Total Number of Fencers: {}\n".format(len(self.fencers_dict.keys()))
        str_rep += "Total Number of Pools: {}".format(len(self.pools_list))

        str_rep += "\n\nPool Results:\n"
        str_rep +=     "---------------\n\n"
        for pool in self.pools_list:
            str_rep += pool.__str__()

        return str_rep
    