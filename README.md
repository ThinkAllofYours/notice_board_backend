# Notice Board API Documentation

This document provides the API documentation for the Notice Board web application. The Notice Board is a simple web application that allows users to view, create, modify, and delete notices, as well as add replies to notices.

## Base URL

The base URL for this API is `http://localhost:5000`.

## Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": false,
    "error": 404,
    "message": "Not found"
}

```

The API will return the following error types when requests fail:

- 400: Bad request
- 404: Not found
- 422: Cannot process the request
- 500: Internal server error

## Endpoints

### GET /notice/list

Returns a list of notices with pagination.

Request arguments:

- `page`

Returns:

- `success`: Boolean indicating if the request was successful or not
- `notices`: List of notices, where each notice is an object containing the following keys:
    - `id`: Notice ID
    - `author_name`: Author's name
    - `title`: Notice title
    - `content`: Notice content
    - `views_count`: Number of times the notice has been viewed
    - `recommends_count`: Number of times the notice has been recommended
    - `not_recommends_count`: Number of times the notice has been not recommended
    - `created_date`: Notice creation date
    - `updated_date`: Notice last update date
    - `prev_id`: ID of the previous notice in the list
    - `next_id`: ID of the next notice in the list
- `total_cnt`: Total number of notices

### GET /notice/detail/int:notice_id

Returns a single notice with the given `notice_id`.

Request arguments: None

Returns:

- `success`: Boolean indicating if the request was successful or not
- `notice`: Object containing the following keys:
    - `id`: Notice ID
    - `author_name`: Author's name
    - `title`: Notice title
    - `content`: Notice content
    - `views_count`: Number of times the notice has been viewed
    - `recommends_count`: Number of times the notice has been recommended
    - `not_recommends_count`: Number of times the notice has been not recommended
    - `created_date`: Notice creation date
    - `updated_date`: Notice last update date
    - `prev_id`: ID of the previous notice in the list
    - `next_id`: ID of the next notice in the list

### POST /notice/create

Creates a new notice.

Request arguments:

- `author_name`: Author's name (required)
- `title`: Notice title (required)
- `content`: Notice content (required)

Returns:

- `success`: Boolean indicating if the request was successful or not
- `id`: Notice ID

### POST /notice/modify/int:notice_id

Modifies an existing notice with the given `notice_id`.

Request arguments:

- `author_name`: Author's name (required)
- `title`: Notice title (required)
- `content`: Notice content (required)

Returns:

- `success`: Boolean indicating if the request was successful or not
- `notice`: Object containing the following keys:
    - `id`: Notice ID
    - `author_name`: Author's name
    - `title`: Notice title
    - `content`: Notice content
    - `views_count`: Number of times the notice has been viewed
    - `recommends_count`: Number of times the notice has been recommended
    - `not_recommends_count`: Number of times the notice has been not recommended
    - `created_date`: Notice creation date
    - `updated_date`: Notice last update date
    - `prev_id`: ID of the previous notice in the list
    - `next_id`: ID of the next notice in the list

### DELETE /notice/delete/int:notice_id

Deletes an existing notice with the given `notice_id`.

Request arguments: None

Returns:

- `success`: Boolean indicating if the request was successful or not

### PUT /notice/increment-view/int:notice_id

Increments the view count of an existing notice with the given `notice_id`.

Request arguments: None

Returns:

- `success`: Boolean indicating if the request was successful or not
- `views_count`: Updated view count

### GET /reply/list/int:notice_id

Returns a list of replies for the notice with the given `notice_id`.

Request arguments: None

Returns:

- `success`: Boolean indicating if the request was successful or not
- `replies`: List of replies, where each reply is an object containing the following keys:
    - `id`: Reply ID
    - `content`: Reply content
    - `author_name`: Author's name
    - `created_date`: Reply creation date
    - `notice_id`: ID of the notice that the reply belongs to

### POST /reply/create

Creates a new reply.

Request arguments:

- `author_name`: Author's name (required)
- `content`: Reply content (required)
- `notice_id`: ID of the notice that the reply belongs to (required)

Returns:

- `success`: Boolean indicating if the request was successful or not
- `id`: Reply ID

## Authentication

This API uses JWT-based authentication. To access any of the endpoints that require authentication, you need to include an `Authorization` header in your request with a valid JWT token.

## Permissions

This API has the following permissions:

- `create:notice`: Allows the user to create new notices
- `edit:notice`: Allows the user to modify existing notices
- `delete:notice`: Allows the user to delete existing notices

## Examples

### Example Request

```
curl <http://localhost:5000/notice/list?page=1>

```

### Example Response

```
{
    "success": true,
    "notices": [
        {
            "id": 1,
            "author_name": "Alice",
            "title": "First Notice",
            "content": "This is the content of the first notice.",
            "views_count": 3,
            "recommends_count": 0,
            "not_recommends_count": 0,
            "created_date": "2022-01-01T00:00:00+09:00",
            "updated_date": "2022-01-01T00:00:00+09:00",
            "prev_id": null,
            "next_id": 2
        },
        {
            "id": 2,
            "author_name": "Bob",
            "title": "Second Notice",
            "content": "This is the content of the second notice.",
            "views_count": 5,
            "recommends_count": 0,
            "not_recommends_count": 0,
            "created_date": "2022-01-02T00:00:00+09:00",
            "updated_date": "2022-01-02T00:00:00+09:00",
            "prev_id": 1,
            "next_id": 3
        },
        {
            "id": 3,
            "author_name": "Charlie",
            "title": "Third Notice",
            "content": "This is the content of the third notice.",
            "views_count": 1,
            "recommends_count": 0,
            "not_recommends_count": 0,
            "created_date": "2022-01-03T00:00:00+09:00",
            "updated_date": "2022-01-03T00:00:00+09:00",
            "prev_id": 2,
            "next_id": null
        }
    ],
    "total_cnt": 3
}

```

### Example Request

```
curl -X POST <http://localhost:5000/notice/create> \\
     -H "Content-Type: application/json" \\
     -H "Authorization: Bearer <your_token_here>" \\
     -d '{"author_name": "Dave", "title": "Fourth Notice", "content": "This is the content of the fourth notice."}'

```

### Example Response

```
{
    "id": 4,
    "author_name": "Dave",
    "title": "Fourth Notice",
    "content": "This is the content of the fourth notice.",
    "views_count": 0,
    "recommends_count": 0,
    "not_recommends_count": 0,
    "created_date": "2022-01-04T00:00:00+09:00",
    "updated_date": "2022-01-04T00:00:00+09:00",
    "prev_id": 3,
    "next_id": null
}

```

### Example Request

```
curl -X PUT <http://localhost:5000/notice/modify/4> \\
     -H "Content-Type: application/json" \\
     -H "Authorization: Bearer <your_token_here>" \\
     -d '{"author_name": "Dave", "title": "Fourth Notice (Modified)", "content": "This is the modified content of the fourth notice."}'

```

### Example Response

```
{
    "success": true,
    "notice": {
        "id": 4,
        "author_name": "Dave",
        "title": "Fourth Notice (Modified)",
        "content": "This is the modified content of the fourth notice.",
        "views_count": 0,
        "recommends_count": 0,
        "not_recommends_count": 0,
        "created_date": "2022-01-04T00:00:00+09:00",
        "updated_date": "2022-01-05T00:00:00+09:00",
        "prev_id": 3,
        "next_id": null
    }
}

```

### Example Request

```
curl -X DELETE <http://localhost:5000/notice/delete/4> \\
     -H "Authorization: Bearer <your_token_here>"

```

### Example Response

```
{
    "success": true
}

```

### GET /reply/list/int:notice_id

Returns a list of all replies for the notice with the given ID.

Request Parameters:

- `notice_id` (int, required): The ID of the notice to retrieve replies for.

Example Response:

```
{
    "success": true,
    "replies": [
        {
            "id": 1,
            "content": "This is a reply to the first notice.",
            "author_name": "Alice",
            "created_date": "2022-01-01T00:00:00+09:00",
            "notice_id": 1
        },
        {
            "id": 2,
            "content": "This is a reply to the first notice as well.",
            "author_name": "Bob",
            "created_date": "2022-01-01T00:00:00+09:00",
            "notice_id": 1
        },
        {
            "id": 3,
            "content": "This is a reply to the second notice.",
            "author_name": "Charlie",
            "created_date": "2022-01-02T00:00:00+09:00",
            "notice_id": 2
        }
    ]
}

```

### POST /reply/create

Creates a new reply.

Request arguments:

- `author_name`: Author's name (required)
- `content`: Reply content (required)
- `notice_id`: ID of the notice that the reply belongs to (required)

Returns:

- `success`: Boolean indicating if the request was successful or not
- `id`: Reply ID

```bash

curl -X POST <http://localhost:5000/reply/create> \\
     -H "Content-Type: application/json" \\
     -d '{"author_name": "Dave", "content": "This is a reply to the first notice.", "notice_id": 1}'

```

**Example Response**

```json
{
    "id": 4,
    "content": "This is a reply to the first notice.",
    "author_name": "Dave",
    "created_date": "2022-01-05T00:00:00+09:00",
    "notice_id": 1
}
```
