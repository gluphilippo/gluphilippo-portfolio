# API testing of a backend microservice

My first API testing project: a friends/social-graph microservice (Spring Boot, Postgres).

## Setup

- Postgres 16 in a Podman container, the service run locally with a `local` profile.
- No Swagger in the repo, so the contract came from the README, the controllers and the API DTOs.

## Work

- A Postman collection of **~70 requests** in folders by scenario: CRUD of players and relations, validation and edge cases, idempotency, versioning, error handling.
- Checks verified both through the API response and directly in the database.

## Findings (reported as questions to the developer)

1. **Version bump on a no-op delete.** Deleting a player that doesn't exist (0 affected rows) still increments the graph version, which contradicts the README. Confirmed in the DB (no rows change, only the version) and in code (the version bump is unconditional).
2. **500 instead of 503 when the database is down.** The README promises 503, but the transaction-creation exception isn't handled by the service's exception handler (only the connection exception is).

Both checks are kept in the collection as intentionally failing tests until the contract or the code is fixed.
