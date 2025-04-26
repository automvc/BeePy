from datetime import datetime
import glob 
import logging  
import os
import subprocess  
import sys  # 导入 sys 模块

from bee.version import Version
from bee.context import HoneyContext


# from bee.config import PreConfig, HoneyConfig
# from pathlib import Path  
if __name__ == '__main__':  
    try:  
        # 定义文件夹路径  
        log_directory = 'logs'  
        # 确保日志目录存在  
        if not os.path.exists(log_directory):  
            os.makedirs(log_directory)  
        
        print("start...")
        
        version = Version.getVersion()
        
        # 记录 Python 版本信息  
        python_version = sys.version  # 获取当前 Python 版本 
        py_version=f'Current Python version: {python_version}' 
        print(py_version)
        # logging.info(py_version) #logging不能用在这。没有报错，但没生成文件。
        
        now_str = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
        
        # PreConfig.config_path="E:\\JavaWeb\\eclipse-workspace202312\\BeePy-automvc\\tests\\resources"
        # HoneyConfig() # how to call first time
        
        dbname = HoneyContext.get_dbname()
        print(dbname)
        
        filename0= f'all_logs-V{version}-{now_str}-{dbname}.log'
        # 定义日志文件名  
        filename0 = os.path.join(log_directory, filename0) 
        print(filename0)
        
        # 配置日志  
        # logging.basicConfig(  
        #     filename=filename0,  # 日志文件名  
        #     level=logging.INFO,       # 日志级别  
        #     # format='%(asctime)s - %(levelname)s - %(message)s',
        #     format='%(levelname)s - %(message)s',
        #     # encoding='utf-8'  # 关键点：解决中文乱码  
        # ) 
        
        # 创建一个日志器  3.8.10 不支持 encoding
        logger = logging.getLogger()  
        logger.setLevel(logging.INFO)  # 设置日志级别  
        # 创建一个文件处理器，并设置编码为 UTF-8  
        file_handler = logging.FileHandler(filename0, encoding='utf-8')  
        formatter = logging.Formatter('%(levelname)s - %(message)s')  
        file_handler.setFormatter(formatter)
        # 将处理器添加到日志器  
        logger.addHandler(file_handler)
        
         
        # scripts = glob.glob('*.py')   #子目录不能获取到
        # scripts.remove('test_all.py')  # 排除主脚本 
        
        # 递归匹配所有子目录的 .py 文件
        scripts = glob.glob('**/*.py', recursive=True)  
        # scripts = [f for f in scripts if not f.endswith('test_all.py')]  # 排除主脚本  
        
        excluding = {'exam\ExceptionTest.py', 'exam\hello.py', 'test_all_3.8.py', 'entity\naming.py', 'exam16\namingTest.py', 'test\table2entity2.py', 'test\tableFromMysql2entity.py', 'test\table2entity.py'}
        
        scripts = [
        f for f in scripts   
        if not (f.endswith('test_all.py') or f.endswith('__init__.py') or f.endswith('.pyc') or f in excluding)  
        ]  
        
        # 要运行的脚本列表  
        # scripts = [  
        #     './exam16/bugTest.py',  
        #     './exam16/cacheTest.py',  
        #     './exam16/cacheTest2.py'  
        # ]  
        
        logging.info(py_version)  # 记录 Python 版本信息  
        
        for script in scripts:  
            try:  
                logging.info(f"开始运行脚本: {script}")  
                # 运行脚本并捕获输出  
                result = subprocess.run(  
                    ['python', script],  
                    check=True,  
                    text=True,  
                    capture_output=True,
                    encoding='utf-8'  # 确保使用 utf-8 编码   
                )  
                # 记录标准输出和错误  
                if result.stdout:  
                    logging.info(f"脚本 {script} 输出:\n{result.stdout.strip()}")  
                if result.stderr:  
                    logging.error(f"脚本 {script} 错误:\n{result.stderr.strip()}")   
            except subprocess.CalledProcessError as e:  
                logging.error(f"脚本 {script} 运行失败: {e}")  
            except Exception as e:  
                print(f"未知错误: {e}")
                logging.error(f"未知错误: {e}")  
        
        logging.info("所有脚本运行完成")  
        
        print("end test...")
    
    except Exception as e:  
        print(e)
        
    print("end ")    
