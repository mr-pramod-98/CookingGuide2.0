from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import Http404
import mysql.connector
from .ScrapyProject.Recipes.Recipes.spiders.user_input import UserInput
import os


class CookingGuide:

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.mydatabase = mysql.connector.connect(host='localhost', user='root', passwd='password', database='recipe_test')
        self.mycursor = self.mydatabase.cursor()

    # "fetch_data" METHOD IS USED TO FETCH DATA FROM THE SPECIFIED TABLE IN THE SPECIFIED DATABASE
    def fetch_data(self, table_name):

        # "cooking_recipes" CONTAINS LIST OF DICTIONARIES
        cooking_recipes = []

        try:
            # "table_name" IS NAME OF THE TABLE FROM WHICH DATA HAS TO BE FETCHED
            query = "SELECT * FROM " + table_name + " ORDER BY TIME DESC"
            self.mycursor.execute(query)

            # "title", "ingredients" AND "directions" ARE THE COLUMN-NAME'S IN THE TABLE
            for (title, ingredients, directions, time) in self.mycursor:
                recipes = {
                            "title": title,
                            "ingredients": ingredients,
                            "directions": directions,
                            "time": time
                           }
                cooking_recipes.append(recipes)

        except mysql.connector.errors.ProgrammingError:
            raise Http404("NO ACCOUNT CREATED BY THE NAME " + table_name)

        # RETURNING LIST OF RECIPES AS LIST OF DICTIONARY
        return cooking_recipes

    # "delete_data" METHOD IS USED TO DELETE A SPECIFIED RECORD FROM THE SPECIFIED TABLE IN THE SPECIFIED DATABASE
    def delete_data(self, table_name, item):

        # QUERY TO DELETE THE SPECIFIED RECORD
        query = "DELETE FROM " + table_name + " WHERE TITLE = %s"
        self.mycursor.execute(query, (item, ))

        # SAVING CHANGES
        self.mydatabase.commit()

        # CLOSING
        self.mycursor.close()
        self.mydatabase.close()

    # "delete_my_account" METHOD IS USED TO DELETE THE SPECIFIED ACCOUNT(table) FROM THE DATABASE
    def delete_my_account(self, table_name):

        # DELETING THE CORRESPONDING ENTRY FROM THE "User" TABLE
        User.objects.filter(username=table_name).delete()

        # DELETING THE USER ACCOUNT FROM THE DATABASE (i.e, dropping the corresponding table)
        self.mycursor.execute("DROP TABLE " + table_name)


class RunCrawler:

    def crawler(self):

        # MOVING TO THE DIRECTORY WHERE THE "spiders" ARE PRESENT
        os.chdir('cook/ScrapyProject/Recipes')

        # INITIATING THE CRAWLER
        os.system('scrapy crawl recipes')

        # MOVING BACK TO THE PREVIOUS WORKING DIRECTORY
        os.chdir('../../..')


# Create your views here.

# "index" METHOD IS CALLED WHET THE USER REQUEST FOR "index" PAGE
def index(request):
    return render(request, "index.html")


# "cook_guide" METHOD IS CALLED WHET THE USER LOGIN'S SUCCESSFULLY AND EVERY-TIME USER CLICK'S CRAWL BUTTON
def cook_guide(request, username):

    # IF THE REQUEST METHOD IS POST EXECUTE if BLOCK
    if request.method == "POST":

        item = request.POST['item name']

        # CHECKING WEATHER "item" ACTUALLY CONTAINS SOMETHING OR NOT
        # RUN SPIDER IF "item" CONTAINS SOMETHING
        if len(item) > 0:
            
            # WRITE THE "item" AND "username" ON TO THE "connector" FILE USING THE "set_item_and_tablename" METHOD
            connector = UserInput()
            UserInput.set_item_and_tablename(connector, item, username)

            # RUN THE WEB-CRAWLER BY CALLING THE "crawler" METHOD
            crawl = RunCrawler()
            crawl.crawler()

        # REDIRECTING BACK TO THE SAME PAGE AFTER CRAWLING
        return redirect('/cook_guide/' + username)

    # IF THE REQUEST METHOD IS GET EXECUTE else BLOCK
    else:

        # "username" IS THE NAME OF THE TABLE
        data = CookingGuide()
        cooking_recipes = data.fetch_data(username)
        return render(request, "cook_guide.html", {'cooking_recipes': cooking_recipes})


# "delete" METHOD IS CALLED WHET THE USER CLICKS DELETE BUTTON
def delete(request, username, title):

    # DELETE THE SPECIFIED ITEM(title) FROM THE SPECIFIED TABLE(username) BY CALLING "delete_data" METHOD
    data = CookingGuide()
    data.delete_data(username, title)

    # REDIRECTING BACK TO THE SAME PAGE AFTER DELETING
    return redirect('/cook_guide/' + username)


def delete_account(request, username):

    # DELETE THE SPECIFIED ACCOUNT(table_name/username) FROM THE DATABASE AND
    # THE CORRESPONDING USER ENTRY IN THE "User" TABLE,
    # BY CALLING "delete_MyAccount" METHOD
    account = CookingGuide()
    account.delete_my_account(username)

    # REDIRECTING THE USER TO THE INDEX(HOME) PAGE AFTER DELETING THE USER'S ACCOUNT
    return redirect('/')
