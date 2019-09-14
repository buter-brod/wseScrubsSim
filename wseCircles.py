import tkinter as tk

teamsMoveStrategy = "Teams"
cycleMoveStrategy = "Cycle"

class Settings:
    def __init__(self):
        self.wndW = 640
        self.wndH = 480
        self.defaultTeamSize = 5
        self.minTeamSize = 2
        self.maxTeamSize = 8

settings = Settings()

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

assert len(names) <= len(questionsStrList)

class Question:
    def __init__(self, str):
        self.str = str

class Logger:
    def __init__(self):
        self.__logs = ""
        self.verbose = False

    def log(self, msg):
        self.__logs = self.__logs + msg + "\n"

    def getLog(self):
        return self.__logs[:]

class Player:
    def __init__(self):
        self.name = ""
        self.currQuestion = None
        self.__questionsAsked = []
        self.__questionsAnswered = []

    def ask(self, anotherPlayer):

        alreadyAnswered = self.currQuestion in anotherPlayer.__questionsAnswered
        
        self.__questionsAsked.append(self.currQuestion)
        anotherPlayer.__questionsAnswered.append(self.currQuestion)

        if self.logger.verbose:
            self.logger.log(self.name + " asks " + anotherPlayer.name + ": " + self.currQuestion.str)

        if alreadyAnswered:
            self.logger.log("oops, " + anotherPlayer.name + " had to answer '" + self.currQuestion.str + "' again..")
            return False
        
        return True

    def exchange(self, anotherPlayer):
        myQuestion = self.currQuestion
        self.currQuestion = anotherPlayer.currQuestion
        anotherPlayer.currQuestion = myQuestion

        if self.logger.verbose:
            pass
            #self.logger.log(self.name + " exchanged questions with " + anotherPlayer.name)

class Simulator:
    def __init__(self):
        self.teamSize = settings.defaultTeamSize
        self.needExchange = False
        self.logger = Logger()
        self.moveType = teamsMoveStrategy

        self.questions = []

        for qStr in questionsStrList:
            self.questions.append(Question(qStr))
        
    @property 
    def teamSize(self):
        return self.__teamSize

    @teamSize.setter
    def teamSize(self, teamSize):

        if (teamSize < settings.minTeamSize):
            teamSize = settings.minTeamSize
        
        if teamSize > settings.maxTeamSize:
            teamSize = settings.maxTeamSize

        self.__teamSize = teamSize

    def preparePlayers(self):
        self.players = []
        allPlayersNum = self.teamSize * 2

        for index in range(allPlayersNum):
            player = Player()
            player.logger = self.logger
            player.name = names[index]
            player.currQuestion = self.questions[index]
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
    
    def simulate(self):

        self.preparePlayers()
        successfulRounds = 0
        self.offset = 0
        canContinue = True

        while canContinue:
            canContinue = self.round()
            if canContinue:
                successfulRounds = successfulRounds + 1
                self.offset = self.offset + 1
    
        self.logger.log("Simulation ended, total successful rounds " + str(successfulRounds))
        self.logger.log("Questions answered: " + str(successfulRounds * self.teamSize * 2))

class AppWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.simulateCallback = None

        self.numPlayersStr = tk.StringVar()
        self.needExchangeVar = tk.IntVar()
        self.verboseVar = tk.IntVar()

        self.create_widgets()

    def getNumPlayersStr(self):
        return self.numPlayersStr.get()

    def getNeedExhange(self):
        return self.needExchangeVar.get() == 1

    def getVerbose(self):
        return self.verboseVar.get() == 1

    def log(self, msg):
        self.logWidget.insert(tk.INSERT, msg + "\n")

    def clearLog(self):
        self.logWidget.delete("0.0", tk.END)

    def simulationStart(self):
        self.simulateCallback(self)

    def create_widgets(self):

        numPlayersLabelStr = tk.StringVar()
        numPlayersLabelStr.set("How many players in each team (" + str(settings.minTeamSize) + "-"+ str(settings.maxTeamSize) + ")")

        self.numPlayersLabel = tk.Label(self, textvariable=numPlayersLabelStr)
        self.numPlayersLabel.pack()
        
        self.numPlayersStr.set(settings.defaultTeamSize)
        
        self.playersNumEntry = tk.Entry(self, textvariable=self.numPlayersStr)
        self.playersNumEntry.pack()
        
        self.needExchangeBox = tk.Checkbutton(self, text = "Exchange questions", variable = self.needExchangeVar, onvalue = 1, offvalue = 0, height=1, width = 20)
        self.needExchangeBox.pack()
        
        self.verboseBox = tk.Checkbutton(self, text = "Verbose", variable = self.verboseVar, onvalue = 1, offvalue = 0, height=1, width = 20)
        self.verboseBox.pack()

        self.simulateBtn = tk.Button(self)
        self.simulateBtn["text"] = "Start!"
        self.simulateBtn["command"] = self.simulationStart
        self.simulateBtn.pack(side="top")

        self.logWidget = tk.Text(self)
        self.logWidget.pack()

root = tk.Tk()
app = AppWindow(master=root)
app.master.minsize(settings.wndW, settings.wndH)
app.master.maxsize(settings.wndW, settings.wndH)

def Simulate(wnd):

    teamSize = 0
    numPlayersStr = wnd.getNumPlayersStr()
    needExchange = wnd.getNeedExhange()
    verbose = wnd.getVerbose()

    try:
        teamSize = int(numPlayersStr)
    except: pass

    simulator = Simulator()
    simulator.logger.verbose = verbose
    simulator.teamSize = teamSize
    simulator.needExchange = needExchange

    simulator.simulate()

    logs = simulator.logger.getLog()

    wnd.clearLog()
    wnd.log(logs)

    wnd.numPlayersStr.set(str(simulator.teamSize))


app.simulateCallback = Simulate
app.mainloop()