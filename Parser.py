class Parser:

    FILE_NAME = "picList.txt"
    USER_INFORMATION = "user.txt"

    @staticmethod
    def readList():

        picList = [None] # para lang ma normalize na level 1 is to index 1

        try:

            with open(Parser.FILE_NAME, "r") as file:
                datas = file.read().split("\n")

                for data in datas:
                    picList.append(data.split(";")[1])

        except FileNotFoundError:
            print(Parser.FILE_NAME, "does not exist.")
        except:
            pass
        else:
            return picList

    @staticmethod
    def readUserInfo():

        user = {
            "coins" : 100, # 100 is the default
            "level" : 1, # level starts with 0, in display 1 will just be added.
        }

        try:

            with open(Parser.USER_INFORMATION, "r") as file:
                data = file.read().split(";")
                user["coins"] = int(data[0])
                user["level"] = int(data[1])

        except FileNotFoundError:
            file = open(Parser.USER_INFORMATION, "x")
            Parser.rewriteUserInfo(user)
            file.close()

        except:
            pass

        return user

    @staticmethod
    def rewriteUserInfo(user):

        try:
            with open(Parser.USER_INFORMATION, "w") as file:
                file.write(str(user["coins"])+";"+str(user["level"]))

        except FileNotFoundError:
            file = open(Parser.USER_INFORMATION, "x")
            Parser.rewriteUserInfo(user)
            file.close()

            Parser.rewriteUserInfo(user)
        except:
            pass