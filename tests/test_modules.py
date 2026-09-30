from qna import answer_question
from explanation_module import explain_topic
from summary_module import summarize_text
from learning_path import (
    get_learning_recommendations
)


def test_empty_qna():

    result = answer_question("")

    assert (
        "Please enter a question"
        in result
    )


def test_empty_explanation():

    result = explain_topic("")

    assert (
        "Please enter a topic"
        in result
    )


def test_empty_summary():

    result = summarize_text("")

    assert (
        "Please enter text"
        in result
    )


def test_empty_learning_path():

    result = get_learning_recommendations("")

    assert (
        "Please enter a topic"
        in result
    )