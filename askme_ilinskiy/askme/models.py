QUESTIONS = [
    {
        "title": f"Question {i}",
        "text": f'Text {i} Lorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для текстов на латинице с начала XVI века. В то время некий безымянный печатник создал большую коллекцию размеров и форм шрифтов, используя Lorem Ipsum для распечатки образцов. Lorem Ipsum не только успешно пережил без заметных изменений пять веков, но и перешагнул в электронный дизайн. Его популяризации в новое время послужили публикация листов Letraset с образцами Lorem Ipsum в 60-х годах и, в более недавнее время, программы электронной вёрстки типа Aldus PageMaker, в шаблонах которых используется Lorem Ipsum.',
        "answers": f"Answers: {i}",
        "tags": [{"name": f"tag{i}", "id": i},
                 {"name": f"tag{i + 1}", "id": i + 1}],
        "rating": f"{i}",
        "id": f"{i}",
    } for i in range(20)
]

TAGS = [
    {
       "text": f"Tag{i}",
        "color": f"black",
        "id": f"{i}"
    } for i in range(15)
]

BEST_MEMBERS = [
    {
        "text": f"Member{i}",
        "href": f"#"
    }for i in range(8)
]

AUTHOR = {
    "login": "dr_temp",
    "email": "temp@mail.ru",
    "nickname": "Dr. Temp",
}

ANSWERS = [
    {
        "text": f'Text answer {i}  Lorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для тек Lorem Ipsum является стандартной "рыбой" для текстов на латини Lorem Ipsum является стандартной "рыбой" для текстов на латини Lorem Ipsum является стандартной "рыбой" для текстов на латини Lorem Ipsum является стандартной "рыбой" для текстов на латинистов на латинице с',
        "rating": f'{i}',
        "isCorrect": False
    }for i in range(8)

]
