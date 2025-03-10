"""
Student information for this assignment:

On my/our honor, Xinyue Yu, this
programming assignment is my own work and I have not provided this code to
any other student.

I have read and understand the course syllabus's guidelines regarding Academic
Integrity. I understand that if I violate the Academic Integrity policy (e.g.
copy code from someone else, have the code generated by an LLM, or give my
code to someone else), the case shall be submitted to the Office of the Dean of
Students. Academic penalties up to and including an F in the course are likely.

UT EID: xy4677
"""

from abc import ABC, abstractmethod
import random

DAILY_EXPENSE = 60
HAPPINESS_THRESHOLD = 50
MANAGER_BONUS = 1000
TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD = 50
PERM_EMPLOYEE_PERFORMANCE_THRESHOLD = 25
RELATIONSHIP_THRESHOLD = 10
INITIAL_PERFORMANCE = 75
INITIAL_HAPPINESS = 50
PERCENTAGE_MAX = 100
PERCENTAGE_MIN = 0
SALARY_ERROR_MESSAGE = "Salary must be non-negative."


class Employee(ABC):
    """
    Abstract base class representing a generic employee in the system.
    """

    def __init__(self, name, manager, salary, savings):
        self.relationships = {}
        self.savings = savings
        self.is_employed = True
        self.__name = name
        self.__manager = manager
        self.performance = INITIAL_PERFORMANCE
        self.happiness = INITIAL_HAPPINESS
        self.salary = salary

    @property
    def name(self):
        """Get the employee's name."""
        return self.__name

    @property
    def manager(self):
        """Get the employee's manager."""
        return self.__manager

    @property
    def performance(self):
        """Get the employee's performance."""
        return self._performance

    @performance.setter
    def performance(self, performance):
        if performance < PERCENTAGE_MIN:
            performance = PERCENTAGE_MIN
        elif performance > PERCENTAGE_MAX:
            performance = PERCENTAGE_MAX
        self._performance = performance

    @property
    def happiness(self):
        """Get the employee's happiness."""
        return self._happiness

    @happiness.setter
    def happiness(self, happiness):
        if happiness < PERCENTAGE_MIN:
            happiness = PERCENTAGE_MIN
        elif happiness > PERCENTAGE_MAX:
            happiness = PERCENTAGE_MAX
        self._happiness = happiness

    @property
    def salary(self):
        """Get the employee's salary."""
        return self._salary

    @salary.setter
    def salary(self, salary):
        if salary < 0:
            raise ValueError(SALARY_ERROR_MESSAGE)
        self._salary = salary

    @abstractmethod
    def work(self):
        """Employee's work method."""

    def interact(self, other):
        """
        Handle interaction between employees, affecting happiness and relationships.
        """
        if other.name not in self.relationships:
            self.relationships[other.name] = 0
        if self.relationships[other.name] > RELATIONSHIP_THRESHOLD:
            self.happiness += 1
        elif self.happiness >= HAPPINESS_THRESHOLD and other.happiness >= HAPPINESS_THRESHOLD:
            self.relationships[other.name] += 1
        else:
            self.relationships[other.name] -= 1
            self.happiness -= 1

    def daily_expense(self):
        """Deduct daily expenses from savings and reduce happiness."""
        self.happiness -= 1
        self.savings -= DAILY_EXPENSE

    def __str__(self):
        return (
            f"{self.name}\n\tSalary: ${self.salary}\n\tSavings: ${self.savings}"
            f"\n\tHappiness: {self.happiness}%\n\tPerformance: {self.performance}%"
        )


class Manager(Employee):
    """
    A subclass of Employee representing a manager.
    """
    def work(self):
        change = random.randint(-5, 5)
        self.performance += change
        if change <= 0:
            self.happiness -= 1
            for employee in self.relationships:
                self.relationships[employee] -= 1
        else:
            self.happiness += 1


class TemporaryEmployee(Employee):
    """
    A subclass of Employee representing a temporary employee.
    """
    def work(self):
        change = random.randint(-15, 15)
        self.performance += change
        if change <= 0:
            self.happiness -= 2
        else:
            self.happiness += 1

    def interact(self, other):
        super().interact(other)
        if other == self.manager:
            if (
                other.happiness > HAPPINESS_THRESHOLD
                and self.performance > TEMP_EMPLOYEE_PERFORMANCE_THRESHOLD
            ):
                self.savings += MANAGER_BONUS
            elif self.salary > 0:
                self.salary //= 2
                self.happiness -= 5
                if self.salary == 0:
                    self.is_employed = False


class PermanentEmployee(Employee):
    """
    A subclass of Employee representing a permanent employee.
    """
    def work(self):
        change = random.randint(-10, 10)
        self.performance += change
        if change >= 0:
            self.happiness += 1

    def interact(self, other):
        super().interact(other)
        if other == self.manager:
            if (
                other.happiness > HAPPINESS_THRESHOLD
                and self.performance > PERM_EMPLOYEE_PERFORMANCE_THRESHOLD
            ):
                self.savings += MANAGER_BONUS
            elif other.happiness <= HAPPINESS_THRESHOLD:
                self.happiness -= 1
