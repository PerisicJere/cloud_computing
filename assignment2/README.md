## How to run
* Use `git clone <path to repo>` cmd to clone the repository
* Once you clone repository, if not already in assignment 2. Use `cd assingment2`.
* Once inside use `bash run_tests.sh`, and to spin api server run `bash run_api.sh`

## How to test
* There is templates/index.html for e2e testing.

## GH workflows
* There is a workflow in github and it is ready to be run manually. 
* I have included one for tests, and one for server (just so we can check if docker is built).

## API Endpoints
- **GET /items**  
  Renders a list of all items.

- **POST /items/create**  
  Creates a new item.  
  ```json
  {
    "name": "Sword",
    "description": "Sharp blade",
    "damage": 10.5
  }
  ```
  
- **PUT /items/<item_id>/update**  
  Updates the `damage` value of a specific item.

  ```json
  {
    "damage": 15.0
  }
  ```

- **DELETE /items/<item_id>/delete**  
  Deletes the item with the specified ID.
