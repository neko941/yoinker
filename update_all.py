# import os
# from multiprocessing import Pool

# def execute(program):
#     exec(open(program).read())

# if __name__ == '__main__':
#     with Pool(3) as p:
#         print(p.map(execute, [
#             os.path.join('writing9.com', 'fetch_data.py'),
#             os.path.join('writing9.com', 'get_links.py'),
#             os.path.join('thanhnien.vn', 'fetch.py'),
#         ]))    