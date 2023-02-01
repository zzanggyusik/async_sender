import time
import rest_api
from datetime import datetime
import json

import asyncio        
        
def id_list_get (config):
    id_list = config["id_list"]
    
    return id_list
    
def check_human(id_list, config):
    res = []
    for i in range(len(id_list)):
        id = id_list[i]
        res_step = rest_api.get(config["human_db"]["db_name"],config["human_db"]["db_collection_name"], config["human_db"]["id_type"], id, config)    
        
        if res_step == []:
            print('Human id {} not found!! ... '.format(id))

        else: 
            res.append(id)
            print('Human id {} found!!'.format(id))
            
        time.sleep(1)

    return res

def model_selector(id_list, config):
    model_list = []
    for i in range(len(id_list)):
        model = config["human_info"][id_list[i]]
        model_list.append(model)
        
    return model_list

async def data_sender(id, model, config):
    for index in range(len(model)):
        print('Index {} \t model {}'.format(index, model[index]))
        model_data = model[index]
        
        for sl in range((model[index][2])):
            print('Sinario task {}'.format(sl))
            data = {"timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),\
                "human_id": id, "smock": model_data[0], "work_intensive": model_data[1]}
            
            res = rest_api.get(config["site_human_db"]["db_name"], config["site_human_db"]["db_collection_name"], config["site_human_db"]["id_type"], id, config)
            
            if res == []:
                rest_api.post(config["site_human_db"]["db_name"], config["site_human_db"]["db_collection_name"], (data), config)
                print(f'{id} {index}/{sl} posted')
                await asyncio.sleep(1)
            else :
                rest_api.put(config["site_human_db"]["db_name"], config["site_human_db"]["db_collection_name"], config["site_human_db"]["id_type"], id, data, config)
                print(f'{id} {index}/{sl} put')
                await asyncio.sleep(1)

    print(f'{id} process finished')   

async def main() -> None:
    with open('./instance/config.json') as _file:
        config = json.load(_file)
    
    id_list = id_list_get(config)
    
    i = 0
    
    while True:
        print(i)
        print('id_list {}'.format(id_list))
        exist_id_list = check_human(id_list, config)
        print('exist_id_list {}'.format(exist_id_list))
        model_list = model_selector(exist_id_list, config)
        
        if exist_id_list == []:
            pass
        
        else :
            asyncio.create_task(data_sender(exist_id_list[0], model_list[0], config))
            id_list.remove(exist_id_list[0])
            
        i += 1
        await asyncio.sleep(1)
        
asyncio.run(main())  

'''

work_intensive_selector and smock_selector based on IP CAM's pose detector

def work_intensive_selector(id, config):
    # TODO Need changes
    id = "100"
    res = rest_api.get(config["inference_db"]["db_name"],config["inference_db"]["db_collection_name"], config['inference_db']['id_type'], id, config)
    pose = res["alphapose_result"]["keypoints"][0]["pose_estimation"]
    cvt_pose = 0
    print('Inferenced Pose is {}'.format(pose))
    if pose == "Sitting":
        cvt_pose = 1
    elif pose == "Standing":
        cvt_pose = 2
    elif pose == "Walking":
        cvt_pose = 3
    
    return cvt_pose
    
def smock_selector(id, config):
    # TODO Need change
    return 0    
    
'''