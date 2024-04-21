import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="uniquec",
  database = "stock"
)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Execute a SELECT query
cursor.execute("SELECT * FROM CUSTUMER")

# Fetch the results
rows = cursor.fetchall()

# Print the column headers
columns = [desc[0] for desc in cursor.description]
print("\t".join(columns))

# Iterate through the results and print each row
for row in rows:
    print("\t".join(str(value) for value in row))

# Close the cursor and connection
cursor.close()
conn.close()
