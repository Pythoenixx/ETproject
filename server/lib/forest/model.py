from typing import Union, Literal

class Tree:
    blockI: int
    blockJ: int
    coordX: int
    coordY: int
    treeNum: str
    speciesCode: str
    speciesGroup: int
    diameter: float
    stemHeight: int
    volume: float
    status: str
    production: Union[Literal[""], float]
    cutAngle: Union[Literal[""], int]
    damageStem: Union[Literal[""], float]
    damageCrown: Union[Literal[""], float]
    diameter30: Union[Literal[""], float]
    volume30: Union[Literal[""], float]

    def __init__(self,
                 blockI: int,
                 blockJ: int,
                 coordX: int,
                 coordY: int,
                 treeNum: str,
                 speciesCode: str,
                 speciesGroup: int,
                 diameter: float,
                 stemHeight: int,
                 volume: float,
                 status: str,
                 production: Union[Literal[""], float],
                 cutAngle: Union[Literal[""], int],
                 damageStem: Union[Literal[""], float],
                 damageCrown: Union[Literal[""], float],
                 diameter30: Union[Literal[""], float],
                 volume30: Union[Literal[""], float]
    ) -> None:
        self.blockI = blockI
        self.blockJ = blockJ
        self.coordX = coordX
        self.coordY = coordY
        self.treeNum = treeNum
        self.speciesCode = speciesCode
        self.speciesGroup = speciesGroup
        self.diameter = diameter
        self.stemHeight = stemHeight
        self.volume = volume
        self.status = status
        self.production = production
        self.cutAngle = cutAngle
        self.damageStem = damageStem
        self.damageCrown = damageCrown
        self.diameter30 = diameter30
        self.volume30 = volume30
    
    def to_csv(self):
        return f"{self.blockI},{self.blockJ},{self.coordX},{self.coordY},{self.treeNum},{self.speciesCode},{self.speciesGroup},{self.diameter},{self.stemHeight},{self.volume},{self.status},{self.production},{self.cutAngle},{self.damageStem},{self.damageCrown},{self.diameter30},{self.volume30}"
