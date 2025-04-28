# FAST API
-   A python framework provides a very fast way to prepare backend.
-   FAST API uses Starlette and Uvicorn internally, which are the python frameworks for building asynchronous web services. 
-   Uses thirdpart source OpenAPI for making schema of the apis that we create.
-   We can see the schema of our API at endpoint: {our-endpoint}/openapi.json.
-   OpenAPI calls HTTP methods as "operations".
-   We can return list, dict, or even a singular values like str, int, etc..
-   Even the python ORM objects will also directly converted to JSON format.
-   Uses a pydantic module for data validation.

### Steps to use it?
-   Step-1: Create FastAPI class instance, FastAPI is available in "fastapi" module
-   Step-2: Create path operation [e.g. @app.get(), @app.post(), etc.]
-   Step-3: Create path operation function

### Type Hints
-   Specify type hints using ` : ` in python.
-   `var1: int = 1  <- It says var1 should be an integer in further flow of program.`
-   Reference: (type_hints)['https://github.com/Yashu-Simform/Python/blob/b1/README.md#type-hint]
-   Type Hints plays a very important role in FAST API, it provides the thing that is missing i.e. the type checking.

### Interact with FAST API
-   Need to create FastAPI class instance which provide the instance for you application.
    ```
        from fastapi import FastAPI

        app = FastAPI()
    ```

### Pydantic
-   It is used in order to validate the data and convert it to the appropriate data type annotated using type hints.

### Query Params (are not Path Params)
```
    @app.get('/items/{skip}')
    def get_items(skip: int, limit: int = 10):
        return {'data': items[skip: skip + limit]}
```
-   Here in the above example the skip is path param and limit is query param.
-   Path params are the ones which are specified in the path which are always required with the path.
-   If we need some params to be as functoinal params which are not declared in specified path are called as Query params.
-   These Query params can be decalred for mulitple purposes:
    -   Required Query Params
    -   Optional Query Parama
    -   Default Query Params
-   Query params are provided after '?' character and seperated by '&' character.
-   eg. 'http://127.0.0.1:8000/items/0?limit=10'