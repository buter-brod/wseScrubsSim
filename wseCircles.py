import tkinter as tk

names = ["Janitor", 
         "Ted", 
         "JD", 
         "Turk", 
         "Cox", 
         "Elliot", 
         "Todd", 
         "Beardface", 
         "Kelso", 
         "Carla", 
         "Lowern", 
         "Jordan", 
         "Lloyd", 
         "Denis", 
         "Dug", 
         "Rowdy"]

questionsStrList = [
             "You put that penny?", 
             "Did you see my girlfriend",  
             "Do you have appletini", 
             "Go EAGLE?", 
             "Do you like Hugh Jackman?", 
             "Am I fat?", 
             "Who said boobs?", 
             "Why do you call me that?", 
             "Where is my muffin", 
             "You know what is your problem", 
             "Do you think Jesus approve that", 
             "Are there any handsome boys",
             "Do you like death metal",
             "Why do I have to play nice",
             "Are you going to die or not", 
             "Woff"]

class Question:
    def __init__(self, str):
        self.str = str

questions = []

for qStr in questionsStrList:
    questions.append(Question(qStr))

assert len(names) <= len(questions)

defaultNumPlayers = 5
minPlayers = 2
maxPlayers = int(len(names) / 2)

class Logger:
    def __init__(self):
        self.cb = None
        self.verbose = False

    def log(self, msg):
        if self.cb != None:
            return self.cb(msg)

logger = Logger()

class Player:
    def __init__(self):
        self.name = ""
        self.currQuestion = None
        self.questionsAsked = []
        self.questionsAnswered = []

    def ask(self, anotherPlayer):

        alreadyAnswered = self.currQuestion in anotherPlayer.questionsAnswered
        
        self.questionsAsked.append(self.currQuestion)
        anotherPlayer.questionsAnswered.append(self.currQuestion)

        if logger.verbose:
            logger.log(self.name + " asks " + anotherPlayer.name + ": " + self.currQuestion.str)

        if alreadyAnswered:
            logger.log("oops, " + anotherPlayer.name + " had to answer '" + self.currQuestion.str + "' again..")
            return False
        
        return True

    def exchange(self, anotherPlayer):
        myQuestion = self.currQuestion
        self.currQuestion = anotherPlayer.currQuestion
        anotherPlayer.currQuestion = myQuestion

        if logger.verbose:
            pass
            #logger.log(self.name + " exchanged questions with " + anotherPlayer.name)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        logger.cb = self.log

    def validatePlayersNum(self):

        numPlayers = minPlayers

        try:
            numPlayers = int(self.numPlayersStr.get())
        except: pass

        if (numPlayers < minPlayers):
            numPlayers = minPlayers
        
        if numPlayers > maxPlayers:
            numPlayers = maxPlayers

        self.numPlayersStr.set(numPlayers)

        self.teamSize = numPlayers

        questionsCount = len(questions)
        namesCount = len(names)
     

    def numPlayersChanged(self, par1, par2, what):
        pass


    def verboseChanged(self, par1, par2, what):
        logger.verbose = self.verboseVar.get() == 1

    def log(self, msg):
        self.logWidget.insert(tk.INSERT, msg + "\n")

    def create_widgets(self):

        numPlayersLabelStr = tk.StringVar()
        numPlayersLabelStr.set("How many players in each team (" + str(minPlayers) + "-"+ str(maxPlayers) + ")")

        self.numPlayersLabel = tk.Label(self, textvariable=numPlayersLabelStr)
        self.numPlayersLabel.pack()

        self.numPlayersStr = tk.StringVar()
        self.numPlayersStr.set(defaultNumPlayers)
        self.numPlayersStr.trace_add("write", self.numPlayersChanged)
        
        self.playersNumEntry = tk.Entry(self, textvariable=self.numPlayersStr)
        self.playersNumEntry.pack()

        self.needExchangeVar = tk.IntVar()
        self.needExchangeBox = tk.Checkbutton(self, text = "Exchange questions", variable = self.needExchangeVar, onvalue = 1, offvalue = 0, height=1, width = 20)
        self.needExchangeBox.pack()

        self.verboseVar = tk.IntVar()
        self.verboseVar.trace_add("write", self.verboseChanged)
        self.verboseBox = tk.Checkbutton(self, text = "Verbose", variable = self.verboseVar, onvalue = 1, offvalue = 0, height=1, width = 20)
        self.verboseBox.pack()

        self.simulateBtn = tk.Button(self)
        self.simulateBtn["text"] = "Simulate!"
        self.simulateBtn["command"] = self.simulationStart
        self.simulateBtn.pack(side="top")

        self.logWidget = tk.Text(self)
        self.logWidget.pack()

    def preparePlayers(self):

        self.players = []

        allPlayersNum = self.teamSize * 2

        for index in range(allPlayersNum):
            player = Player()
            player.name = names[index]
            player.currQuestion = questions[index]
            self.players.append(player)

        self.players1 = self.players[:self.teamSize]
        self.players2 = self.players[self.teamSize:]

    def round(self):
        
        for pairInd in range(self.teamSize):
            player1 = self.players1[pairInd]

            index2 = (pairInd + self.offset) % self.teamSize
            player2 = self.players2[index2]

            askOk1 = player1.ask(player2)

            if not askOk1:
                return False

            askOk2 = player2.ask(player1)

            if not askOk2:
                return False

            if self.needExchange:
                player1.exchange(player2)

        return True

    def simulationStart(self):

        self.validatePlayersNum()
        self.needExchange = self.needExchangeVar.get() == 1

        self.logWidget.delete("0.0", tk.END)
        #self.log("Simulation started!")

        self.preparePlayers()

        successfulRounds = 0
        self.offset = 0

        canContinue = True

        while canContinue:
            
            roundOk = self.round()

            if roundOk:
                successfulRounds = successfulRounds + 1
                self.offset = self.offset + 1

            canContinue = roundOk

        #self.log("Simulation ended, total successful rounds " + str(successfulRounds))

        
root = tk.Tk()
app = Application(master=root)
app.master.minsize(640, 480)
app.master.maxsize(640, 480)

app.mainloop()