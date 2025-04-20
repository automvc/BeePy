from bee.api import PreparedSql
from bee.context import HoneyContext

import MyConfig
from entity.Orders import Orders


if __name__ == "__main__":
    
    MyConfig.init()    
    pre = PreparedSql()
    
    print("-------------------")
    # orders_list = pre.select_dict("SELECT * FROM orders WHERE name=#{name} and id=#{id} and name=#{name}", Orders, params_dict={"name":"bee1", "id":4})
    # print(orders_list)
    
    sql = "update orders set name = ?, remark = ? where id = ?"
    # placeholder=HoneyContext.get_placeholder() #in python different db have diffent placeholder
    # sql=sql.replace("?", placeholder)
    
    params = ('bee130', 'test-update', 1)
    updateNum = pre.modify(sql, params)
    print("updateNum:", updateNum)
    
    
    sql ="update orders set name = %s, remark = %s where id = %s"
    params = ('bee130', 'test-update', 1)
    updateNum = pre.modify(sql, params)
    print("updateNum:", updateNum)
    
    # print("-------------------")
    # orders_list = pre.select_dict("SELECT * FROM orders", Orders)
    # print(orders_list)
    #
    # orders_list = pre.select_dict("SELECT * FROM orders where id = #{id}", Orders, params_dict={"id":1})
    # print(orders_list)
    #
    # sql = "update orders set name = #{name}, remark = #{remark} where id = #{id}"
    # params_dict = {"id":1, "name":"newName", "remark":"remark2"}
    # updateNum = pre.modify_dict(sql, params_dict)
    #
    # orders_list = pre.select_dict("SELECT * FROM orders where id=#{id}", Orders, params_dict={"id":1})
    # print(orders_list)
    
    print("finished")
