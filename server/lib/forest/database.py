import aiohttp
import json
from pocketbase import PocketBase
from .model import Tree

client = PocketBase("https://backend.pleb.moe")

def authenticateUser():
    user = client.collection("users").auth_with_password(
        "unikl-projects@pleb.moe", "LIVFPCdtNIL1Mps"
    )
    if (user.is_valid):
        return user
    return None

def createTreeBatchItem(tree: Tree, table_name: str):
    return {
        "method": "POST",
        "url": f"/api/collections/{table_name}/records",
        "body": {
            "blockX": tree.blockI,
            "blockY": tree.blockJ,
            "coordX": tree.coordX,
            "coordY": tree.coordY,
            "treeNum": tree.treeNum,
            "speciesCode": tree.speciesCode,
            "speciesGroup": tree.speciesGroup,
            "diameter": tree.diameter,
            "stemHeight": tree.stemHeight,
            "volume": tree.volume,
            "status": tree.status,
            "production": tree.production,
            "cutAngle": tree.cutAngle,
            "damageStem": tree.damageStem,
            "damageCrown": tree.damageCrown,
            "diameter30": tree.diameter30,
            "volume30": tree.volume30
        }
    }

def removeTreeBatchItem(id: str, table_name: str):
    return {
        "method": "DELETE",
        "url": f"/api/collections/{table_name}/records/{id}"
    }

async def loadForest():
    user = authenticateUser()
    
    if user:
        allRecords = client.collection("forest_data").get_full_list()
        forestList: list[Tree] = []
        
        for record in allRecords:
            forestList.append(Tree(
                record.block_x, # type: ignore
                record.block_y, # type: ignore
                record.coord_x, # type: ignore
                record.coord_y, # type: ignore
                record.tree_num, # type: ignore
                record.species_code, # type: ignore
                record.species_group, # type: ignore
                record.diameter, # type: ignore
                record.stem_height, # type: ignore
                record.volume, # type: ignore
                record.status, # type: ignore
                record.production, # type: ignore
                record.cut_angle, # type: ignore
                record.damage_stem, # type: ignore
                record.damage_crown, # type: ignore
                record.diameter30, # type: ignore
                record.volume30 # type: ignore
            ))

        return forestList

async def saveForest(forestList: list[Tree], table_name: str):
    user = authenticateUser()
    
    if user:
        batchList: list[dict] = [createTreeBatchItem(tree, table_name) for tree in forestList]
            
        chunkSize = 5000
        chunkedLists = [batchList[i:i + chunkSize] for i in range(0, len(batchList), chunkSize)]
        
        for chunk in chunkedLists:
            retriesCount = 0
            while retriesCount < 5:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.post("https://backend.pleb.moe/api/batch", data=json.dumps({
                            "requests": chunk
                        }), headers={ "Authorization": f"Bearer {user.token}", "Content-Type": "application/json" }) as r:
                            print("Sent")
                            break
                except:
                    retriesCount += 1

async def clearForest():
    user = authenticateUser()
    
    if user:
        allTables = ["forest_data_base", "forest_data_45", "forest_data_50", "forest_data_55", "forest_data_60"]
        for table in allTables:
            allIDsRaw = client.collection(table).get_full_list(batch=1000,query_params={
                "fields": "id"
            })
            
            allIDs = [removeTreeBatchItem(x.id, table) for x in allIDsRaw]
            chunkSize = 5000
            chunkedLists = [allIDs[i:i + chunkSize] for i in range(0, len(allIDs), chunkSize)]
            
            for chunk in chunkedLists:
                retriesCount = 0
                while retriesCount < 5:
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.post("https://backend.pleb.moe/api/batch", data=json.dumps({
                                "requests": chunk
                            }), headers={ "Authorization": f"Bearer {user.token}", "Content-Type": "application/json" }) as r:
                                print("Sent")
                                break
                    except:
                        retriesCount += 1
