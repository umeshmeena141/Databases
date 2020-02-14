#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import sqlite3


# In[2]:


data = pd.read_csv('./age-education.csv')
# print(data.head())

# In[2]:


conn = sqlite3.connect("population.db")
c = conn.cursor()


# In[6]:


def drop_tables(c):
    
    tables = ['AGE_LITERACY','AREA_AGE_ID','LANGUAGE_AGE','AREA','EDUCATION','LANG_EDUCATION']
    try:
        for t in tables:
            sql = '''DROP TABLE '''+ t
            c.execute(sql)
    except sqlite3.IntegrityError as e:
        print('sqlite error: ', e.args[0]) # column name is not unique
    conn.commit()
    print('done')

# drop_tables(c)
# In[7]:


# drop_tables(c)


# In[8]:


def create_table(c,query,name):
    try:
        c.execute(query)
    except sqlite3.IntegrityError as e:
        print('sqlite error: ', e.args[0]) # column name is not unique
    conn.commit()
    print(name,'done')


# In[9]:


def insert_many(c,schema,values,table):
    try:
        sql = '''INSERT INTO '''+table + schema[0] + ''' VALUES '''+ schema[1]
        c.executemany(sql, values)
    except sqlite3.IntegrityError as e:
        print('sqlite error: ', e.args[0]) # column name is not unique
    conn.commit()
    print('Insertion done')


# In[10]:


def avg_age(tup):
#     print(tup)
    if tup=='Total' or tup == 'Age not stated' or tup == 'All ages':
        return -1
    elif '+' in tup:
        return int(tup[:-1])+5
    elif '-' in tup:
        a_b = tup.split("-")
#         print(a_b)
        return (int(a_b[0]) + int(a_b[1]))//2
    else:
        return int(tup)

from collections import defaultdict
def age_group(data):
    grps = ['0-9','10-14','15-19','20-24','25-29','30-49','50-69','70+','Age not stated']
    df = defaultdict(int)
#     print(df)
    for row in data.values:
#         print(row)
        if row[5][0]=='A':
            col = 'Age not stated'
        elif '+' in row[5] or int(row[5].split('-')[0])>=70:
            col = '70+'
        else:    
            a = [int(c) for c in row[5].split('-')]
            for grp in grps[:-2]:
                c,d = [int(c) for c in grp.split('-')]
                if len(a)>1:
                    if c<=a[0] and d>= a[1]:
                        col = grp
                else:
                    if c<=a[0] and d>= a[0]:
                        col = grp
        df[col] +=int(row[6])
    return df


# ## AREA TABLE

# In[11]:


table_1 = '''CREATE TABLE AREA(
ID INTEGER PRIMARY KEY AUTOINCREMENT,
STATE_CODE INT NOT NULL,
DISTT_CODE INT NOT NULL,
NAME TEXT NOT NULL);'''
create_table(c,table_1,'AREA')


# In[12]:


area_db = data.iloc[6:,1:4].drop_duplicates().values


# In[8]:


# area_db


# In[14]:


schema =['''(STATE_CODE,DISTT_CODE,NAME)''','''(?,?,?)''']
insert_many(c,schema,area_db,'''AREA''')


# ## AGE_LITERACY TABLE
table_2 = '''CREATE TABLE AGE_POPULATION(
ID INTEGER PRIMARY KEY AUTOINCREMENT,
AGE_GROUP TEXT NOT NULL,
TOTAL_POPULATION INTEGER)'''
create_table(c,table_2,'AGE POPULATION')

data_un = data.iloc[6:]
total_pop = data_un[data_un.iloc[:,3]=='INDIA']
total_pop = data_un[data_un.iloc[:,4]=='Total']
total_pop = data_un[data_un.iloc[:,5]!='All ages']
_dict = age_group(total_pop)
_dict_values = [[a,b] for a,b in _dict.items()]
schema_2 =['''(AGE_GROUP,TOTAL_POPULATION)''','''(?,?)''']
insert_many(c,schema_2,_dict_values,'''AGE_POPULATION''')
# In[18]:


table_3 = '''CREATE TABLE AGE_LITERACY(
ID INTEGER PRIMARY KEY AUTOINCREMENT,
STATE_CODE INTEGER NOT NULL,
GEOGRAPHIC_AREA TEXT NOT NULL,
AGE_GROUP TEXT,
TOTAL_PERSONS INTEGER,TOTAL_MALE INTEGER,TOTAL_FEMALE INTEGER,
ILLITERATE_PERSONS INTEGER,ILLITERATE_MALE INTEGER,ILLITERATE_FEMALE INTEGER,LITERATE_PERSONS INTEGER,LITERATE_MALE INTEGER,LITERATE_FEMALE INTEGER,
AVG_AGE INTEGER,
FOREIGN KEY (STATE_CODE) REFERENCES AREA(STATE_CODE)
);'''
create_table(c,table_3,'AGE_LITERACY')


# In[19]:


# data.head()


# In[20]:


age_lit = data.iloc[6:,[1,4,5,6,7,8,9,10,11,12,13,14]]
age_lit['avg_age']=age_lit.iloc[:,2].map(avg_age)


# In[21]:


age_lit = age_lit.fillna(0)


# In[23]:


schema_3 =['''(STATE_CODE,GEOGRAPHIC_AREA,AGE_GROUP,TOTAL_PERSONS,TOTAL_MALE,TOTAL_FEMALE,ILLITERATE_PERSONS,ILLITERATE_MALE,ILLITERATE_FEMALE,LITERATE_PERSONS,LITERATE_MALE,LITERATE_FEMALE,AVG_AGE)''','''(?,?,?,?,?,?,?,?,?,?,?,?,?)''']
insert_many(c,schema_3,age_lit.values,'''AGE_LITERACY''')


# ## Education Table

# In[43]:


table_4 = '''CREATE TABLE EDUCATION(
STATE_CODE INTEGER NOT NULL,
GEOGRAPHIC_AREA TEXT NOT NULL,
AGE_GROUP TEXT,
LITERATE_WITHOUT_EDUCATION_TOTAL INTEGER,LITERATE_WITHOUT_EDUCATION_MALE INTEGER,LITERATE_WITHOUT_EDUCATION_FEMALE INTEGER,
BELOW_PRIMARY_TOTAL INTEGER,BELOW_PRIMARY_MALE INTEGER,BELOW_PRIMARY_FEMALE INTEGER,
PRIMARY_TOTAL INTEGER,PRIMARY_MALE INTEGER,PRIMARY_FEMALE INTEGER,
MIDDLE_TOTAL INTEGER,MIDDLE_MALE INTEGER,MIDDLE_FEMALE INTEGER,
SECONDARY_TOTAL INTEGER,SECONDARY_MALE INTEGER,SECONDARY_FEMALEINTEGER,
HIGHER_SECONDARY_TOTAL INTEGER,HIGHER_SECONDARY_MALE INTEGER,HIGHER_SECONDARY_FEMALE INTEGER,
NON_TECHNICIAN_TOTAL INTEGER,NON_TECHNICIAN_MALE INTEGER,NON_TECHNICIAN_FEMALE INTEGER,
TECHNICIAN_TOTAL INTEGER,TECHNICIAN_MALE INTEGER,TECHNICIAN_FEMALE INTEGER,
GRADUATE_TOTAL INTEGER,GRADUATE_MALE INTEGER,GRADUATE_FEMALE INTEGER,
UNCLASSIFIED_TOTAL INTEGER,UNCLASSIFIED_MALE INTEGER,UNCLASSIFIED_FEMALE INTEGER,
FOREIGN KEY (STATE_CODE) REFERENCES AREA(STATE_CODE)
);'''
create_table(c,table_4,'EDUCATION')


# In[44]:


ids = [1,4,5]+[i for i in range(15,len(data.columns))]
edu = data.iloc[6:,ids]


# In[45]:


edu = edu.fillna(0)


# In[47]:


schema_3 =['''''','''(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''']
insert_many(c,schema_3,edu.values,'''EDUCATION''')


# ## Language_Age Table

# In[48]:


table_5 = '''CREATE TABLE LANGUAGE_AGE(
STATE_CODE INTEGER NOT NULL,
GEOGRAPHIC_AREA TEXT NOT NULL,
AGE_GROUP TEXT,
SECOND_LANGUAGE_TOTAL INTEGER,SECOND_LANGUAGE_MALE INTEGER,SECOND_LANGUAGE_FEMALE INTEGER,
THIRD_LANGUAGE_TOTAL INTEGER,THIRD_LANGUAGE_MALE INTEGER,THIRD_LANGUAGE_FEMALE INTEGER,AVG_AGE INTEGER,
FOREIGN KEY (STATE_CODE) REFERENCES AREA(STATE_CODE),
PRIMARY KEY (STATE_CODE, GEOGRAPHIC_AREA, AGE_GROUP)
);'''
create_table(c,table_5,'LANGUAGE_AGE')


# In[49]:


data_2 = pd.read_csv('./multilingual-age.csv')
data_2.fillna(0)


# In[50]:


ids = data_2.iloc[4:,[0,3,4,5,6,7,8,9,10]]


# In[51]:


def avg_age(tup):
#     print(tup)
    if tup=='Total' or tup == 'Age not stated':
        return -1
    elif '+' in tup:
        return int(tup[:-1])+5
    else:
        a_b = tup.split("-")
#         print(a_b)
        return (int(a_b[0]) + int(a_b[1]))//2
ids['avg_age']=ids.iloc[:,2].map(avg_age)


# In[53]:


schema_4 =['''''','''(?,?,?,?,?,?,?,?,?,?)''']
insert_many(c,schema_4,ids.values,'''LANGUAGE_AGE''')


# ## Language_Education Table

# In[54]:


table_6='''CREATE TABLE LANG_EDUCATION(
STATE_CODE INTEGER NOT NULL,
GEOGRAPHIC_AREA TEXT NOT NULL,
EDUCATION_LEVEL TEXT,
SECOND_LANGUAGE_TOTAL INTEGER,SECOND_LANGUAGE_MALE INTEGER,SECOND_LANGUAGE_FEMALE INTEGER,
THIRD_LANGUAGE_TOTAL INTEGER,THIRD_LANGUAGE_MALE INTEGER,THIRD_LANGUAGE_FEMALE INTEGER,
FOREIGN KEY (STATE_CODE) REFERENCES AREA(STATE_CODE),
PRIMARY KEY (STATE_CODE, GEOGRAPHIC_AREA, EDUCATION_LEVEL)
);'''
create_table(c,table_6,'LANG_EDUCATION')


# In[55]:


data_3 = pd.read_csv('./multilingual-education.csv')
data_3.fillna(0)


# In[56]:


ids = data_3.iloc[4:,[0,3,4,5,6,7,8,9,10]]


# In[57]:


schema_5 =['''''','''(?,?,?,?,?,?,?,?,?)''']
insert_many(c,schema_5,ids.values,'''LANG_EDUCATION''')


# In[58]:


ids


# ## Queries

# In[5]:


query_1 = ''' SELECT AREA.NAME,AREA.STATE_CODE 
FROM LANG_EDUCATION AS L , AGE_LITERACY  AS A, AREA 
WHERE L.STATE_CODE != '0' AND L.STATE_CODE = A.STATE_CODE AND AREA.STATE_CODE ==L.STATE_CODE AND
L.EDUCATION_LEVEL= 'Total' and A.AGE_GROUP ='All ages'  AND L.GEOGRAPHIC_AREA ='Total' AND A.GEOGRAPHIC_AREA ='Total' 
ORDER BY CAST(L.THIRD_LANGUAGE_TOTAL AS FLOAT)/CAST(A.TOTAL_PERSONS AS FLOAT) ASC'''


# In[6]:





# In[7]:

print("\nQuery 1 is running")
c.execute(query_1)
rows = c.fetchall()
for row in rows:
    print(row)


# In[107]:

print("\nQuery 2 is running")
query_2 = ''' 
SELECT AGE FROM 
(SELECT AGE_GROUP as AGE,MAX(CAST(S AS FLOAT)/ CAST(TOTAL_POPULATION AS FLOAT))  FROM ((SELECT AGE_GROUP,SUM(SECOND_LANGUAGE_TOTAL) AS S FROM LANGUAGE_AGE 
WHERE AGE_GROUP != 'Total' AND GEOGRAPHIC_AREA='Total' AND STATE_CODE !='0'
GROUP BY AGE_GROUP) NATURAL JOIN (AGE_POPULATION))  )
'''


# In[108]:


c.execute(query_2)
rows = c.fetchall()
for row in rows:
    print(row)


# In[8]:

print("\nQuery 3 is running")
query_3 = ''' 
SELECT AGE FROM 
(SELECT AGE_GROUP AS AGE, MAX(R) 
FROM (SELECT AGE_GROUP, MAX(CAST(TOTAL_MALE AS FLOAT)/CAST(TOTAL_FEMALE AS FLOAT)) AS R   
FROM AGE_LITERACY WHERE STATE_CODE = 0 AND GEOGRAPHIC_AREA = 'Total' AND AGE_GROUP != 'All ages'
UNION 
SELECT AGE_GROUP, MAX(CAST(TOTAL_FEMALE AS FLOAT)/CAST(TOTAL_MALE AS FLOAT)) AS R     
FROM AGE_LITERACY WHERE STATE_CODE = 0 AND GEOGRAPHIC_AREA = 'Total' AND AGE_GROUP != 'All ages'))'''
c.execute(query_3)
rows = c.fetchall()
for row in rows:
    print(row)


# In[36]:

print("\nQuery 4 is running")
query_4 = ''' SELECT A.TOTAL_PERSONS - L.SECOND_LANGUAGE_TOTAL
FROM AGE_LITERACY AS A,LANG_EDUCATION AS L WHERE L.STATE_CODE = A.STATE_CODE AND L.EDUCATION_LEVEL = 'Total'
AND A.STATE_CODE = '0' AND L.GEOGRAPHIC_AREA='Total' AND A.GEOGRAPHIC_AREA = 'Total' AND A.AGE_GROUP = 'All ages'
'''


# In[37]:


c.execute(query_4)
rows = c.fetchall()
for row in rows:
    print(row)


# In[66]:

print("\nQuery 5 is running")
query_5 = '''
SELECT N FROM 
(SELECT AREA.NAME as N,MAX(R)
FROM AREA,(
SELECT STATE_CODE, CAST(SUM(AVG_AGE*TOTAL_PERSONS) AS FLOAT)/CAST(SUM(TOTAL_PERSONS) AS FLOAT) AS R
FROM AGE_LITERACY WHERE STATE_CODE != '0' AND GEOGRAPHIC_AREA = 'Total' AND AGE_GROUP!= 'All ages' AND AGE_GROUP!= 'Age not stated'
GROUP BY STATE_CODE) AS P
WHERE AREA.STATE_CODE = P.STATE_CODE)
'''


# In[67]:


c.execute(query_5)
rows = c.fetchall()
for row in rows:
    print(row)

