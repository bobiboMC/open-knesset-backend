from contextlib import contextmanager

import psycopg2
from psycopg2.extensions import quote_ident


from . import config
from flask import request
import re

def get_db_connection():
    return psycopg2.connect(
        host=config.OKNESSET_DB_HOST,
        port=config.OKNESSET_DB_PORT,
        database=config.OKNESSET_DB_NAME,
        user=config.OKNESSET_DB_USER,
        password=config.OKNESSET_DB_PASSWORD,
    )


@contextmanager
def get_db_cursor():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        yield cur
    finally:
        cur.close()
        conn.close()
        
def get_data(sql):
    with get_db_cursor() as cur:
        cur.execute(f"{sql} LIMIT 5")
        data = cur.fetchall()
    return data


#get all known info about current minister or kns member  
def get_fully_today_member(query,value):
    try:
        with get_db_cursor() as cur:
            cur.execute(query,value)
            data = cur.fetchone()
            column_names = [desc[0] for desc in cur.description]
            result = {column_names[i]: data[i] for i in range(len(column_names))}            
    except Exception as e:
        return ValueError('No such member exist!')
    return result

    
#get list data        
def get_data_list(start_query,table_name):
    table_name=psycopg2.extensions.AsIs(table_name)#so 'table_name'-->table_name will work in query and not throw error for bad syntax
    result=create_query_list(start_query)
    if isinstance(result, Exception):
        return result
    query=result[0]
    values=result[1]
    try:
        with get_db_cursor() as cur:
            cur.execute(query,(table_name,)+tuple(values))
            data=cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            result = [{column_names[i]: value for i, value in enumerate(row)} for row in data]
            return result
    except Exception as e:
        return e

#create query that returns data list 
def create_query_list(start_query):
    where_optional_args = []
    other_optional_args=[] #options: limit, offset, order_by
    values = [] #values to put in placeholders in query

    limit = request.args.get('limit')
    offset = request.args.get('offset')
    order_by = request.args.get('order_by')
    used_clause = ["limit", "offset", "order_by"]

    #add arguments to where clause
    for key, val in request.args.items():
        if key not in used_clause:
            where_optional_args.append('"{0}" = %s'.format(key))
            values.append(val)

    # No arguments for where clause
    if not where_optional_args:
        where_optional_args.append("1 = 1")

    #add arguments to order by clause
    if order_by is not None:
        order_by_clause=''
        pattern = r'^(\w+\s+(?i)(?:asc|desc))(?:,\s*\w+\s+(?i)(?:asc|desc))*\s*$'
        if not re.match(pattern, order_by):
            return ValueError('Must be this format: column1 asc/desc,column2 asc/desc..')

        for elemt in order_by.split(','):
            parts=elemt.split(' ')
            column=parts[0]
            order_type=parts[1]
            order_by_clause += f'"{column}" {order_type},'
        #remove last ','
        order_by_clause=order_by_clause[:-1]
        other_optional_args.append(f" ORDER BY {order_by_clause}")
    #add arguments to limit clause
    if limit is not None:
        if not limit.isdigit() and not limit[1:].isdigit():
            return ValueError('Limit Must be an Integer!')

        other_optional_args.append(" LIMIT %s")
        values.append(int(limit))
    #add arguments to offset clause
    if offset is not None:
        if not offset.isdigit() and not offset[1:].isdigit():
            return ValueError('Offset Must be an Integer!')    

        other_optional_args.append(" OFFSET %s")
        values.append(int(offset))
    #create the query
    query = (
        f"{start_query} WHERE "
        + " AND ".join(where_optional_args)
        + "".join(other_optional_args)
    )
    return [query,values]

    
def get_discribe(table):
    with get_db_cursor() as cur:
        sql = f"SELECT * FROM information_schema.columns WHERE table_name = '{table}'"
        cur.execute(sql)
        data = cur.fetchall()
    return data
