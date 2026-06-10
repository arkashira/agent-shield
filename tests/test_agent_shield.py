def test_ci_checks_pass_on_pr():
    # Create a PR
    pr_response = create_pr()
    assert pr_response.status_code == 201

    # Trigger the CI workflow
    workflow_response = check_workflow_run_status()
    assert workflow_response.status_code == 200

    # Verify that all checks pass
    ci_result = run_ci_checks()
    assert ci_result == "All checks passed"