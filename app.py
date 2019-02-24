from flask import Flask,render_template,redirect,url_for,request
import boto3
import time
from werkzeug.utils import secure_filename

ak = 'OL43P2GTN7OFDPD86QEL'
sk = 'OJRFnHF7mYiS42Nzrihoh9YPWMrr7fJFj9OwHqmm'
# ak = '42UVJUELV6BP6O9EEEHV'
# sk = 'Fq9i5TkpWPdDR2ECzk0iJwzNt1CFkEMA3hMoQ6FQ'
end = 'http://10.20.7.3:9000'

session = boto3.session.Session()
s3_client = session.client(
    service_name='s3',
    aws_access_key_id=ak,
    aws_secret_access_key=sk,
    endpoint_url=end,
)
s3 = session.resource(service_name='s3',
    aws_access_key_id = ak,
    aws_secret_access_key = sk,
    endpoint_url=end)

gc_client = session.client(
    service_name='glacier',
    aws_access_key_id=ak,
    aws_secret_access_key=sk,
    endpoint_url=end,
    region_name='',
)

app = Flask(__name__)


@app.route('/')
@app.route('/hot')
def hot():
    dic = s3_client.list_buckets()
    return render_template('hot_bucket.html',dic = dic)


@app.route('/hot/create',methods=['GET','POST'])
def create_bucket():
    bucket_name = request.form.get('bucket_name')
    s3_client.create_bucket(Bucket=bucket_name)
    return redirect(url_for('hot'))


@app.route('/hot/<bucket_name>/empty_bucket')
def empty_bucket(bucket_name):
    objs = s3_client.list_objects(
        Bucket=bucket_name
    )
    for obj in objs['Contents']:
        obj_name = obj['Key']
        s3_client.delete_object(
            Bucket=bucket_name,
            Key=obj_name,)
    return redirect(url_for('hot'))


@app.route('/hot/<bucket_name>/del_bucket')
def del_bucket(bucket_name):
    s3_client.delete_bucket(Bucket=bucket_name)
    return redirect(url_for('hot'))


@app.route('/hot/<bucket_name>/')
def detail(bucket_name):
    objs = s3_client.list_objects(
        Bucket=bucket_name
    )
    return render_template('hot_object3.html',bucket_name=bucket_name,objects=objs,s3_client=s3_client)


@app.route('/hot/<bucket_name>/upload',methods=['GET','POST'])
def upload(bucket_name):
    tit = request.files['filename']
    s3.Object(bucket_name, tit.filename).put(Body=tit.read())
    return redirect(url_for('detail', bucket_name=bucket_name))


@app.route('/hot/<bucket_name>/<object_name>/download')
def download(bucket_name, object_name):
    s3_client.download_file(bucket_name, object_name, 'D:/'+object_name)
    return redirect(url_for('detail', bucket_name=bucket_name))


@app.route('/hot/<bucket_name>/<object_name>/delete')
def del_obj(bucket_name, object_name):
    bucket = s3.Bucket(bucket_name)
    bucket.Object(object_name).delete()
    return redirect(url_for('detail', bucket_name=bucket_name))


@app.route('/hot/<bucket_name>/<object_name>/restore')
def restore_obj(bucket_name, object_name):
    response = s3_client.restore_object(
        Bucket=bucket_name,
        Key=object_name,
        RestoreRequest={
            'Days': 5,
        },
    )
    return redirect(url_for('detail', bucket_name=bucket_name))

# ———————————————————————

@app.route('/cold')
def cold():
    dic = gc_client.list_vaults(
        accountId='-',
        limit='',
        marker='',
    )
    return render_template('cold_vault.html', dic=dic)

@app.route('/cold/<vault_name>/')
def cold_detail(vault_name):
    response = gc_client.initiate_job(
        accountId='-',
        jobParameters={
            'Description': 'My inventory job',
            'Type': 'inventory-retrieval',
        },
        vaultName=vault_name,
    )
    time.sleep(5)
    response2 = gc_client.get_job_output(vaultName=vault_name, jobId=response["jobId"], )
    bstr = response2['body'].read()
    rstr = bstr.decode().replace(':null', ':None')
    results = eval(rstr)
    return render_template('cold_object.html',vault_name=vault_name,results=results)


@app.route('/cold/<vault_name>/upload',methods=['GET','POST'])
def upload_arc(vault_name):
    tit = request.files['filename']
    response = gc_client.upload_archive(
        accountId='-',
        archiveDescription=tit.filename,
        body=tit.read(),
        checksum='',
        vaultName=vault_name,
    )
    return redirect(url_for('cold_detail', vault_name=vault_name))


@app.route('/cold/<vault_name>/<archive_id>/delete')
def del_arc(vault_name, archive_id):
    gc_client.delete_archive(
        accountId='-',
        archiveId=archive_id,
        vaultName=vault_name,
    )
    return redirect(url_for('cold_detail', vault_name=vault_name))


@app.route('/task')
def task():
    return render_template('task.html')


if __name__ == '__main__':
    app.run()
