from bee.api import Suid


# from bee.api import Suid
# from bee.HoneyUtil import HoneyUtil
class MyClass:
    i = 10
    name = "default name"

    def f(self):
        return "hello world"


if __name__ == '__main__':
    print("start")
    
    x = MyClass()

    print("x.i   ", x.i)
    print("MyClass.i   ", MyClass.i)

    x.i = 100
    print("x.i   ", x.i)
    print("MyClass.i   ", MyClass.i)

    MyClass.i = 200
    print("x.i   ", x.i)
    print("MyClass.i   ", MyClass.i)
    
    suid = Suid()

    suid.select(x)
    
    # HoneyUtil.print_obj_dict(x)
    # HoneyUtil.print_class_dict(MyClass)

