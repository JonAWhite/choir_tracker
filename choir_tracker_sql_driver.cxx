#include <mysql.h>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <cstring>


// just going to input the general details and not the port numbers
struct connection_details
{
    char *server;
    char *user;
    char *password;
    char *database;
};

MYSQL* mysql_connection_setup(struct connection_details mysql_details)
{
     // first of all create a mysql instance and initialize the variables within
    MYSQL *connection = mysql_init(NULL);

    // connect to the database with the details attached.
    if (!mysql_real_connect(connection,mysql_details.server, mysql_details.user, mysql_details.password, mysql_details.database, 0, NULL, 0)) {
      printf("Conection error : %s\n", mysql_error(connection));
      exit(1);
    }
    return connection;
}

MYSQL_RES* mysql_perform_query(MYSQL *connection, char *sql_query)
{
   // send the query to the database
   if (mysql_query(connection, sql_query))
   {
      printf("MySQL query error : %s\n", mysql_error(connection));
      exit(1);
   }

   return mysql_use_result(connection);
}

int main()
{
  MYSQL *conn;      // the connection
  MYSQL_RES *res;   // the results
  MYSQL_ROW row;    // the results row (line by line)

  struct connection_details mysqlD;

  std::string server = std::getenv("MYSQL_PORT_3306_TCP_ADDR");
  mysqlD.server = new char[server.length() + 1];  // where the mysql database is
  strncpy(mysqlD.server, server.c_str(), server.length() + 1);

  std::string user("root");
  mysqlD.user = new char[user.length() + 1];     // the root user of mysql   
  strncpy(mysqlD.user, user.c_str(), user.length() + 1);

  std::string password("my-secret-pw");
  mysqlD.password = new char[password.length() + 1]; // the password of the root user in mysql
  strncpy(mysqlD.password, password.c_str(), password.length() + 1);

  std::string database("mysql");
  mysqlD.database = new char[database.length() + 1];    // the database to pick
  strncpy(mysqlD.database, database.c_str(), database.length() + 1);

  // connect to the mysql database
  conn = mysql_connection_setup(mysqlD);

  // assign the results return to the MYSQL_RES pointer
  std::string query("show tables"); 
  char* my_query = new char[query.length() + 1];
  strncpy(my_query, query.c_str(), query.length() + 1);

  res = mysql_perform_query(conn, my_query);

  printf("MySQL Tables in mysql database:\n");
  while ((row = mysql_fetch_row(res)) !=NULL)
      printf("%s\n", row[0]);
   // clean up the database result set 
  mysql_free_result(res);
  // clean up the database link 
  mysql_close(conn);

  delete [] mysqlD.server;
  delete [] mysqlD.user;
  delete [] mysqlD.password;
  delete [] mysqlD.database;
  delete [] my_query;

  return 0;
}
