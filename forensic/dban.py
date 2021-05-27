import sqlite3
import os
from sys import argv
from colorama import Fore, Style, init
#import textwrap ~ Almost crap..wraps on words and not char..bugs

def help():
    help_string = f"""\n Welcome To Database Analysis! (Version: 1.0)\n\t\t ~ Made by Md Zidan Khan\n{"-".ljust(46, "-")}
\n Help \n-----------\n\nSyntax:\n\t\tdban.py [-h]
\t\tdban.py [-d] <PATH TO DATABASE> [-s]
\t\tdban.py [-d] <PATH TO DATABASE> [-t] <TABLE NAME> [-hd] <TABLE HEADER> [-id] <ROWID> [-w] <WHERE> [-o] <ORDER BY> <ASCENDING OR DESCENDING> [-l] <LIMIT>
\nDetails:
\t1. Database [-d]:
\t\t[+] You MUST provide the complete path to the database inside quotation marks ("")
\t\tExample:
\t\t\tdban.py -d "C:\..\example.db"
\n\t2. Structure [-s]:
\t\t[+] It doesNOT take any arguments.
\t\t[+] It is used to show the Table Names of the database and their corresponding Headers (or columns)
\n\t3. Table [-t]:
\t\t[+] It only takes the table name as argument
\t\t[+] If you don't know the table name, feel free to see the structure of the table using the following syntax:
\t\t\tdban.py [-d] <PATH TO DATABASE> [-s]
\n\t4. Table Header [-hd]:
\t\t[+] It only takes the table header (or column) as argument
\t\t[+] If you don't know the table header, feel free to see the structure of the table using the following syntax:
\t\t\tdban.py [-d] <PATH TO DATABASE> [-s]
\t\t[+] You may provide several table headers seperated by a comma (,)
\t\tExample:
\t\t\tdban.py -d "C:\..\example.db" -t example -hd name,value
\n\t5. Rowid [-id]:
\t\t[+] It MUST be an integer value
\t\t[+] Decimals or anything else are NOT accepted
\t\t[+] You may provide several rowid seperated by a comma (,)
\t\tExample:
\t\t\tdban.py -d "C:\..\example.db" -t example -id 6780,690
\t\t\tdban.py -d "C:\..\example.db" -t example -hd name,value -id 320,6780
\n\t6. Where [-w]:
\t\t[+] It utilizes the "WHERE" clause of sqlite3 and so provides the same functionality
\t\t[+] You can provide several conditions through this argument seperated by ",AND" or ",OR"
\t\t[+] ",AND" is the same as "AND" in WHERE clause of sqlite3
\t\t[+] ",OR" is the same as "OR" in WHERE clause of sqlite3
\t\t[-] Can't handle argument when both ",AND" and ",OR" are present.
\t\t[+] This will be fixed soon
\t\t[+] Please give the "where" argument inside quotation marks
\t\tExample:
\t\t\tdban.py -d "C:\..\example.db" -t example -w "name=don"
\t\t\tdban.py -d "C:\..\example.db" -t example -w "name=don,ANDaddress=bangladesh,ANDrowid>=50"
\t\t\tdban.py -d "C:\..\example.db" -t example -hd name,value -w "value<60,ORname=joe"
\n\t7. Order By [-o]:
\t\t[+] It is the only option that takes 2 arguments
\t\t[+] 1st argument is the table header based on which the datas will be ordered by
\t\t[+] 2nd argument determines whether order will be done in ascending or descending
\t\t[+] 2nd argument ONLY takes "asc" or "desc" as arguments regardless of them being in lowercase or uppercase or mixed
\t\tExample:
\t\t\tdban.py -d "C:\..\example.db" -t example -o name asc
\t\t\tdban.py -d "C:\..\example.db" -t example -o name desc
\t\t\tdban.py -d "C:\..\example.db" -t example -o name DesC
\n\t8. Limit [-l]:
\t\t[+] It MUST be an integer value
\t\t[+] It always comes in the last option
\t\tExample:
\t\t\tdban.py -d "C:\..\example.db" -t example -l 100
\t\t\tdban.py -d "C:\..\example.db" -t example -hd name -w "nameLIKE%john%" -l 100
"""
    print(help_string)

def more_h():
    print(f"[+] For more info, type \"dban.py -h\" or simply \"dban.py\"")
    exit(0)

def struc_an(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Enables coloring in windows
    init(convert = True)

    # list all the tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")

    table_names = c.fetchall()
    print("\nTables\n---------------")
    for table_name in table_names:
        # table_name is a tuple
        print(Fore.GREEN + table_name[0] + Style.RESET_ALL)

        if table_name[0]:
            # selects all the data from table
            c.execute(f"SELECT * FROM {table_name[0]}")

            # print each row in the table
            rows = c.description
            space = " "
            for row in rows:
                print(Fore.CYAN + space * 20 + row[0] + Style.RESET_ALL)                  # prints the tuple
    c.close()



def db_fetch_handler(db, table, header, rowid, where, order_by, limit):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    if (table != "") and (header == "") and (rowid == ""):
        if where == "":
            if order_by == "":
                # Fetches full table WITH LIMIT
                if limit != "":
                    c.execute(f"SELECT rowid, * FROM {table} LIMIT {limit}")
                # Fetches FULL TABLE
                else:
                    c.execute(f"SELECT rowid, * FROM {table}") # default order by

            # Fetches full table IN ORDER WITH LIMIT
            elif order_by != "":
                property_name = order_by[0]
                asc_desc = order_by[1]
                if limit != "":
                    c.execute(f"SELECT rowid, * FROM {table} ORDER BY {property_name} {asc_desc} LIMIT {limit}")

                # Fetches full table IN ORDER
                else:
                    c.execute(f"SELECT rowid, * FROM {table} ORDER BY {property_name} {asc_desc}")
        elif where != "":
            where = where_handler(db, table, where)
            if order_by == "":
                # Fetches rows IN CONDITION WITH LIMIT
                if limit != "":
                    c.execute(f"SELECT rowid, * FROM {table} WHERE {where} LIMIT {limit}")
                # Fetches rows IN CONDITION
                else:
                    c.execute(f"SELECT rowid, * FROM {table} WHERE {where}") # default order by

            # Fetches rows IN CONDITION IN ORDER WITH LIMIT
            elif order_by != "":
                property_name = order_by[0]
                asc_desc = order_by[1]
                if limit != "":
                    c.execute(f"SELECT rowid, * FROM {table} WHERE {where} ORDER BY {property_name} {asc_desc} LIMIT {limit}")

                # Fetches rows IN CONDITION IN ORDER
                else:
                    c.execute(f"SELECT rowid, * FROM {table} WHERE {where} ORDER BY {property_name} {asc_desc}")


        # print the headers
        headers = c.description
        header_format = ""
        for header in headers:
            if header[0] == "rowid":
                header_format += header[0].ljust(10)
            else:
                header_format += header[0].ljust(50)
        print(header_format)
        underscore = "-"
        print(underscore.ljust(10+50*(len(headers)-1), "-"))

        # print the description or values of headers
        all_table_info = c.fetchall()
        for column in all_table_info:
            i = 0
            column_format = ""
            while i < len(column):
                if len(str(column[i])) > 48:
                    if i == len(column) - 1:
                        item = str(column[i])
                    else:
                        item = str(column[i])[:44] + " [..] "
                else:
                    item = str(column[i])
                if i == 0:
                    column_format = column_format + item.ljust(10)
                else:
                    column_format = column_format + item.ljust(50)
                i += 1
            print(column_format)


    # Fetches a header or column from the table
    elif (table != "") and (header != "") and (rowid == ""):
        if where == "":
            if order_by == "":
                # Fetches full column WITH LIMIT
                if limit != "":
                    c.execute(f"SELECT rowid, {header} FROM {table} LIMIT {limit}")
                # Fetches FULL HEADER/COLUMN
                else:
                    c.execute(f"SELECT rowid, {header} FROM {table}") # default order by

            # Fetches a column IN ORDER WITH LIMIT
            elif order_by != "":
                property_name = order_by[0]
                asc_desc = order_by[1]
                if limit != "":
                    c.execute(f"SELECT rowid, {header} FROM {table} ORDER BY {property_name} {asc_desc} LIMIT {limit}")
                # Fetches a column IN ORDER
                else:
                    c.execute(f"SELECT rowid, {header} FROM {table} ORDER BY {property_name} {asc_desc}")
        elif where != "":
            where = where_handler(db, table, where)
            if order_by == "":
                # Fetches rows of headers WITH LIMIT
                if limit != "":
                    c.execute(f"SELECT rowid, {header} FROM {table} WHERE {where} LIMIT {limit}")
                # Fetches rows of HEADER/COLUMN
                else:
                    c.execute(f"SELECT rowid, {header} FROM {table} WHERE {where}") # default order by

            # Fetches rows of column IN ORDER WITH LIMIT
            elif order_by != "":
                property_name = order_by[0]
                asc_desc = order_by[1]
                if limit != "":
                    c.execute(f"SELECT rowid, {header} FROM {table} WHERE {where} ORDER BY {property_name} {asc_desc} LIMIT {limit}")
                # Fetches rows of column IN ORDER
                else:
                    c.execute(f"SELECT rowid, {header} FROM {table} WHERE {where} ORDER BY {property_name} {asc_desc}")

        # print the headers
        headers = c.description
        header_format = ""
        for header in headers:
            if header[0] == "rowid":
                header_format += header[0].ljust(10)
            else:
                header_format += header[0].ljust(50)
        print(header_format)
        underscore = "-"
        print(underscore.ljust(10+50*(len(headers)-1), "-"))

        # print the description or values of headers
        fetched_info = c.fetchall()
        for r in fetched_info:
            i = 0
            r_format = ""
            while i < len(r):
                if len(str(r[i])) > 48:
                    if i == len(r) - 1:
                        item = str(r[i])
                    else:
                        item = str(r[i])[:44] + " [..] "
                else:
                    item = str(r[i])
                if i == 0:
                    r_format = r_format + item.ljust(10)
                else:
                    r_format = r_format + item.ljust(50)
                i += 1
            print(r_format)

    # Fetches a rowid from the table
    elif (table != "") and (header == "") and (rowid != ""):
        rowids = rowid.split(",")
        #row_id = ""
        for row_id in rowids:
            # Rowid checker
            try:
                int(row_id)
            except:
                print(f"[-] \"{row_id}\" is NOT valid!")
                print("[-] Please provide a valid rowid")
                more_h()
            if row_id == rowids[0]:
                r = f"rowid = {row_id}"
            else:
                r += f" OR rowid = {row_id}"
        c.execute(f"SELECT rowid, * FROM {table} WHERE {r}")

        # print the headers
        headers = c.description
        header_format = ""
        for header in headers:
            if header[0] == "rowid":
                header_format += header[0].ljust(10)
            else:
                header_format += header[0].ljust(50)
        print(header_format)
        underscore = "-"
        print(underscore.ljust(10+50*(len(headers)-1), "-"))
        
        # print the description or values of headers
        all_table_info = c.fetchall()
        for column in all_table_info:
            i = 0
            column_format = ""
            while i < len(column):
                if len(str(column[i])) > 48:
                    if i == len(column) - 1:
                        item = str(column[i])
                    else:
                        item = str(column[i])[:44] + " [..] "
                else:
                    item = str(column[i])
                if i == 0:
                    column_format = column_format + item.ljust(10)
                else:
                    column_format = column_format + item.ljust(50)
                i += 1
            print(column_format)

    c.close()

def arg_validator(database, table, hdr, order_by, limit):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    table_matched = False
    order_by_0 = False
    hdr_matched = 0

    # Table Name checker
    c.execute("SELECT name FROM sqlite_master WHERE type='table';") # list all the tables

    table_names = c.fetchall()
    for table_name in table_names:
        if table == table_name[0]:
            table_matched = True
    if table_matched == False:
        print("[-] No such table Found!")
        more_h()

    # Header checker
    if hdr != "":
        hdr = hdr.split(",")
        hdr_len = len(hdr)
        c.execute(f"SELECT rowid, * FROM {table}")
        headers = c.description
        for header in headers:
            for i in hdr:
                if i == header[0]:
                    hdr_matched += 1
        if hdr_matched != hdr_len:
            print("[-] No such column exists!")
            more_h()
    
    # Order Checker
    if order_by != "":
        c.execute(f"SELECT rowid, * FROM {table}")
        headers = c.description
        for header in headers:
            if order_by[0] == header[0]:
                order_by_0 = True
        if order_by_0 == False:
            print("[-] No such column exists!")
            more_h()

        if (order_by[1].lower() == "asc") or (order_by[1].lower() == "desc"):
            pass
        else:
            print("[-] Please type \"asc\" or \"desc\" as argument of order (regardless of small letter or captial letter)")
            more_h()

    # Limit Checker
    if limit != "":
        try:
            int(limit)
        except:
            print(f"[-] \"{limit}\" is NOT an integer!")
            print("[-] Please provide an integer value for limit.")
            more_h()

    c.close()


def where_handler(db, table, where):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(f"SELECT rowid, * FROM {table}")
    headers = c.description
    
    where_math = False
    header_match = 0
    condi_splitter = ""
    splitter = ""
    where_clause = ""
    
    if ",AND" in where:
        condi_splitter = ",AND"
    elif ",OR" in where:
        condi_splitter = ",OR"
    else:
        if ">=" in where:
            splitter = ">="
            where_math = True
        elif "<=" in where:
            splitter = "<="
            where_math = True
        elif ">" in where:
            splitter = ">"
            where_math = True
        elif "<" in where:
            splitter = "<"
            where_math = True
        elif "=" in where:
            splitter = "="
        elif "LIKE" in where:
            splitter = "LIKE"
        else:
            print("[-] Invalid WHERE Clause")
            c.close()
            more_h()
        condi_array = where.split(f"{splitter}")

        # Header Checker
        for header in headers:
            if condi_array[0] == header[0]:
                header_match = 1
        if header_match != 1:   # Only 1 condition/tuple
            print("[-] No such column exists!")
            more_h()

        if where_math == False:
            condition_formatted = f"{condi_array[0]} {splitter} '{condi_array[1]}'"
        else:
            condition_formatted = f"{condi_array[0]} {splitter} {condi_array[1]}"
        c.close()
        return condition_formatted

    conditions = where.split(f"{condi_splitter}")
    for condition in conditions:
        if ">=" in condition:
            splitter = ">="
            where_math = True
        elif "<=" in condition:
            splitter = "<="
            where_math = True
        elif ">" in condition:
            splitter = ">"
            where_math = True
        elif "<" in condition:
            splitter = "<"
            where_math = True
        elif "=" in condition:
            splitter = "="
        elif "LIKE" in condition:
            splitter = "LIKE"
        else:
            print("[-] Invalid WHERE Clause")
            c.close()
            more_h()
        
        condi_array = condition.split(f"{splitter}")

        # Header Checker
        for header in headers:
            if condi_array[0] == header[0]:
                header_match += 1
        
        if where_math == False:
            condition_formatted = f"{condi_array[0]} {splitter} '{condi_array[1]}'"
        else:
            condition_formatted = f"{condi_array[0]} {splitter} {condi_array[1]}"

        if condition == conditions[0]:
            where_clause = condition_formatted
        else:
            where_clause += f" {condi_splitter[1:]} {condition_formatted}"

    if header_match != len(conditions):
            print("[-] No such column exists!")
            more_h()
    c.close()
    return where_clause


def main():
    table = ""
    header = ""
    rowid = ""
    where = ""
    order_by = ""
    limit = ""

    # Help
    if len(argv) == 1:
        help()
        exit(0)

    # Help
    if argv[1] == "-h":
        help()
        exit(0)

    if len(argv) < 4:
        print("Error: arguments must be equal to or greater than 3")
        more_h()

    # database
    if argv[1] == "-d":
        database = argv[2]
        if os.path.isfile(database) == False:
            print("[-] database NOT Found!")
            more_h()

    # analyse the structue
    if argv[3] == "-s":
        struc_an(database)

    # Table
    elif argv[3] == "-t":
        try:
            table = argv[4]
        except:
            print("[-] Table Name cannot be empty...")
            more_h()
        arg_validator(database, table, header, order_by, limit)
        
        # Full table fetch
        if len(argv) == 5:
            db_fetch_handler(database, table, header, rowid, where, order_by, limit)

        elif len(argv) == 7:
            # Fetches a single row
            if argv[5] == "-id":
                rowid = argv[6]
                db_fetch_handler(database, table, header, rowid, where, order_by, limit)
            # Fetches full table WITH LIMIT
            elif argv[5] == "-l":
                limit = argv[6]
                arg_validator(database, table, header, order_by, limit)
                db_fetch_handler(database, table, header, rowid, where, order_by, limit)
            # Feteches A FULL header
            elif argv[5] == "-hd":
                header = argv[6]
                arg_validator(database, table, header, order_by, limit)
                db_fetch_handler(database, table, header, rowid, where, order_by, limit)
            # Fetches rows IN CONDITION
            elif argv[5] == "-w":
                where = argv[6]
                db_fetch_handler(database, table, header, rowid, where, order_by, limit)
            else:
                print("[-] Invalid Argument")
                more_h()

        elif len(argv) == 8:
            # Fetches full table IN ORDER
            if argv[5] == "-o":
                order_by = [argv[6], argv[7]]
                arg_validator(database, table, header, order_by, limit)
                db_fetch_handler(database, table, header, rowid, where, order_by, limit)
            else:
                print("[-] Invalid Argument")
                more_h()

        elif len(argv) == 9:
            # Fetches full header WITH LIMIT
            if argv[5] == "-hd":
                header = argv[6]
                if argv[7] == "-l":
                    limit = argv[8]
                    arg_validator(database, table, header, order_by, limit)
                    db_fetch_handler(database, table, header, rowid, where, order_by, limit)
                # Fetches rows of header in Conditon
                elif argv[7] == "-w":
                    where = argv[8]
                    db_fetch_handler(database, table, header, rowid, where, order_by, limit)
                else:
                    print("[-] Invalid Argument")
                    more_h()
            # Fetches rows IN CONDITION WITH LIMIT
            elif argv[5] == "-w":
                where = argv[6]
                if argv[7] == "-l":
                    limit = argv[8]
                    arg_validator(database, table, header, order_by, limit)
                    db_fetch_handler(database, table, header, rowid, where, order_by, limit)
                else:
                    print("[-] Invalid Argument")
                    more_h()
            else:
                print("[-] Invalid Argument")
                more_h()

        elif len(argv) == 10:
            # Feteches Full table IN ORDER WITH LIMIT
            if argv[5] == "-o":
                order_by = [argv[6], argv[7]]
                arg_validator(database, table, order_by, limit)
                if argv[8] == "-l":
                    limit = argv[9]
                    arg_validator(database, table, header, order_by, limit)
                    db_fetch_handler(database, table, header, rowid, where, order_by, limit)
                else:
                    print("[-] Invalid Argument")
                    more_h()
            # Fetches a Full Header IN ORDER
            elif argv[5] == "-hd":
                header = argv[6]
                if argv[7] == "-o":
                    order_by = [argv[8], argv[9]]
                    arg_validator(database, table, header, order_by, limit)
                    db_fetch_handler(database, table, header, rowid, where, order_by, limit)
                else:
                    print("[-] Invalid Argument")
                    more_h()
            # Fetches rows IN CONDITION IN ORDER
            elif argv[5] == "-w":
                where = argv[6]
                if argv[7] == "-o":
                    order_by = [argv[8], argv[9]]
                    arg_validator(database, table, header, order_by, limit)
                    db_fetch_handler(database, table, header, rowid, where, order_by, limit)
                else:
                    print("[-] Invalid Argument")
                    more_h()
            else:
                print("[-] Invalid Argument")
                more_h()

        elif len(argv) == 11:
            # Fetches rows of headers IN CONDITION WITH LIMIT
            if argv[5] == "-hd":
                header = argv[6]
                if argv[7] == "-w":
                    where = argv[8]
                    if argv[9] == "-l":
                        limit = argv[10]
                        arg_validator(database, table, header, order_by, limit)
                        db_fetch_handler(database, table, header, rowid, where, order_by, limit)
                    else:
                        print("[-] Invalid Argument")
                        more_h()
                else:
                    print("[-] Invalid Argument")
                    more_h()
            else:
                print("[-] Invalid Argument")
                more_h()

        elif len(argv) == 12:
            # Fetches a Full Header IN ORDER WITH LIMIT
            if argv[5] == "-hd":
                header = argv[6]
                if argv[7] == "-o":
                    order_by = [argv[8], argv[9]]
                    arg_validator(database, table, header, order_by, limit)
                    if argv[10] == "-l":
                        limit = argv[11]
                        arg_validator(database, table, header, order_by, limit)
                        db_fetch_handler(database, table, header, rowid, where, order_by, limit)
                    else:
                        print("[-] Invalid Argument")
                        more_h()
                # Fetches rows of header IN CONDITION IN ORDER
                elif argv[7] == "-w":
                    where = argv[8]
                    if argv[9] == "-o":
                        order_by = [argv[10], argv[11]]
                        arg_validator(database, table, header, order_by, limit)
                        db_fetch_handler(database, table, header, rowid, where, order_by, limit)
                    else:
                        print("[-] Invalid Argument")
                        more_h()
                else:
                    print("[-] Invalid Argument")
                    more_h()
            # Fetches rows IN CONDITION IN ORDER WITH LIMIT
            elif argv[5] == "-w":
                where = argv[6]
                if argv[7] == "-o":
                    order_by = [argv[8], argv[9]]
                    arg_validator(database, table, header, order_by, limit)
                    if argv[10] == "-l":
                        limit = argv[11]
                        arg_validator(database, table, header, order_by, limit)
                        db_fetch_handler(database, table, header, rowid, where, order_by, limit)
                    else:
                        print("[-] Invalid Argument")
                        more_h()
                else:
                    print("[-] Invalid Argument")
                    more_h()
            else:
                print("[-] Invalid Argument")
                more_h()

        elif len(argv) == 14:
            # Fetches rows of headers IN CONDITION IN ONDER WITH LIMIT
            if argv[5] == "-hd":
                header = argv[6]
                if argv[7] == "-w":
                    where = argv[8]
                    if argv[9] == "-o":
                        order_by = [argv[10], argv[11]]
                        arg_validator(database, table, header, order_by, limit)
                        if argv[12] == "-l":
                            limit = argv[13]
                            arg_validator(database, table, header, order_by, limit)
                            db_fetch_handler(database, table, header, rowid, where, order_by, limit)
                        else:
                            print("[-] Invalid Argument")
                            more_h()
                    else:
                        print("[-] Invalid Argument")
                        more_h()
                else:
                    print("[-] Invalid Argument")
                    more_h()
            else:
                print("[-] Invalid Argument")
                more_h()

        else:
            print("[-] Invalid Argument")
            more_h()
            
    else:
        print("[-] Invalid Argument")
        more_h()


if __name__ == "__main__":
    main()
