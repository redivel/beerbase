# BeerBase API

The project is a backend RESTful API for a databse containing information about different beers.

To use you have to provide the following commandline arguments:

`--templates` `<Absolute path to the templates folder>` In the package it is `beerbase/assets/templates`

`--assets` `<Absolute path to the assets folder>` In the package it is `beerbase/assets/`

`--init` This is and optional argument. If added the tables in the provided database will all be deleted and created again.

`--csv` `<Absolute path to csv data file>` If `--init` is added this allows uploading data from a csv data file into the database. For this I used the provided `data.csv`.

The configuration for the app is provided by `openapi_cfg.yaml`inside the assets folder using openapi 3.0.3. The package includes `openapi-ui-bundle` which allows for a nicely generated documentation page under `localhost:5000/ui` where the endpoints can even be tested.

The api has two endpoints:
1. `/beer`
This is used to get beers by certain parameters from the database. The parameters by which the data can be filtered:
   1. `abv` ABV (Alcohol by Volume) of searched beer(s).
   2. `ibu` IBU (International Bitterness Unit) of searched beer(s).
   3. `beer_id` ID of searched beer.
   4. `name` Name of searched beer.
   5. `style` Style of searched beer(s).
   6. `brewery_id` ID of brewer of searched beer(s).
   7. `size` Size of searched beer(s) in ounces.

    One parameter can only be filtered by one value. If multiple parameters ar added there is an OR relation between them.

2. `/beer/delete`
This can be used to delete a specific beer specified by its ID. It requires one query parameter:

    `beer_id` The id of the beer to be deleted.

#### Tests
- [ ] Succesfully query of one beer with correct code
- [ ] Unsuccesfully query of a beer with correct code
- [ ] Successfull deletion of a beer with correct code.
- [ ] Unsuccessfull deletion of a beer with correct code.
- [ ] Serialization of a Beer (to_dict)
- [ ] Creating a Beer from a serialized form (from_dict)




