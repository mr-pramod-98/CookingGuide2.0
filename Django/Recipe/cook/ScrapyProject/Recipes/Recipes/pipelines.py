# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
from datetime import datetime
from .spiders.user_input import UserInput


class RecipesPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.mydatabase = mysql.connector.connect(host='localhost', user='root', passwd='password', database='recipe_test')
        self.mycursor = self.mydatabase.cursor()

    def store_to_database(self, item):

        # FETCHING TABLE NAME BY USING "get_tablename" METHOD
        table = UserInput()
        table_name = UserInput.get_tablename(table)

        try:
            # CONVERTING THE LIST OF INGREDIENTS INTO STRING
            ingredients = ''
            for ingredient in item['ingredients']:

                # IGNORING THE STRING "Add all ingredients to list"
                if ingredient == "Add all ingredients to list":
                    continue
                ingredients = ingredients + ingredient + "\n"

            # CONVERTING THE LIST COOKING PROCEDURE INTO STRING
            procedures = ''
            for procedure in item['procedures']:
                procedures = procedures + procedure + "\n"

            # GETTING CURRENT DATE AND TIME  OF INSERTION
            timestamp = datetime.now()

            query = "INSERT INTO " + table_name + "(TITLE, INGREDIENTS, DIRECTIONS, TIME) VALUES(%s, %s, %s, %s)"
            values = (item['title'], ingredients, procedures, timestamp)

            self.mycursor.execute(query, values)
            self.mydatabase.commit()

        # EXCEPTS THE "IntegrityError" (i.e, INSERTING A TUPLE WHICH ALREADY EXIST)
        except mysql.connector.errors.IntegrityError:
            pass

        print(self.mycursor.rowcount, "record inserted")

    def process_item(self, item, spider):
        self.store_to_database(item)
        return item
