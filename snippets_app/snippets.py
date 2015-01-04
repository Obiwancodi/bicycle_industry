import logging
import argparse
import sys
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")



def put(name, snippet, hide, unhide, no_hide, show):
    
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    with connection,connection.cursor() as cursor: 
        cursor.execute("select * from snippets where keyword=%s", (name,))
        row_exists = cursor.fetchone()
        if row_exists:
            cursor.execute("update snippets set message=%s where keyword=%s", (snippet, name))
        else:
            cursor.execute( "insert into snippets values (%s, %s)", (name, snippet))
    logging.debug("Snippet stored successfully.")
    return name, snippet, hide, unhide, no_hide, show
    
def catalog():
    logging.info("Retrieving keywords")
    cursor = connection.cursor()
    cursor.execute( "select * from snippets where hidden=false order by keyword", )
    keys = cursor.fetchall()
    connection.commit()
    print keys
   

      
def search(word):
    logging.info("Searching for word in snippet")
    cursor = connection.cursor()
    command = "select * from snippets where message like %s and hidden=false"
    sure = '%' + word + '%'
    cursor.execute(command, (sure,))
    words = cursor.fetchall()
    connection.commit()
    print words
    
def get(name):
    logging.info("Retrieving snippet {!r}".format(name))
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s and hidden=False", (name,))
        row = cursor.fetchone()
        return row[0]
   



def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    put_parser.add_argument("--hide", help="Hide snippet from search and catalog", default=False, action="store_true")
    put_parser.add_argument("--unhide", help="Unhide snippet from search and catalog", default=True, action="store_false")
    put_parser.add_argument("--no_hide", help="Unhide all snippets from search and catalog", default=True, action="store_false")
    put_parser.add_argument("--show", help="Show hidden snippets", default=False, action="store_true")
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")
    
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Shows keywords")
    
    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search", help="Find a word in a snippet")
    search_parser.add_argument("word", help="The word in the snippet")
    
    arguments = parser.parse_args(sys.argv[1:])
    
    
    arguments = vars(arguments)
            
    command = arguments.pop("command")

    
    
    if command == "put":
        name, snippet, hide, unhide, no_hide, show = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name,)) 
        
        if arguments["hide"]==True:
            with connection,connection.cursor() as cursor:
                cursor.execute("update snippets set hidden=True where keyword=%s",(name,))
                connection.commit()
                
        elif arguments["show"]==True:
            with connection, connection.cursor() as cursor:
                cursor.execute("select * from snippets where hidden=True")
                hides = cursor.fetchall()
                connection.commit()
                print hides
                
        elif arguments["unhide"] == False:
            with connection,connection.cursor() as cursor:
                cursor.execute("update snippets set hidden=False where keyword=%s",(name,))
                connection.commit()

        elif arguments["no_hide"] == False:
            with connection,connection.cursor() as cursor:
                cursor.execute("update snippets set hidden=False",)
                connection.commit()
        
                      
                        
    elif command == "catalog":
        catalog()
    
    elif command == "search":
        word = search(**arguments)
        print ("Retrieved snippets")
        
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
        
            
if __name__ == "__main__":
    main()
    connection.close()