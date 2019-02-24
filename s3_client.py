import boto3
import datetime
import botocore
import json

ak = 'P258ABC80MFG7M9A2NDZ'
sk = 'IbEFixBUveywDD2jypsxACXt3NPbX3aE32HM3YHZ'
ep = 'http://10.20.7.3:9000'
ep = 'http://192.168.231.31:9000'


session = boto3.session.Session()
s3_client = session.client(
    service_name='s3',
    aws_access_key_id=ak,
    aws_secret_access_key=sk,
    endpoint_url = ep,
)

s3 = session.resource(service_name='s3',
    aws_access_key_id = ak,
    aws_secret_access_key = sk,
    endpoint_url = ep)

# 1.创建一个桶

# s3_client.create_bucket(Bucket='rambo')  # 不能使用下划线

# 2.列出来看看
# dic = s3_client.list_buckets()
# buckets = [bucket['Name'] for bucket in dic['Buckets']]
# print(buckets)

# 3.创建对象
# filename = 'D:/TEST-s3.txt'
# bucket_name = 'rambo'
# s3_client.upload_file(filename, bucket_name, 'testfile')

# 4.列出对象
# objs = s3_client.list_objects(
#     Bucket='lifecycle-rules'
# )
#
# print(objs['Contents'])


# 5.下载对象
# BUCKET_NAME = 'rambo' # replace with your bucket name
# KEY = 'D:/TEST-s3.txt' # replace with your object key
#
# s3_client.download_file(BUCKET_NAME,KEY, 'D:/haha.txt')

# 6.删除对象
# s3 = session.resource(service_name='s3',
#     aws_access_key_id='E62TLZS7A9AD3NUY7MB4',
#     aws_secret_access_key='DDwsqExCainK0DJtlM1LaaA1lpWPbbMn9bGHaoll',
#     endpoint_url='http://10.20.7.3:9000')
# bucket = s3.Bucket('rambo')
# bucket.Object('D:/TEST-s3.txt').delete()

# 7. 查看对象类型
# object = s3.Object('lifecycle-rules','tra2018M50M')
# object2 = s3.Object('rambo','data_gravity.pdf')
# print(object.metadata)
# print(object2.metadata)

# 8.对象转换存储类型
# bucket_lifecycle_configuration = s3.BucketLifecycleConfiguration('rambo')

# bucket_lifecycle_configuration.put(
#     LifecycleConfiguration={
#         'Rules': [
#             {
#                 'ID': 'rambo_1',
#                 'Prefix': 'data_gravity.pdf',
#                 'Status': 'Enabled',
#                 'Transitions': [
#                     {
#                         'Date': '2018-08-30T08:55:59.019430',
#                         'StorageClass': 'GLACIER'
#                     },
#                 ],
#             },
#         ]
#     }
# )

# print(bucket_lifecycle_configuration.rules)

# 时间转换
# n = datetime.datetime.now()
# m = datetime.timedelta(minutes=10)
# f=(n+m).isoformat()
# f
# '2018-08-30T16:36:34.995745'
# n.isoformat()
# '2018-08-30T16:26:34.995745'

9.获得桶的acl规则
