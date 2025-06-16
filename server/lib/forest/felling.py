import copy
import math
import random

from quart import websocket

from .model import Tree
from .database import saveForest, loadForest

def negative_cope(darjah):

    return max(1.0001, darjah)

def cut_damage(x0, x, y0, y, stemHeight, cutting_angle):
    x_length = abs(x0 - x)
    y1 = 0
    y2 = 0
    if 0 < cutting_angle <= 90:

        if (
            x0 < x < x0 + stemHeight + 5 + 5
            and y0 < y < y0 + stemHeight + 5 + 5
        ):

            theta = cutting_angle

            y1 = y0 + x_length / math.tan(negative_cope((theta + 1)) / 180 * 3.142)

            y2 = y0 + x_length / math.tan(negative_cope((theta - 1)) / 180 * 3.142)

    elif 90 < cutting_angle <= 180:

        if (
            x0 < x < x0 + stemHeight + 5 + 5
            and y0 > y > y0 - stemHeight - 5 - 5
        ):

            theta = 180 - cutting_angle

            y1 = y0 - x_length / math.tan(
                negative_cope((theta + 1)) / 180 * 3.142
            )

            y2 = y0 - x_length / math.tan(
                negative_cope((theta - 1)) / 180 * 3.142
            )

    elif 180 < cutting_angle <= 270:

        if (
            x0 > x > x0 - stemHeight - 5 - 5
            and y0 > y > y0 - stemHeight - 5 - 5
        ):

            theta = cutting_angle - 180

            y1 = y0 - x_length / math.tan(
                negative_cope((theta + 1)) / 180 * 3.142
            )

            y2 = y0 - x_length / math.tan(
                negative_cope((theta - 1)) / 180 * 3.142
            )

    elif 270 < cutting_angle <= 360:

        if (
            x0 > x > x0 - stemHeight - 5 - 5
            and y0 < y < y0 + stemHeight + 5 + 5
        ):

            theta = 360 - cutting_angle

            y1 = y0 + x_length / math.tan(
                negative_cope((theta + 1)) / 180 * 3.142
            )  # dua ni tak sama mcm sir punya

            y2 = y0 + x_length / math.tan(negative_cope((theta - 1)) / 180 * 3.142)

    cutting_y_min = min(y1, y2)

    cutting_y_max = max(y1, y2)
    
    return cutting_y_min, cutting_y_max

async def simulateFelling(forest_generated: list[Tree]):
    regimes = [45, 50, 55, 60]
    for regime in regimes:
        await _simulateFelling(copy.deepcopy(forest_generated), regime)
    await websocket.close(1000)

async def _simulateFelling(forest_generated: list[Tree], regime: int):
    cut_trees_list = []
    victim_trees_list = []
    victim_tree_list_skipped = []

    stem_damage_count = 0
    crown_damage_count = 0
    cut_count = 0
    treeCount = 0
    for tree in forest_generated:
        treeCount += 1
        x0 = tree.coordX

        y0 = tree.coordY

        species_group = tree.speciesGroup

        diameter = tree.diameter

        stemHeight = tree.stemHeight

        if species_group in {1, 2, 3, 5} and tree.status != "VICTIM":

            if diameter > regime and tree.status == "NO STATUS":
                pokok2_victim = ""

                pokok2_victim_skipped = []

                status = "CUT"
                cut_count += 1
                tree.status = status

                tree.production = tree.volume

                cutting_angle = random.randint(0, 360)
                # Convert cutting angle to radians with coordinate system transformation
                # Rationale: Original coordinate system uses +x-axis as reference (CCW positive). 
                # For crown damage calculations, transform to +y-axis reference (CW positive) to match 
                # the slide's coordinate system convention. Stem damage calculations maintain the original 
                # coordinate system as the reference formulas are already aligned.
                cutting_rad = math.radians((90 - cutting_angle) % 360) 

                tree.cutAngle = cutting_angle

                length_x = (stemHeight + 5) * math.sin(cutting_rad)

                length_y = (stemHeight + 5) * math.cos(cutting_rad)
                
                crown_x = x0 + length_x

                crown_y = y0 + length_y

                # if 0 < cutting_angle <= 90:

                #     crown_x = x0 + length_x

                #     crown_y = y0 + length_y

                # elif 90 < cutting_angle <= 180:

                #     crown_x = x0 + length_x

                #     crown_y = y0 - length_y

                # if 180 < cutting_angle <= 270:

                #     crown_x = x0 - length_x

                #     crown_y = y0 - length_y

                # elif 270 < cutting_angle <= 360:

                #     crown_x = x0 - length_x

                #     crown_y = y0 + length_y

                for pokok in forest_generated:

                    if pokok.status != "VICTIM" and pokok.status != "CUT":

                        x = pokok.coordX

                        y = pokok.coordY

                        x1 = x
                        # x_length = abs(x0 - x)
                        #print(f"Input parameters: x0={x0}, x_length={x_length}, y0={y0}, y={y}, stemHeight={stemHeight}, cutting_angle={cutting_angle}")
                        cutting_y_min, cutting_y_max = cut_damage(x0, x, y0, y, stemHeight, cutting_angle)
                        # cutting_y_min, cutting_y_max = y0 + cutting_y_min_length, y0 + cutting_y_max_length
                        # print("is", cutting_y_min, "<", y, "<", cutting_y_max, "?", "theta:", theta, "cutting angle:", cutting_angle)
                        if cutting_y_min <= y <= cutting_y_max:
                            stem_damage_count += 1
                            pokok.status = "VICTIM"
                            pokok.damageStem = pokok.volume
                            cut_trees_list.append([tree.treeNum, pokok.treeNum, 1])
                        elif math.sqrt(((crown_x - x) ** 2) + ((crown_y - y) ** 2)) <= 5:

                            pokok.status = "VICTIM"
                            crown_damage_count += 1
                            # print(pokok, "kene crown damage")
                            pokok.damageCrown = pokok.volume * 0.5  # 50% damage
                            cut_trees_list.append([tree.treeNum, pokok.treeNum, 2])
                    else:

                        pokok2_victim_skipped.append(pokok)

                # print("bilangan pokok victim yg diskipped:", len(pokok2_victim_skipped))
                cut_tree = [tree.treeNum, pokok2_victim, ]

            else:

                tree.status = "KEEP"

        elif tree.status != "VICTIM":

            tree.status = "-"

        else:

            victim_tree_list_skipped.append(tree)

        # print("pokok blockX:", tree[0])
        
        await websocket.send_json({
            "type": "update",
            "status": "Felling Simulation",
            "details": {
                "regime": regime,
                "progress": treeCount / len(forest_generated),
                "description": "Simulating felling"
            }
        })
    await websocket.send_json({
        "type": "update",
        "status": "Felling Simulation",
        "details": {
            "regime": regime,
            "progress": treeCount / len(forest_generated),
            "description": "Saving forest data"
        }
    })
    
    await saveForest(forest_generated, f"forest_data_{regime}")
    
    """ fileData = ["BlockX,BlockY,x,y,TreeNum,species,spgroup,Diameter (dbc cm),Stem Height,Volume (m3),status,PROD,Damage(Cut angle),Damage STEM,Damage Crown,d30,VOL30\n"]

    for tree in forest_generated:
        fileData.append(f"{tree.to_csv()}\n")

    # Writing to a CSV file
    with open("Forest.csv", "w", newline="") as file:
        file.writelines(fileData) """