from dataclasses import dataclass


from model.pilot import Pilot


@dataclass

class Edge:
    p1:Pilot
    p2:Pilot
    weight: int