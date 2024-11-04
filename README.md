# TPCDS-FOR-SPARK：

## 1. set up
```shell
vi tpcds-env.sh
```
- 数据量
- 环境变量
- 设置数据生成节点```vi nodenum.sh```

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
cp presto-fix.py query_sql_1000
cd query_sql_1000
python presto-fix.sh
```

