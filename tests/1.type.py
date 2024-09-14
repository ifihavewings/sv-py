def my_function(*args):
    print(type(args))
    for arg in args:
        print(arg)

my_function(1, 2, 3)  # 输出: 1 2 3
my_function("apple", "banana")  # 输出: apple banana


def greet(name, message="Hello"):
    print(f"{message}, {name}!")

# 使用位置参数
greet("Alice")  # 输出: Hello, Alice!
# 使用关键字参数
greet(name="Bob", message="Hi")  # 输出: Hi, Bob!

def introduce(name, age, country="Unknown"):
    print(f"Name: {name}, Age: {age}, Country: {country}")

# 位置参数调用（按顺序传递）
introduce("Alice", 30)
# 输出: Name: Alice, Age: 30, Country: Unknown

# 关键字参数调用（顺序无关）
introduce(age=25, name="Bob", country="USA")
# 输出: Name: Bob, Age: 25, Country: USA

def describe_person(name, **kwargs):
    print(type(kwargs))
    print(f"Name: {name}")
    for key, value in kwargs.items():
        print(f"{key}: {value}")

describe_person("Alice", age=30, country="USA", occupation="Engineer")

from app.utils.os_utils import get_project_absolute_path
print(get_project_absolute_path())
