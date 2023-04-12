QUESTIONS = [
    {
        "title": f"Question {i}",
        "text": f"Text {i}",
        "answers": f"Answers: {i}",
        "tags": [{"name": f"tag{i}", "ref": f"#"},
                 {"name": f"tag{i + 1}", "ref": f"#"}],
        "rating": f"{i}"
    } for i in range(20)
]

TAGS = [
    {
       "text": f"Tag{i}",
        "color": f"black",
        "href": f"#"
    } for i in range(15)
]

BEST_MEMBERS = [
    {
        "text": f"Member{i}",
        "href": f"#"
    }for i in range(8)
]
