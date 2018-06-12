import os
import flask
import flask_kerberos

from pyhive import presto
from requests_kerberos import HTTPKerberosAuth, OPTIONAL

DEBUG  = True
KEYTAB = '/etc/krb5.keytab'

# Flask Configuration
app = flask.Flask('krbpy')
app.config.from_object(__name__)

# Simple endpoint that requires KRB auth
# and returns the authenicated user
@app.route('/')
@flask_kerberos.requires_authentication
def index(ctx):
  return flask.jsonify({'user': ctx.kerberos_user})

# Ednpoint that passes the user context through as a delegated state
@app.route('/query')
@flask_kerberos.requires_authentication
def run_query(ctx):
  krb5_auth = HTTPKerberosAuth(
    mutual_authentication=OPTIONAL,
    service="presto",
    principal="host/krb5-service.example.com@EXAMPLE.COM",
    force_preemptive=True,
    delegate=True,
    delegated_state=ctx.kerberos_state,
  )

  requests_kwargs = {
    'auth': krb5_auth,
    'verify': False
  }

  cursor = presto.connect(
    host='10.5.0.5',
    port=7778,
    protocol='https',
    catalog='jmx',
    schema='current',
    requests_kwargs=requests_kwargs,
  ).cursor()
  cursor.execute('select * from "java.lang:type=classloading"')
  print cursor.fetchall()
  return flask.jsonify({'user': ctx.kerberos_user})

@app.route('/noauth')
def other():
  return flask.jsonify({'user': 'anonymous'})

if __name__ == '__main__':
  # KRB Configuration
  os.environ['KRB5_KTNAME'] = KEYTAB
  flask_kerberos.init_kerberos(app, service='host', hostname='krb5-service.example.com')

  # GO
  app.run(host='0.0.0.0')
