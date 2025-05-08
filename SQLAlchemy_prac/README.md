# SQLAlchemy ORM

### Ways to define model class using SQLAlchemy
-   Using declarative, which is highly recommended.
    -   Here we create a class inheriting the declarative base which provides the descriptors in order to be mapped as Db Table.
-   Using mapper() function known as imperative mapping.
    -   Any normal python class can be mapped to Db class by using mapper() function.

### Declare model class using declarative, Python Class -> Db Table:
-   Using declarative base class
-   We can map the python class to be database table by inheriting it using the class provided by the declarative_base() method in the sqlalchemy.orm module.
    ```
        from sqlalchemy.orm import declarative_base
        from sqlalchemy import Column, Integer

        Base = declarative_base()

        class User(Base):
            __tablename__ = 'User'

            id = Column(Integer, primary_key=True)
    ```
    -   The minimum requirements to create a mapped class for db table named 'User' are:
        -   `__tablename__`: tablename for the db
        -   at least one column specifying the primary key for the table.

-   <b>Terminologies</b>: 
    -   Instrumentation: A process where some additional behaviour or attribute set are augmented to a regular class. The overall behaviour of the class remains very close to the regular class, but some functionalities are added to it.
    -   Descriptor: A python object having mehods like `__get__`, `__set__` and `__delete__` can be considered as a descriptor.

-   In SQLAlchemy, when a class is mapped to a db table, Column attributes are replaced with python object i.e. descriptor through instrumentation.
-   Here the descriptors are implemented in such a way that using `__get__`, `__set__` and `__delete__` methods we can interact with the data in db.     

### Imperative Mapping:
```
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry

mapper_registry = registry()

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("fullname", String(50)),
    Column("nickname", String(12)),
)


class User:
    pass


mapper_registry.map_imperatively(User, user_table)
```


### Declare a Schema:
-   SQLAlchemy by default provide one attribute named `__table__` to mapped class which gives the metadata of the table. `__table__` returns the `Table` object where `Table` is the built in class provided by SQLAlchemy.   


### Creating an instance of Model class or Mapped class:
```
    ed_user = User(name="ed", fullname="Ed Jones", nickname="edsnickname")
    ed_user.name    -> result: 'ed'
    ed_user.nickname    -> result: 'edsnickname'
    str(ed_user.id)     -> result: None
```
-   <b>Strange thing</b>: We have neither provided the value of id attribute nor the default value as None to it. For a noraml python class it interpreter produces an AttributeError. But here we are getting the value as `None` it is due to instrumentation. When instrumentation is applied a default value is assigned to each attribute. That is why we are getting value as `None` instead of AttributeError. 

### Let's create Session object for db.
-   Session object provides us the workspace where we can do operations on objects binded with the engine. It hold these object references and allow us to perform operations with them until we closes the session.
-   sessionmaker from sqlalchemy.orm provides the `Session` object.
-   Example:
    ```
        from sqlalchemy.orm import sessionmaker

        session = sessionmaker(bind=engine) <= If engine is avaialble here
        
        #otherwise

        session = sessionmaker()
        session.configure(bind=engine)
    ```
-   Say our application thread through which we are performing the db operations on different objects, a session object provides us the scope where this thread works on associated objects.
-   #### Transaction Cycle
    -   Transaction cycle within a session gets executed in three different stages:
        -   Beginning
        -   Executing Operation
        -   Ending
    -   Beginning: When session starts to track changes within it related to db.
    -   Executing Operation: Any set of operations like adding, updating or deleting the objects are tracked by the session but not written immediately to the session, but it writes to DB when session commits or rollbacks.
    -   Ending: Transaction ends when session commits or rollbacks.

-   #### Object or Instance states within the session
    -   <b>Transient</b> - an instance that’s not in a session, and is not saved to the database; i.e. it has no database identity. The only relationship such an object has to the ORM is that its class has a Mapper associated with it.
    -   <b>Pending</b> - when you Session.add() a transient instance, it becomes pending. It still wasn’t actually flushed to the database yet, but it will be when the next flush occurs.
    -   <b>Persistent</b> - any object which is in the session and has a record in a database are said to be persistent instances. Any instances in `Pending` state can be saved and thus moved to `Persistent` state and we can query to DB for already existing record.
    -   <b>Detached</b> - an instance which corresponds, or previously corresponded, to a record in the database, but is not currently in any session. The detached object will contain a database identity marker, however because it is not associated with a session, it is unknown whether or not this database identity actually exists in a target database. Detached objects are safe to use normally, except that they have no ability to load unloaded attributes or attributes that were previously marked as “expired”.  
    -   <b>Deleted</b> - An instance which has been deleted within a flush, but the transaction has not yet completed. Objects in this state are essentially in the opposite of “pending” state; when the session’s transaction is committed, the object will move to the detached state. Alternatively, when the session’s transaction is rolled back, a deleted object moves back to the persistent state.

### Adding and Updating the objects
-   objects are going to be the rows or records into our DB Table.
-   Example:
    ```
        my_user = User(name="ed", fullname="Ed Jones", nickname="edsnickname")
        session.add(my_user)
    ```
-   Now when `session.add(my_user)` line gets executed, it will not immediately perform `INSERT` query. 
-   These changes of insertion or updation are going to be commited when we try to `retrive` some data from DB. It flushes the changes and commit them to DB first then gives the reloaded data.
-   We can explicitly use `session.commit()` in order to commit the changes to the database.
-   Adding multiple objects or records to DB table:
    ```
        session.add_all(
            [
                User(name="wendy", fullname="Wendy Williams", nickname="windy"),
                User(name="mary", fullname="Mary Contrary", nickname="mary"),
                User(name="fred", fullname="Fred Flintstone", nickname="freddy"),
            ]
        )
    ```