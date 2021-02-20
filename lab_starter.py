#NAME   : Abdulhakim 
#SURNAME: Özcan
#ID     : 53766


class Employee:
   
   empCount = 0

   def __init__(self, name, salary):
      self.name = name
      self.salary = salary
      Employee.empCount += 1
   
   def displayCount(self):
     print ("Total Employee",Employee.empCount)

   def displayEmployee(self):
      print ("Name : ", self.name,  ", Salary: ", self.salary)

emp1 = Employee("Harry", 2000)
emp2 = Employee("Alex", 5000)
emp1.displayEmployee()
emp2.displayEmployee()
print ("Total Employee",Employee.empCount)

    
        
    

