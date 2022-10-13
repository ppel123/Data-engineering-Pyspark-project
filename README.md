# Data Engineering Project

## Tasks

The goal of this project is to implement a distributed system that processes, transforms, and persists CSV data in Parquet format. The system consists of two modules:
1. A distributed file system "Hadoop cluster".The CSV files will be stored there and the resulting parquet files will be persisted.
2. A spark cluster running on top of Hadoop and will process the csv data to create the parquet files.

<p align="center">
  <img src="https://user-images.githubusercontent.com/42607603/195686237-afd41443-c962-4b58-8546-59be85bbf674.png">
</p>  

Python was used as the main language for preparing the Spark Application (using PySpark).

### First Task

The first task is to setup the Hadoop and Spark cluster. In this project, a single-node cluster setup was made at a single virtual machine. Spark has been setup over yarn. 
More information can be found at the below sites and repositories:
* https://hadoop.apache.org/docs/r3.2.1/
* https://archive.apache.org/dist/hadoop/common/
* https://spark.apache.org/releases/spark-release-3-1-1.html
* https://archive.apache.org/dist/spark/

### Second Task

The second objective has three distinct steps:
1. Upload the input data (CSV format file) to HDFS
2. Submit a spark job at Spark cluster that will read, transform and clean the input CSV data
3. Produce the parquet output and upload back it to HDFS

Each row in the CSV file is composed of three columns.  
The first column is the timestamp of a transaction, the second one is the amount of the transactions and the third one is the channel through which the transaction was done. 
To illustrate the format of the file, consider the below:
* 2020-11-21 10:15:02+01,0.15,Call
* 2020-11-21 09:46:51+01,0.75,Call
* 2020-11-21 10:31:13+01,0.15,Call  
  
The file will be read by the Spark job, which will then carry out the required transformations, clean up, and persist parquet files back to an output directory at HDFS.
The following three columns in the table, each with the appropriate data type: 
1. **timestamp**: data type **TimestampType** created from the first column of CSV
2. **amount**: data type **DecimalType** with four decimal digits created from the second column of CSV
3. **channel**: data type **StringType** created from the third column of CSV

Through the implementation of this project, we will give various information on the topics that are used.

## Hadoop 

Apache Hadoop is an open-source framework that is used to efficiently store and process large datasets ranging in size from gigabytes to petabytes of data. Instead of using one large computer to store and process the data, Hadoop allows clustering multiple computers to analyze massive datasets in parallel more quickly.

Hadoop consists of four main modules:

* Hadoop Distributed File System (HDFS) – A distributed file system that runs on standard or low-end hardware. HDFS provides better data throughput than traditional file systems, in addition to high fault tolerance and native support of large datasets.

* Yet Another Resource Negotiator (YARN) – Manages and monitors cluster nodes and resource usage. It schedules jobs and tasks.

* MapReduce – A framework that helps programs do the parallel computation on data. The map task takes input data and converts it into a dataset that can be computed in key-value pairs. The output of the map task is consumed by reducing tasks to aggregate output and providing the desired result.

* Hadoop Common – Provides common Java libraries that can be used across all modules.

The Hadoop ecosystem has grown significantly over the years due to its extensibility. Today, the Hadoop ecosystem includes many tools and applications to help collect, store, process, analyze, and manage big data. One of the most popular applications is:

* Spark – An open-source, distributed processing system commonly used for big data workloads. Apache Spark uses in-memory caching and optimized execution for fast performance, and it supports general batch processing, streaming analytics, machine learning, graph databases, and ad hoc queries.

## Spark

Spark is a general-purpose distributed data processing engine that is suitable for use in a wide range of circumstances. On top of the Spark core data processing engine, there are libraries for SQL, machine learning, graph computation, and stream processing, which can be used together in an application. Programming languages supported by Spark include: Java, Python, Scala, and R. Application developers and data scientists incorporate Spark into their applications to rapidly query, analyze, and transform data at scale. Tasks most frequently associated with Spark include ETL and SQL batch jobs across large data sets, processing of streaming data from sensors, IoT, or financial systems, and machine learning tasks.


## First Task

In order to start with the project we will firstly setup a Linux installation in VirtualBox, and download the necessary files in order to have the working environment ready.
The steps to setup the installation are:
1. Download and install the VirtualBox ([Download VirtualBox For Windows](https://download.virtualbox.org/virtualbox/6.1.32/VirtualBox-6.1.32-149290-Win.exe))
2. Download the preferred Linux Distribution. We are going to use Ubuntu 20.04 ([Download Ubuntu 20.04](https://ubuntu.com/download/desktop/thank-you?version=20.04.4&architecture=amd64)).
3. Setup Virtual Environment with Ubuntu 20.04 through VirtualBox. More information on how to do it can be found [here](https://www.nakivo.com/blog/use-virtualbox-quick-overview/).  
The following settings have been used for the VM:
   * RAM: 7 GB
   * CPU Processors: 4
   * Video Memory: 128 MB
   * HDD Space: 60 GB
 4. Setup a shared folder between the local PC and the virtual machine for better file exchange ([More details](https://carleton.ca/scs/tech-support/troubleshooting-guides/creating-a-shared-folder-in-virtualbox/)).
 5. Download Java 8, because it is necessary for Hadoop to run ([Download](https://download.oracle.com/otn/java/jdk/8u321-b07/df5ad55fdd604472a86a45a217032c7d/jdk-8u321-linux-x64.tar.gz)).
 6. Download Hadoop 3.2.1 ([Download](https://archive.apache.org/dist/hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz))
 7. Download Spark 3.1.3 ([Download](https://www.apache.org/dyn/closer.lua/spark/spark-3.1.3/spark-3.1.3-bin-hadoop3.2.tgz))
 8. Copy all the downloaded files in the Shared Folder

Now that we have all the necessary files in place we will proceed with the installation of these in our virtual machine.
1. Install the requisite software by typing 
```
sudo apt-get install ssh
```
2. Move the downloaded files from shared folder to desktop in a folder named Files
3. Unzip the 3 downloaded files in a selected directory
We will unzip them in the /usr/local/ folder by first going to this folder with `cd /usr/local/` and then `tar -xvf ~/Desktop/Files/file_name.tar.gz`.
We unzip the java, hadoop and spark zipped folders.
In the end we will have a folder like the following image:

<p align="center">
  <img src="https://user-images.githubusercontent.com/42607603/161052854-495e2ccc-7e38-4e85-ab66-26b87175728f.png">
</p>  

### Install Java
To install Java and make it available system-wide we have to add it to the .bashrc file.  
In order to this:
1. Open a terminal fand type `sudo su` and enter the credentials
2. Go to ~ with `cd ~`
3. Now enter the command `sudo nano .bashrc` 
4. Go to the end of file and add
```
export JAVA_HOME=/usr/local/jdk1.8.0_321/
export PATH=$JAVA_HOME/bin:$PATH
```
5. Save and close the file
6. Reload in order to apply the changes with the command `source ~/.bashrc`

To test if Java is correctly installed we can go to a terminal and type `java -version`.   
If the version of Java is shown, the installation was successfull. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/42607603/161060276-97b79138-8c0c-41b9-bb5e-0e26359c289d.png">
</p> 

### Install Hadoop
To install Hadoop we will follow the same process as above:
1. Open a terminal for all the users first type `sudo su` and enter the credentials
2. Go to ~ with `cd ~`
3. Now enter the command `sudo nano .bashrc` 
4. Go to the end of file and add
```
export HADOOP_HOME=/usr/local/hadoop-3.2.1/
export PATH=$HADOOP_HOME/sbin:$PATH
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
```
5. Save and close the file
6. Reload in order to apply the changes with the command `source ~/.bashrc`
7. Now we must tell Hadoop where is the Java installation. To do this we should go to the hadoop-env.sh file located in /usr/local/hadoop-3.2.1/etc/hadoop (we may need to open it with leverage privileges) and add the following line `export JAVA_HOME=/usr/local/jdk1.8.0_321` in the correct section, as the image below.

<p align="center">
  <img src="https://user-images.githubusercontent.com/42607603/161061898-87b121cf-db37-48da-85e4-cfd4581723b7.png">
</p>  

8. To check the installation we can go to the installation folder of Hadoop by typing `cd /usr/local/hadoop-3.2.1` and then typing `bin/hadoop version` to find the version of Hadoop. 
If we get a result like the image below the installation is completed.

<p align="center">
  <img src="https://user-images.githubusercontent.com/42607603/161062489-51fbc2ac-083f-4d48-b69d-c3b720831067.png">
</p>    

9.To finish the installation we are going to make some additions in the configuration files of Hadoop:
* /usr/local/hadoop-3.2.1/etc/hadoop/core-site.xml  
We edit the property mentioned below inside configuration tag. The core-site.xml informs Hadoop daemon where NameNode runs in the cluster. It contains configuration settings of Hadoop core such as I/O settings that are common to HDFS & MapReduce.

```
<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://localhost:9000</value>
</property>
</configuration>
```

![image](https://user-images.githubusercontent.com/42607603/161065719-729bdfe1-3cbb-408e-b237-cc6021ae1eee.png)


* /usr/local/hadoop-3.2.1/etc/hadoop/hdfs-site.xml  
We edit the property mentioned below inside configuration tag. The hdfs-site.xml contains configuration settings of HDFS daemons (i.e. NameNode, DataNode, Secondary NameNode). It also includes the replication factor and block size of HDFS.

```
<configuration>
<property>
<name>dfs.replication</name>
<value>1</value>
</property>
<property>
<name>dfs.permission</name>
<value>false</value>
</property>
</configuration>
```

![image](https://user-images.githubusercontent.com/42607603/161066739-983010fc-99db-4056-9639-ad3503e80807.png)

* /usr/local/hadoop-3.2.1/etc/hadoop/mapred-site.xml    
We edit the property mentioned below inside configuration tag. The mapred-site.xml contains configuration settings of MapReduce application like number of JVM that can run in parallel, the size of the mapper and the reducer process,  CPU cores available for a process, etc.

In some cases, mapred-site.xml file is not available. So, we have to create the mapred-site.xml file using mapred-site.xml template.

```
<configuration>
<property>
<name>mapreduce.framework.name</name>
<value>yarn</value>
</property>
</configuration>
```

![image](https://user-images.githubusercontent.com/42607603/161073420-84d6db70-5bbc-45d6-9cec-fc0aa4c0933e.png)


* /usr/local/hadoop-3.2.1/etc/hadoop/yarn-site.xml    
We edit the property mentioned below inside configuration tag. The yarn-site.xml contains configuration settings of ResourceManager and NodeManager like application memory management size, the operation needed on program & algorithm, etc.

```
<configuration>
<property>
<name>yarn.nodemanager.aux-services</name>
<value>mapreduce_shuffle</value>
</property>
<property>
<name>yarn.nodemanager.auxservices.mapreduce.shuffle.class</name>
<value>org.apache.hadoop.mapred.ShuffleHandler</value>
</property>
</configuration>
```

![image](https://user-images.githubusercontent.com/42607603/161075816-1c20a236-74ba-46f0-b061-7a464a0bea98.png)

### Start Hadoop
In order to start the hadoop cluster we have to format the namenode first.   
Hadoop NameNode is the centralized place of an HDFS file system which keeps the directory tree of all files in the file system, and it tracks where across the cluster the file data is kept. In short, it keeps the metadata related to datanodes. When we format namenode it formats the meta-data related to data-nodes, and original Datanode remains unaffected.   
Hadoop Namenode is used to specify the default file system and also the defaults of your local file system.   
When we format namenode (bin/hadoop namenode -format) it formats the meta-data related to data-nodes but don’t effect original nodes. By doing this, all the information on the datanodes are lost and the datanodes becomes reusable for new data.    
To do this open a terminal and:
1. Go to hadoop installation folder with `cd /usr/local/hadoop-3.2.1`
2. Run the command `sudo nano bin\hdfs namenode -format`

After formatting the namenode we will proceed with the start of the cluster by:  
1. Add the following to the /usr/local/hadoop-3.2.1/etc/hadoop/hadoop-env.sh file
```
export HDFS_NAMENODE_USER=hadoop_user
export HDFS_DATANODE_USER=hadoop_user
export HDFS_SECONDARYNAMENODE_USER=hadoop_user
export YARN_RESOURCEMANAGER_USER=hadoop_user
export YARN_NODEMANAGER_USER=hadoop_user
```
Here we could have created a specific user for managing the Hadoop functions.
2. Configure passwordless ssh Hadoop cluster.      
Configuring passwordless ssh from master to all the slave nodes is necessary when you want to run some scripts on all the nodes in the cluster from master. Though passwordless ssh is not required for hadoop daemons to work, it is a good practice to have a passwordless ssh configured on all hosts so that master node can interact with hosts seamlessly when in need.  
Type `ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa`
Now, if you go to the  ~/.ssh  directory, you can see two files id_rsa and id_rsa.pub.
* id_rsa.pub contains the public key that should be shared to all the servers that you want to connect via ssh without a password. 
* id_rsa contains a private key which should NOT be shared with anyone.  
3. Copy id_rsa.pub to authorized-keys by typing `cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys1`   
4. Type `ssh locahlost`  
5. Give the appropriate permissions to folders (`sudo chmod 777 /home/hdoop/hadoop-3.2.2/logs`)  
4. Go to the sbin folder of Hadoop with `cd /usr/local/hadoop-3.2.1/sbin/start-all.sh`   
5. Verify that everything is running by typing `jps` in a terminal.   

Now we have the Hadoop cluster up and running we could open a Browser and navigate to http://localhost:9870/dfshealth.html#tab-overview, in order to see the preview tab.

<p align="center">
  <img src="https://user-images.githubusercontent.com/42607603/161110202-e248eaba-546b-4aa1-bd83-a43d0153a73a.png">
</p>   

Moreover we can access the datanodes by going to the Datanodes tab on top and then choosing the desired one from the "In operation" list.

<p align="center">
  <img src="https://user-images.githubusercontent.com/42607603/161110476-0e367b11-e0ee-4349-906d-c4cc3d834248.png">
</p>   

## Install Spark
In order to be able to use Spark we have to add to the .bashrc file the appropriate paths. 

1. Go to ~ with `cd ~`
2. Now enter the command `sudo nano .bashrc` 
3. Go to the end of file and add
```
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export SPARK_HOME=/usr/local/spark-3.1.3-bin-hadoop3.2
export PATH=$PATH:$SPARK_HOME/bin
export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native:$LD_LIBRARY_PATH
```
4. Save and close the file
5. Reload in order to apply the changes with the command `source ~/.bashrc`

Then we must add some configurations in the spark-defaults.conf.template file located in the conf folder in the installation folder of Spark. 
Just add the below lines in the end of the file.
```
spark.master yarn
spark.driver.memory 512m
spark.yarn.am.memory 512m
spark.executor.memory 512m
```

## Upload File to HDFS
In order to be able to read files from HDFS we have to upload a file there first.    
To do this we have to have the Hadoop cluster up and running.   
The steps to upload a file are:  
1. Go to the Hadoop installation folder with `cd /usr/local/hadoop-3.2.1`
2. Check if there are any files in HDFS by typing `bin/hadoop fs -ls \`  
If nothing is return then the HDFS is empty. So lets add a folder and the CSV file in there.
3. To create a folder we type the command `bin/hadoop fs -mkdir /files`  
Then if we try to see if there are files in HDFS again we will find out that there is a new folder.  
4. Now to copy a CSV file from our system to HDFS we will use the command `-put` or `-copyFromLocal`.   
We do not use the Linux `cp` command here.    
So lets add the file by typing `bin/hadoop fs -put ~/Desktop/Files/data.csv /files`
If we check again there is a file in the /files folder

# Coding Part
After completing the above part we will proceed with the coding part.  
Python will be used as the main language for developing the process needed.  
**Python is preinstalled in Ubuntu 20.04.4, so we do not have to install it manually**  
In order to use Spark with Python we can install PySpark and use it from there directly **or** prepare the script and run it through the terminal by using spark-submit.

## Installing PySpark with pip
1. Open a terminal 
2. Install pip with `sudo apt install python3-pip`
3. Install PySpark with `pip install pyspark`

## Python Script
Now that we have installed PySpark we can have a look at the code for the PySpark tasks.  
The code can be found in this repository (two .py files with explanatory comments).   
The write-parquet.py reads the data from the CSV, transforms it and writes it to a Parquet file.  
The read-parquet.py reads the Parquet file and writes the data to a Spark dataframe.  

### CSV File - Data Cleaning and Transformation
The CSV file format is as described above. 
As we can see there are some errors in this file (e.g. in dates or values) that must been cleaned before uploading it to the HDFS as a parquet file.

The assumption that we make for this CSV file are:
* The first column contains datetime values - timestamps 
* The second column contains only decimal values
* The third column strings with values that must be Call or Email

The data cleaning and transformation process consists of the following steps:
* Remove unwanted values based on the above assumptions
* Transform the columns to the specified data type
* Check if everything is working properly

### How to run scripts

The scripts can be executed either via Python or via Spark itself with the spark-submit command.

#### Python Execution
To run the script that creates the Parquet file with Python we should:
1. Open a terminal
2. Go to script's folder (lets suppose that the scripts are in the Desktop) with `cd ~/Desktop`
3. Run `python3 write-parquet.py`  

To run the script that reads the Parquet file created in a Spark dataframe we follow the same procedure, but at the end we execute the read-parquet.py with the command `python3 read-parquet.py` in a terminal.  

#### Spark Execution
To run the scripts through Spark directly we should:
1. Open a terminal and go to the installation folder of Spark with `cd /usr/local/spark-3.1.3-bin-hadoop3.2`
2. Now to submit the job in Spark and run it we are going to use the spark-submit located in the bin folder.  
We should execute this as follows `bin/spark-submit ~/Desktop/write-parquet.py`

The application is submitted and processed by Spark.   
We follow the same procedure for reading the Parquet file to a Spark dataframe.

After the successful execution of the creation script we can see that there is the parquet file in HDFS.

![image](https://user-images.githubusercontent.com/42607603/161443840-3d59ccc4-d405-4f3f-ac61-067ddd0fbd23.png)



# Spark UI
Spark comes with a handy UI to help us monitor our applications.  
To access this UI, there must be a Spark application running and access it through (http://localhost:4040/) **or** setup the Spark History server in order to be able to see all submitted Spark jobs without needing a running application.

The steps to set up the Spark history Server are:
1. Add the JAVA_HOME variable to the 'spark-config.sh' file in the 'sbin'.
2. Create the spark-events folder like `mkdir /tmp/spark-events`
3. Go to the installation folder of Spark with `cd /usr/local/spark-3.1.3-bin-hadoop3.2` 
4. Run `sbin/start-history-server.sh`
5. Run a Spark Job
6. Access the History Server from a browser by typing the address (http://localhost:18080/)

