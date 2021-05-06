from dataclasses import dataclass
import numpy as np


@dataclass
class poolData:
    '''
    A dataclass to represent data from a single pool

    Attributes:
    -----------
    pool_size : int
        number of fencers in the pool
    fencer_names : list[str]
        (ordered) list of a names of fencers in the pool
    fencer_IDs : list[int]
        (ordered) list of fencer IDs on the FIE website
    winners : np.ndarray
        np binary array with 1's indicating bout winners
    scores : np.ndarray
        np array of scores representing the pool table 
    '''
    pool_ID: int
    pool_size: int
    fencer_names: list[str]
    fencer_IDs: list[int]
    winners: np.ndarray
    scores: np.ndarray
    date: str # come back an change to date 


    def __str__(self):
        str_rep = ""
        str_rep += "Pool #{:<3}                           |".format(self.pool_ID)
        for i in range(1, self.pool_size+1):
            str_rep += " # {} |".format(i)
        #change to be variable length based on pool size
        str_rep += "\n-------------------------------------"
        str_rep += "------"*self.pool_size
        str_rep += "\n"

        for idx, name in enumerate(self.fencer_names):
            # center the ID value in the parens? 
            str_rep += "#{i} {name:<20s} (ID {id: <5})  |".format(
                i=idx+1, name=name[0:19], id=self.fencer_IDs[idx])
            for j in range(0, self.pool_size):
                if(j == idx):
                    str_rep += " --- |"
                else:
                    victory_indicator = "V" if self.winners[idx][j] == 1 else "D"
                    str_rep += " {vw}/{sc} |".format(vw=victory_indicator,
                        sc=self.scores[idx][j])
            str_rep += "\n"
        str_rep += "\n"
        return str_rep
    
    def get_fencer_name_by_idx(self, idx):
        return self.fencer_names[idx]
    
    def get_fencer_ID_by_idx(self, idx):
        return self.fencer_IDs[idx]
