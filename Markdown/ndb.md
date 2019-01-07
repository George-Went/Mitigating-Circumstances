# No SQL Database (NDB)

## What is NDB?

ndb is googles NoSQL database - it is not a realational database, 

Comparison with traditional databases

While the Cloud Datastore interface has many of the same features as traditional databases, as a NoSQL database it differs from them in the way it describes relationships between data objects. Here’s a high-level comparison of Cloud Datastore and relational database concepts:


| Concept                          | Cloud Datastore  | Cloud firestore  | Relational Database |
| -------------------------------  |:----------------:| ----------------:|--------------------:|
| Catagory of object               | Kind             | Collection Group | Table               |
| One Object                       | Enitity          | Document         | Row                 |
| Induvidual data for an object    | Property         | Field            | Column              |
| Uniqure ID for an Object         | Key              | Document ID      | Primary Key         |


## Getting started with ndb 

### importing the modules 
As ndb is a google addon it will need to be imported, however it is already part of the dev_appserver / deployment pakage, so dont worry about putting it into the correct /lib files

```python
from google.appengine.ext import ndb
```

### Creating a table (entity kind) 

in the same way you would create a table with attributes in SQL, you also need to create the entitys for ndb - due to the way that ndb works, these can be created on the fly - they do not need to be pre-made for them to work in the program, and any new tables (entity kinds) made in the code, will be created in the datastore 

Here is an example model
```python
class CarModel(ndb.Model):
    name = ndb.StringProperty()
    make = ndb.StringProperty()
    doors = ndb.IntegerProperty()
    dateAdded = ndb.DateTimeProperty()

```
> note - this does not deploy the table, it only creates the model

#### Hidden Attributes

As well as the attributes you add to a dataset, there are also  hidden attributes - kind,key and id

Kind is used to denote the entity kind of the dataset - in the above example it would be 

ID is similary to a primary key id in a relational database - each tuple has a designated id that will last the lifetime of the tuple 

Keys are induvidual addresses that are different for *every* tuple, as a single tuple may have multiple versions (due to updating datat etc.) which can be saved to the ndb database, keys can be used to retrive specific results. 


## Functions

### Creating a dataset
while the tables do not need to be pre-made, they do still need to be generated, in most cases, if a applicaiton is new, the tabel will be generated when new a new data set is put into the data store.

Once data has been added to a dataset, the *put()* will send the data to the google ndb database 

The below example shows code that puts 2 sets of data into the datastore when the user visits *"/generate"*

```python
from models import CarModel # imports the above car example model

@app.route('/generateexample')
def generate():
    car = CarModel() 
    car.name = "Yaris" 
    car.make = "Toyota"
    car.doors = "5"
    car.dateAdded = "12/3/18"
    car.put()
    return redirect('/')
        sdf
```

### Editing an existing dataset 
while the general process is similar to creating a new dataset, the main differnet is the need to aquire an existing dataset, this is usually done by referanceing the id, which due to the induvidual nature of the id, will most likely only return one result.

### Queries 






#### Create 
```python
def create (self,name,email,password):
    car = CarModel() #car is instanceated as a CarModel class 
    car.name = car 
    car.make = make
    car.doors = doors 
    car.dateAdded = date
    car.put()#will create a new tuple in the database 
    return user
```
#### Read 
```python

```

#### Update
```python
def edit (self,id,name,text):
    car = ExampleDataModel.get_by_id(int(id)) 
    car.name = car 
    car.make = make
    car.doors = doors 
    car.dateAdded = date
    car.put()
    return exampleData
```

#### Delete
```python
def delete(self,id):
    exampleData = ExampleDataModel.get_by_id(int(id))
    return exampleData.key.delete()
```



```yaml
runtime: python27
api_version: 1
threadsafe: true


handlers:
- url: /static
  static_dir: static
- url: /.*
  script: main.app

```