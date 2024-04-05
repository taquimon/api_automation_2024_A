@sections @todoist @sanity
Feature: Sections

  Scenario: Verify all sections are returned when get all sections endpoint is call
  As a user I want to get all the projects from TODOIST API

    When I call to sections endpoint using "GET" method  and without body
    Then I receive the response and validate using "get_all_sections" json
    And I validate the status code is 200

  @section_id
  Scenario: Verify that a section can be deleted using delete project endpoint
      As a user I want to create a projects from TODOIST API

    When I call to sections endpoint using "DELETE" method  and without body
    Then I validate the status code is 204

  @project_id
  Scenario Outline: Verify can create multiple sections with name <section_name>
    AS a user I want to create multiple sections

    When I call to sections endpoint using "POST" method  and "param" body
    """
    {
      "project_id": "project_id",
      "name": "<section_name>"
    }
    """
    Examples:
      | section_name           |
      | First Section created  |
      | Second Section created |
      | Third Section created  |
      | Fourth Section created |

    @section_id @wip
    Scenario: Verify can be updated a section using update section endpoint

      When I call to sections endpoint using "POST" method  and "without" body
      Then I validate the status code is 200