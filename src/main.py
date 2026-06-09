from src.sdk.sdk import CrewPipelineSDK


def main():
    topic = input("Enter topic: ")

    language = input(
        "Enter language (english/bidi): ",
    ).strip().lower()

    author = input(
        "Author (optional): ",
    ).strip()

    date = input(
        "Date (optional): ",
    ).strip()

    course = input(
        "Course (optional): ",
    ).strip()

    lecturer = input(
        "Lecturer (optional): ",
    ).strip()

    cover_sheet = {
        "author": author,
        "date": date,
        "course": course,
        "lecturer": lecturer,
    }

    sdk = CrewPipelineSDK()

    result = sdk.run(
        topic=topic,
        language=language,
        cover_sheet=cover_sheet,
    )

    print("\nGenerated Output:\n")
    print(result)


if __name__ == "__main__":
    main()
