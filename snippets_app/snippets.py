import logging
import argparse
import sys
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")



def put(name, snippet):
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    with connection,connection.cursor() as cursor: 
        try:
            cursor.execute( "insert into snippets values (%s, %s)", (name, snippet))
        except psycopg2.IntegrityError as e:
            connection.rollback()
            cursor.execute("update snippets set message=%s where keyword=%s", (snippet, name))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet
    
def catalog():
    logging.info("Retrieving keywords")
    cursor = connection.cursor()
    cursor.execute( "select * from snippets order by keyword", )
    keys = cursor.fetchall()
    connection.commit()
    print keys
    
      
def search(word):
    logging.info("Searching for word in snippet")
    cursor = connection.cursor()
    command = "select * from snippets where message like %s"
    sure = ['%' + word +'%']
    cursor.execute(command, sure,)
    words = cursor.fetchall()
    connection.commit()
    print words

def get(name):
    logging.info("Retrieving snippet {!r}".format(name))
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        row = cursor.fetchone()
    if row:
        return row[0]
    else:
        print "Sorry that snippet does not exist."
    

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
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name)) 
        
    elif command == "catalog":
        it = catalog()
        return it
    
    elif command == "search":
        word = search(**arguments)
        print ("Retrieved snippets")
        
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))

if __name__ == "__main__":
    main()