import os
import json
import numpy as np
import asyncio
import concurrent.futures
import requests
import shutil



start = 0
stop = 21099

url = 'http://vargt.website/actas2v/sim/'

save_path = './actas2vuelta/'
if not os.path.exists(save_path):
    os.mkdir(save_path)


def query_api(num):

	image_name = '{:05d}'.format(num+1)+'1.jpg'
	image_url = url + image_name

	with open(save_path + image_name, 'wb') as handle:
	    response = requests.get(image_url, stream=True)

	    print("Now getting {}".format(image_name))

	    if not response.ok:
	        print (response)

	    shutil.copyfileobj(response.raw, handle)



async def main():
    starting = 0
    ending = 21099
    #excluded = [int(f.replace('.json', '')) for f in os.listdir(output_folder_raw)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:

        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(executor, query_api, i)
            for i in range(ending) #np.setdiff1d([i for i in range(starting, ending)], excluded)
        ]
        for response in await asyncio.gather(*futures):
            pass

loop = asyncio.get_event_loop()
loop.run_until_complete(main())