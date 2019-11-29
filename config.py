from configparser import ConfigParser
  
def config(filename='voem_web.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        dbparams = parser.items(section)
        for dbparam in dbparams:
            db[dbparam[0]] = dbparam[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db