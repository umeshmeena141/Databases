Question 1. I have created 5 tables named 'AREA','AGE_LITERACY','LANGUAGE_AGE','EDUCATION','LANG_EDUCATION', 'AGE_POPULATION'.
'AREA' : It contains information about state codes, district codes and names of the states. Act as a referenced table for querying name of state.
        SCHEMA is (ID,STATE_CODE,DISTT_CODE,NAME)

'AGE_LITERACY' : The large table is divided into two tables, one containing information total litertates and illiterates and other containing information about division inside literates.
        One extra attribute is added which is avg age in case of age groups and only state code is inserted instead of whole other area information.
        SCHEMA is (ID,STATE_CODE,GEOGRAPHIC_AREA,AGE_GROUP,TOTAL_PERSONS,TOTAL_MALE,TOTAL_FEMALE,ILLITERATE_PERSONS,ILLITERATE_MALE,ILLITERATE_FEMALE,LITERATE_PERSONS,LITERATE_MALE,LITERATE_FEMALE,AVG_AGE)

'EDUCATION' : Information of internal division of literates.
        SCHEMA is similar to above table for all divisions of literates, e.g. TECHNICIAN_TOTAL, SECONDARY_MALE, MIDDLE_FEMALE

'LANGUAGE_AGE' : Information about age groups v/s multilingualism
        SCHEMA is (STATE_CODE,GEOGRAPHIC_AREA,AGE_GROUP,SECOND_LANGUAGE_TOTAL,SECOND_LANGUAGE_MALE,SECOND_LANGUAGE_FEMALE,THIRD_LANGUAGE_TOTAL,THIRD_LANGUAGE_MALE,THIRD_LANGUAGE_FEMALE)
,
'LANG_EDUCATION' : Information about education levels v/s multilingualism
        SCHEMA is (STATE_CODE,GEOGRAPHIC_AREA,EDUCATION_LEVEL,SECOND_LANGUAGE_TOTAL,SECOND_LANGUAGE_MALE,SECOND_LANGUAGE_FEMALE,THIRD_LANGUAGE_TOTAL,THIRD_LANGUAGE_MALE,THIRD_LANGUAGE_FEMALE)

'AGE_POPULATION' : Total Population vs age groups
        SCHEMA is (ID, AGE_GROUP, TOTAL_POPULATION)

This type of schema is chosen because similar kind of information is now separated and can be easily referenced through these tables.
In case of different age groups in 1st and 2nd csv file, a new table is created which contains age groups matched with 2nd csv file with total population for querying 2nd query.
 It also index groups of columns occurring simultaneously multiple times. Most of the schema's are chosen due to their ease in querying queries given.

Question 2. Data is inserted in the database using sqlite3 library of python which allows querying in the database. Code is written in the population_database.py

Question 3. Please run population_database.py for creating database and finding results to query.

Results in asc order
Query_1 : ('State - UTTAR PRADESH', 9)
('State - RAJASTHAN', 8)
('State - BIHAR', 10)
('State - CHHATTISGARH', 22)
('State - MADHYA PRADESH', 23)
('State - UTTARAKHAND', 5)
('State - WEST BENGAL', 19)
('State - TAMIL NADU', 33)
('State - HARYANA', 6)
('State - MIZORAM', 15)
('State - JHARKHAND', 20)
('State - HIMACHAL PRADESH', 2)
('State - TRIPURA', 16)
('State - PUDUCHERRY', 34)
('State - ANDHRA PRADESH', 28)
('State - NCT OF DELHI', 7)
('State - MEGHALAYA', 17)
('State - KERALA', 32)
('State - KARNATAKA', 29)
('State - ODISHA', 21)
('State - ASSAM', 18)
('State - GUJARAT', 24)
('State - DAMAN & DIU', 25)
('State - LAKSHADWEEP', 31)
('State - JAMMU & KASHMIR', 1)
('State - MAHARASHTRA', 27)
('State - ANDAMAN & NICOBAR ISLANDS', 35)
('State - DADRA & NAGAR HAVELI', 26)
('State - MANIPUR', 14)
('State - NAGALAND', 13)
('State - PUNJAB', 3)
('State - SIKKIM', 11)
('State - ARUNACHAL PRADESH', 12)
('State - CHANDIGARH', 4)
('State - GOA', 30)

Query_2 : '20-24'

Query_3 : '18'

Query_4 : 895866207

Query_5 : State - KERALA'
