class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
  getName() {
    return this.name;
  }
}

class Employee extends Person {
  constructor(name, age, employeeId) {
    super(name, age);
    this.employeeId = employeeId;
  }
  getEmployeeId() {
    return this.employeeId;
  }
  getNameAndEmployeeId() {
    return `${this.getName()} (${this.getEmployeeId()})`;
  }
}
