kartoffel
=========
ML project: Real Time Map Matching with HMMs
--------------------------
Click [here](https://github.com/juhanaka/kartoffel) to visit original page.
--------------------------

Store OSM data in Postgres
--------------------------

### Get data
* Download California .pbf file from [this website](http://download.geofabrik.de/north-america/us/california.html).

### Convert data to .osm
* Download and install osmconvert [here](http://wiki.openstreetmap.org/wiki/Osmconvert).
* Run
```osmconvert ./california-latest.osm.pbf >california.osm```

### Filter everything but highways
* Download and install osmfilter [here](http://wiki.openstreetmap.org/wiki/Osmfilter).
* Run
```osmfilter ./california.osm --keep="highway=" -o=california_roads.osm```

### Store to postgres
* Install Postgres and get PostGIS (Google instructions)
* Install osm2pgsql (on mac with homebrew: brew install osm2pgsql)
* Create a Postgres database
* Enable PostGIS on the db:
    * Connect to db: ```psql databasename```
    * In the db prompt: ```CREATE EXTENSION postgis;```
* Run ```osm2pgsql -s -U username -d databasename /path/to/file.osm```

