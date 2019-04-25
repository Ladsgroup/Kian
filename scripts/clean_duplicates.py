import sys
import MySQLdb
import urllib2


from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = "SELECT ?item WHERE {{?item wdt:{0} wd:{1}}}"

def get_results(endpoint_url, query_):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query_)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()["results"]["bindings"]

#res_human = [i["results"]["bindings"][0] for i in get_results(endpoint_url, query.format('P31', 'Q5'))]
#print(res_human[:500])

def main():
    db = MySQLdb.connect(host="tools-db", db="s52709__kian_p",
                         read_default_file="/data/project/kian/replica.my.cnf")
    cursor = db.cursor()
    select_statement = (
        "SELECT property, value from kian "
        "where status = 0 "
        "group by property, value;")
    cursor.execute(select_statement)
    cases = list(cursor.fetchall())
    for case in cases:
        print('Working on {case}'.format(case=case))
        url = "http://tools.wmflabs.org/autolist/index.php?wdq=claim[" \
            "{statemnt}:{value}]&run=Run&download=1"
        if case[1] != 'Q5':
            res = [i['item']['value'].replace('http://www.wikidata.org/entity/', '') for i in get_results(endpoint_url, query.format(case[0], case[1]))]
        else:
            continue
            #res = res_human
        res = set(res)
        select_statement = (
            "SELECT qid from kian "
            "where status = 0 and property = "
            "'{prop}' and value = '{val}';".format(prop=case[0], val=case[1]))
        cursor.execute(select_statement)
        res2 = set([i[0] for i in cursor.fetchall()])
        intersection = res & res2
        print(len(intersection))
        if not intersection:
            continue
        print(len(res), len(res2), len(intersection))
        str_intersection = str(tuple(intersection)).replace('u\'Q', '\'Q')
        set_statement = (
            "UPDATE kian SET status = 1 "
            "where qid in {qid} and property = "
            "'{prop}' and value = '{val}';".format(qid=str_intersection,
                                                   prop=case[0], val=case[1]))
        cursor.execute(set_statement)
    db.commit()
    cursor.close()
    db.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

