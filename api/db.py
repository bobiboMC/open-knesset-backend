from functools import lru_cache
import logging
from typing_extensions import Annotated
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor

import config

import re
from fastapi import Depends

class DoubleQuotedString(str):
    def __repr__(self):
        return f'"{self}"'

logger = logging.getLogger(__name__)


@lru_cache
def get_settings():
    return config.Settings()

def get_db_connection(settings: Annotated[config.Settings, Depends(get_settings)]):
    return psycopg2.connect(
        host=settings.oknesset_db_host,
        port=settings.oknesset_db_port,
        database=settings.oknesset_db_name,
        user=settings.oknesset_db_user,
        password=settings.oknesset_db_password,
    )


@contextmanager
def get_db_cursor():
    conn = get_db_connection(get_settings())
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        yield cur
    finally:
        cur.close()
        conn.close()
        

# get table names from database 
def get_data_tables(limit,offset):
    sql = f"SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog', 'information_schema') LIMIT {limit} OFFSET {offset}"
    with get_db_cursor() as cur:
        cur.execute(sql)
        data = cur.fetchall()
    return data

# get all columns from some table    
def get_data_columns(table_name):
    sql = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
    with get_db_cursor() as cur:
        cur.execute(sql)
        data = cur.fetchall()
    return data
  
# get single data from table
def get_single_data(table, field, value):
    sql = f'select * from {table} where "{field}"={value}'
    with get_db_cursor() as cur:
        cur.execute(sql)
        data = cur.fetchone()
    return data

#get all known info about current minister or kns member
def get_fully_today_member(query,value):
    try:
        with get_db_cursor() as cur:
            cur.execute(query,value)
            data = cur.fetchone()
            column_names = [desc[0] for desc in cur.description]
    except Exception as e:
        return ValueError('No such member exist!')
    return data


# get list data
def get_data_list(start_query, limit, offset, order_by, qs):
    result = create_query_list(start_query, limit, offset, order_by, qs)
    if isinstance(result, Exception):
        return result
    query=result[0]
    values=result[1]
    try:
        with get_db_cursor() as cur:
            cur.execute(query,tuple(values))
            return cur.fetchall()
    except Exception as e:
        return e


# create query that returns data list
def create_query_list(start_query, limit: int = 0, offset: int = 0, order_by=None, qs: str | None = None):
    # options: limit, offset, order_by
    where_optional_args = []
    # options: limit, offset, order_by
    other_optional_args = []
    # values to put in placeholders in query
    values = []
    crc32c=False
    # add arguments to where clause
    if qs:
        qs = qs.split('&')
        for item in qs:
            # dealing with crc32c format
            if item[-2:]=='==':
                item = item[:-2]
                crc32c=True
            key, val = item.split('=')
            # checking if it's crc32c format
            if crc32c:
                val+='=='
                crc32c=False
            # checks if it's simple array of strings or integers
            if '[' in val:
                val_splited=val[1:-1].split(',')
                # checks if it's integers array
                try:
                    val = [int(element) for element in val_splited]
                    is_all_digits = all(str(element).isdigit() for element in val)
                    val=str(val)
                # if here, it's strings array
                except:  
                    val = [val[2:-2]]
                    val = str(val).replace("'", '"')
                
                val = val.replace('\\\\\\\\', '\\')                
                values.append(val)
                where_optional_args.append('"{0}" @> %s'.format(key))    
            # checks if it's array of objects  
            elif '<' in val:
                key_splited=key.split('_')
                object_key=key_splited[0]
                # checks if field of object has two words combine  
                if len(key_splited)==3:
                   object_field='{0}_{1}'.format(key_splited[1],key_splited[2])
                # if here, field of object is one word     
                else:
                   object_field=key_splited[1]
                   
                # checks if field of object is integer   
                if not(val[1:-1].isdigit()):
                    val='[{{"{0}": "{1}"}}]'.format(object_field,val[1:-1])
                # if here, field of object is string     
                else:
                    val='[{{"{0}": {1}}}]'.format(object_field,val[1:-1])
                values.append(val)
                where_optional_args.append('"{0}" @> %s'.format(object_key, val))
            # if here, it's simple data type integer, string or bool   
            else:
                where_optional_args.append('"{0}" = %s'.format(key))
                values.append(val)

    # No arguments for where clause
    if not where_optional_args:
        where_optional_args.append("1 = 1")
    
    # add arguments to order by clause
    if order_by is not None:
        order_by_clause = ''
        pattern = r'^(\w+\s+(?:asc|desc))(?:,\s*\w+\s+(?:asc|desc))*\s*$'
        if not re.match(pattern, order_by, re.IGNORECASE):
            return ValueError('Must be this format: column1 asc/desc,column2 asc/desc..')
        
        for elemt in order_by.split(','):
            parts = elemt.split(' ')
            column = parts[0]
            order_type = parts[1]
            order_by_clause += f'"{column}" {order_type},'
        # remove last ','
        order_by_clause = order_by_clause[:-1]
        other_optional_args.append(f" ORDER BY {order_by_clause}")
    # add arguments to limit clause
    if limit > 0:
        other_optional_args.append(" LIMIT %s")
        values.append(int(limit))
    # add arguments to offset clause
    if offset > 0:
        other_optional_args.append(" OFFSET %s")
        values.append(int(offset))
    # create the query
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
