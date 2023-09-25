from drf_spectacular.utils import extend_schema, OpenApiExample

question_post_extend_schema = extend_schema(
    request="gs",
    description="Add question multiple or simple for multiple 8 options, for simple questions 5 options. Answer for multiple 1-3, simple must be only 1 answer",
    examples=[
        OpenApiExample(
            name="Simple Successful request",
            value={
                "question": "What is the capital of France?",
                "content": "https://raw.githubusercontent.com/guinnod/photo-base/main/13.jpg",
                "task": "Find the capital",
                "taskContent": "https://raw.githubusercontent.com/guinnod/photo-base/main/14.jpg",
                "options": ["Paris", "London", "Berlin", "Astana", "Moscow"],
                "answers": ["Paris"],
                "type": "simple",
                "topic": ["Geography", "Tourism"],
                "format": "text"
            },
            description="Simple question post",
        ),
        OpenApiExample(
            name="Multiple Successful request",
            value={
                "question": "What is the capitals of France, Kazakhstan?",
                "content": "https://raw.githubusercontent.com/guinnod/photo-base/main/13.jpg",
                "task": "Find the capital",
                "taskContent": "https://raw.githubusercontent.com/guinnod/photo-base/main/14.jpg",
                "options": ["Paris", "London", "Berlin", "Astana", "Moscow", "Ulan-Bator", "Kiev", "America"],
                "answers": ["Paris", "Astana"],
                "type": "simple",
                "topic": ["Geography", "Tourism"],
                "format": "text"
            },
            description="Multiple answer question post",
        ),
    ]
)

questions_check_post_extend_schema = extend_schema(
    request="ww",
    examples=[
        OpenApiExample(
            name="Submit test",
            value=[
                {"id": "650ec192065c71759465d03b",
                 "answers": ["1000"]
                 },
                {"id": "650ec192065c71759465d03c",
                 "answers": ["1000", "300"]
                 }
            ],
        ),
    ]
)
