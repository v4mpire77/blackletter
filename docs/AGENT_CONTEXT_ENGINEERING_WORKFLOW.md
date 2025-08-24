# Agent Context Engineering Workflow

This document defines the mandatory workflow that all agents must follow when working with the Blackletter Systems codebase. Following this workflow ensures consistency, quality, and maintainability across the project.

## 1. Workflow Sequence

Every agent MUST follow this exact sequence when handling any task:

### 1.1. Context Assessment (ALWAYS FIRST)

1. **Review Implementation Plan** (`docs/Implementation.md`)
   - Understand the feature being implemented in the broader context
   - Identify which implementation stage the task belongs to
   - Note any dependencies or prerequisites

2. **Examine Project Structure** (`docs/project_structure.md`)
   - Locate where new code should be placed
   - Understand how components should interact
   - Follow established naming conventions

3. **Check UI/UX Guidelines** (`docs/UI_UX_doc.md`)
   - For frontend tasks, ensure compliance with design system
   - Verify component usage patterns
   - Confirm accessibility requirements

4. **Review Bug Tracking** (`docs/Bug_tracking.md`)
   - Check for known issues related to the current task
   - Avoid reintroducing fixed bugs
   - Follow established resolution workflows

### 1.2. Code Implementation (AFTER Context Assessment)

1. **Follow Established Patterns**
   - Examine similar existing code before writing new code
   - Maintain consistent coding style and patterns
   - Use existing utilities and helpers

2. **Adhere to Architecture**
   - Keep adapters vendor-agnostic (everything behind `core/*`)
   - Use dependency injection for providers
   - Follow the modular design pattern

3. **Implement with Quality**
   - Write small, composable functions
   - Include type hints and docstrings
   - Avoid "magic" or unexplained code

4. **Ensure Testability**
   - Write unit tests for pure logic
   - Make components easy to test
   - Consider edge cases

### 1.3. Documentation (CONCURRENT with Implementation)

1. **Update Documentation**
   - Add/update docstrings for all functions, classes, and modules
   - Document any non-obvious design decisions
   - Update relevant documentation files

2. **Maintain Changelog**
   - Document significant changes
   - Note any breaking changes or deprecations
   - Record bug fixes

## 2. Critical Rules

### 2.1. NEVER Rules

- **NEVER** ignore the Context Engineering workflow
- **NEVER** hardcode API keys or secrets
- **NEVER** write to local disk for artifacts (use S3/MinIO)
- **NEVER** embed PDFs without chunking (target 1-2k tokens)
- **NEVER** implement features without consulting documentation first
- **NEVER** leave code in a broken state
- **NEVER** commit code that doesn't follow established patterns

### 2.2. ALWAYS Rules

- **ALWAYS** follow the workflow sequence (Context → Implementation → Documentation)
- **ALWAYS** keep adapters vendor-agnostic
- **ALWAYS** write tests for core functionality
- **ALWAYS** include proper error handling
- **ALWAYS** use existing components and utilities
- **ALWAYS** follow naming conventions
- **ALWAYS** document your code
- **ALWAYS** consider security implications

## 3. File Reference Priority

When working on a task, ALWAYS consult files in this exact order:

1. `docs/Implementation.md` - Overall project plan
2. `docs/project_structure.md` - Where code should go
3. `docs/UI_UX_doc.md` - Design guidelines (for frontend)
4. `docs/Bug_tracking.md` - Known issues
5. `docs/ARCHITECTURE.md` - System architecture
6. Similar existing code files - For patterns and examples

## 4. Quality Standards

### 4.1. Code Quality

- Follow language-specific best practices
- Maintain consistent formatting
- Use meaningful variable and function names
- Keep functions small and focused
- Use comments for complex logic
- Implement proper error handling

### 4.2. Testing Requirements

- Write unit tests for pure functions
- Include integration tests for key workflows
- Test edge cases and error conditions
- Maintain 80%+ test coverage for core modules

### 4.3. Documentation Quality

- Clear and concise docstrings
- Updated README files
- Accurate architectural documentation
- Proper changelog entries

## 5. Context Engineering Checklist

Before considering any task complete, verify:

- [ ] All relevant documentation was reviewed
- [ ] Code follows established project patterns
- [ ] Tests are implemented and passing
- [ ] Documentation is updated
- [ ] Code meets quality standards
- [ ] No NEVER rules were violated
- [ ] All ALWAYS rules were followed

## 6. Implementation Example

### Good Implementation (Following Context Engineering)

```python
# First reviewed docs/Implementation.md to understand the feature
# Then checked docs/project_structure.md to determine placement
# Examined existing code in app/core/ for patterns

"""
OCR module for Blackletter Systems.

This module provides functionality for extracting text from PDF documents using:
- pdfplumber for direct text extraction
- pytesseract for OCR when needed
"""

import os
from typing import Dict, List, Optional
import logging

import pdfplumber
from PIL import Image
import pytesseract

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text(file_path: str) -> str:
    """
    Extract text from a PDF document.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        str: Extracted text content
    """
    # Implementation following established patterns
    # ...
```

### Bad Implementation (Ignoring Context Engineering)

```python
# Jumped straight to coding without reviewing documentation
# Ignored existing patterns and project structure

def get_pdf_text(pdf):
    # No docstring
    # Hardcoded paths
    # No error handling
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # ...
```

## 7. Conclusion

The Context Engineering workflow is not optional. It is a mandatory process that ensures the Blackletter Systems codebase remains consistent, maintainable, and high-quality. All agents MUST follow this workflow without exception.

By adhering to this workflow, you will:
- Produce higher quality code
- Maintain consistency across the codebase
- Reduce bugs and technical debt
- Make the codebase more maintainable
- Ensure documentation stays up-to-date
- Deliver a better product
