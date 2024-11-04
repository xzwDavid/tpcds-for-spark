# TPCDS-FOR-SPARK：
This is used to generate fixed tpcds query for spark/presto/trino
## 1. set up
```shell
vi tpcds-env.sh
```
- data size
- env variance


## 2. data generation

```shell
cd tpcds-kit/tools
make clean
make
cd ../..
./gen-data.sh
```

## 3. query sql

```shell
./gen-sql.sh
```

## 4. fix for presto and trino
You first generate the query following the above steps then you use the fix script to fix some dialect in generated query:
```shell
cp fix_spark.py query_sql_1000
cd query_sql_1000
python fix_spark.sh
```

## 5. fix for presto and trino
You first generate the query following the above steps then you use the fix script to fix some dialect in generated query:
```shell
cp fix_presto.py query_sql_1000
cd query_sql_1000
python fix_presto.sh
```

