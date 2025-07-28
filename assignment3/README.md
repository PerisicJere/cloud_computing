# Assignment 3

## Installation

* Use `git clone <path to repo>` cmd to clone the repository
* Once you clone repository, if not already in assignment 2. Use `cd assingment3`.
* Once you are inside the folder, run `Dockerfile` image to create a container.
* Once the image is up, run `./test.sh` to run tests.
* If the `./test.sh` doesn't run, try `chmod +x ./test.sh`, and then repeat `./test.sh`

### API Endpoints

#### Get All Items
```
GET /items
```
This will fetch all items, without params.


#### Get Single Item
```
GET /items?id=<item_id>
```
This will fetch a specified item. Id as indicator of which item.

#### Create Item
```http
POST /items
JSON ->
{
  "name": "item name",
  "description": "item description"
}
```

This will create an item with params in json.

#### Update Item
```http
PUT /items/<item_id>
JSON -> 
{
  "name": "new name",
  "description": "new description"
}
```

This will update an item with specified item id, and changed params.

#### Delete Item
```http
DELETE /items/<item_id>
```

This will delete an item with a specified item id.


### Resources used
1. https://stackoverflow.com/questions/61749489/getting-could-not-connect-to-the-endpoint-url-error-with-boto3-when-deploying
2. https://stackoverflow.com/questions/75875534/table-created-successfully-but-dynamodb-cannot-find-it-boto3
3. https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
4. https://github.com/orgs/community/discussions/116610
5. claude prompt: Write an short Docker Compose up build for docker-compose.test.yml, with down and exit_code
