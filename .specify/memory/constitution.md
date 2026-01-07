<!--
Sync Impact Report:
Version: 1.0.0 → 1.0.1
Change Type: PATCH - Technology matrix ratification and policy clarification
Modified Principles:
  - IV. Technology Stack Constraints - Policy clarified (Phase II tech explicitly ratified)
Added Sections:
  - None (existing content already aligned)
Removed Sections:
  - None
Templates Requiring Updates:
  ✅ .specify/templates/plan-template.md - Constitution Check section compatible
  ✅ .specify/templates/spec-template.md - Requirements section compatible
  ✅ .specify/templates/tasks-template.md - Task organization aligns with principles
  ⚠ .specify/templates/commands/*.md - No command files exist (N/A)
Follow-up TODOs:
  - None - All placeholders filled, technology matrix ratified as policy
-->

# Evolution of Todo — Project Constitution

## Preamble

This Constitution governs all development work across the **Evolution of Todo** project, spanning Phase I through Phase V. It establishes the supreme rules and principles that all agents, processes, and contributors MUST follow. No code may be written, no feature may be added, and no architectural decision may be made without adherence to this Constitution.

**Scope**: All phases, all features, all agents, all contributors.

**Authority**: This Constitution supersedes all other practices, guidelines, or preferences. Compliance is mandatory and non-negotiable.

---

## Core Principles

### I. Spec-Driven Development Mandate (NON-NEGOTIABLE)

**Rule**: No agent or contributor may write production code without approved specifications and tasks.

**Workflow Enforcement**:
- All work MUST follow: **Constitution → Specs → Plan → Tasks → Implement**
- Specifications MUST be approved before planning begins
- Plans MUST be approved before tasks are generated
- Tasks MUST be approved before implementation begins
- Implementation MUST strictly follow the approved tasks

**Prohibited Actions**:
- Writing code without a corresponding approved task
- Creating features not defined in specifications
- Making architectural decisions not documented in plans
- Deviating from approved specifications during implementation

**Rationale**: Spec-Driven Development ensures intentional, traceable, and controllable software evolution. It prevents scope creep, undocumented decisions, and architectural drift.

---

### II. Agent Behavior Rules (NON-NEGOTIABLE)

**Human-Agent Division**:
- Humans define requirements, approve specifications, and make final decisions
- Agents generate specifications, plans, tasks, and implementations
- No manual coding by humans unless explicitly required for debugging or hotfixes

**Agent Constraints**:
- Agents MUST NOT invent features beyond the approved specification
- Agents MUST NOT deviate from approved specifications without explicit user approval
- Agents MUST NOT make architectural decisions not documented in the plan
- Agents MUST NOT refactor or "improve" code outside the scope of current tasks

**Refinement Process**:
- All refinements MUST occur at the specification level, not the code level
- If implementation reveals issues, halt and propose specification updates
- Specification updates require user approval before continuing implementation

**Rationale**: Clear boundaries prevent agents from introducing unintended features, maintaining predictability and control.

---

### III. Phase Governance (NON-NEGOTIABLE)

**Phase Isolation**:
- Each phase (I through V) is strictly scoped by its specification
- Phase boundaries MUST NOT be crossed during implementation
- Future-phase features MUST NEVER leak into earlier phases
- Each phase MUST be fully functional and deployable independently

**Phase Evolution**:
- Architecture MAY evolve across phases, but only through updated specifications and plans
- Cross-phase dependencies MUST be explicitly documented in specifications
- Phase transitions MUST be deliberate and approved

**Phase Validation**:
- Each phase MUST have measurable completion criteria
- No phase may be considered complete without passing all acceptance tests
- Phase completion MUST be validated before proceeding to the next phase

**Rationale**: Phase isolation ensures incremental delivery, prevents scope creep, and allows for course correction between phases.

---

### IV. Technology Stack Constraints (MANDATORY)

**Phase I - Console Application (Current)**:
- Architecture: In-memory console application
- Language: Python 3.11+
- No database required (in-memory state only)
- No authentication required
- No web frontend

**Phase II - Full-Stack Web Application**:
- **Backend**:
  - Language: Python 3.11+
  - Web Framework: FastAPI
  - ORM/Data Layer: SQLModel or equivalent
  - API Style: REST
- **Database**:
  - Neon Serverless PostgreSQL
- **Frontend**:
  - Framework: Next.js (React-based)
  - Language: TypeScript
  - API Communication: REST
- **Authentication**:
  - Better Auth (signup/signin)
- **Architecture**: Full-stack web application

**Phase III and Later**:
- Advanced cloud infrastructure (Docker, Kubernetes)
- Agent frameworks (OpenAI Agents SDK)
- AI integrations and orchestration
- Model Context Protocol (MCP) for agent integrations

**Phase-Gated Technology Rules**:
- Authentication frameworks are NOT allowed in Phase I
- Web frontend frameworks are NOT allowed in Phase I
- Database persistence (PostgreSQL) is NOT allowed in Phase I
- AI or agent frameworks are NOT allowed until Phase III
- Cross-phase technology usage requires constitutional amendment

**Deviation Policy**:
- Technology stack changes require constitutional amendment
- Agents MUST NOT suggest or use alternative technologies without explicit approval
- All dependencies MUST be justified in the implementation plan

**Rationale**: Standardizing the technology stack ensures consistency, maintainability, and skill transferability across phases while preserving phase isolation.

---

### V. Clean Architecture Principles (MANDATORY)

**Separation of Concerns**:
- Business logic MUST be separated from infrastructure concerns
- Domain models MUST NOT depend on frameworks or external libraries
- Dependencies MUST point inward (from infrastructure to domain)

**Layering**:
- **Domain Layer**: Core business entities and logic (framework-agnostic)
- **Application Layer**: Use cases and application-specific business rules
- **Infrastructure Layer**: External concerns (database, APIs, frameworks)
- **Presentation Layer**: User interfaces and API endpoints

**Dependency Rule**:
- Outer layers MAY depend on inner layers
- Inner layers MUST NEVER depend on outer layers
- Use dependency inversion for required outward communication

**Rationale**: Clean architecture ensures long-term maintainability, testability, and adaptability to changing requirements.

---

### VI. Testing and Quality Standards (MANDATORY)

**Test-Driven Development**:
- Tests MUST be written before implementation (Red-Green-Refactor cycle)
- All tests MUST fail initially to validate they test real behavior
- Implementation MUST make tests pass without changing test expectations

**Test Coverage Requirements**:
- **Unit Tests**: Required for all business logic and domain models
- **Integration Tests**: Required for API endpoints, database interactions, and service integrations
- **Contract Tests**: Required for all public APIs and inter-service communication
- **End-to-End Tests**: Required for critical user journeys (per phase specification)

**Quality Gates**:
- No code may be merged without passing all tests
- No code may be merged without meeting coverage thresholds (defined per phase)
- Static analysis and linting MUST pass before merge
- Security scans MUST pass before merge (when applicable)

**Rationale**: Testing ensures correctness, prevents regressions, and documents expected behavior.

---

### VII. Stateless Design Principles (MANDATORY WHERE APPLICABLE)

**Service Design**:
- Services SHOULD be stateless wherever possible
- Session state MUST be externalized (database, cache, or token-based)
- Services MUST be horizontally scalable by design

**State Management**:
- Persistent state MUST reside in databases or managed storage
- Temporary state MUST reside in caches (Redis, in-memory) with TTL
- User session state MUST be token-based (JWT) or externalized

**Exceptions**:
- Stateful components MUST be explicitly justified in the plan
- Stateful components MUST be isolated and clearly documented

**Rationale**: Stateless services enable horizontal scaling, simplify deployment, and improve resilience.

---

### VIII. Cloud-Native Readiness (MANDATORY FOR PHASE III+)

**12-Factor App Principles**:
- Configuration via environment variables (no hardcoded secrets)
- Logs to stdout/stderr (structured logging)
- Processes are stateless and share-nothing
- Services expose health checks and readiness probes

**Observability**:
- All services MUST emit structured logs
- All services MUST expose metrics (Prometheus-compatible)
- All services MUST support distributed tracing (when applicable)

**Resilience**:
- Services MUST handle transient failures gracefully (retries with backoff)
- Services MUST implement circuit breakers for external dependencies
- Services MUST degrade gracefully under load

**Rationale**: Cloud-native design ensures scalability, reliability, and operational excellence in production environments.

---

## Governance

**Constitutional Authority**:
- This Constitution is the supreme governing document for the Evolution of Todo project
- All specifications, plans, tasks, and implementations MUST comply with this Constitution
- Non-compliance is grounds for rejection and rework

**Amendment Procedure**:
- Constitutional amendments require explicit approval from the project owner
- Amendment proposals MUST include rationale and impact analysis
- All amendments MUST be versioned using semantic versioning (MAJOR.MINOR.PATCH)

**Versioning Policy**:
- **MAJOR**: Backward-incompatible changes (principle removals, redefinitions, or policy reversals)
- **MINOR**: Additions (new principles, new sections, expanded guidance)
- **PATCH**: Clarifications, wording improvements, non-semantic refinements

**Compliance Review**:
- All specifications MUST include a Constitution Check section
- All plans MUST verify compliance with constitutional principles
- All pull requests MUST confirm adherence to this Constitution

**Complexity Justification**:
- Any deviation from constitutional principles MUST be explicitly justified
- Justifications MUST be documented in the implementation plan
- Simpler alternatives MUST be evaluated and rejected with reasoning

**Conflict Resolution**:
- In case of conflicts between this Constitution and other documents, the Constitution prevails
- Ambiguities MUST be resolved by the project owner
- Interpretations MUST be documented as amendments or ADRs

---

**Version**: 1.0.1 | **Ratified**: 2025-12-28 | **Last Amended**: 2026-01-04
