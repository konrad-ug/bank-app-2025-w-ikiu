Feature: Account registry

Scenario: User is able to create 2 accounts
    Given Account registry is empty
    When I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    And I create an account using name: "tadeusz", last name: "szcześniak", pesel: "79101011234"
    Then Number of accounts in registry equals: "2"
    And Account with pesel "89092909246" exists in registry
    And Account with pesel "79101011234" exists in registry

Scenario: User is able to update surname of already created account
    Given Account registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    When I update "surname" of account with pesel: "95092909876" to "filatov"
    Then Account with pesel "95092909876" has "surname" equal to "filatov"

Scenario: User is able to update name of already created account
    Given Account registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    When I update "name" of account with pesel: "95092909876" to "ola"
    Then Account with pesel "95092909876" has "name" equal to "ola"

Scenario: Created account has all fields correctly set
    Given Account registry is empty
    When I create an account using name: "krzysztof", last name: "kowal", pesel: "11122233344"
    Then Account with pesel "11122233344" has "name" equal to "krzysztof"
    And Account with pesel "11122233344" has "surname" equal to "kowal"
    And Account with pesel "11122233344" has "pesel" equal to "11122233344"
    And Account with pesel "11122233344" has "balance" equal to "0.0"

Scenario: User is able to delete created account
    Given Account registry is empty
    And I create an account using name: "parov", last name: "stelar", pesel: "01092909876"
    When I delete account with pesel: "01092909876"
    Then Account with pesel "01092909876" does not exist in registry
    And Number of accounts in registry equals: "0"

Scenario: Incoming transfer increases account balance
    Given Account registry is empty
    And I create an account using name: "Jan", last name: "Kowalski", pesel: "12345678901"
    When I make a transfer of type "incoming" with amount "1000" to account with pesel "12345678901"
    Then Account with pesel "12345678901" has "balance" equal to "1000.0"

Scenario: Outgoing transfer decreases account balance
    Given Account registry is empty
    And I create an account using name: "Adam", last name: "Nowak", pesel: "98765432109"
    And I make a transfer of type "incoming" with amount "500" to account with pesel "98765432109"
    When I make a transfer of type "outgoing" with amount "200" to account with pesel "98765432109"
    Then Account with pesel "98765432109" has "balance" equal to "300.0"

Scenario: Outgoing transfer fails when insufficient funds
    Given Account registry is empty
    And I create an account using name: "Ewa", last name: "Lis", pesel: "55050512345"
    And I make a transfer of type "incoming" with amount "100" to account with pesel "55050512345"
    When I make a transfer of type "outgoing" with amount "200" to account with pesel "55050512345"
    Then Account with pesel "55050512345" has "balance" equal to "100.0"