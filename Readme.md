# Main
Main is a python application that answers the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Usage
This application can only be used to display the answers to the three questions above.

## Application Design
Main.py is designed with three classes:

```python
class Question1:
    def runquery(self):
        
class Question2:
    def runquery(self):
        
class Question3:
    def runquery(self):

if __name__ == "__main__":
    question1 = Question1()
    question1.runquery()
    question2 = Question2()
    question2.runquery()
    question3 = Question3()
    question3.runquery()

```

Each class has a function that is called by the application titled 'runquery'.
Within runquery the following occurs:

1. A connection is made to the news database
2. A cursor is created
3. A select statement is built
4. The select statement is executed and stored
5. The result is iterated in a for loop
6. The result is displayed to the user
7. The connection to the database is closed

## Instructions to Run Application
In order to run the application a user will need:
1. Python2 or Python3 installed
2. Access to a terminal application
3. Access to the news database
4. main.py file

To run the application:

Open a terminal window

```bash
$ cd my-directory
$ python3 main.py
```
