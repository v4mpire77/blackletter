# Context Engineering Enforcement

This document outlines how to enforce the Context Engineering workflow for all agents working on the Blackletter Systems project.

## Enforcement Checklist

Use this checklist to verify that an agent is properly following the Context Engineering workflow:

### 1. Context Assessment Verification

- [ ] Agent explicitly mentioned reviewing `docs/Implementation.md`
- [ ] Agent explicitly mentioned reviewing `docs/project_structure.md`
- [ ] Agent explicitly mentioned reviewing relevant UI/UX documentation (for frontend tasks)
- [ ] Agent explicitly mentioned reviewing bug tracking documentation
- [ ] Agent demonstrated understanding of the feature's place in the overall architecture
- [ ] Agent identified the correct location for code changes based on project structure

### 2. Implementation Verification

- [ ] Agent followed established code patterns
- [ ] Agent adhered to the architectural guidelines
- [ ] Agent used existing utilities and components where appropriate
- [ ] Agent implemented proper error handling
- [ ] Agent's code is testable
- [ ] Agent's code follows naming conventions
- [ ] Agent's code is properly typed (where applicable)

### 3. Documentation Verification

- [ ] Agent included proper docstrings
- [ ] Agent updated relevant documentation
- [ ] Agent explained any non-obvious design decisions
- [ ] Agent documented any breaking changes

### 4. Rule Compliance Verification

- [ ] Agent did not violate any NEVER rules
- [ ] Agent followed all ALWAYS rules
- [ ] Agent's code meets quality standards
- [ ] Agent's implementation is consistent with the rest of the codebase

## Enforcement Actions

If an agent fails to follow the Context Engineering workflow, take these actions:

1. **First Violation**: Remind the agent of the Context Engineering workflow and ask them to redo the task following the proper sequence.

2. **Second Violation**: Provide the agent with the full Context Engineering documentation (`docs/AGENT_CONTEXT_ENGINEERING_WORKFLOW.md`) and require them to explicitly address each step.

3. **Persistent Violations**: Replace the agent with one that will follow the Context Engineering workflow.

## Enforcement Prompts

### Reminder Prompt

```
I notice you haven't followed the Context Engineering workflow. Before implementing any solution, you MUST:

1. Review the Implementation Plan (docs/Implementation.md)
2. Examine the Project Structure (docs/project_structure.md)
3. Check relevant guidelines and documentation

Please restart your approach following the proper Context Engineering workflow sequence.
```

### Correction Prompt

```
Your implementation does not follow the Context Engineering workflow. Specifically:

[List specific violations]

Please revise your approach to:
1. Explicitly review the required documentation
2. Follow established patterns
3. Adhere to the project architecture
4. Include proper documentation

Reference the Context Engineering workflow documentation for guidance.
```

## Monitoring Compliance

To ensure ongoing compliance with the Context Engineering workflow:

1. Regularly review agent outputs for workflow adherence
2. Document common workflow violations
3. Update the Context Engineering documentation as needed
4. Provide feedback to improve agent compliance

## Success Criteria

An agent is successfully following the Context Engineering workflow when:

1. They explicitly perform context assessment before implementation
2. Their code follows established patterns and architecture
3. They provide proper documentation
4. They verify their work against the Context Engineering checklist
5. They do not violate any NEVER rules
6. They follow all ALWAYS rules

## Conclusion

Enforcing the Context Engineering workflow is essential for maintaining code quality, consistency, and maintainability in the Blackletter Systems project. All agents must follow this workflow without exception.
