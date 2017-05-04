
####################################
# This solver cannot get the best path,
# but it can solve a path better than 
# the initial path.
##################

####################################
# Enter the file name there.
#                   ||||||
##################  vvvvvv
# filename = 'TSP_berlin52.txt'
# filename_list = ['TSP_berlin52.txt','TSP_ch130.txt','TSP_ch150.txt','TSP_pr1002.txt','TSP_rd100.txt','TSP_st70.txt','TSP_tsp225.txt']


####################################


####################################
# Import model
##################
import copy
from Tkinter import *

####################################
# TSPSolver Class
##################
class TSPSolver():
  """TSPSolver(filename)"""
  def __init__(self, filename):
    self.filename = filename
    self.__l_dict = {}
    self.__d_dict = {}
    self.__num_of_cus = 0
    self.__translate2dict()
    self.__countDistance()


  def __translate2dict(self):
    ####################################
    # Read the file and translate to dictionary,
    # and save in self.__d_dict.
    ##################
    f = open(self.filename, 'r')

    self.__num_of_cus = int(f.readline())

    for line in f:
      line = line.strip()

      temp_str = ''
      switch = True
      for word in line:
        if word != " ":
          temp_str += word
          switch = True
        elif word == " " and switch == True:
          temp_str += ','
          switch = False

      temp_str = temp_str.split(',')
      if temp_str != ['']:
        temp_num = ''
        for i in range(len(temp_str)):
          if i == 0:
            temp_num = int(temp_str[i])
            self.__l_dict[int(temp_str[i])] = {}
          elif i == 1:
            self.__l_dict[temp_num]['x'] = float(temp_str[i])
          else:
            self.__l_dict[temp_num]['y'] = float(temp_str[i])

    f.close()


  def __countDistance(self):
    ####################################
    # Count the distance between every customers,
    # and save in self.__l_dict.
    ##################
    for i in self.__l_dict:
      self.__d_dict[i] = {}
      for j in self.__l_dict:
        if j > i:
          dx = self.__l_dict[j]['x'] - self.__l_dict[i]['x']
          dy = self.__l_dict[j]['y'] - self.__l_dict[i]['y']
          distance = (dx*dx+dy*dy)**0.5
          self.__d_dict[i][j] = distance


  def getDistanceBt2Cus(self, a, b):
    """
    getDistanceBt2Cus(a, b)
    Return the distance between two customers a and b
    """
    if a < b:
      return self.__d_dict[a][b]
    elif a > b:
      return self.__d_dict[b][a]
    else:
      # print 'a=',a,', b=',b
      print "Error! Need two different customers!"
      return 0


  def getNumOfCus(self):
    """Return a number of customers(int)"""
    return self.__num_of_cus


  def getNameAndCoordinateOfCus(self):
    """Return a dict with {num(int): {x: (float), y: (float)}, ... }"""
    return copy.deepcopy(self.__l_dict)


  def getDistancesBtCus(self):
    """Return a dict with {num(int): {num(int): distance(float), ... }, ... }"""
    return copy.deepcopy(self.__d_dict)


  def outputGraph(self):
    """
    Draw a simple graph with text, and
    save a text file named 'graph.txt'.
    (num_of_cus should < 100)
    """
    ####################################
    # Just fun~
    ##################    
    temp_dict = self.getNameAndCoordinateOfCus()

    for num in temp_dict:
      temp_dict[num]['x'] = int(temp_dict[num]['x']/10)
      temp_dict[num]['y'] = int(temp_dict[num]['y']/10)

    x_sorted = sorted(temp_dict.items(), key = lambda s: s[1]['x'])
    # print x_sorted
    y_sorted = sorted(x_sorted, key = lambda s: s[1]['y'], reverse=True)
    # print y_sorted

    max_x = x_sorted[-1][1]['x']
    min_x = x_sorted[0][1]['x']
    waste_dot = min_x-2
    if waste_dot < 0:
      waste_dot = 0
    # print max_x

    graph_text = open(self.filename.split('.')[0]+'_graph.txt','w')

    for unit in y_sorted:
      p = ''
      if unit[0] < 10:
        for i in range(unit[1]['x']-1-waste_dot):
          p += '.'
        p += str(unit[0])
        for i in range(max_x-unit[1]['x']):
          p += '.'
      else:
        for i in range(unit[1]['x']-2-waste_dot):
          p += '.'
        p += str(unit[0])
        for i in range(max_x-unit[1]['x']):
          p += '.'
      graph_text.write(p+'\n')

    graph_text.close()


  def __change_two_point(self,the_list):
    ####################################
    # Find a better path by compare two point 
    # and change them to get a shorter distance.
    ##################
    num_of_cus = self.__num_of_cus

    temp_list = copy.copy(the_list)
    final_list = []

    run_times = 0
    while final_list != temp_list:
      final_list = copy.copy(temp_list)

      # Change i-th and 1-st~num_of_cus-th to find a better path
      for i in range(1,num_of_cus):
        for j in range(1,num_of_cus):
          it = 1
          jt = 1
          if i == j:
            continue
          elif i < num_of_cus-1 and j == num_of_cus-1:
            jt = 1-num_of_cus
          elif i == num_of_cus-1 and j < num_of_cus-1:
            it = 1-num_of_cus

          run_times += 1    # run_times is here!

          # print i+1,j+1

          before_distance = 0
          after_distance = 0
          if (i-j)**2 != 1:
            distance1 = self.getDistanceBt2Cus(temp_list[i-1],temp_list[i])
            distance2 = self.getDistanceBt2Cus(temp_list[i],temp_list[i+it])
            distance3 = self.getDistanceBt2Cus(temp_list[j-1],temp_list[j])
            distance4 = self.getDistanceBt2Cus(temp_list[j],temp_list[j+jt])

            before_distance = distance1 + distance2 + distance3 + distance4

            distance5 = self.getDistanceBt2Cus(temp_list[i-1],temp_list[j])
            distance6 = self.getDistanceBt2Cus(temp_list[j],temp_list[i+it])
            distance7 = self.getDistanceBt2Cus(temp_list[j-1],temp_list[i])
            distance8 = self.getDistanceBt2Cus(temp_list[i],temp_list[j+jt])

            after_distance = distance5 + distance6 + distance7 + distance8
          elif i-j == -1:
            distance1 = self.getDistanceBt2Cus(temp_list[i-1],temp_list[i])
            distance2 = self.getDistanceBt2Cus(temp_list[j],temp_list[j+jt])

            before_distance = distance1 + distance2

            distance3 = self.getDistanceBt2Cus(temp_list[i-1],temp_list[j])
            distance4 = self.getDistanceBt2Cus(temp_list[i],temp_list[j+jt])

            after_distance = distance3 + distance4
          else:
            distance1 = self.getDistanceBt2Cus(temp_list[i+it],temp_list[i])
            distance2 = self.getDistanceBt2Cus(temp_list[j],temp_list[j-1])

            before_distance = distance1 + distance2

            distance3 = self.getDistanceBt2Cus(temp_list[i+it],temp_list[j])
            distance4 = self.getDistanceBt2Cus(temp_list[i],temp_list[j-1])

            after_distance = distance3 + distance4

          if before_distance > after_distance:
            temp = temp_list[i]
            temp_list[i] = temp_list[j]
            temp_list[j] = temp

    print '\nfor-loop\'s calculations run_times =', run_times
    return temp_list


  def __popInsertEveryWhere(self,the_list):
    ####################################
    # Find a better path by pop a point 
    # and insert to another place.
    ##################
    num_of_cus = self.__num_of_cus

    temp_list = copy.copy(the_list)
    final_list = self.getInitPathBySortNum()

    run_times = 0
    while final_list != temp_list:
      if self.getPathDistance(final_list) > self.getPathDistance(temp_list):
        final_list = copy.copy(temp_list)

      for i in range(1,num_of_cus):
        old_distance = self.getDistanceBt2Cus(temp_list[i-1],temp_list[i])
        if i != num_of_cus-1:
          old_distance += self.getDistanceBt2Cus(temp_list[i],temp_list[i+1])
        else:
          old_distance += self.getDistanceBt2Cus(temp_list[i],temp_list[0])

        apop = temp_list.pop(i)
        
        for j in range(1,num_of_cus):

          temp_distance = old_distance
          if i == j:
            continue
          if i != num_of_cus-1:
            new_distance = self.getDistanceBt2Cus(temp_list[i-1],temp_list[i])
            if j != num_of_cus-1:
              temp_distance += self.getDistanceBt2Cus(temp_list[j-1],temp_list[j])
            else:
              temp_distance += self.getDistanceBt2Cus(temp_list[j-1],temp_list[0])
          else:
            new_distance = self.getDistanceBt2Cus(temp_list[i-1],temp_list[0])
            if j != num_of_cus-1:
              temp_distance += self.getDistanceBt2Cus(temp_list[j-1],temp_list[j])
            else:
              temp_distance += self.getDistanceBt2Cus(temp_list[j-1],temp_list[0])

          run_times += 1    # run_times is here!

          temp_list.insert(j,apop)
          new_distance += self.getDistanceBt2Cus(temp_list[j-1],temp_list[j])
          if j!= num_of_cus-1:
            new_distance += self.getDistanceBt2Cus(temp_list[j],temp_list[j+1])
          else:
            new_distance += self.getDistanceBt2Cus(temp_list[j],temp_list[0])
          if new_distance < temp_distance:
            break
          temp_list.pop(j)

        if len(temp_list) != num_of_cus:
          temp_list.insert(i,apop)

    print '\nfor-loop\'s calculations run_times =', run_times
    # print self.getPathDistance(final_list)
    return final_list


  def tabuSearch_beta(self,the_list):
    """tabuSearch_beta(your_list)"""
    ####################################
    # Use Tabu List and just reverse to the shorter path
    ##################
    num_of_cus = self.getNumOfCus()

    temp_list = copy.copy(the_list)
    temp_list.append(temp_list[0])

    final_list = []
    
    tabu_list = []

    run_times = 0

    while final_list != temp_list[0:-1]:
      if_first_time = True

      for i in range(1,num_of_cus-2):
        for j in range(i+1,num_of_cus):

          run_times += 1    # run_times is here!

          # if run_times%10000 == 0:
          #   print "Tabu run times now =", run_times
            # print temp_list[0:-1]

          if if_first_time:
            final_list = temp_list[0:-1]


          if [temp_list[i-1],temp_list[i]] in tabu_list:
            continue
          elif [temp_list[j],temp_list[j+1]] in tabu_list:
            continue


          if len(tabu_list) >= 4:   # prevent tabu_list size bigger than 4
            tabu_list.pop(0)
            tabu_list.pop(0)

          tabu_list.append([i-1,i])
          tabu_list.append([j,j+1])


          old_distance = self.getDistanceBt2Cus(temp_list[i-1],temp_list[i]) + self.getDistanceBt2Cus(temp_list[j],temp_list[j+1])
          new_distance = self.getDistanceBt2Cus(temp_list[i-1],temp_list[j]) + self.getDistanceBt2Cus(temp_list[i],temp_list[j+1])

          if old_distance < new_distance:
            continue


          reverse_list = []
          for times in range(i,j+1):
            reverse_list.append(temp_list.pop(i))

          for unit in reverse_list:
            temp_list.insert(i,unit)

          final_list = temp_list[0:-1]


    print '\nfor-loop\'s calculations run_times =', run_times
    # print final_list
    return final_list


  def getInitPathBySortNum(self):
    """Return an initial path list = 1->2->3->...->num_of_cus"""
    initial_list = []

    for i in range(self.getNumOfCus()):
      i = i+1
      initial_list.append(i)

    return initial_list


  def getInitPathBySortXY(self):
    """Return an initial path (sorted by x and y)"""
    bottom_list = []
    top_list = []

    temp_dict = copy.deepcopy(self.getNameAndCoordinateOfCus())
    y_sorted = sorted(temp_dict.items(), key = lambda s: s[1]['y'])
    # print x_sorted
    x_sorted = sorted(y_sorted, key = lambda s: s[1]['x'])
    # print y_sorted

    bottom_right_point = x_sorted[0]
    top_right_point = x_sorted[1]
    for unit in x_sorted:
      bottom_right_dy = (unit[1]['y'] - bottom_right_point[1]['y'])**2
      top_right_dy = (unit[1]['y'] - top_right_point[1]['y'])**2
      if bottom_right_dy > top_right_dy:
        top_right_point = unit
        top_list.append(unit[0])
      else:
        bottom_right_point = unit
        bottom_list.append(unit[0])
      
    # print top_list+bottom_list[::-1]
    return top_list+bottom_list[::-1]


  def getPathDistance(self,path_list):
    """
    getPathDistance(path_list)
    Return a distance of the path_list
    """
    total_distance = 0

    length = len(path_list)
    for i in range(length):
      unit_here = path_list[i]
      if i != length-1:
        unit_next = path_list[i+1]
        distance = self.getDistanceBt2Cus(unit_here,unit_next)
      else:
        distance = self.getDistanceBt2Cus(path_list[0],unit_here)
      total_distance += distance

    # print total_distance
    return total_distance


  def solve(self):
    ####################################
    # Solve it!
    ##################

    # get list and distance by initial path by sort num
    print '\n[[[ Get an initial path by sort num...'
    init_path_num = self.getInitPathBySortNum()
    init_path_num_distance = self.getPathDistance(init_path_num)
    print '\ninit_path_num_distance =', init_path_num_distance
    print 'init_path_num =', init_path_num

    # get list and distance by initial path by sort x and y
    print '\n[[[ Get an initial path by sort x and y...'
    init_path_XY = self.getInitPathBySortXY()
    init_path_XY_distance = self.getPathDistance(init_path_XY)
    print '\ninit_path_XY_distance =', init_path_XY_distance
    print 'init_path_XY =', init_path_XY

    if init_path_XY_distance > init_path_num_distance:
      shorter_init_path = init_path_num
      print '\n\n[[[ Select init_path_num.'
    else:
      shorter_init_path = init_path_XY
      print '\n\n[[[ Select init_path_XY.'

    # Use method
    print '\n\n[[[ Now Solving...'
    tabuSearch_path = self.tabuSearch_beta(shorter_init_path)
    tabuSearch_path_distance = self.getPathDistance(tabuSearch_path)
    print '\ntabuSearch_path_distance =', tabuSearch_path_distance
    print 'tabuSearch_path =', tabuSearch_path

    while True:
      print '\n\n   -> Run in while loop...'

      popInsertEveryWhere_path = self.__popInsertEveryWhere(tabuSearch_path)
      popInsertEveryWhere_path_distance = self.getPathDistance(popInsertEveryWhere_path)
      print '\npopInsertEveryWhere_path_distance =', popInsertEveryWhere_path_distance
      print 'popInsertEveryWhere_path =', popInsertEveryWhere_path

      print '\n\n   -> Run in while loop...'

      tabuSearch_path = self.tabuSearch_beta(popInsertEveryWhere_path)
      tabuSearch_path_distance = self.getPathDistance(tabuSearch_path)
      print '\ntabuSearch_path_distance =', tabuSearch_path_distance
      print 'tabuSearch_path =', tabuSearch_path

      if round(popInsertEveryWhere_path_distance) == round(tabuSearch_path_distance):
        break

    # change_two_point_path = self.__change_two_point(tabuSearch_path)
    # change_two_point_path_distance = self.getPathDistance(change_two_point_path)
    # print '\nchange_two_point_path_distance =', change_two_point_path_distance
    # print 'change_two_point_path =', change_two_point_path


    print '\n========== Result ========='

    final_path = tabuSearch_path
    final_path_distance = tabuSearch_path_distance

    print "\n>>> Final path =", final_path
    print "\n>>> Final path distance =", final_path_distance
    print '\n==========================='


    # save to txt file
    result_file_name = '1_TS_'+self.filename.split('.')[0]+'.txt'
    print '\n[[[ Save to ' + result_file_name + '...'
    result_file = open(result_file_name,'w')

    for i in range(len(final_path)):
      result_file.write(str(final_path[i])+' ')
    result_file.write('\n'+str(int(round(final_path_distance))))

    result_file.close()
    print '\n[[[ Done.'

    return [final_path,final_path_distance,result_file_name]



####################################
# App-window Class
##################
class AppWindow(Frame):
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.grid()
    self.createWidgets()

  def say_hi(self):
    print "hi there, everyone!"

  def createWidgets(self):
    self.displayTextTop = Label(self)
    self.displayTextTop["text"] = "TSP-Solver"
    self.displayTextTop.grid(row=0, column=1, columnspan=7)

    self.about = Button(self)
    self.about["text"] = "about"
    self.about.grid(row=0, column=0)
    self.about["command"] =  self.aboutMethod

    self.inputText = Label(self)
    self.inputText["text"] = "Enter your filename:"
    self.inputText.grid(row=1, column=0)
    self.inputField = Entry(self)
    self.inputField["width"] = 20
    self.inputField.grid(row=1, column=1, columnspan=6)

    self.example = Button(self)
    self.example["text"] = "Filename example"
    self.example.grid(row=2, column=0)
    self.example["command"] =  self.exampleMethod

    self.clear = Button(self)
    self.clear["text"] = "Clear"
    self.clear.grid(row=2, column=1)
    self.clear["command"] =  self.clearMethod

    self.solve = Button(self)
    self.solve["text"] = "solve"
    self.solve.grid(row=2, column=2)
    self.solve["command"] =  self.solveMethod

    self.displayTextBottom = Label(self)
    self.displayTextBottom["text"] = "Welcome to TSPSolver!"
    self.displayTextBottom.grid(row=3, column=0, columnspan=7)

    self.displayTextBottom2 = Label(self)
    self.displayTextBottom2["text"] = ""
    self.displayTextBottom2.grid(row=4, column=0, columnspan=7)

    self.displayTextBottom3 = Label(self)
    self.displayTextBottom3["text"] = ""
    self.displayTextBottom3.grid(row=5, column=0, columnspan=7)

  def aboutMethod(self):
    self.displayTextTop["text"] = "Made by NTUST OR2 Group One"

  def exampleMethod(self):
    self.displayTextBottom["text"] = "The filename 'TSP_berlin52.txt' is an example."
    self.inputField.delete(0, 200)
    self.inputField.insert(0, "TSP_berlin52.txt")

  def clearMethod(self):
    self.displayTextTop["text"] = "TSP-Solver"
    self.displayTextBottom["text"] = "All Clear."
    self.inputField.delete(0, 200)
    self.displayTextBottom2["text"] = ""
    self.displayTextBottom3["text"] = ""

  def solveMethod(self):
    if self.testFileName():
      self.displayTextBottom["text"] = "Filename: " + self.inputField.get()
      TSPS = TSPSolver(self.inputField.get())
      self.displayTextBottom2["text"] = "Now Solving..."

      result = TSPS.solve()
      self.displayTextBottom2["text"] = "The result is save to a file named '" + result[2] + "'"
      self.displayTextBottom3["text"] = "Final path distance = " + str(int(round(result[1])))

  def testFileName(self):
    try:
      f = open(self.inputField.get(), 'r')
      f.close()
      return True
    except Exception, e:
      self.displayTextBottom["text"] = 'Error! No such of file: ' + self.inputField.get()
      return False



# TSPS = TSPSolver(filename)

# # TSPS.outputGraph()
# TSPS.solve()

if __name__ == '__main__':
  root = Tk()
  root.title("TSP-Solver")
  app = AppWindow(master=root)
  app.mainloop()