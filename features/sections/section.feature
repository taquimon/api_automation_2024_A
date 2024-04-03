@sections @todoist @sanity
  Feature: Sections
    Scenario: Verify all sections are returned when get all sections endpoint is call
      As a user I want to get all the projects from TODOIST API

      When I call to sections endpoint using "GET" method  and without body
      Then I receive the response and validate using "get_all_sections" json
      And I validate the status code is 200