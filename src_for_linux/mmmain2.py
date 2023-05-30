from ex import main

import asyncio
# from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import chromedriver_binary

# async def one():
    
#     with open(f"data2\\following\\following - 第1段目 - all_ID.txt")as f:
#         id_set = set([s.rstrip() for s in f.readlines()])

#     num = 0
#     for i in id_set:
#         num += 1
#         main.GET_FOLLOWS(i.replace(".txt",""),"following")
with open(f"src/data2/following/following - 第1段目 - all_ID.txt")as f:
    id_set = set([s.rstrip() for s in f.readlines()])




def MAIN():

    print("dasdfa")
    with ProcessPoolExecutor(max_workers=4) as executor:
        for i in id_set:
            executor.submit(main.GET_FOLLOWS,i.replace(".txt",""),"following")
        # for i in id_set:
        #     executor.submit(main.GET_FOLLOWS,i.replace(".txt",""),"following")
        # for i in id_set:
        #     executor.submit(main.GET_FOLLOWS,i.replace(".txt",""),"following")
    
# async def one():
    
#     print("fuck_you")


# async def MAIN():
# #    """並列処理"""
#     await one()
#     await one()


if __name__ == "__main__":
    # asyncio.run(MAIN())
    MAIN()
    # executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

    # num = 0
    # for i in id_set:
    #     num += 1
    #     executor.submit(main.GET_FOLLOWS(i.replace(".txt",""),"following"),i)
