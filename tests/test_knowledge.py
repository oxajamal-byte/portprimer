from portprimer.knowledge import get_port_knowledge


def test_known_port_knowledge():
    knowledge = get_port_knowledge(22)
    assert knowledge.service == "SSH"
    assert knowledge.learning_label == "Admin Door"
    assert "vulnerability" not in knowledge.why_it_matters.lower()


def test_unknown_port_knowledge():
    knowledge = get_port_knowledge(65000)
    assert knowledge.service == "Unknown service"
    assert knowledge.learning_label == "Unknown Door"
    assert knowledge.action_hint == "Learn more before changing"


def test_playground_knowledge_is_honest():
    knowledge = get_port_knowledge(15432)
    assert knowledge.service == "Playground Database-style service"
    assert "not a real database" in knowledge.why_it_matters
    assert "127.0.0.1" in knowledge.beginner_note
    assert "safe local practice service" in knowledge.what_it_is
