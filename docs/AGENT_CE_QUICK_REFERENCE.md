# Context Engineering Quick Reference

## Mandatory Workflow Sequence

1. **CONTEXT FIRST**
   - Review Implementation Plan (`docs/Implementation.md`)
   - Check Project Structure (`docs/project_structure.md`)
   - Consult UI/UX Guidelines (`docs/UI_UX_doc.md`)
   - Check Bug Tracking (`docs/Bug_tracking.md`)

2. **THEN IMPLEMENT**
   - Follow established patterns
   - Adhere to architecture
   - Write quality, testable code

3. **DOCUMENT CONCURRENTLY**
   - Update docstrings
   - Maintain documentation
   - Record changes

## Critical Rules

### NEVER
- ❌ Skip context assessment
- ❌ Hardcode API keys
- ❌ Write to local disk (use S3)
- ❌ Embed PDFs without chunking
- ❌ Ignore established patterns
- ❌ Leave code in a broken state

### ALWAYS
- ✅ Follow workflow sequence
- ✅ Keep adapters vendor-agnostic
- ✅ Write tests for core functionality
- ✅ Include proper error handling
- ✅ Use existing components
- ✅ Follow naming conventions
- ✅ Document your code

## File Reference Priority
1. `docs/Implementation.md`
2. `docs/project_structure.md`
3. `docs/UI_UX_doc.md`
4. `docs/Bug_tracking.md`
5. `docs/ARCHITECTURE.md`
6. Similar existing code files

## Pre-Completion Checklist
- [ ] All relevant documentation was reviewed
- [ ] Code follows established project patterns
- [ ] Tests are implemented and passing
- [ ] Documentation is updated
- [ ] Code meets quality standards
- [ ] No NEVER rules were violated
- [ ] All ALWAYS rules were followed

## Core Principles
- Context before code
- Patterns over invention
- Documentation is not optional
- Quality is non-negotiable
- Consistency across the codebase
- Testability from the start
