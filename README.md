Make sure you have `pyenv` and `make` installed.
    
Run the following commands from project root directory to initialiaze the backend project:
```
make init
make run_migration
```    

Execute the following command to run the dev server:
```
make run_dev
```
  
Run following command everytime any `ORM Data Models` are added, changed, or removed:
```
make run_migration
```