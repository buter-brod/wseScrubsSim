import tkinter as tk
import sys

TEAMS_MOVE_STRATEGY = "Teams"
CYCLE_MOVE_STRATEGY = "Cycle"

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

class Logger:
    def __init__(self):
        self.__logs = ""
        self.verbose = False

    def log(self, msg):
        self.__logs = f"{self.__logs}{msg}\n"
        

    def getLog(self):
        return self.__logs[:]

class Player:
    def __init__(self, name, question, logger):
        self.name = name
        self.logger = logger
        self.currQuestion = question
        self.__questionsAnswered = set()

    def ask(self, anotherPlayer):

        alreadyAnswered = self.currQuestion in anotherPlayer.__questionsAnswered
        
        anotherPlayer.__questionsAnswered.add(self.currQuestion)

        if self.logger.verbose:
            self.logger.log(self.name + " asks " + anotherPlayer.name + ": " + self.currQuestion)

        if alreadyAnswered:
            self.logger.log("oops, " + anotherPlayer.name + " had to answer '" + self.currQuestion + "' again..")
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
        self.moveType = TEAMS_MOVE_STRATEGY
        self.questions = [qStr for qStr in questionsStrList]

        self.players = []
        allPlayersNum = self.teamSize * 2

        self.players = [Player(names[index], self.questions[index], self.logger) for index in range(allPlayersNum)]

        self.players1 = self.players[:self.teamSize]
        self.players2 = self.players[self.teamSize:]
      
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

    def round(self):
        for pairInd in range(self.teamSize):
            player1 = self.players1[pairInd]

            index2 = pairInd

            if self.moveType == TEAMS_MOVE_STRATEGY:
                index2 = (pairInd + self.offset) % self.teamSize
            
            player2 = self.players2[index2]

            if not player1.ask(player2) or not player2.ask(player1): 
                return False

            if self.needExchange:
                player1.exchange(player2)

        if self.moveType == CYCLE_MOVE_STRATEGY:
            players1 = self.players2[0:1] + self.players1[:-1]
            players2 = self.players2[1:] + self.players1[-1:]
            self.players1 = players1
            self.players2 = players2
        else:
            self.offset += 1

        return True
    
    def simulate(self):
        successfulRounds = 0
        self.offset = 0
        
        while True:
            if self.round():
                successfulRounds += 1
            else:
                break
    
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
        self.cycleVar = tk.IntVar()

        self.create_widgets()

    def getNumPlayersStr(self):
        return self.numPlayersStr.get()

    def getNeedExhange(self):
        return self.needExchangeVar.get() == 1

    def getCycled(self):
        return self.cycleVar.get() == 1

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

        self.cycleBox = tk.Checkbutton(self, text = "Cycle", variable = self.cycleVar, onvalue = 1, offvalue = 0, height=1, width = 20)
        self.cycleBox.pack()

        self.simulateBtn = tk.Button(self)
        self.simulateBtn["text"] = "Start!"
        self.simulateBtn["command"] = self.simulationStart
        self.simulateBtn.pack(side="top")

        self.logWidget = tk.Text(self)
        self.logWidget.pack()

def getInt(numStr):
    result = 0
    try:
        result = int(numStr)
    except: pass
    return result

def SimulateWithUICB(wnd):

    simulator = Simulator()
    simulator.moveType = CYCLE_MOVE_STRATEGY if wnd.getCycled() else TEAMS_MOVE_STRATEGY
    simulator.logger.verbose = wnd.getVerbose()
    simulator.teamSize = getInt(wnd.getNumPlayersStr())
    simulator.needExchange = wnd.getNeedExhange()

    simulator.simulate()

    logs = simulator.logger.getLog()

    wnd.clearLog()
    wnd.log(logs)

    wnd.numPlayersStr.set(str(simulator.teamSize))

def StartWithUI():

    root = tk.Tk()
    app = AppWindow(master=root)
    app.master.minsize(settings.wndW, settings.wndH)
    app.master.maxsize(settings.wndW, settings.wndH)
    app.simulateCallback = SimulateWithUICB
    app.mainloop()

def StartWithConsole():
    
    simulator = Simulator()
    simulator.teamSize = getInt(input("players in each team: "))
    simulator.moveType = CYCLE_MOVE_STRATEGY if input("cycle? (y/n)") == "y" else TEAMS_MOVE_STRATEGY
    simulator.logger.verbose = input("verbose? (y/n)") == "y"
    simulator.needExchange = input("exchange? (y/n)") == "y"

    simulator.simulate()

    logs = simulator.logger.getLog()

    print(logs)    

console = "console" in sys.argv

if console:
    StartWithConsole()
else:
    StartWithUI()
