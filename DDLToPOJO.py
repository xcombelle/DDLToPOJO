import sqlparse, re


def main():

        with open('yourDDL.ddl') as ddl_file:
            
            sql = ddl_file.read()
            ddls = sqlparse.split(sql)

            # Creating Regex filters
            create_tables_regex = re.compile("^CREATE TABLE.*\(")
            primary_keyword_regex = re.compile("^\tPRIMARY KEY")
            sys_columns_regex = re.compile(r"^\tSYS_.*$")
            comma_regex = re.compile(" ")
            java_classes = []
            # In Create Statement
            for ddl in ddls:
                members = []
                # In each line of CREATE Statement
                for line in ddl.splitlines():
                    # Determining if the regex filter is a match
                    create_table_match = create_tables_regex.match(line) is not None
                    primary_keyword_regex_match = primary_keyword_regex.match(line) is not None
                    comma_regex_match = comma_regex.match(line) is not None
                    sys_columns_match = sys_columns_regex.match(line) is not None
                    # Extracting the File/Class name from Create Statements
                    if create_table_match:
                        list = re.split("[\s]+|[.]", line)
                        if len(list) >= 2:
                            table_name_list = list[len(list) - 2].split("_")
                            table_name = ''
                            for table_item in table_name_list:
                                table_name += table_item.capitalize()
                    # Filtering out the non essential lines in DDL and focusing on the SQL DataType Columns
                    elif not create_table_match and not primary_keyword_regex_match and not comma_regex_match and not sys_columns_match:
                        list = re.split("\s", line)
                        if len(list) >= 3:
                            name_list = list[1].split("_")
                            member_name = ''
                            if len(name_list) == 1:
                                member_name = name_list[0].lower()
                            else:
                                first = True
                                for item in name_list:
                                    if first:
                                        first = False
                                        member_name += item.lower()
                                    else:
                                        member_name += item.capitalize()
                            # Converting SQL Data Types to Java Data Types
                            data_type = ''
                            for sql_type in data_types.keys():
                                if sql_type in list[2]:
                                    data_type = data_types.get(sql_type)
                                    break
                            member = {'member_name': member_name, 'data_type': data_type}
                            members.append(member)

                    # Creating imports
                    import_sets = set()
                    for member in members:
                        if member.get('data_type') in 'Date':
                            import_sets.add('import java.sql.Date;')
                        if member.get('data_type') in 'Timestamp':
                            import_sets.add('import java.sql.Timestamp;')
                        if member.get('data_type') in 'BigDecimal':
                            import_sets.add('java.math.BigDecimal;')

                    # Create Java Model Object
                    javaObj = JavaObj(table_name, members, import_sets)

                # Add Model to list of java_classes
                java_classes.append(javaObj)

            # Creating files for each Java Class in the list
            for jObj in java_classes:
                createClass(jObj)


    def upcase_first_letter(s):
        return s[0].upper() + s[1:]

    #
    # Writing my Java Class to file
    #
    def createClass(jObj):
        # Creating the File based of jObj name
        javaFilePath = 'your/file/path/here/' + jObj.name + '.java'
        f = open(javaFilePath, 'w')
        # Adding the package information to file
        f.write(jObj.package + '\n\n')
        # Adding Import statements
        for item in jObj.imports:
            print jObj.name
            print(item)
            f.write(item + '\n')
        f.write('\n')
        f.write('public class ' + jObj.name + ' {\n\n')

        # Starting body of Class
        for member in jObj.members:
            f.write('\tprivate ' + member.get('data_type') + ' ' + member.get('member_name') + ';\n')

        # Starting Constuctor
        constructor = '\npublic ' + jObj.name + '('
        i = 1
        for member in jObj.members:
            if i == len(jObj.members):
                constructor += member.get('data_type') + ' ' + member.get('member_name') + ''
            else:
                constructor += member.get('data_type') + ' ' + member.get('member_name') + ', '
            i += 1
        # i = 0
        constructor += ') {\n\n'

        f.write(constructor)
        # Writing getters to file
        for member in jObj.members:
            f.write('\tthis.' + member.get('member_name') + ' = ' + member.get('member_name') + ';\n')
        f.write('\n')
        for member in jObj.members:
            f.write('\n\tpublic ' + member.get('data_type') + ' get' + upcase_first_letter(
                member.get('member_name')) + '() {\n\t\treturn ' + member.get('member_name') + ';\n\t}')
        f.write('\n}\n')
        f.close()

    #
    # My Java Class Model
    #
    class JavaObj(object):
        """
            Attributes:
                name: String representing the name of the java class
                members:  List of member names and datatypes
                imports: Set of import statements
        """

        # Hard code the package you want your files to belong to
        package = "domain"

        def __init__(self, name, members, imports):
            self.name = name
            self.members = members
            self.imports = imports


    data_types = {'VARCHAR2': 'String', 'CHAR': 'String', 'NUMBER': 'BigDecimal', 'DATE': 'Date',
                  'TIMESTAMP': 'Timestamp'}


if __name__ == "__main__":
    main()
    '''
        This saved me from writing 3310 lines of code :)
        add package
        add constuctor
        add getters
        add setters

        import java.util.Date;
        java.math.BigDecimal
        import java.sql.Timestamp
        import java.sql.Date
    '''
