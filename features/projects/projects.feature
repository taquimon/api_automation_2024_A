@projects @todoist @sanity
  Feature: Projects
    Scenario: Verify all projects are returned when get all projects endpoint is call
      As a user I want to get all the projects from TODOIST API

      Given I set the URL and headers
      When I call to projects endpoint using "DELETE" method  and without body
      Then I receive the response
      And I validate the status code is 200

    @project_id @acceptance
    Scenario: Verify all projects are returned when get all projects endpoint is call
      As a user I want to get all the projects from TODOIST API

      Given I set the URL and headers
      When I call to projects endpoint using "DELETE" method  and without body
      Then I receive the response
      And I validate the status code is 200