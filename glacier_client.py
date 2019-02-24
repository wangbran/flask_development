import boto3
import time
import datetime
import json

session = boto3.session.Session()
gc_client = session.client(
    service_name='glacier',
    aws_access_key_id='E62TLZS7A9AD3NUY7MB4',
    aws_secret_access_key='DDwsqExCainK0DJtlM1LaaA1lpWPbbMn9bGHaoll',
    endpoint_url='http://10.20.7.3:9100',
    region_name='',
)

'''
gc = session.resource(service_name='glacier',
    aws_access_key_id='E62TLZS7A9AD3NUY7MB4',
    aws_secret_access_key='DDwsqExCainK0DJtlM1LaaA1lpWPbbMn9bGHaoll',
    endpoint_url='http://10.20.7.3:9100')
'''
# 1.创建一个文件库vault
# response = gc_client.create_vault(
#     accountId='-',
#     vaultName='rambo-value2'
# )
# print(response)

# 2.列出来看看
# response2 = gc_client.list_vaults(
#     accountId='-',
#     limit='',
#     marker='',
# )
# print(response2['VaultList'])

# 3.创建归档
# response3 = gc_client.upload_archive(
#     accountId='-',
#     archiveDescription='have a try2',
#     body='‪D:/datalakeV2_Glacier_API.pdf',
#     checksum='',
#     vaultName='rambo_vault',
# )
# print(response3)

'''
{'ResponseMetadata': {'RequestId': '154FE8E42C890187', 'HTTPStatusCode': 200, 'HTTPHeaders': {'location': '/admin/vaults/rambo_vault/archives/s-b33358aa96944dfd8129b45a1c891999', 'x-amz-archive-id': 's-b33358aa96944dfd8129b45a1c891999', 'x-amzn-requestid': '154FE8E42C890187', 'date': 'Fri, 31 Aug 2018 07:54:24 GMT', 'content-length': '0'}, 'RetryAttempts': 0}, 'location': '/admin/vaults/rambo_vault/archives/s-b33358aa96944dfd8129b45a1c891999', 'archiveId': 's-b33358aa96944dfd8129b45a1c891999'}
'''

# 4.列出所有归档
response4_1 = gc_client.initiate_job(
    accountId='-',
    jobParameters={
        'Description': 'My inventory job',
        'Type': 'inventory-retrieval',
    },
    vaultName='rambo_vault',
)

job_id=response4_1["jobId"]
time.sleep(10)
response4_2 = gc_client.get_job_output(vaultName='rambo_vault',jobId=job_id,)
print(response4_2['body'].read())

# 5.下载归档


# 6.删除归档
# response6 = gc_client.delete_archive(
#     accountId='-',
#     archiveId='s-78963383d95d4447bda995d6aaf34314',
#     vaultName='rambo_vault',
# )
#
# print(response6)
'''
{'ResponseMetadata':
{'HTTPStatusCode': 204, 'HTTPHeaders': {'date': 'Fri, 31 Aug 2018 07:39:07 GMT'}, 'RetryAttempts': 0}}
'''
