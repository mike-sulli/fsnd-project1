#!/usr/bin/env python3

import psycopg2


class Question1:
    DBNAME = "news"

    def runquery(self):
        print("Question 1 - What are the most popular three " +
              "articles of all time?:\n")

        dbconnection = psycopg2.connect(database=self.DBNAME)
        dbcursor = dbconnection.cursor()

        selectstatement = """
            SELECT newArticles.title,
                count(log.id) as success_count
            FROM (SELECT
                    title,
                    '/article/' || slug as newSlug
                FROM articles) as newArticles
            INNER JOIN log
            ON newArticles.newSlug = log.path
            GROUP BY newArticles.title, log.path
            HAVING path != '/'
            ORDER BY success_count desc limit 3;"""

        dbcursor.execute(selectstatement)
        records = dbcursor.fetchall()

        for record in records:
            articlename = record[0]
            articlecount = record[1]
            print("\t-{}: {} views".format(articlename, articlecount))

        dbconnection.close()


class Question2:
    DBNAME = "news"

    def runquery(self):
        print("\nQuestion 2 - Who are the most popular article " +
              "authors of all time?:\n")

        dbconnection = psycopg2.connect(database=self.DBNAME)
        dbcursor = dbconnection.cursor()

        selectstatement = """
            SELECT authors.name,
                SUM(articlesuccess.success) as views
            FROM (SELECT newlog.newpath,
                    articles.slug,
                    articles.author,
                    newlog.success
                FROM (SELECT
                        REPLACE(path, '/article/', '') as newpath,
                        status,
                        count(id) as success
                    FROM log
                    GROUP BY path, status
                    HAVING status = '200 OK' AND path != '/') as newlog
                    INNER JOIN articles
                    ON newlog.newpath = articles.slug) as articlesuccess
            INNER JOIN authors
            ON articlesuccess.author = authors.id
            GROUP BY authors.name
            ORDER BY views desc;"""

        dbcursor.execute(selectstatement)
        records = dbcursor.fetchall()

        for record in records:
            authorname = record[0]
            viewcount = record[1]
            print("\t-{}: {} views".format(authorname, viewcount))

        dbconnection.close()


class Question3:
    DBNAME = "news"

    def runquery(self):
        print("\nQuestion 3 - On which days did more than 1% " +
              "of requests lead to errors?:\n")

        dbconnection = psycopg2.connect(database=self.DBNAME)
        dbcursor = dbconnection.cursor()

        selectstatement = """
            SELECT success.requestdate,
                ROUND(failure.statuscount::numeric/
                success.statuscount::numeric, 4) * 100 as failureratio
            FROM (SELECT time::date as requestdate,
                    status,
                    count(id) as statuscount
                FROM log
                GROUP BY requestdate, status
                HAVING status = '200 OK') as success
                LEFT OUTER JOIN (SELECT time::date as requestdate,
                    status,
                    count(id) as statuscount
                    FROM log
                    GROUP BY requestdate, status
                    HAVING status = '404 NOT FOUND') as failure
            ON success.requestdate = failure.requestdate
            GROUP BY
                success.requestdate,
                failure.statuscount,
                success.statuscount
            HAVING
                ROUND(failure.statuscount::numeric/
                success.statuscount::numeric, 4) > 0.01;"""

        dbcursor.execute(selectstatement)
        records = dbcursor.fetchall()

        for record in records:
            recorddate = record[0]
            failureratio = record[1]
            print("\t-{}: {}% errors".format(recorddate, failureratio))

        dbconnection.close()


if __name__ == "__main__":
    question1 = Question1()
    question1.runquery()
    question2 = Question2()
    question2.runquery()
    question3 = Question3()
    question3.runquery()
