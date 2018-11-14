# master Data Science
projects from the Data Science Master course 17-18

1) From Distributed system subject: mapper and reducer to read tweeter json file and with a positive and negative word dictionary file, (AFINN-111.txt), explore the "happiness" of USA different states.

all project with D. Córdoba Ruiz, using a MRjob program and a set of mapper and reducer programs.

mapper= tweetsent_mapper.py
reducer= tweetsent_reducer.py

execution:
inline:

cat descargatweetspracticasd.json | python2.7
tweetsent_mapper.py | sort -t 1 | python2.7 tweetsent_reducer.py -r inline

local:
cat descargatweetspracticasd.json | python2.7
tweetsent_mapper.py | sort -t 1 | python2.7 tweetsent_reducer.py -r local

cloudera hdfs:
yarn jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar
-files tweetsent_mapper.py,tweetsent_reducer.py,AFINN-111.txt
-mapper "python tweetsent_mapper.py" -reducer "python tweetsent_reducer.py"
-input hdfs:///user/cloudera/descargadatos_10.json -output mc_output_v0


with amazon EMR:
Create the buckect in S3 and load all files. Apply for the EC2 key. In
EMR create a Cluster by using the "Step execution" way by adding "Streaming program".
For the Streaming we add configuration files including the dictionary in CacheFile mode:
-cacheFile
s3://practicasd1/AFINN-111.txt#AFINN-111.txt

Take the default confing of Software that includes Hadoop 2.7.3 with the
 m3xlarge hardware: 1 master and 2 nodes. Execute the Cluster.


2) subject of Data Bases:
MDS_Memoria_CordovaRuizDavidGalvezortizMCruz.pdf is the memory with all information and description of the files, etc... programs included:
 *transform_to_json.py: take the xml file and move it into few json files each of them corresponding to each collection we want to create. 
 *enter_data_in_Mongodb.py: connects the MongoDB data bses, create a data base called dblp and write the json files into the the collections of the data base.
 *queries.py: Makes the queries, 10 questions of part I of the project. 
 *transform_csv.py: transform the json files to csv adapting the structure to use it in Neo4j.
 Also a README.tex file with procedure explanation.

