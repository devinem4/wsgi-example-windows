# wsgi-example-windows
This repo documents the steps I took to get apache with the mod_wsgi module working on my winodows machine.

My project_root =  `c:\users\devinem4\documents\projects\wsgi-example`. Wherever you see this in the steps below, you'll need to replace with your project root directory.


## installing apache
1. I downloaded the latest version of [apache](https://www.apachelounge.com/download/), but if you're following along you can use [httpd-2.4.43-win64-VS16.zip](./httpd-2.4.43-win64-VS16.zip) from this repo.

2. Extract the zip file to your project root directory. For me, that is `c:\users\devinem4\documents\projects\wsgi-example`.

3. Update the `httpd.conf` file @ `c:\users\devinem4\documents\projects\wsgi-example\httpd-2.4.43-win64-VS16\Apache24\conf\httpd.conf`, with the path to the Apache folder:
```yaml
# line 37 of httpd.conf
Define SRVROOT "c:/Users/devinem4/Documents/projects/wsgi-example/httpd-2.4.43-win64-VS16/Apache24/"
```

3. Start the server
```console
> cd c:\users\devinem4\documents\projects\wsgi-example\httpd-2.4.43-win64-VS16\Apache\bin
> httpd.exe
```

4. Test it out -- visit [localhost](http://localhost/) via your web browser and you should see `It works!`. By default, apache is serving `c:\users\devinem4\documents\projects\wsgi-example\httpd-2.4.43-win64-VS16\Apache24\htdocs\index.html`.

4. If you really want to test that things are working, make a change to `c:\users\devinem4\documents\projects\wsgi-example\httpd-2.4.43-win64-VS16\Apache24\htdocs\index.html` and reload [localhost](http://localhost/). No need to restart the server.


## installing mod-wsgi
Next up, we need to install the `mod-wsgi` module and then tell our apache configure how to use it. This does not seem to come with the default version of Apache.

I could not get this to work with a virtual environment, but it worked with my main python installation :shrug:

1. run `pip install mod_wsgi`
2. run `mod_wsgi-express module-config`
3. Copy the output of step 2 and paste into `httpd.conf`. I added mine on line 61, right after the `Listen 80` setting.

```yaml
# line 61 or so
LoadFile "c:/users/devinem4/appdata/local/programs/python/python38/python38.dll"
LoadModule wsgi_module "c:/users/devinem4/appdata/local/programs/python/python38/lib/site-packages/mod_wsgi/server/mod_wsgi.cp38-win_amd64.pyd"
WSGIPythonHome "c:/users/devinem4/appdata/local/programs/python/python38"
```


## creating our mod-wsgi app
Apache is now setup to serve a python app, so let's add one.  

The example we're following says to put our app in the `\var\www\test` directory. I don't think the location actually matters (we can point apache to serve any directory) -- but this seems to be industry standard so we'll follow suit.

1. create a the new `\var\www\test` directories:
```console
mkdir -p c:\users\devinem4\documents\projects\wsgi-example\var\www\test
```

2. The example we're following uses `bottle`, so let's install that:
```console
pip install bottle
```

3. create a new file `c:\users\devinem4\documents\projects\wsgi-example\var\www\test\home.wsgi` with contents:
```python
import bottle

application = bottle.default_app()

@bottle.route('/')
def home():
    return "hello world from my bottle mod_wsgi home.wsgi!"
```

4. Now we have to update our `httpd.conf` file to use this new `home.wsgi` app:
```yaml
# i think there is lots of ways to do this, but this seemed to work best for me
# approx line 514, after the `# Virtual Hosts` line.
#
# WSGIScriptAlias maps a { url_path } to a { file_path }
#     ie, if we wanted our app url to be http://localhost/home, WSGIScriptAlias would look like this:
#     WSGIScriptAlias home "c:/users/devinem4/documents/projects/wsgi-example/var/www/test/home.wsgi"
# 
# By default, Apache does not have access to read the files in `var/www/test`. We'll grant Apache access to our `var/www/test` directory with the `<Directory>` directive.
<VirtualHost *:80>
    WSGIScriptAlias / "c:/users/devinem4/documents/projects/wsgi-example/var/www/test/home.wsgi"

    <Directory "c:/users/devinem4/documents/projects/wsgi-example/var/www/test">
        Require all granted
    </Directory>
</VirtualHost>
```

5. Run `httpd.exe` and go to [localhost](http://localhost). We should finally see the message we coded in our bottle app.
