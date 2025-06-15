import random
import csv
import numpy as np
from quart import websocket
from .model import Tree
from .database import saveForest, clearForest
from .felling import simulateFelling

async def generateForest():
    await websocket.send_json({
        "type": "update",
        "status": "Generating forest.",
        "details": f"Clearing forest data"
    })
    await clearForest()
    
    group_species = ["mersawa", "keruing", "Dip commercial", "Dip Non Commercial", "NonDip commercial", "NonDip Non Commercial", "Others"]
    diameter_class = [(5, 15), (15, 30), (30, 45), (45, 60), (60, 100)]
    total_trees = [
        [15, 12, 4, 2, 2],
        [21, 18, 6, 4, 4],
        [21, 18, 6, 4, 4],
        [30, 27, 9, 5, 3],
        [30, 27, 9, 4, 4],
        [39, 36, 12, 7, 4],
        [44, 42, 14, 9 ,4]
    ]
    group_mapping = [(0, 0), (1, 4), (5, 11), (12, 18), (19, 58), (59, 315)]
    species_list = [
        "PHDK", "CHBG", "CHBR", "CHTR", "CHMI", "CHRH", "CRMS", "KKMS", "KKPN", "LMBI", "PCEK", "TBEG", "KHOV",
        "KKDK", "KKKS", "KKTM", "PPEL", "RINM", "TRLT", "ANKM", "ATTT", "BENG", "BSNK", "CHBK", "CHKM", "CHKO",
        "CHKR", "CHLK", "CHMC", "CHTP", "DCSP", "DYKL", "HUDN", "KMPR", "KRAY", "KREL", "KRKO", "KRPM", "KRYS",
        "MASK", "NNON", "PRDL", "PRLO", "PRNG", "SKRM", "SMPN", "SRAL", "SRKR", "SRLO", "SROL", "SWPR", "SYCR",
        "TAUR", "TEPI", "THNR", "THNS", "TRTM", "TRYG", "TTRV", "ANKN", "ANKT", "ANOM", "ATNG", "BADM", "BAKG",
        "BDNG", "BELY", "BKSV", "BNKO", "BYPV", "CASA", "CCHB", "CHMK", "CHNY", "CHPL", "CHRK", "CHRM", "CHRS",
        "CHUT", "CKTM", "CREY", "DKOR", "DOKM", "HISN", "KAOM", "KCAS", "KDAG", "KDCH", "KDOL", "KES", "KKCM",
        "KKGN", "KKOM", "KNDL", "KNPR", "KRAG", "KRAS", "KRBO", "KRLA", "KRON", "KTOM", "KWAV", "LGNG", "MAKG",
        "MAKP", "MAKU", "MNPR", "NENS", "PANG", "PHNV", "PHON", "PHUT", "PLON", "PNAG", "PNGS", "POBY", "POCV",
        "POKH", "PONR", "PPTH", "PPUL", "PRPN", "PRUS", "PYPK", "RAIT", "ROKA", "RUNG", "SABL", "SARG", "SBMS",
        "SDAV", "SDEY", "SLEN", "SMCH", "SME", "SMKB", "SNAY", "SNOL", "SOUY", "SPOR", "SPPY", "SPTK", "SRKM",
        "SVAK", "SVCT", "SVPT", "TKOV", "TLOK", "TOLP", "TPOG", "TRAG", "TREN", "TRMN", "TRSK", "WYNG", "ACSA",
        "ADCH", "AKSL", "AMBB", "AMCN", "AMPI", "ANCH", "ANKB", "ANRD", "APEN", "ATES", "ATSR", "BAKK", "BAKP",
        "BBOK", "BOPR", "BRCH", "BTIL", "CABB", "CHCK", "CHEK", "CHHA", "CHHU", "CHKG", "CHKP", "CHKU", "CHLS",
        "CHNA", "CHNO", "CHOV", "CHPS", "CHTU", "CTES", "DAKD", "DGPR", "DKPO", "DNKY", "DRDV", "DYSP", "EPSH",
        "KACL", "KAKU", "KANA", "KANE", "KANT", "KATG", "KAYK", "KBAL", "KBDA", "KBDK", "KBKK", "KCHP", "KDCE",
        "KDCK", "KHMA", "KHNH", "KHOS", "KHTN", "KHVG", "KKAL", "KKKK", "KKLG", "KLIG", "KLNG", "KLPO", "KMPT",
        "KNAL", "KNAY", "KODK", "KOKH", "KOMT", "KOMY", "KORK", "KOTT", "KRAK", "KREG", "KREM", "KRMN", "KROH",
        "KRSR", "KRUS", "KRVN", "KTIT", "LORT", "LORV", "LOVG", "LRLT", "MADN", "MDAS", "MMAG", "MTYK", "NGOK",
        "NHAM", "NIV", "ONLK", "PAGA", "PAGS", "PECH", "PHLG", "PHMA", "PHNO", "PHOR", "PLNG", "PLOG", "PLOK",
        "PLOR", "PLPH", "PMVG", "PNKP", "PNOM", "POCH", "POPL", "POUN", "PPPR", "PPVK", "PREL", "PROM", "PROM",
        "RANG", "ROCG", "RODL", "ROML", "ROTY", "ROVN", "RPCK", "SADA", "SAHA", "SAND", "SANK", "SAVP", "SBTS",
        "SEMN", "SKPL", "SLCH", "SLET", "SLNG", "SOPI", "SREG", "SRMO", "TAPL", "TBOT", "TENG", "THME", "THNO",
        "THTR", "TMAK", "TNIV", "TOUK", "TRBL", "TRCU", "TREL", "TROG", "TRSK", "TRYA", "TRYG", "TTPY", "UNKN",
        "VEAY", "VOEG", "YEAM", "YOUK", "KHLG", "TRAC", 
    ]
    forest_generated: list[Tree] = []

    for i in range(1, 11):  # For I = 1, 10           /* Block I */
        for j in range(1, 11):  # For j = 1,10            /* Block J */
            await websocket.send_json({
                "type": "update",
                "status": "Generating forest.",
                "details": f"Block {i}, {j}"
            })
            for g in range(len(group_species)):  # For Group G = 1,7
                for d in range(len(diameter_class)):  #  For Dclass = 1, 5
                    trees_to_gen = total_trees[g][d]  #  NoTrees = Table[G, Dclass, NoTrees]
                    # Generate Data
                    for tree in range(trees_to_gen):  # For Tree = 1,NoTree
                        # Coordinate
                        # x = rand(0,99); coordX = (I-1)*100+x;
                        # y = rand(0,99); coordY = (J-1)*100+y;
                        x = random.randint(0, 99)
                        coordX = (i - 1) * 100 + x
                        y = random.randint(0, 99)
                        coordY = (j - 1) * 100 + y
                        # Species
                        # If the group species does not have any local name at all
                        # then use group species name as the species name
                        if g < len(group_mapping):
                            mapStrt, mapEnd = group_mapping[g]
                            species = species_list[random.randint(mapStrt, mapEnd)]
                        else:
                            species = group_species[g]

                        # Diameter class
                        diamStrt, diamEnd = diameter_class[
                            d
                        ]  # Dclass(Dclass, StartD, EndD);
                        diameter = (
                            random.randint(diamStrt * 10, diamEnd * 10) / 10
                        )  # diameter = rand(StartD*10, EndD*10)/10;
                        # Height
                        if d == 0:
                            height = random.randint(5, 10)
                        elif d == 1:
                            height = random.randint(11, 15)
                        elif d == 2:
                            height = random.randint(16, 20)
                        elif d == 3:
                            height = random.randint(21, 25)
                        else:
                            height = random.randint(26, 30)

                        BlockX = f"{i:02}"
                        BlockY = f"{j:02}"
                        frmt_coordX = f"{coordX:03}"
                        frmt_coordY = f"{coordY:03}"

                        TreeNum = "T" + BlockX + BlockY + frmt_coordX + frmt_coordY

                        diameter_m = diameter / 100

                        if g in {0, 1, 2, 3}:  # assuming this group are dipterocarp
                            if diameter < 15:
                                volume = 0.022 + 3.4 * diameter_m * diameter_m
                            else:  # since ada height or length so just default guna formula yg guna length
                                volume = (
                                    0.015
                                    + 2.137 * diameter_m * diameter_m
                                    + 0.513 * diameter_m * diameter_m * height
                                )
                        else:
                            if diameter < 30:
                                volume = 0.03 + 2.8 * diameter_m * diameter_m
                            else:
                                volume = (
                                    -0.0023
                                    + 2.942 * diameter_m * diameter_m
                                    + 0.262 * diameter_m * diameter_m * height
                                )

                        default_status = "NO STATUS"
                        production = ""
                        cut_angle = ""
                        damage_stem = ""
                        damage_crown = ""
                        d30 = ""
                        vol30 = ""

                        tree_info = Tree(
                            i,
                            j,
                            coordX,
                            coordY,
                            TreeNum,
                            species,
                            g + 1,
                            diameter,
                            height,
                            round(volume, 2),
                            default_status,
                            production,
                            cut_angle,
                            damage_stem,
                            damage_crown,
                            d30,
                            vol30,
                        )

                        forest_generated.append(tree_info)
    
    await websocket.send_json({
        "type": "update",
        "status": "Generating forest.",
        "details": f"Saving forest data"
    })
    """ fileData = ["BlockX,BlockY,x,y,TreeNum,species,spgroup,Diameter (dbc cm),Stem Height,Volume (m3),status,PROD,Damage(Cut angle),Damage STEM,Damage Crown,d30,VOL30\n"]

    for tree in forest_generated:
        fileData.append(f"{tree.to_csv()}\n")

    # Writing to a CSV file
    with open("Forest.csv", "w", newline="") as file:
        file.writelines(fileData) """
    await saveForest(forest_generated, "forest_data_base")
    await websocket.send_json({
        "type": "next_stage",
        "details": f"Change to felling simulation"
    })
    await simulateFelling(forest_generated)
