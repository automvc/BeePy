from entity.Orders import Orders

if __name__ == '__main__':
    print("start")
    
    # MyConfig.init()
    
    # orders=Orders()
    # orders.name = "bee"
        
    # print(Orders.__annotations__)    
    anno={}
    try:
        anno =Orders.__annotations__
    except Exception:
        pass
    print(anno)  
    
    print("finished")
