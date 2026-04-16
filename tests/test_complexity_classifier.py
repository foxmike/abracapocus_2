from agents.complexity_classifier import ComplexityClassifier


def test_micro_scope_maps_to_single_phase():
    classifier = ComplexityClassifier()
    score = classifier.classify(
        title="Fix typo",
        description="Update one typo in docs.",
        acceptance_criteria=["typo fixed"],
        context_files=["README.md"],
    )

    assert score.scope == "micro"
    assert score.recommended_phases == 1


def test_standard_scope_maps_to_three_phases():
    classifier = ComplexityClassifier()
    score = classifier.classify(
        title="Improve CLI flow",
        description="Improve output shape and small task handling.",
        acceptance_criteria=["flow updated", "tests updated", "docs updated"],
        context_files=["scripts/ops.py", "tests/test_orchestration_flow.py"],
    )

    assert score.scope == "standard"
    assert score.recommended_phases == 3


def test_complex_scope_for_five_or_more_criteria():
    classifier = ComplexityClassifier()
    score = classifier.classify(
        title="Large workflow rollout",
        description="Coordinate broad workflow changes across layers.",
        acceptance_criteria=["a", "b", "c", "d", "e"],
        context_files=["a.py", "b.py"],
    )

    assert score.scope == "complex"
    assert score.recommended_phases == 5


def test_complex_scope_for_high_risk_keywords():
    classifier = ComplexityClassifier()
    score = classifier.classify(
        title="Add auth gateway",
        description="Implement auth checks for API requests.",
        acceptance_criteria=["auth checks enforced"],
        context_files=["runtime/router.py"],
    )

    assert score.risk == "high"
    assert score.scope == "complex"
    assert score.recommended_phases == 5


def test_recommended_backend_matches_task_type():
    classifier = ComplexityClassifier()

    planning_score = classifier.classify(
        title="Design rollout plan",
        description="Design and research options for plan quality.",
        acceptance_criteria=["plan documented", "tradeoffs captured"],
        context_files=["plans/master.json"],
    )
    coding_score = classifier.classify(
        title="Implement feature",
        description="Implement core behavior for execution path with stable interfaces.",
        acceptance_criteria=["feature implemented", "tests pass"],
        context_files=["agents/planning_agent.py", "tests/test_models.py"],
    )

    assert planning_score.recommended_backend == "claude_code_cli"
    assert coding_score.recommended_backend == "codex_cli"

