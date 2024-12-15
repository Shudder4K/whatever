Feature: Manage Products

  Scenario: Create a new product
    Given the following products
      | name     | description | price | available | category   |
      | Fedora   | A red hat   | 12.5  | True      | CLOTHS     |
    When I visit the "home" page
    And I set the "name" to "Bowler"
    And I set the "description" to "A black hat"
    And I set the "price" to "15.0"
    And I set the "available" to "True"
    And I set the "category" to "CLOTHS"
    And I press the "Create" button
    Then I should see "Bowler" in the results

  Scenario: List all products
    Given the following products
      | name     | description | price | available | category   |
      | Fedora   | A red hat   | 12.5  | True      | CLOTHS     |
      | Hammer   | A tool      | 25.0  | False     | TOOLS      |
    When I visit the "home" page
    Then I should see "Fedora" in the results
    And I should see "Hammer" in the results

  Scenario: Search products by category
    Given the following products
      | name     | description | price | available | category   |
      | Fedora   | A red hat   | 12.5  | True      | CLOTHS     |
      | Hammer   | A tool      | 25.0  | False     | TOOLS      |
    When I visit the "home" page
    And I set the "category" filter to "CLOTHS"
    And I press the "Search" button
    Then I should see "Fedora" in the results
    And I should not see "Hammer" in the results
