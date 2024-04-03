@projects @todoist @sanity
  Feature: Projects

    @critical
    @allure.label.owner:ET
    @allure.link:https://dev.example.com/
    @allure.issue:API-123
    Scenario: Verify all projects are returned when get all projects endpoint is call
      As a user I want to get all the projects from TODOIST API

      When I call to projects endpoint using "GET" method  and without body
      Then I receive the response and validate using "get_all_projects" json
      And I validate the status code is 200

    @critical
    @allure.label.owner:ET
    @allure.link:https://dev.example.com/
    @allure.issue:API-123
    @acceptance
    Scenario: Verify that a project can be created using create project endpoint
      As a user I want to create a projects from TODOIST API

      When I call to projects endpoint using "POST" method  and without body
      Then I receive the response and validate using "create_project" json
      And I validate the status code is 200

    @project_id @acceptance @wip
    Scenario: Verify that a project can be deleted using delete project endpoint
      As a user I want to create a projects from TODOIST API

      When I call to projects endpoint using "DELETE" method  and without body
      Then I receive the response and validate using "delete_project" json
      And I validate the status code is 204