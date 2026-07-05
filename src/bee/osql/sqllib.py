from bee.bee_enum import LocalType
from bee.context import HoneyContext
from bee.exception import SqlBeeException, BeeException
from bee.osql.base import AbstractBase
from bee.osql.cache import CacheUtil
from bee.osql.logger import Logger
from bee.osql.transform import ParamUtil, ResultUtil


class BeeSql(AbstractBase):
    '''
    BeeSql is a lib for operation database.
    '''

    def select(self, sql, entityClass, params = None):
    # def select(self, sql: str, entityClass: type, params=None) -> list:

        cacheObj = CacheUtil.get(sql)
        if cacheObj is not None:
            super().loginfo("---------------get from cache")
            super().loginfo(" | <--  select rows: " + str(len(cacheObj)))
            return cacheObj

        conn = self.__getConn()
        rs_list = []
        try:
            cursor = conn.cursor()
            # # with conn.cursor() as cursor:  # SQLite不支持with语法
            params = ParamUtil.transform_param(params)
            # 执行 SQL 查询
            cursor.execute(sql, params or [])
            # 获取列名
            column_names = [description[0] for description in cursor.description]
            # 获取所有结果
            results = cursor.fetchall()

            for row in results:
                # 将行数据映射到新创建的实体对象
                target_obj = ResultUtil.transform_result(row, column_names, entityClass)
                rs_list.append(target_obj)
            super().loginfo(" | <--  select rows: " + str(len(rs_list)))
            super().addInCache(sql, rs_list, len(rs_list))
        except Exception as e:
            raise SqlBeeException(e)
        finally:
            self.__close(cursor, conn)
        return rs_list

    # 执行 UPDATE/INSERT/DELETE 操作
    # def modify(self, sql: str, params=None) -> int:
    def modify(self, sql, params = None):
        '''
        modify: UPDATE/INSERT/DELETE
        :param sql: SQL statement which use placeholder.
        :param params: list type params for placeholder.
        :return: the number of affected successfully records.
        '''
        conn = self.__getConn()
        a = 0
        try:
            cursor = conn.cursor()
            params = ParamUtil.transform_param(params)
            cursor.execute(sql, params or [])
            conn.commit()
            a = cursor.rowcount  # 返回受影响的行数
            super().loginfo(" | <--  Affected rows: " + str(a))

            if a > 0:
                CacheUtil.clear(sql)
            return a
        except Exception as e:
            Logger.warn(f"Error in modify: {e}")
            conn.rollback()
            return 0
        finally:
            self.__close(cursor, conn)

    def batch(self, sql, params = None):
        conn = self.__getConn()
        a = 0
        try:
            cursor = conn.cursor()
            params = ParamUtil.transform_list_tuple_param(params)
            cursor.executemany(sql, params or [])
            conn.commit()
            a = cursor.rowcount  # 返回受影响的行数
            super().loginfo(" | <--  Affected rows: " + str(a))

            if a > 0:
                CacheUtil.clear(sql)

            return a
        except Exception as e:
            Logger.warn(f"Error in batch: {e}")
            conn.rollback()
            return 0
        finally:
            self.__close(cursor, conn)

    def select_fun(self, sql, params = None):

        cacheObj = CacheUtil.get(sql)
        if cacheObj is not None:
            super().loginfo("---------------get from cache")
            super().loginfo(" | <--  select rows: 1")
            return cacheObj

        conn = self.__getConn()
        rs_fun = ''
        try:
            cursor = conn.cursor()
            params = ParamUtil.transform_param(params)
            cursor.execute(sql, params or [])
            result = cursor.fetchone()  # 返回一个元组，例如 (1,)
            if result[0]:
                super().loginfo(" | <--  select rows: 1")

                super().addInCache(sql, result[0], 1)

            return result[0]

        except Exception as e:
            raise SqlBeeException(e)
        finally:
            self.__close(cursor, conn)

        return rs_fun

    def moreTableSelect(self, sql, entityClass, params = None):
        cacheObj = CacheUtil.get(sql)
        if cacheObj is not None:
            super().loginfo("---------------get from cache")
            super().loginfo(" | <--  select rows: " + str(len(cacheObj)))
            return cacheObj

        conn = self.__getConn()
        rs_list = []
        try:
            cursor = conn.cursor()
            # # with conn.cursor() as cursor:  # SQLite不支持with语法
            params = ParamUtil.transform_param(params)
            cursor.execute(sql, params or [])
            # 获取列名
            column_names = [description[0] for description in cursor.description]
            # 获取所有结果
            results = cursor.fetchall()

            moreTableStructDict = HoneyContext.get_data(LocalType.MoreTableStruct, entityClass)

            current_subObject_list_cache_dict = {}  # main_key#sub_fieldname : [subObject]    # 对象list缓存
            current_single_subObject_cache_dict = {}  # main_key#sub_fieldname : subObject    #单个对象缓存
            one_to_one_for_two_layer_set = set()
            no_obj_layer_set= set()

            for row in results:
                # 将行数据映射到新创建的实体对象
                # str2_cache_dict sub_field_value_str_cache_dict
                #subObj_cache_dict reutrn_subObject_cache_dict
                # transform_result3
                main_obj, main_key, str2_cache_dict, subObj_cache_dict = \
                ResultUtil.transform_result3(row, column_names, entityClass, moreTableStructDict)
                no_obj_layer = None
                
                if not moreTableStructDict or not subObj_cache_dict:
                    rs_list.append(main_obj)
                    continue

                for mtStruct in moreTableStructDict.values():
                    if mtStruct.layer == 2:
                        ptree = mtStruct.ptree
                        key0 = main_key
                        sub_field_value_str = str2_cache_dict.get(ptree[0], None)
                        current_key1 = ""
                        if sub_field_value_str:
                            current_key1 = "#".join(sub_field_value_str)
                        layer_key = key0 + ".." + ptree[0] + "##" + current_key1
                        
                        try:
                            sub_obj = subObj_cache_dict[mtStruct.sub_alias]
                        except KeyError:
                            print(mtStruct.has_next_layer)
                            if mtStruct.has_next_layer and mtStruct.sub_alias not in no_obj_layer_set:
                                no_obj_layer_set.add(mtStruct.sub_alias)
                                Logger.info(f"Not found the value in object {mtStruct.sub_alias}, will ignore it and its sub layers!")
                            if no_obj_layer is None:
                                no_obj_layer = mtStruct.layer  # 第一次出现
                                continue

                        if mtStruct.current_is_list:
                            sub_list_obj = current_subObject_list_cache_dict.get(key0, None)
                            # one_to_one_for_two_layer_set.add(key0) #1:n:1  第二级是list的属性将第一层添加了； 非list的第二层属性也不用再添加第一层的对象。

                            if sub_list_obj is None:
                                sub_list_obj = [sub_obj]
                                current_subObject_list_cache_dict[key0] = sub_list_obj
                                setattr(main_obj, mtStruct.fieldname, sub_list_obj)
                                if key0 not in one_to_one_for_two_layer_set:
                                    rs_list.append(main_obj)
                                    one_to_one_for_two_layer_set.add(key0)  # 1:n:1  第二级是list的属性将第一层添加了； 非list的第二层属性也不用再添加第一层的对象。
                                current_single_subObject_cache_dict[layer_key] = sub_obj
                            else:  # 二级列表有了
                                # 但第二级的对象还未加有，则要加到一级对象list下
                                if layer_key not in current_single_subObject_cache_dict:
                                    current_subObject_list_cache_dict[key0].append(sub_obj)
                                    current_single_subObject_cache_dict[layer_key] = sub_obj
                                # else:  二级的对象已经加有了，就不用再加。
                                    # pass #已经存在，则不用放。
                        else:  # not list
                            setattr(main_obj, mtStruct.fieldname, sub_obj)
                            current_single_subObject_cache_dict[layer_key] = sub_obj #fixed
                            
                            if key0 not in one_to_one_for_two_layer_set:
                                rs_list.append(main_obj)  # 第二层为1时，每行只需要添加一次
                                one_to_one_for_two_layer_set.add(key0)
                            # one has one时，第三层会找不到第二层的缓存；  因非list,第二层没放缓存。  是通过将三级子对象设置到二级子对象的属性完成对象关联的

                    elif mtStruct.layer >= 3:
                        
                        if no_obj_layer is not None and mtStruct.layer > no_obj_layer:
                            continue  # 若该层没有数据返回，则直接不处理它的子类了，不能断层。
                        else:
                            no_obj_layer = None  # reset  这样，同层的其它对象就可以被处理
                        try:
                            sub_obj = subObj_cache_dict[mtStruct.sub_alias]

                        except KeyError:
                            # print(mtStruct.has_next_layer)
                            if mtStruct.has_next_layer and mtStruct.sub_alias not in no_obj_layer_set:
                                no_obj_layer_set.add(mtStruct.sub_alias)
                                Logger.info(f"Not found the value in object {mtStruct.sub_alias}, will ignore it and its sub layers!")
                            if no_obj_layer is None:
                                no_obj_layer = mtStruct.layer  # 第一次出现
                                continue

                        ptree = mtStruct.ptree
                        key0 = main_key
                        sub_field_value_str = str2_cache_dict.get(ptree[0], None)
                        current_key1 = "#".join(sub_field_value_str)
                        key1 = key0 + ".." + ptree[0] + "##" + current_key1

                        # ptree不存root,长度会比层数少1, key1只计算到ptree倒数第二层.
                        loop_n = mtStruct.layer - 2 - 1
                        if loop_n >= 1:
                            for i in range(1, loop_n + 1):
                                sub_field_value_str = str2_cache_dict.get(ptree[i], None)
                                current_key_i = "#".join(sub_field_value_str)
                                key1 = key1 + ".." + ptree[i] + "##" + current_key_i

                        current_single_subObject = current_single_subObject_cache_dict.get(key1, None)

                        if current_single_subObject:
                            if mtStruct.current_is_list:
                                sub_list_obj = current_subObject_list_cache_dict.get(key1, None)
                                sub_field_value_str2 = str2_cache_dict.get(ptree[mtStruct.layer - 2], None)
                                current_key2 = "#".join(sub_field_value_str2)
                                layer_key = key1 + ".." + ptree[mtStruct.layer - 2] + "##" + current_key2
                                if sub_list_obj is None:
                                    sub_list_obj = [sub_obj]
                                    setattr(current_single_subObject, mtStruct.fieldname, sub_list_obj)
                                    current_subObject_list_cache_dict[key1] = sub_list_obj
                                    current_single_subObject_cache_dict[layer_key] = sub_obj
                                else:  # 第三级列表是有了，
                                    # 但，第三级的对象还未加有，则要加到二级对象list下
                                    if layer_key not in current_single_subObject_cache_dict:
                                        current_subObject_list_cache_dict[key1].append(sub_obj)
                            else:
                                setattr(subObj_cache_dict[mtStruct.main_alias], mtStruct.fieldname, sub_obj)
                                current_single_subObject_cache_dict[layer_key] = sub_obj #fixed
                        else:
                            if not mtStruct.current_is_list:
                                setattr(subObj_cache_dict[mtStruct.main_alias], mtStruct.fieldname, sub_obj)

            # clear the cache
            current_subObject_list_cache_dict.clear()
            current_single_subObject_cache_dict.clear()
            one_to_one_for_two_layer_set.clear()

            super().loginfo(" | <--  select rows: " + str(len(rs_list)))
            super().addInCache(sql, rs_list, len(rs_list))

        except Exception as e:
            raise SqlBeeException(e)
        finally:
            self.__close(cursor, conn)
        return rs_list

    def __getConn(self):
        try:
            conn = HoneyContext.get_connection()
        except Exception as e:
            raise BeeException(e)

        if not conn:
            raise SqlBeeException("DB conn is None!")
        return conn

    def __close(self, cursor, conn):
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()

