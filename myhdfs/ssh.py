# -*- coding: UTF-8 -*-
import paramiko


class SSHClient:
    """ssh连接远程虚拟机并执行命令
    """
    def __init__(self, hostname, port="22", username="root", password="123"):
        """实例化ssh客户端,创建默认的白名单
        """
        self.ssh = paramiko.SSHClient()
        self.policy = paramiko.AutoAddPolicy()
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

    def connect(self):
        """设置白名单,连接服务器，
        设置服务器的ip，服务器的端口，服务器的用户名，用户名对应的密码
        """
        self.ssh.set_missing_host_key_policy(self.policy)
        self.ssh.connect(
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password
        )

    def exec_download_cmd(self, hdfs_file, host_path):
        """远程执行命令
        exec_command 返回的对象都是类文件对象
        command为命令字符串，如 "ls"
        stdin 标准输入 用于向远程服务器提交参数，通常用write方法提交
        stdout 标准输出 服务器执行命令成功，返回的结果  通常用read方法查看
        stderr 标准错误 服务器执行命令错误返回的错误值  通常也用read方法
        """
        self.connect()
        command = "hdfs dfs -get" + " " + hdfs_file + " " + host_path
        stdin, stdout, stderr = self.ssh.exec_command(command)
        # 返回的为字节，解码为字符串
        result = stdout.read().decode()
        error = stderr.read().decode()
        # print("结果", result)
        # print("错误", error)
        return result, error
    
    def test_directory(self, path):
        """判断路径是否存在
        """
        self.connect()
        command = "ls" + path
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if stdout.readline() != '':
            pass
        else:
            # 不存在时创建目录
            result = self.ssh.exec_command("mkdir -p" + " " + path)
    
    def sqoop_pro(
        self,
        db_type,
        IP,
        database,
        username,
        password,
        table,
        job_name,
        target_dir,
        map_nums
    ):
        """将数据从MySQL导入到hdfs中
        IP: 执行命令的主机IP，通常为namemode
        db_type: 数据库类型，MySQL，SQL server...
        database: 数据库名
        username: 远程连接数据库的用户名
        password: 远程连接数据库的用户名对应的密码
        table: 数据库中的表名
        job_name: 设置提交的mapreduce任务名
        target_dir: 输出文件在hdfs上的目录，必须为不存在的目录，不然会报错
        map_nums: map的任务数量，决定着输出文件part-m-*的数量
        """
        command = "sqoop import" \
                  + " --connect jdbc:" + db_type + "://" + IP + ":3306/" + database \
                  + " --username " + username \
                  + " --password " + password \
                  + " --table " + table \
                  + " --job_name " + job_name \
                  + " --target_dir " + target_dir \
                  + " --map_nums " + map_nums
        # stdin, stdout, stderr = self.ssh.exec_command(command)
        return command


if __name__ == "__main__":
    CLI = SSHClient("192.168.112.103")
    # CLI.exec_download_cmd("/test.xls", "~")
    # CLI.test_directory('/download_hdfs')
