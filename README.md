# Example hostname webhook

This is an example Webhook integration that shows how to pull hostnames from an external
system to assign them to your Scalr servers.

This example webhook handler just generates a random string when Scalr requests a hostname. See the
[webhook.py](webhook.py) file for additional details.

## Setup instructions

The instructions below are written for RHEL 7 / Centos 7. Adapt as necessary for other distributions.

#### Webhook handler setup

- Install the required packages:
```
yum install epel-release
yum install git gcc python python-devel python-pip uwsgi uwsgi-plugin-python
```
- Retrieve the webhook code:
```
mkdir -p /opt/example-hostname-webhook
cd /opt/example-hostname-webhook
git clone https://github.com/scalr-integrations/example-hostname-webhook.git .
```
- Install the Python dependencies
```
pip install -r requirements.txt
```
- Configure uwsgi to serve the webhook
```
cp uwsgi.ini /etc/uwsgi.d/example-hostname-webhook.ini
chown uwsgi:uwsgi /etc/uwsgi.d/example-hostname-webhook.ini
systemctl enable uwsgi
```
Uwsgi will  bind to 0.0.0.0 and serve the webhook on port 5008 by default. Edit the ini file to change
this behaviour.

#### Scalr webhook setup

Log into Scalr at the global scope, and click on Webhooks in the main menu.
In the Endpoints section, create a new endpoint with URL: `http://<server-ip>:5008/hostname/`

Note down the signing key that Scalr generated, we will need it later.

#### Webhook configuration

Edit the `/etc/uwsgi.d/example-hostname-webhook.ini` file and complete the `env = SCALR_SIGNING_KEY`
statement with the Scalr signing key that Scalr generated.

Reload the configuration:
```
systemctl restart uwsgi
```

## Testing and troubleshooting

The uwsgi logs are appended to `/var/log/messages` by default on centos 7.

To check that the web server is serving our webhook, run the following command on the webhook server:
```
curl -XPOST http://localhost:5008/hostname/
```

You should get a 403 error, because this request was not signed. If that is not the case, check for errors in the uwsgi logs.

Now to use this webhook to assign hostnames to some instances, go in a Farm's configuration. Click
on a Farm Role, and in the Network tab, select "Webhook" as the hostname source. In the dropdown,
select the endpoint you just created. Then save the Farm and launch it. Scalr will make a request
to the webhook handler and assign the generated hostname to the instance.

