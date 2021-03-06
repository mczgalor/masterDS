# master Data Science
Projects (assessment tasks) from the Data Science Master course 17-18. The task memories and comments inside programs are in Spanish.

1) Subject: Distributed system I. 

Mapper and reducer program in python to read tweeter json file and, with a positive and negative word dictionary file, (AFINN-111.txt), explore the "happiness" of USA different states.
This project was done with D. Córdoba Ruiz, using a MRjob program and a set of mapper and reducer programs.

mapper= tweetsent_mapper.py

reducer= tweetsent_reducer.py

execution modes:

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

Create the bucket in S3 and load all files. Apply for the EC2 key. In EMR create a Cluster by using the "Step execution" way by adding "Streaming program". For the Streaming we add configuration files including the dictionary in CacheFile mode:

-cacheFile
s3://practicasd1/AFINN-111.txt#AFINN-111.txt

Take the default configuration of Software that includes Hadoop 2.7.3 with the m3xlarge hardware: 1 master and 2 nodes. Execute the Cluster.

2) Subject: Distributed system II. 

Jupyter notebook to solve some questions about a dataset using pyspark with DataFrames or spark.sql.

 *SD2_galvezortiz.ipynb: Notebook 
 
 *DATASET-Twitter-23-26-Mar-2014-MotoGP-Qatar.csv: Dataset

3) Subject: Distributed system III. 

Jupyter notebook to solve some questions about a dataset using Spark streaming with KAFKA.

 *SD3_mcgalvezortiz.ipynb: Notebook 
 
 *DATASET-Twitter-23-26-Mar-2014-MotoGP-Qatar.csv: Dataset 
 
4) Subject: Data analytics and business intelligence I.

 *practicaIAN_galvezortiz.Rmd: Analysis in R of a business case.
 
 *candy-data.csv: Data file.

5) Subject: Data Bases. This project was done with D. Córdoba Ruiz.

MDS_Memoria_CordovaRuizDavidGalvezortizMCruz.pdf is the memory with all information and description of the files, etc. 

Programs included:

 *transform_to_json.py: Takes the xml file and moves it into few json files each of them corresponding to each collection we want to create. 
 
 *enter_data_in_Mongodb.py: Connects to MongoDB database, creates a database called "dblp" and writes the json files into the  collections of the database.
 
 *queries.py: Makes the queries, 10 questions (part I) of the project. 
 
 *transform_csv.py: Transforms the json files to csv adapting the structure to use it in Neo4j.
 
 Also a README.tex file with procedure explanation.
 

6) Subject: Information recovery, ELK environment.

memoriaELK.pdf is the memory with all information and description of the files, etc.

Included programs:

 *practica.elk_mov.conf: Logstash configuration file.
 
 *movies_metadata.csv: Data file.
 
 *consulta1_movies.sh, consulta2_movies.sh, consulta3_movies.sh, consulta4_movies.sh and consulta5_movies.sh: Files with the queries.
 
 *outputconsulta1_movies.sh, outputconsulta2_movies.sh, outputconsulta3_movies.sh, outputconsulta4_movies.sh and outputconsulta5_movies.sh: Files with results of the queries. 
 
 7) Subject: Data Mining I and II. Work developed with David Cordoba Ruiz, Laura Lopez Parrilla, and Victor Valero Fernandez.

 *Mineria_main.pdf: Complete memory. 
 
 *mineriaDatos.rmd and mineriaDatos2.rmd: R files used. The work was divided in two parts.
 
 *Mineria_main.Rmd: R file that joins two previous files.
 
8) Subject: Graph analysis. Work developed with David Cordoba Ruiz.

We took data from Spotify and created a graph, we performed a detailed analysis of the graph and obtained some conclusions. We also plot the graph. We used two sets of data, one downloaded with certain USA singers/groups and other with Spanish ones.
See details in the Memoria_final.pdf file.

 *Memoria_final.pdf: Memory with all information and description of the files and the process, etc. 

 *Included programs:  AccesoAPI.py, AnalisisGrafo.py, VisComponente2.html, Vis_USA.html, g_json.json, g_json_USA.json, grafo1.json, grafo2.json, leyenda.css.
