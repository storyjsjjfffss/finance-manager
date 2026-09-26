from celery.worker.state import total_count


class Employee:
    def __init__(self, emp_id, name ,department):
        self.emp_id = emp_id
        self.name = name
        self.department = department
    def calculate_pay(self):
        raise NotImplementedError("子类必须实现具体的薪资计算逻辑！")
    def print_pay_slip(self):
        print(f"工号: {self.emp_id} | 姓名: {self.name} | 部门: {self.department} | 实发工资: ¥{self.calculate_pay():.2f}")

class SalaryEmployee(Employee):
    def __init__(self, emp_id, name ,department, monthly_salary):
        super().__init__(emp_id,name, department )
        self.monthly_salary = monthly_salary
    def calculate_pay(self):
        return self.monthly_salary

class HourlyEmployee(Employee):
    def __init__(self, emp_id, name ,department, hourly_rate,hours_worked):
        super().__init__(emp_id,name,department)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked
    def calculate_pay(self):
        if self.hours_worked<=160:
            return self.hourly_rate*self.hours_worked
        else:
            return self.hourly_rate*160+(self.hourly_rate*1.5*(self.hours_worked-160))



if __name__ == "__main__":
    total_budget=0
    day_emp = SalaryEmployee("E001","Alex","技术部",15000.0)
    hour_emp = HourlyEmployee("H001","Bob","客服部",60.0,180)
    staff_list=[day_emp,hour_emp]
    for emp in staff_list:
        emp.print_pay_slip()
        total_budget+=emp.calculate_pay()
    print(f"本月公司需要支付{total_budget:.2f}")
    print(f"本月公司需要支付{day_emp.calculate_pay()+hour_emp.calculate_pay()}")
