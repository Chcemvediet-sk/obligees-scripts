# Obligees scripts

# Overview

This repository contains input data related to obligees – Slovak municipality offices. Several scripts in this repository extracts useful information, compares them with official Slovak Post ZIP code database (using their API) and with Chcemvediet.sk internal database. The aim of these scripts is to add new entries and/or verify and update existing ones.

## Input data

```text
+-- input
|   +-- cities.json
|   +-- cities-original.js
|   +-- obligees_obligee.sql
```

The `cities-original.js` is the former input file. Its sub-part is transformed 
(mostly manually and formatting in the IDE) to the `cities.json` file with 
better structure for further usage. The `obligees_obligee.sql` is the SQL dump
of relevant Chcemvediet.sk tables.

## Database

You can import input SQL dump file into a docker based MySQL database using
commands
```shell script
cd <full path to the repository>/input/sql

xz --decompress obligees_obligee.sql.xz

cat > 000-init.sql <<<
CREATE DATABASE chcemvediet;
USE chcemvediet
EOT

docker run \
  --name chcemvediet-mysql \
  -v <full path to the repository>/input/sql/sql-data:/sql-data \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
  -p 3306:3306 \
  mysql:5.7.28
```
where you should edit at least `<full path to the repository>` (twice). Other 
values must correspond with contents of the `database.py` file.

Then models (see `model.py`) can be generated using simple command
```shell script
sqlacodegen \
  --tables obligees_obligee \
  --outfile model.py \
  mysql://root:my-secret-pw@127.0.0.1:3306/chcemvediet
```

## Initialization

```shell script
virtualenv -p python3 .venv
source .venv/bin/activate
```


## Scripts

### `script_suggest_updates.py`

Loop over all data from `input/cities.json` file and suggest updates – new email
addresses – to the Chcemvediet.sk database: **new email addresses**.

#### Output

* Warning if ZIP codes differ.
* Info log message if email address from `cities.json` file is not in the SQL
database already.

#### Usage

```shell script
python -m script_suggest_updates
```

### `script_new_settlements.py`

Loop over all data from `input/cities.json` file and add new entries – new
settlements – to the Chcemvediet.sk database: **new settlements** (table `obligees_obligee_nove_obce`)

#### Output

Raw data which should be inserted into the Chcemvediet.sk database.

#### Usage

```shell script
python -m script_new_settlements
```

### `script_add_zip.py`

Loop over all data from `input/citiees.json` file and add new entries to the `obligees_zipcodes` table.

* `json_zip` column: ZIP directly from `cities.json` input file
* `post_json_zip` column: ZIP from Post API – input value is an address from `cities.json`
* `post_oblifee_zip` column: ZIP from Post API – address from Post API – input value is an address from Chcemvediet.sk database

#### Usage

```shell script
python -m script_add_zip
```

### `script_guess_settlement_web_page.py`

Guess web page from the email address.
Guess means that the script excludes all (probably) mail hosting sites — sites used for multiple settlements.

The script adds all web pages to the `obligees_webpage` table.

#### Usage

```shell script
python -m script_guess_settlement_web_page
```
