"""
Employees testing suite.
"""

import unittest
import random
import sys
from employees import Employee, Manager, TemporaryEmployee, PermanentEmployee


class TestEmployee(unittest.TestCase):
    """Employee Class Test Suite"""

    def test_1(self):
        """Test that Employee cannot be instantiated (abstract class)."""
        with self.assertRaises(TypeError):
            Employee("A", None, 200, 10000)


class TestManager(unittest.TestCase):
    """Manager Class Test Suite"""

    def test_1(self):
        """Test initialization of Manager attributes."""
        e = Manager("A", None, 200, 10000)
        self.assertEqual(e.relationships, {})
        self.assertEqual(e.salary, 200)
        self.assertTrue(e.is_employed)
        self.assertEqual(e.name, "A")
        self.assertEqual(e.manager, None)
        self.assertEqual(e.performance, 75)
        self.assertEqual(e.happiness, 50)
        self.assertEqual(e.savings, 10000)

    def test_2(self):
        """Test changing name."""
        e = Manager("A", None, 200, 10000)
        with self.assertRaises(AttributeError):
            e.name = "B"

    def test_3(self):
        """Test setting performance to a normal value."""
        e = Manager("A", None, 200, 10000)
        e.performance = 85
        self.assertEqual(e.performance, 85)

    def test_4(self):
        """Test performance value below zero should set to 0."""
        e = Manager("A", None, 200, 10000)
        e.performance -= 101
        self.assertEqual(e.performance, 0)

    def test_5(self):
        """Test performance value above 100 should set to 100."""
        e = Manager("A", None, 200, 10000)
        e.performance = 150
        self.assertEqual(e.performance, 100)

    def test_6(self):
        """Test setting happiness to a normal value."""
        e = Manager("A", None, 200, 10000)
        e.happiness = 70
        self.assertEqual(e.happiness, 70)
    
    def test_7(self):
        """Test happiness value below zero should set to 0."""
        e = Manager("A", None, 200, 10000)
        e.happiness -= 101
        self.assertEqual(e.happiness, 0)

    def test_8(self):
        """Test happiness value above 100 should set to 100."""
        e = Manager("A", None, 200, 10000)
        e.happiness = 120
        self.assertEqual(e.happiness, 100)

    def test_9(self):
        """Test setting salary to a normal value."""
        e = Manager("A", None, 200, 10000)
        e.salary = 6000
        self.assertEqual(e.salary, 6000)

    def test_10(self):
        """Test setting salary to a negative value."""
        e = Manager("A", None, 200, 10000)
        with self.assertRaises(ValueError):
            e.salary = -6000

    def test_11(self):
        """Test savings set to a normal value."""
        e = Manager("A", None, 200, 0)
        e.savings += 15000
        self.assertEqual(e.savings, 15000)

    def test_12(self):
        """Test decrementing savings to negative value."""
        e = Manager("A", None, 200, 0)
        e.savings -= 500
        self.assertEqual(e.savings, -500)

    def test_13(self):
        """Test daily expense deduction on savings."""
        e = Manager("A", None, 200, 10000)
        e.daily_expense()
        self.assertEqual(e.savings, 9940)

    def test_14(self):
        """Test daily expense deduction on happiness."""
        e = Manager("A", None, 200, 10000)
        e.daily_expense()
        self.assertEqual(e.happiness, 49)

    def test_15(self):
        """Test daily expense results in negative savings."""
        e = Manager("A", None, 200, 50)
        e.daily_expense()
        self.assertEqual(e.savings, -10)

    def test_16(self):
        """Test interaction creates a new relationship."""
        e1 = Manager("A", None, 200, 10000)
        e2 = Manager("B", e1, 6000, 15000)
        e1.interact(e2)
        self.assertIn("B", e1.relationships)
        self.assertEqual(e1.relationships["B"], 1)

    def test_17(self):
        """Test interaction increases happiness when relationship score is high."""
        e1 = Manager("A", None, 200, 10000)
        e2 = Manager("B", e1, 6000, 15000)
        e1.relationships["B"] = 15
        e1.interact(e2)
        self.assertEqual(e1.happiness, 51)

    def test_18(self):
        """Test interaction decreases happiness when both employees are unhappy."""
        e1 = Manager("A", None, 200, 10000)
        e2 = Manager("B", e1, 6000, 15000)
        e1.happiness = 40
        e2.happiness = 40
        e1.interact(e2)
        self.assertEqual(e1.happiness, 39)
        self.assertEqual(e1.relationships["B"], -1)

    def test_19(self):
        """Test interaction with a new employee starts with 0 relationship score."""
        e1 = Manager("A", None, 200, 10000)
        e2 = Manager("B", e1, 6000, 15000)
        e1.interact(e2)
        e2.interact(e1)
        self.assertEqual(e1.relationships["B"], 1)
        self.assertEqual(e2.relationships["A"], 1)

    def test_20(self):
        """Test manager work increases performance."""
        e = Manager("A", None, 200, 10000)
        random.seed(999)
        e.work()
        self.assertGreaterEqual(e.performance, 80)

    def test_21(self):
        """Test manager work decreases performance."""
        e = Manager("A", None, 200, 10000)
        random.seed(123)
        e.work()
        self.assertEqual(e.performance, 70)

    def test_22(self):
        """Test work when performance is at zero."""
        e = Manager("A", None, 200, 10000)
        e.performance = 1
        random.seed(123)
        e.work()
        self.assertGreaterEqual(e.performance, 0)

    def test_23(self):
        """Test work maintains performance at boundary when it reaches zero."""
        e = Manager("A", None, 200, 10000)
        e.performance = 0
        random.seed(6)
        e.work()
        self.assertGreaterEqual(e.performance, 0)

    def test_24(self): 
        """Test performance does not exceed 100 when increased."""
        e = Manager("A", None, 200, 10000)
        e.performance = 100
        random.seed(0)
        e.work()
        self.assertEqual(e.performance, 100)

    def test_25(self):
        """Test that relationships decrease if manager performance decreases."""
        e = Manager("A", None, 200, 10000)
        e.relationships = {"B": 3}
        random.seed(2)  # Ensure performance decreases
        e.work()
        self.assertEqual(e.relationships["B"], 2)

    def test_26(self):
        """Test happiness and relationship after multiple interactions."""
        e1 = Manager("H", None, 2500, 7000)
        e2 = Manager("I", e1, 3000, 9000)
        e1.happiness = 52
        for i in range(5):
            e1.interact(e2)
            self.assertEqual(e1.relationships["I"], i + 1)
        self.assertEqual(e1.happiness, 52)
        random.seed(123)
        e1.work()
        self.assertEqual(e1.happiness, 51)
        self.assertEqual(e1.relationships["I"], 4)

    def test_27(self):
        """Interact with the manager multiple times."""
        e1 = Manager("P", None, 5500, 15000)
        e2 = Manager("Q", e1, 5000, 12000)
        e1.happiness = 60
        e2.happiness = 60
        for _ in range(10):
            e1.interact(e2)
        e2.interact(e1)

        self.assertEqual(e1.relationships["Q"], 10)
        self.assertEqual(e2.relationships["P"], 1)
        self.assertEqual(e1.happiness, 60)

    def test_28(self): 
        """Interact with the manager and work."""
        e1 = Manager("J", None, 5000, 10000)
        e2 = Manager("K", e1, 6000, 12000)
        e1.happiness = 20
        e2.happiness = 30
        e1.interact(e2)
        random.seed(54)
        e1.work()
        self.assertEqual(e1.happiness, 18)
        self.assertEqual(e1.relationships["K"], -2)

    def test_29(self):
        """Test string representation of a manager."""
        e = Manager("A", None, 500, 100000)
        self.assertEqual(
            str(e),
            "A\n\tSalary: $500\n\tSavings: $100000\n\tHappiness: 50%\n\tPerformance: 75%",
        )


class TestTemporaryEmployee(unittest.TestCase):
    """Temporary Employee Test Suite"""

    def test_1(self):
        """Test temporary employee work decreases performance."""
        e = TemporaryEmployee("A", None, 200, 10000)
        random.seed(3)
        e.work()
        self.assertEqual(e.performance, 67)

    def test_2(self):
        """Test temporary employee work increases performance."""
        e = TemporaryEmployee("A", None, 200, 10000)
        random.seed(5)
        e.work()
        self.assertEqual(e.performance, 79)

    def test_3(self):
        """Test temporary employee work decreases happiness."""
        e = TemporaryEmployee("A", None, 200, 10000)
        random.seed(3)
        e.work()
        self.assertEqual(e.happiness, 48)

    def test_4(self):
        """Test temporary employee work increases happiness."""
        e = TemporaryEmployee("A", None, 200, 10000)
        random.seed(10)
        e.work()
        self.assertEqual(e.happiness, 51)

    def test_5(self):
        """Test happiness value below 0 should set to 0."""
        e = TemporaryEmployee("A", None, 200, 10000)
        e.happiness = 0
        random.seed(3)
        e.work()
        self.assertEqual(e.happiness, 0)

    def test_6(self):
        """Test happiness value above 100 should set to 100."""
        e = TemporaryEmployee("A", None, 200, 10000)
        e.happiness = 100
        random.seed(10)
        e.work()
        self.assertEqual(e.happiness, 100)
    
    def test_7(self):
        """Test temp employee interaction gives bonus when performance is high."""
        manager = Manager("M", None, 10000, 20000)
        employee = TemporaryEmployee("A", manager, 200, 10000)
        employee.performance = 60
        manager.happiness = 60
        employee.interact(manager)
        manager.interact(employee)
        self.assertEqual(employee.savings, 11000)

    def test_8(self):
        """Test temp employee salary halves and becomes unemployed if performance is low."""
        manager = Manager("M", None, 10000, 20000)
        employee = TemporaryEmployee("A", manager, 200, 10000)
        employee.performance = 40
        manager.happiness = 40
        employee.interact(manager)
        manager.interact(employee)
        self.assertEqual(employee.salary, 100)
        self.assertTrue(employee.is_employed)

    def test_9(self):
        """Test interaction with a non-manager employee does not change salary or savings."""
        manager = Manager("M", None, 10000, 20000)
        employee = TemporaryEmployee("A", manager, 200, 10000)
        other_employee = TemporaryEmployee("B", manager, 4000, 8000)
        employee.interact(other_employee)
        self.assertEqual(employee.savings, 10000)
        self.assertEqual(employee.salary, 200)

    def test_10(self):
        """Test work does not modify savings."""
        e = TemporaryEmployee("A", None, 200, 10000)
        random.seed(6)
        e.work()
        self.assertEqual(e.savings, 10000)

    def test_11(self):
        """Test daily expense reduces savings and happiness but not salary."""
        e = TemporaryEmployee("A", None, 200, 1000)
        e.daily_expense()
        self.assertEqual(e.savings, 940)
        self.assertEqual(e.salary, 200)
        self.assertEqual(e.happiness, 49)

    def test_12(self):
        """Test temp employee becomes unemployed when salary is halved to 0."""
        manager = Manager("M", "Bob", 10000, 20000)
        employee = TemporaryEmployee("A", manager, 1, 10000)
        manager.happiness = 40
        employee.performance = 40
        employee.interact(manager)
        manager.interact(employee)
        self.assertFalse(employee.is_employed)

    def test_13(self):
        """Test temp employee does not get bonus if manager happiness is low."""
        manager = Manager("M", None, 10000, 20000)
        employee = TemporaryEmployee("A", manager, 200, 10000)
        employee.performance = 60
        manager.happiness = 40
        employee.interact(manager)
        manager.interact(employee)
        self.assertEqual(employee.savings, 10000)

    def test_14(self):
        """Test interaction with a manager who is not the employee's direct manager."""
        manager = Manager("M", None, 10000, 20000)
        employee = TemporaryEmployee("A", manager, 200, 10000)
        other_employee = TemporaryEmployee("B", None, 4000, 8000)
        other_employee.interact(manager)
        self.assertEqual(other_employee.salary, 4000)
        self.assertEqual(other_employee.savings, 8000)

    def test_15(self):
        """Test string representation of a temp employee."""
        e = TemporaryEmployee("A", None, 200, 10000)
        self.assertEqual(
            str(e),
            "A\n\tSalary: $200\n\tSavings: $10000\n\tHappiness: 50%\n\tPerformance: 75%",
        )


class TestPermanentEmployee(unittest.TestCase):
    """Permanent Employee Test Suite"""

    def test_1(self):
        """Test permanent employee work decreases performance."""
        e = PermanentEmployee("A", None, 200, 10000)
        random.seed(3)
        e.work()
        self.assertEqual(e.performance, 72)

    def test_2(self):
        """Test permanent employee work increases performance."""
        e = PermanentEmployee("A", None, 200, 10000)
        random.seed(5)
        e.work()
        self.assertEqual(e.performance, 84)

    def test_3(self):
        """Test perm employee interaction gives bonus when performance is high."""
        manager = Manager("M", None, 10000, 20000)
        employee = PermanentEmployee("A", manager, 200, 10000)
        employee.performance = 30
        manager.happiness = 60
        employee.interact(manager)
        self.assertEqual(employee.savings, 11000)

    def test_4(self):
        """Test perm employee interaction gives bonus depend on manager's happiness."""
        manager = Manager("M", None, 10000, 20000)
        employee = PermanentEmployee("A", manager, 200, 10000)
        employee.performance = 30
        manager.happiness = 60
        employee.interact(manager)
        self.assertEqual(employee.savings, 11000)    
        manager.happiness = 30
        employee.interact(manager)
        self.assertEqual(employee.savings, 11000)    

    def test_5(self):
        """Test perm employee does not get bonus when performance is low."""
        manager = Manager("M", None, 10000, 20000)
        employee = PermanentEmployee("A", manager, 200, 10000)
        employee.performance = 20
        manager.happiness = 60
        employee.interact(manager)
        self.assertEqual(employee.savings, 10000)

    def test_6(self):
        """Test interaction with a non-manager employee does not give bonus."""
        manager = Manager("M", None, 10000, 20000)
        employee = PermanentEmployee("A", manager, 200, 10000)
        other_employee = PermanentEmployee("B", manager, 4000, 8000)
        employee.interact(other_employee)
        self.assertEqual(employee.savings, 10000)

    def test_7(self):
        """Test work does not modify salary and savings."""
        e = PermanentEmployee("A", None, 200, 10000)
        e.work()
        self.assertEqual(e.savings, 10000)
        self.assertEqual(e.salary, 200)

    def test_8(self):
        """Test permanent employee does not become unemployed after interaction and 0 salary."""
        manager = Manager("M", None, 10000, 20000)
        employee = PermanentEmployee("A", manager, 0, 10000)
        manager.happiness = 40
        employee.performance = 20
        employee.interact(manager)
        manager.interact(employee)
        self.assertTrue(employee.is_employed)

    def test_9(self):
        """Test permanent employee performance does not exceed 100."""
        e = PermanentEmployee("A", None, 200, 10000)
        e.performance = 99
        random.seed(5)
        e.work()
        self.assertEqual(e.performance, 100)

    def test_10(self):
        """Test permanent employee performance remains non-negative at boundary."""
        e = PermanentEmployee("A", None, 200, 10000)
        e.performance = 1
        random.seed(6)
        e.work()
        self.assertGreaterEqual(e.performance, 0)

    def test_11(self):
        """Test permanent employee happiness decreases after daily expense."""
        e = PermanentEmployee("A", None, 200, 10000)
        e.daily_expense()
        self.assertEqual(e.happiness, 49)

    def test_12(self):
        """Test permanent employee savings decreases after daily expense."""
        e = PermanentEmployee("A", None, 200, 10000)
        e.daily_expense()
        self.assertEqual(e.savings, 9940)

    def test_13(self):
        """Test permanent employee interactions with manager with different performance levels."""
        manager = Manager("M", None, 10000, 20000)
        employee = PermanentEmployee("A", manager, 200, 10000)
        employee.performance = 20
        manager.happiness = 80
        employee.interact(manager)
        self.assertEqual(employee.savings, 10000)
        self.assertEqual(employee.performance, 20)
        random.seed(5)
        employee.work()
        self.assertEqual(employee.performance, 29)
        employee.work()  
        self.assertEqual(employee.performance, 27)
        employee.interact(manager)
        self.assertEqual(employee.savings, 11000)
        self.assertEqual(employee.performance, 27)

    def test_14(self): 
        """Test perm employee with two unhappy managers (one is the direct manager)."""
        manager1 = Manager("M1", None, 10000, 20000)
        manager2 = Manager("M2", None, 12000, 25000)
        employee = PermanentEmployee("A", manager1, 200, 10000)
        manager1.happiness = 5
        manager2.happiness = 6
        employee.interact(manager1)
        self.assertEqual(employee.happiness, 48)
        employee.interact(manager2)
        self.assertEqual(employee.happiness, 47)

    def test_15(self):
        """Test string representation of a perm employee."""
        e = PermanentEmployee("A", None, 300, 1000)
        self.assertEqual(
            str(e),
            "A\n\tSalary: $300\n\tSavings: $1000\n\tHappiness: 50%\n\tPerformance: 75%",
        )


if __name__ == "__main__":
    unittest.main()
