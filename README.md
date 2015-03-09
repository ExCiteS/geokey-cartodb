# geokey-cartodb

Provide API endpoints that can be used to import GeoKey Data into CartoDB


## Install

Install the package

```
sudo pip install -U git+https://github.com/ExCiteS/geokey-cartodb.git
```

## Quick start

1. Add "geokey_cartodb" to your INSTALLED_APPS settings (`core/settings/project.py`) like this:

    ```
        INSTALLED_APPS = (
            ...
            'geokey_cartodb',
        )
    ```

2. Include the cartodb URLconf in your extensions urls.py (`core/url/extensions.py`) like this:

    ```
        url(r'^', include('geokey_cartodb.urls', namespace='geokey_cartodb')),
    ```
3. Add the cartodb table to the db like this: 

 ```
 ../env/bin/python manage.py migrate

```
