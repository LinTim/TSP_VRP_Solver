
####################################
# This solver cannot get the best path,
# but it can solve a path better than 
# the initial path.
##################

####################################
# Enter the file name there.
#                   ||||||
##################  vvvvvv
# filename = 'VRP_A-n32-k5.txt'
# filename_list = ['VRP_A-n32-k5.txt','VRP_A-n33-k5.txt','VRP_A-n37-k6.txt','VRP_A-n38-k5.txt','VRP_A-n39-k6.txt','VRP_A-n45-k6.txt','VRP_A-n46-k7.txt']


####################################


####################################
# Import model
##################
import copy
import math
from Tkinter import *

####################################
# VRPSolver Class
##################
class VRPSolver():
  """VRPSolver(filename)"""
  def __init__(self, filename):
    self.filename = filename
    self.__l_dict = {}
    self.__d_dict = {}
    self.__num_of_nodes = 0
    self.__vehicle_capacity = 0
    self.__translate2dict()
    self.__countDistance()


  def __translate2dict(self):
    ####################################
    # Read the file and translate to dictionary,
    # and save in self.__d_dict.
    ##################
    f = open(self.filename, 'r')

    self.__num_of_nodes = int(f.readline())

    count_s = 0
    count_num = 0
    for line in f:
      line = line.strip()

      if line == '':
        count_s += 1
        continue

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

      if count_s < 2:
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
      elif count_s > 2:
        if count_num < self.__num_of_nodes:
          temp_num = ''
          for i in range(len(temp_str)):
            if i == 0:
              temp_num = int(temp_str[i])
            elif i == 1:
              self.__l_dict[temp_num]['d'] = int(temp_str[i])
          count_num += 1
      else:
        self.__vehicle_capacity = int(temp_str[0])

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
          distance = round((dx*dx+dy*dy)**0.5)
          self.__d_dict[i][j] = distance


  def getDistanceBt2Nodes(self, a, b):
    """
    getDistanceBt2Nodes(a, b)
    Return the distance between two customers a and b
    """
    if a < b:
      return self.__d_dict[a][b]
    elif a > b:
      return self.__d_dict[b][a]
    else:
      print 'a =',a,', b =',b,"; Error! Need two different customers!"
      return 0


  def getNumOfNodes(self):
    """Return a number of nodes(int)"""
    return self.__num_of_nodes


  def getNameAndInfoOfNodes(self):
    """Return a dict with {num(int): {x: (float), y: (float)}, ... }"""
    return copy.deepcopy(self.__l_dict)


  def getDistancesBtNodes(self):
    """Return a dict with {num(int): {num(int): distance(float), ... }, ... }"""
    return copy.deepcopy(self.__d_dict)


  def getDemandByName(self,name):
    """
    getDemandByName(name)
    Return a demand.
    """
    return self.__l_dict[name]['d']


  def getVehicleCapacity(self):
    """Return Vehicle Capacity."""
    return self.__vehicle_capacity


  def __popInsertEveryWhere(self,the_list):
    ####################################
    # Find a better path by pop a point 
    # and insert to another place.
    ##################
    vehicle_capacity = self.getVehicleCapacity()

    ori_path_distance = self.getPathDistance(the_list)

    temp_list = copy.copy(the_list)
    temp_list.append(0)
    temp_list.insert(0,0)
    num_of_nodes = len(temp_list)

    final_list = self.getInitPathBySortNum()

    for i in range(num_of_nodes):
      if temp_list[i] == 0:
        temp_list[i] = 1

    # run_times = 0
    while final_list != temp_list[1:-1]:
      if self.getPathDistance(final_list) > self.getPathDistance(temp_list[1:-1]):
        final_list = temp_list[1:-1]

      for i in range(1,num_of_nodes-1):
        if temp_list[i] == 1:
          continue

        for j in range(1,num_of_nodes-1):
          if i == j:
            continue

          # check if the demand > vehicle capacity
          cannot_insert = False
          temp_demand = 0
          temp_depot_point1 = 0
          temp_depot_point2 = 0
          for index in range(num_of_nodes):
            if i > j:
              if index < j and temp_list[index] == 1:
                temp_depot_point1 = index
              elif index >= j and temp_list[index] == 1:
                temp_depot_point2 = index
                break
            else:
              if index < j+1 and temp_list[index] == 1:
                temp_depot_point1 = index
              elif index >= j and temp_list[index] == 1:
                temp_depot_point2 = index
                break
          if not(i > temp_depot_point1 and i < temp_depot_point2):
            temp_demand += self.getDemandByName(temp_list[i])
            for index in range(num_of_nodes):
              if index <= temp_depot_point1:
                continue
              elif index > temp_depot_point1 and index < temp_depot_point2:
                temp_demand += self.getDemandByName(temp_list[index])
                if temp_demand > vehicle_capacity:
                  cannot_insert = True
                  break
              else:
                break

          if cannot_insert:
            continue
 
          # run_times += 1    # run_times is here!

          if i > j:
            old_distance = self.getDistanceBt2Nodes(temp_list[j-1],temp_list[j])
          else:
            old_distance = self.getDistanceBt2Nodes(temp_list[j],temp_list[j+1])
          if j-1 != i:
            old_distance += self.getDistanceBt2Nodes(temp_list[i],temp_list[i+1])
          if i != j+1:
            old_distance += self.getDistanceBt2Nodes(temp_list[i-1],temp_list[i])

          if i > j:
            new_distance = self.getDistanceBt2Nodes(temp_list[j-1],temp_list[i])
          else:
            new_distance = self.getDistanceBt2Nodes(temp_list[i],temp_list[j+1])
          if j-1 != i:
            if i != j+1:
              new_distance += self.getDistanceBt2Nodes(temp_list[j],temp_list[i])
            else:
              new_distance += self.getDistanceBt2Nodes(temp_list[j],temp_list[i+1])
          if i != j+1:
            new_distance += self.getDistanceBt2Nodes(temp_list[i-1],temp_list[i+1])

          if new_distance < old_distance:
            apop = temp_list.pop(i)
            temp_list.insert(j,apop)
            break


    for i in range(len(final_list)):
      if final_list[i] == 1:
        final_list[i] = 0

    # print '\nfor-loop\'s calculations run_times =', run_times
    # print self.getPathDistance(final_list)
    return final_list


  def tabuSearch_beta(self,the_list):
    """tabuSearch_beta(your_list)"""
    ####################################
    # Use Tabu List and just reverse to the shorter path
    ##################
    vehicle_capacity = self.getVehicleCapacity()
    depot_index_list = []
    temp_list = copy.copy(the_list)
    temp_list.append(0)
    temp_list.insert(0,0)
    for i in range(len(temp_list)):
      if temp_list[i] == 0:
        temp_list[i] = 1
        depot_index_list.append(i)

    num_of_nodes = len(temp_list)

    final_list = []
    
    tabu_list = []

    # run_times = 0

    while final_list != temp_list[1:-1]:
      if_first_time = True

      for i in range(1,num_of_nodes-2):
        for j in range(i+1,num_of_nodes-1):

          # run_times += 1    # run_times is here!

          # if run_times%10000 == 0:
          #   print "Tabu run times now =", run_times
            # print temp_list[0:-1]

          if if_first_time:
            final_list = temp_list[1:-1]

          if temp_list[i] == 1 or temp_list[j] == 1:
            continue
          elif [temp_list[i-1],temp_list[i]] in tabu_list:
            continue
          elif [temp_list[j],temp_list[j+1]] in tabu_list:
            continue

          # build a check_depot_dict
          check_depot_dict = {}
          check_depot_dict[1] = 0
          for depot_index in depot_index_list:
            if i > depot_index:
              check_depot_dict[0] = depot_index

            if j > depot_index:
              check_depot_dict[2] = depot_index

            if i < depot_index and check_depot_dict[1] == 0:
              check_depot_dict[1] = depot_index

            if j < depot_index:
              check_depot_dict[3] = depot_index
              break

          # prevent demand > vehicle_capacity
          cannot_reverse = False
          temp_demand1 = 0
          temp_demand2 = 0
          for index in range(num_of_nodes):
            if index <= check_depot_dict[0]:
              continue
            elif index < i:
              temp_demand1 += self.getDemandByName(temp_list[index])
            elif index < check_depot_dict[1]:
              temp_demand2 += self.getDemandByName(temp_list[index])

            if index > check_depot_dict[2] and index <= j:
              temp_demand1 += self.getDemandByName(temp_list[index])
              if temp_demand1 > vehicle_capacity:
                cannot_reverse = True
                break
            elif index < check_depot_dict[3]:
              temp_demand2 += self.getDemandByName(temp_list[index])
              if temp_demand2 > vehicle_capacity:
                cannot_reverse = True
                break

          if cannot_reverse:
            continue


          if len(tabu_list) >= 4:   # prevent tabu_list size bigger than 4
            tabu_list.pop(0)
            tabu_list.pop(0)

          tabu_list.append([i-1,i])
          tabu_list.append([j,j+1])


          old_distance = self.getDistanceBt2Nodes(temp_list[i-1],temp_list[i]) + self.getDistanceBt2Nodes(temp_list[j],temp_list[j+1])
          new_distance = self.getDistanceBt2Nodes(temp_list[i-1],temp_list[j]) + self.getDistanceBt2Nodes(temp_list[i],temp_list[j+1])

          if old_distance < new_distance:
            continue


          reverse_list = []
          for times in range(i,j+1):
            reverse_list.append(temp_list.pop(i))

          for unit in reverse_list:
            temp_list.insert(i,unit)

          depot_index_list = []
          for index in range(len(temp_list)):
            if temp_list[index] == 1:
              depot_index_list.append(index)

          final_list = temp_list[1:-1]


    for i in range(len(final_list)):
      if final_list[i] == 1:
        final_list[i] = 0

    # print '\nfor-loop\'s calculations run_times =', run_times
    # print final_list
    return final_list


  def getInitPathBySortNum(self):
    """Return an initial path list = 1->2->3->...->num_of_nodes"""
    initial_list = []

    vehicle_capacity = self.getVehicleCapacity()

    temp_demand = 0
    for i in range(1,self.getNumOfNodes()):
      i = i+1
      temp_demand += self.getDemandByName(i)
      if temp_demand > vehicle_capacity:
        temp_demand = self.getDemandByName(i)
        initial_list.append(0)
      initial_list.append(i)

    return initial_list


  def getInitPathByVehicle(self):
    """Return an initial path list."""

    total_demand = 0
    for i in range(1,self.getNumOfNodes()):
      i = i+1
      total_demand += self.getDemandByName(i)

    vehicle_capacity = self.getVehicleCapacity()
    Min_Cars_num = int(math.ceil(float(total_demand)/float(vehicle_capacity)))

    demand_dict = {}
    for num in range(Min_Cars_num):
      demand_dict[num] = [0,[]]

    temp_dict = self.getNameAndInfoOfNodes()

    d_sorted = sorted(temp_dict.items(), key = lambda s:s[1]['d'], reverse = True)
    d_sorted.pop()

    for i in range(len(d_sorted)):
      d = d_sorted[i][1]['d']
      name = d_sorted[i][0]

      no_car = True
      min_capacity = vehicle_capacity
      for num in range(Min_Cars_num):
        if demand_dict[num][0] < min_capacity:
          min_capacity = demand_dict[num][0]
          use_the_car = num

          no_car = False
        elif num == Min_Cars_num-1 and no_car:
          print 'Error! Out of vehicle capacity'
          return 0

      if demand_dict[use_the_car][0] + d <= vehicle_capacity:
        demand_dict[use_the_car][0] += d
        demand_dict[use_the_car][1].append(name)
      else:
        no_car = True
        for num in range(Min_Cars_num):
          if demand_dict[num][0] + d <= vehicle_capacity:
            demand_dict[num][0] += d
            demand_dict[num][1].append(name)

            no_car = False
          elif num == Min_Cars_num-1 and no_car:
            print 'Error! Out of vehicle_capacity'
            return 0

    initial_list = []
    for num in demand_dict:
      initial_list += demand_dict[num][1]
      if num != Min_Cars_num-1:
        initial_list.append(0)

    return initial_list


  def getPathDistance(self,path_list):
    """
    getPathDistance(path_list)
    Return a distance of the path_list
    """
    temp_list = copy.copy(path_list)

    for i in range(len(temp_list)):
      if temp_list[i] == 0:
        temp_list[i] = 1
    temp_list.append(1)
    temp_list.insert(0,1)

    total_distance = 0

    for i in range(1,len(temp_list)):
      distance = self.getDistanceBt2Nodes(temp_list[i],temp_list[i-1])
      total_distance += distance

    # print total_distance
    return total_distance


  def checkDemand(self,path_list):
    """
    checkDemand(path_list)
    Check every demand of route in the path_list
    and return a demand_list.
    """
    temp_list = copy.copy(path_list)
    temp_list.append(0)

    vehicle_capacity = self.getVehicleCapacity()

    demand_list = []
    demand = 0
    for i in range(len(temp_list)):
      if temp_list[i] != 0:
        demand += self.getDemandByName(temp_list[i])
      else:
        demand_list.append(demand)
        if demand > vehicle_capacity:
          print 'demand =',demand,'Error!'
        demand = 0
    return demand_list


  def solve(self):
    ####################################
    # Solve it!
    ##################

    # # get list and distance by initial path by vehicle
    init_path_vehicle = self.getInitPathByVehicle()
    init_path_vehicle_distance = self.getPathDistance(init_path_vehicle)
    print '\ninit_path_vehicle_distance =', init_path_vehicle_distance
    print 'init_path_vehicle =', init_path_vehicle


    # # get list and distance by initial path by sort num
    # print '\n[[[ Get an initial path by sort num...'
    # init_path_num = self.getInitPathBySortNum()
    # init_path_num_distance = self.getPathDistance(init_path_num)
    # print '\ninit_path_num_distance =', init_path_num_distance
    # print 'init_path_num =', init_path_num


    # # Use method
    print '\n\n[[[ Now Solving...'
    popInsertEveryWhere_path = self.__popInsertEveryWhere(init_path_vehicle)
    # popInsertEveryWhere_path_distance = self.getPathDistance(popInsertEveryWhere_path)
    # print '\npopInsertEveryWhere_path_distance =', popInsertEveryWhere_path_distance
    # print 'popInsertEveryWhere_path =', popInsertEveryWhere_path

    tabuSearch_path = self.tabuSearch_beta(popInsertEveryWhere_path)
    tabuSearch_path_distance = self.getPathDistance(tabuSearch_path)
    print '\ntabuSearch_path_distance =', tabuSearch_path_distance
    print 'tabuSearch_path =', tabuSearch_path

    tabuSearch_path = self.tabuSearch_beta(init_path_vehicle)
    # tabuSearch_path_distance = self.getPathDistance(tabuSearch_path)
    # print '\ntabuSearch_path_distance =', tabuSearch_path_distance
    # print 'tabuSearch_path =', tabuSearch_path

    popInsertEveryWhere_path = self.__popInsertEveryWhere(tabuSearch_path)
    popInsertEveryWhere_path_distance = self.getPathDistance(popInsertEveryWhere_path)
    print '\npopInsertEveryWhere_path_distance =', popInsertEveryWhere_path_distance
    print 'popInsertEveryWhere_path =', popInsertEveryWhere_path

    if tabuSearch_path_distance > popInsertEveryWhere_path_distance:
      tabuSearch_path = popInsertEveryWhere_path


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

    depot = 1
    for num in final_path:
      if num == 0:
        depot += 1

    result_file.write(str(self.getNumOfNodes())+' '+str(depot)+'\n')

    for i in range(len(final_path)):
      result_file.write(str(final_path[i])+' ')
    result_file.write('\n\n'+str(int(round(final_path_distance))))

    result_file.write('\n')

    temp_list = copy.copy(final_path)
    for i in range(depot):
      result_file.write('\nRoute #'+str(i+1)+': ')
      for j in range(len(temp_list)):
        if temp_list[0] == 0:
          temp_list.pop(0)
          break
        result_file.write(str(temp_list.pop(0))+' ')

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
    self.displayTextTop["text"] = "VRP-Solver"
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
    self.displayTextBottom["text"] = "Welcome to VRPSolver!"
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
    self.displayTextBottom["text"] = "The filename 'VRP_berlin52.txt' is an example."
    self.inputField.delete(0, 200)
    self.inputField.insert(0, "VRP_A-n32-k5.txt")

  def clearMethod(self):
    self.displayTextTop["text"] = "VRP-Solver"
    self.displayTextBottom["text"] = "All Clear."
    self.inputField.delete(0, 200)
    self.displayTextBottom2["text"] = ""
    self.displayTextBottom3["text"] = ""

  def solveMethod(self):
    if self.testFileName():
      self.displayTextBottom["text"] = "Filename: " + self.inputField.get()
      VRPS = VRPSolver(self.inputField.get())
      self.displayTextBottom2["text"] = "Now Solving..."

      result = VRPS.solve()
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



# VRPS = VRPSolver(filename)

# VRPS.solve()

if __name__ == '__main__':
  root = Tk()
  root.title("VRP-Solver")
  app = AppWindow(master=root)
  app.mainloop()