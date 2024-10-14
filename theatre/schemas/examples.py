play_create_example_scheme = {
    "title": "Romeo and Juliet",
    "description": "is a tragedy written by William Shakespeare early in his career about the romance between two Italian youths from feuding families.",
    "duration": 180,
    "actors": [1, 2],
    "genres": [1],
    "image": "path/to/image.jpg | null"
}
play_create_response_example_scheme = {
  "id": 9,
  "title": "Romeo and Juliet",
  "description": "is a tragedy written by William Shakespeare early in his career about the romance between two Italian youths from feuding families.",
  "duration": 180,
  "actors": [
    1,
    2
  ],
  "genres": [
    1
  ],
  "image": "null"
}
reservation_create_example_scheme = {
    "tickets": [
        {
            "row": 5,
            "seat": 10,
            "performance": 1
        },
        {
            "row": 5,
            "seat": 11,
            "performance": 1
        }
    ]
}
reservation_create_response_example_scheme = {
  "id": 8,
  "tickets": [
    {
      "id": 9,
      "row": 5,
      "seat": 10,
      "performance": 1
    },
    {
      "id": 10,
      "row": 5,
      "seat": 11,
      "performance": 1
    }
  ],
  "created_at": "2024-10-14T10:31:10.333028Z"
}

