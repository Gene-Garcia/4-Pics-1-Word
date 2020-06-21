from tkinter import *
from ButtonTextPopulator import ButtonPopulator as BP
# Maam dapat po naka-install yung Pillow module
from PIL import Image, ImageTk
from functools import partial
from Game import Game

class Window:

    # Component Initialization, Start

    def __init__(self, game):
        self.__GAME_ASSETS = {"coins" : "coins.png", "pass" : "passbutton.PNG", "hint" : "hintbutton.PNG", "logo" : "4pics1wordlogo.png"} # contains the images used
        self.__game = game

        self.__pictureWord = "Blank" # A word is initially set at this variable because it helps in displaying initial guess boxes; however, it will be replaced when the actual game starts
        self.__btnGuessBoxes = [] # Button, eto yung mga box na mag kaka letter or the guess box
        self.__btnGuessBoxesStrVar = [] # StringVar, each guess box has an associated StringVar that is located here.
        self.__guessBoxButtonLocation = {} # dictionary, this variable helps in identifying which buttons are in the guess boxes. On click of an guess box, btn location can be determinened return to its normal state

        self.root = Tk(className='4 Pics 1 Word')
        self.root.configure(background='#161824')
        self.root.resizable(False, False)

        self.initComponents()

        # start level
        self.prepareForNextLevel()

        # displays the game in the center of the screen
        self.h = 680
        self.w = 480
        xCoords = int((self.root.winfo_screenwidth() / 2) - (self.w / 2))
        yCoords = int((self.root.winfo_screenheight() / 2) - (self.h / 2))
        self.root.geometry("{}x{}+{}+{}".format(self.w, self.h, xCoords, yCoords))

        self.root.mainloop()

    def initComponents(self):
        # Top, Start
        informationFrame = Frame(self.root, background="#222831")
        informationFrame.pack(fill="x")

        # level
        self.lblLevel = Label(informationFrame, text="Level 1", fg="#ffffff", font="helvetica 12 bold", background="#222831")
        self.lblLevel.pack(side=LEFT, padx=50, ipady=9)

        # coins
        self.userCoins = StringVar()
        self.userCoins.set("0")
        self.lblCoins = Label(informationFrame, background="#222831", fg="#ffffff", font="helvetica 15 bold", textvariable=self.userCoins)
        self.lblCoins.pack(side=RIGHT, padx=13)

        imgCoins = Image.open(self.__GAME_ASSETS["coins"])
        renderImg = ImageTk.PhotoImage(imgCoins)
        lblCoinsImg = Label(informationFrame, image=renderImg, background="#222831")
        lblCoinsImg.image = renderImg
        lblCoinsImg.pack(side=RIGHT, ipady=9)
        # Top, End

        # Middle, Start (Image display)
        imageFrame = Frame(self.root, background="#161824")
        imageFrame.pack(pady=50)

        picture = Image.open(self.__GAME_ASSETS["logo"]).resize((300,280)) #this is the default image to be displayed before starting the game.
        renderPicture = ImageTk.PhotoImage(picture)
        self.lblPicture = Label(imageFrame, image=renderPicture, background="#161824")
        self.lblPicture.image = renderPicture
        self.lblPicture.pack()
        # Middle, End (Image display)

        # Middle 2, Start
        self.guessFrame = Frame(self.root, background="#161824")
        self.guessFrame.pack(pady=(0, 50))

        # dynamic creation of guess boxes based on self.__pictureWord
        self.loadGuessBoxes()

        imgHint = Image.open(self.__GAME_ASSETS["hint"]).resize((38, 38))
        imgHintRender = ImageTk.PhotoImage(imgHint)
        self.btnHint = Button(self.guessFrame, image=imgHintRender, borderwidth=-4, background="#161824", command=self.hint)
        self.btnHint.image = imgHintRender
        self.btnHint.pack(side=RIGHT, padx=10)
        # Middle 2, End

        # Bottom, Start
        self.buttonsFrame = Frame(self.root, background="#161824")
        self.buttonsFrame.pack()

        #pass button
        imgPass = Image.open(self.__GAME_ASSETS["pass"]).resize((40,85))
        imgPassRender = ImageTk.PhotoImage(imgPass)
        self.btnPass = Button(self.buttonsFrame, image=imgPassRender, background="#161824", borderwidth=0, command=self.passLevel)
        self.btnPass.image = imgPassRender
        self.btnPass.grid(row=0, column=6, rowspan=2, padx=5)

        # dynamic creation of buttons
        self.createButtonsList()
        # Bottom, End

    def createButtonsList(self):
        BUTTON_COUNT = 12
        self.__buttonsList = [] # Contains the buttons that will be used as the guess boxes' populator
        self.__buttonStringVars = [] # Each button has a connected string vars. The value in the string vars will be set to the guess box. However, letters will only be set to the buttons later on.

        row = 0
        col = 0
        for i in range(BUTTON_COUNT): # clicking a button would be hard to identify which button was it; hence, i is the location of the button, it determines which button was clicked.
            tempText = StringVar()
            tempText.set(" ")
            tempBtn = Button(self.buttonsFrame, textvariable=tempText, disabledforeground="#e0e0ec",
                                      font="Helvetica 14 bold", background="#fafafa", width=2, height=0,
                                      command=partial(self.buttonToGuessBoxes, letterVar=tempText, btnIndex=i), state=NORMAL)
            tempBtn.grid(row=row, column=col, padx=5, pady=5)

            self.__buttonsList.append(tempBtn)
            self.__buttonStringVars.append(tempText)

            col += 1
            if col == 6:
                row = 1
                col = 0

    def loadGuessBoxes(self):
        """ Dynamic creation of guess box with the same length as the picture's word"""
        self.__pictureWord = self.__pictureWord.upper()

        for i in range(len(self.__pictureWord)):
            tempStringVar = StringVar()
            tempStringVar.set(" ")
            tmpBtnGuess = Button(self.guessFrame, background="#0f101a",disabledforeground="white", textvariable=tempStringVar, fg="#fafafa", font="helvetice 12 bold", borderwidth=2, relief="raised", justify=CENTER, width=3, command=partial(self.onclickGuessBox, i))
            tmpBtnGuess.pack(side=LEFT, padx=5, ipady=6)

            self.__btnGuessBoxes.append(tmpBtnGuess)
            self.__btnGuessBoxesStrVar.append(tempStringVar)

    # Component Initialization, End

    """--------------------------"""

    # Special Button Commands, Start

    def passLevel(self):
        if int(self.__game.getUserCoins()) < Game.PASS_COST:
            PopUp.popUpMessage("Insufficient Coins!", PopUp.INVALID)

        else:
            self.btnPass.config(state=DISABLED)
            self.btnHint.config(state=DISABLED)

            self.__game.decreaseUserCoins("pass")
            self.userCoins.set(self.__game.getUserCoins())
            self.__game.moveLevel()

            # display correct answer
            ctr = 0
            for letter in self.__pictureWord:

                button = None
                buttonText = None
                for i in range(len(self.__buttonsList)):
                    if self.__buttonStringVars[i].get() == letter:
                        button = self.__buttonsList[i]
                        buttonText = self.__buttonStringVars[i]
                        break

                if button != None and buttonText != None:
                    button.config(state=DISABLED, background="#eeeeee")
                    self.__btnGuessBoxes[ctr].config(background="#8cba51", state=DISABLED)
                    self.__btnGuessBoxesStrVar[ctr].set(letter)

                ctr += 1

            self.root.after(1500, self.prepareForNextLevel) # so that the user can still read the correct answer

    def hint(self):
        blankBoxIndex = 0
        hintCost = 2

        if int(self.__game.getUserCoins()) < hintCost:
            PopUp.popUpMessage("Insufficient Coins!", PopUp.INVALID)
        else:
            for i in self.__btnGuessBoxesStrVar:
                if i.get() == " " or i.get() == None:
                    break
                else:
                    blankBoxIndex += 1

            try:
                letterMissing = self.__pictureWord[blankBoxIndex]

                buttonIndex = 0
                for i in range(len(self.__buttonsList)):
                    if self.__buttonStringVars[i].get() == letterMissing:
                        buttonIndex = i
                        self.__buttonsList[i].config(state=DISABLED, background="#eeeeee")
                        self.__btnGuessBoxes[blankBoxIndex].config(background="#8cba51", state=DISABLED)
                        self.__btnGuessBoxesStrVar[blankBoxIndex].set(self.__pictureWord[blankBoxIndex])
                        break

                self.__game.decreaseUserCoins("hint")
                self.userCoins.set(self.__game.getUserCoins())

            except IndexError as e:
                pass # This occurs when all the guess boxes are filled
            finally:
                self.checkUserGuess()

    # Special Button Commands, End

    """--------------------------"""

    # Button Onclick, Start

    def buttonToGuessBoxes(self, letterVar, btnIndex):
        if self.__pictureWord != "": #at the start of the window, the buttons are blank; hence, user might click the button.
            for i in range(len(self.__btnGuessBoxesStrVar)):
                # self.__btnGuessBoxesStrVar[i]
                if self.__btnGuessBoxesStrVar[i].get() == " ":
                    # this is because clicking a guess box would remove a letter; hence, the array would have an " " index
                    # that is why we add the letter like this
                    self.__btnGuessBoxesStrVar[i].set(letterVar.get())
                    self.__guessBoxButtonLocation[i] = btnIndex
                    self.__buttonsList[btnIndex].config(state=DISABLED, background="#eeeeee")

                    # everytime a button click, or for later, if the guess boxes are full
                    # check if the user has the correct answer already
                    self.checkUserGuess()
                    break

    def onclickGuessBox(self, guessBoxIndex):
        """ A function that deletes the letter of the guess box and reverts the associated button to its normal state again """
        try:
            self.__btnGuessBoxesStrVar[guessBoxIndex].set(" ")
            self.__buttonsList[ self.__guessBoxButtonLocation[guessBoxIndex] ].config(state=NORMAL, background="#fafafa")
        except KeyError:
            pass # this happens when the guess box is clicked even though it does not have a content

    # Button Onclick, End

    """--------------------------"""

    def changeButtonTexts(self):
        """ Changes each button with letters of the word of the picture mixed with different letters """
        texts = BP.populateButton(self.__pictureWord)

        ctr = 0
        for buttonStr in self.__buttonStringVars:
            buttonStr.set(texts[ctr])
            self.__buttonsList[ctr].config(state=NORMAL)
            ctr += 1

    def checkUserGuess(self):
        answer = ""
        for stringVar in self.__btnGuessBoxesStrVar:
            if stringVar.get() == " ":
                return None # may blank pa, no need to proceed, sayang lang sa loop
            else:
                answer += stringVar.get()

        # all guess box are populated
        if str(answer).upper() == self.__pictureWord:
            self.btnHint.config(state=DISABLED)
            self.btnPass.config(state=DISABLED)

            for i in self.__btnGuessBoxes:
                i.config(background="#8cba51", disabledforeground="white", state=DISABLED)

            self.__game.incrementUserCoins()
            self.__game.moveLevel()

            self.root.after(1500, self.prepareForNextLevel)

        else:
            # turns the guess box text colors to red, and after 2 seconds reverts to white
            for i in self.__btnGuessBoxes:
                i.config(disabledforeground="#e7305b", foreground="#e7305b")
            self.root.after(2000, self.incorrectAns)

    def incorrectAns(self):
        """ this method reverts the guess box to white, this line of code were just seperated because the self.root.after(i, method) needs to call a method """
        for i in self.__btnGuessBoxes:
            i.config(disabledforeground="white", foreground="white")

    def destroyGuessBoxes(self):
        """ destroys the set guess boxes because new guess boxes will be generated based on the new level """
        for i in range(len(self.__btnGuessBoxesStrVar)):
            self.__btnGuessBoxes[i].destroy()

        self.__btnGuessBoxes.clear()
        self.__btnGuessBoxesStrVar.clear()

    def loadImage(self):
        """ Changes the display image based on the current level """
        imgLoc = self.__game.getLevelImage()

        if imgLoc == False:
            self.root.after(1000, lambda: self.showPopUp("There was an error in finding the picture.", PopUp.INVALID))
            self.invalidGame()
        else:
            picture = Image.open(imgLoc).resize((300, 280))
            renderPicture = ImageTk.PhotoImage(picture)
            self.lblPicture.config(image=renderPicture)
            self.lblPicture.image = renderPicture

    def prepareForNextLevel(self):
        """ The function that makes the picture, word, guess box, and buttons change """
        # if current level is equals to MAX than dont proceed, dislay a  congratulatory message

        if self.__game.getCurrentLevel() <= Game.MAX_LEVEL:

            # The hint and pass button were disabled
            self.btnHint.config(state=NORMAL)
            self.btnPass.config(state=NORMAL)

            self.destroyGuessBoxes()
            self.__pictureWord = self.__game.getLevelWord()
            self.loadGuessBoxes()
            self.changeButtonTexts()

            self.loadImage()
            self.userCoins.set( self.__game.getUserCoins() )
            self.lblLevel["text"] = "Level " + str(self.__game.getCurrentLevel())

        else:
            self.btnHint.config(state=DISABLED)
            self.btnPass.config(state=DISABLED)

            self.root.after(1000, lambda: self.showPopUp("CONGRATULATIONS YOU HAVE FINISHED THE GAME!", PopUp.WIN))

    def showPopUp(self, msg, level):
        PopUp.popUpMessage(msg, level)

    def invalidGame(self):
        """ This method will disable the hint and pass button to not allow the user to perform further actions. This happens when the picList does not match and image in the folder"""
        self.btnHint.config(state=DISABLED)
        self.btnPass.config(state=DISABLED)

        for i in range(len(self.__buttonsList)):
            self.__buttonsList[i].config(state=DISABLED)

class PopUp:
    """ A static class the is responsible for displaying pop-up messages """
    INVALID = 1
    WIN = 0

    @staticmethod
    def popUpMessage(message, level):
        textColor = ""
        bg = "#161824"

        if level == PopUp.INVALID:
            textColor = "#e2979c"
        elif level == PopUp.WIN:
            textColor = "#f7fbe1"

        popUp = Tk()
        popUp.wm_title("4 Pics 1 Word")
        popUp.configure(background=bg)

        Label(popUp, background="#222831", font="helvetica 14 bold", text="4 Pics 1 Word", fg="white", justify=LEFT).pack(side=TOP, fill="x", ipady=10)

        Label(popUp, font="helvetica 11 bold", background=bg, wraplength=200, width=43, justify=CENTER, fg=textColor, text=message).pack(side=TOP, padx=18, ipady=10, pady=(30,0), fill="x")

        btnExit = Button(popUp, text="Okay", command=popUp.destroy, background="#222831", fg="white", relief=SOLID, font="helvetica 10 bold", width=10,).pack(side=RIGHT, ipady=10, padx=34)

        popUp.resizable(False, False)
        w = 500
        h = 230
        xCoords = int((popUp.winfo_screenwidth() / 2) - (w / 2))
        yCoords = int((popUp.winfo_screenheight() / 2) - (h / 2))
        popUp.geometry("{}x{}+{}+{}".format(w, h, xCoords, yCoords))
        popUp.mainloop()
