from fuzzywuzzy import process


class UserInput:

    def set_item_and_tablename(self, item, table_name):

        # OPEN THE FILE "test" AND WRITE THE "item" AND "table_name" NAME's TO THE FILE
        # AND SEPERATE THEM BY A SPACE
        f = open("/home/pramod/PycharmProjects/CookingGuide/Django/Recipe/connector", "w")
        f.write(item + " " + table_name)
        f.close()

    def get_item(self):

        # INITIALLY "index" POINT TO THE LAST CHARECTER
        index = -1
        f = open("/home/pramod/PycharmProjects/CookingGuide/Django/Recipe/connector", "r")
        text = f.read()

        # FINDING THE FIRST SPACE FROM THE END
        while text[index] != " ":
            index -= 1

        f.close()

        # "text[:index]" CONTAINS THE ITEM NAME
        return text[:index]

    def get_tablename(self):

        # INITIALLY "index" POINT TO THE LAST CHARECTER
        index = -1
        f = open("/home/pramod/PycharmProjects/CookingGuide/Django/Recipe/connector", "r")
        text = f.read()

        # FINDING THE FIRST SPACE FROM THE END
        while text[index] != " ":
            index -= 1

        f.close()

        # "text[index + 1:]" CONTAINS THE TABLE NAME
        return text[index + 1:]


class Filter:

    def optimize_search_result(self, string, reference):

        # reference -> {title : url}
        choices = []
        optimized_result = {}

        # CREATING A LIST USING THE keys IN THE "reference"
        for key in reference.keys():
            choices.append(key)

        # GETTING RELAVENT SEARCH RESULTS
        # result -> [(title, probability)]
        results = process.extract(string, choices, limit=5)

        # OPTIMIZING THE SEARCH RESULTS
        # optimized_result -> {title : url}
        for item in results:
            if item[1] > 70:
                optimized_result[item[0]] = reference[item[0]]

        return optimized_result
