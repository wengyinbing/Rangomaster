import json
import urllib.parse as parse
import urllib.request as request
import os

def read_webhose_key():
    '''
    从search.key 文件中读取webhose API秘钥
    返回None（没有找到秘钥），找到了返回秘钥的字符串形式
    将search.key写入.gitignore文件，禁止提交
    :return:
    '''
    webhose_api_key = None
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path1 = os.path.join(BASE_DIR, 'rango')
    path2 = os.path.join(path1, 'search.key')
    try:
        with open(path2,'r') as f:
            webhose_api_key = f.readline().strip()
    except:
        raise IOError('search.key file not found')

    return webhose_api_key

def run_query(search_terms,size=10):
    '''
    :param search_terms: 搜索词条
    :param size: 结果数目
    :return:
    将webhose API 返回的结果存入列表，没个结果都有标题，链接地址和摘要
    '''
    webhose_api_key = read_webhose_key()

    if not webhose_api_key:
        raise KeyError('Webhose key not found')
    # webhose APD的基URL
    root_url = 'http://webhose.io/search'
    #将查询字符串转换为特殊字符
    query_string =parse.quote(search_terms)

    search_url = ('{root_url}?token={key}&format=json&q={query}'
                  '&sort=relevancy&size={size}').format(
                    root_url=root_url,
                    key=webhose_api_key,
                    query=query_string,
                    size=size)
    results = []
    try:
        #
        response = request.urlopen(search_url).read().decode('utf-8')
        json_response = json.loads(response)

        for post in json_response['posts']:
            results.append({'title':post['title'],
                            'link':post['url'],
                            'summary':post['text'][:200]})
    except:
        print("Error when querying the webhose API")

    return results

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path1 = os.path.join(BASE_DIR,'rango')
    path2 = os.path.join(path1,'search.key')
    print(path2)