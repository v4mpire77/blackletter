# Context Engineering PowerShell Script
# Provides easy access to Context Engineering tools and validation

param(
    [Parameter(Mandatory=$false)]
    [string]$Task,
    
    [Parameter(Mandatory=$false)]
    [string]$Action = "help",
    
    [Parameter(Mandatory=$false)]
    [string]$Output,
    
    [Parameter(Mandatory=$false)]
    [switch]$Template,
    
    [Parameter(Mandatory=$false)]
    [switch]$Validate
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Colors for output
$Colors = @{
    Success = "Green"
    Warning = "Yellow"
    Error = "Red"
    Info = "Cyan"
    Header = "Magenta"
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

function Show-Header {
    Write-ColorOutput "=" * 60 "Header"
    Write-ColorOutput "CONTEXT ENGINEERING WORKFLOW TOOLS" "Header"
    Write-ColorOutput "Blackletter Systems" "Header"
    Write-ColorOutput "=" * 60 "Header"
    Write-Host ""
}

function Show-Help {
    Write-ColorOutput "Usage Examples:" "Info"
    Write-Host ""
    Write-ColorOutput "1. Generate context summary for a task:" "Success"
    Write-Host "   .\context_engineering.ps1 -Task 'Implement user authentication' -Action summary"
    Write-Host ""
    Write-ColorOutput "2. Generate workflow template:" "Success"
    Write-Host "   .\context_engineering.ps1 -Task 'Add file upload component' -Template"
    Write-Host ""
    Write-ColorOutput "3. Validate agent response:" "Success"
    Write-Host "   .\context_engineering.ps1 -Action validate -Input 'response.txt'"
    Write-Host ""
    Write-ColorOutput "4. Show Context Engineering workflow:" "Success"
    Write-Host "   .\context_engineering.ps1 -Action workflow"
    Write-Host ""
    
    Write-ColorOutput "Available Actions:" "Info"
    Write-Host "  summary    - Generate context summary for a task"
    Write-Host "  template   - Generate workflow template"
    Write-Host "  validate   - Validate agent response against workflow"
    Write-Host "  workflow   - Show Context Engineering workflow"
    Write-Host "  docs       - List required documentation files"
    Write-Host "  help       - Show this help message"
    Write-Host ""
    
    Write-ColorOutput "Parameters:" "Info"
    Write-Host "  -Task      - Description of the task to analyze"
    Write-Host "  -Action    - Action to perform (default: help)"
    Write-Host "  -Output    - Output file path"
    Write-Host "  -Template  - Generate workflow template"
    Write-Host "  -Validate  - Validate agent response"
}

function Show-Workflow {
    Write-ColorOutput "CONTEXT ENGINEERING WORKFLOW (MANDATORY)" "Header"
    Write-Host ""
    Write-ColorOutput "1. CONTEXT ASSESSMENT (ALWAYS FIRST)" "Info"
    Write-Host "   • Review Implementation Plan (docs/Implementation.md)"
    Write-Host "   • Examine Project Structure (docs/project_structure.md)"
    Write-Host "   • Check UI/UX Guidelines (docs/UI_UX_doc.md)"
    Write-Host "   • Review Bug Tracking (docs/Bug_tracking.md)"
    Write-Host ""
    Write-ColorOutput "2. IMPLEMENTATION PLAN" "Info"
    Write-Host "   • Create detailed implementation plan"
    Write-Host "   • Identify dependencies and prerequisites"
    Write-Host "   • Plan testing strategy"
    Write-Host ""
    Write-ColorOutput "3. IMPLEMENTATION" "Info"
    Write-Host "   • Follow established patterns"
    Write-Host "   • Adhere to architecture"
    Write-Host "   • Write quality, testable code"
    Write-Host ""
    Write-ColorOutput "4. DOCUMENTATION (CONCURRENT)" "Info"
    Write-Host "   • Update docstrings and documentation"
    Write-Host "   • Maintain changelog"
    Write-Host ""
    Write-ColorOutput "5. VERIFICATION" "Info"
    Write-Host "   • Check against quality standards"
    Write-Host "   • Verify workflow compliance"
    Write-Host "   • Run tests and validation"
    Write-Host ""
}

function Show-Documentation {
    Write-ColorOutput "REQUIRED DOCUMENTATION FILES" "Header"
    Write-Host ""
    Write-ColorOutput "Core Documentation:" "Info"
    Write-Host "  • docs/Implementation.md - Overall project plan"
    Write-Host "  • docs/project_structure.md - File organization"
    Write-Host "  • docs/UI_UX_doc.md - Design system"
    Write-Host "  • docs/Bug_tracking.md - Known issues"
    Write-Host "  • docs/ARCHITECTURE.md - System architecture"
    Write-Host ""
    Write-ColorOutput "Context Engineering:" "Info"
    Write-Host "  • docs/AGENT_CONTEXT_ENGINEERING_WORKFLOW.md - Workflow rules"
    Write-Host "  • docs/AGENT_CE_QUICK_REFERENCE.md - Quick reference"
    Write-Host "  • docs/AGENT_CE_ENFORCEMENT.md - Enforcement rules"
    Write-Host "  • docs/AGENT_CE_SYSTEM_PROMPT.md - System prompt template"
    Write-Host ""
}

function Invoke-PythonTool {
    param(
        [string]$Tool,
        [string]$Arguments
    )
    
    try {
        # Check if Python is available
        $pythonPath = Get-Command python -ErrorAction SilentlyContinue
        if (-not $pythonPath) {
            $pythonPath = Get-Command python3 -ErrorAction SilentlyContinue
        }
        
        if (-not $pythonPath) {
            throw "Python is not installed or not in PATH"
        }
        
        # Execute Python tool
        $command = "$($pythonPath.Source) tools/$Tool $Arguments"
        Write-ColorOutput "Executing: $command" "Info"
        
        $result = Invoke-Expression $command
        return $result
        
    } catch {
        Write-ColorOutput "Error executing Python tool: $_" "Error"
        return $null
    }
}

function New-ContextSummary {
    param([string]$TaskDescription)
    
    if (-not $TaskDescription) {
        Write-ColorOutput "Error: Task description is required" "Error"
        return
    }
    
    Write-ColorOutput "Generating context summary for task..." "Info"
    Write-Host "Task: $TaskDescription"
    Write-Host ""
    
    $args = "--project-root ."
    if ($Output) {
        $args += " --output $Output"
    }
    
    $result = Invoke-PythonTool "context_engineering_automation.py" "$TaskDescription $args"
    
    if ($result) {
        Write-ColorOutput "Context summary generated successfully!" "Success"
    } else {
        Write-ColorOutput "Failed to generate context summary" "Error"
    }
}

function New-WorkflowTemplate {
    param([string]$TaskDescription)
    
    if (-not $TaskDescription) {
        Write-ColorOutput "Error: Task description is required" "Error"
        return
    }
    
    Write-ColorOutput "Generating workflow template..." "Info"
    Write-Host "Task: $TaskDescription"
    Write-Host ""
    
    $args = "--template --project-root ."
    if ($Output) {
        $args += " --output $Output"
    }
    
    $result = Invoke-PythonTool "context_engineering_automation.py" "$TaskDescription $args"
    
    if ($result) {
        Write-ColorOutput "Workflow template generated successfully!" "Success"
    } else {
        Write-ColorOutput "Failed to generate workflow template" "Error"
    }
}

function Test-ResponseValidation {
    param([string]$InputFile)
    
    if (-not $InputFile) {
        Write-ColorOutput "Error: Input file is required for validation" "Error"
        return
    }
    
    if (-not (Test-Path $InputFile)) {
        Write-ColorOutput "Error: Input file not found: $InputFile" "Error"
        return
    }
    
    Write-ColorOutput "Validating agent response..." "Info"
    Write-Host "Input file: $InputFile"
    Write-Host ""
    
    $args = "--project-root ."
    if ($Output) {
        $args += " --output $Output"
    }
    
    $result = Invoke-PythonTool "context_engineering_validator.py" "$InputFile $args"
    
    if ($result) {
        Write-ColorOutput "Validation completed successfully!" "Success"
    } else {
        Write-ColorOutput "Validation failed" "Error"
    }
}

# Main execution
try {
    Show-Header
    
    switch ($Action.ToLower()) {
        "summary" {
            New-ContextSummary -TaskDescription $Task
        }
        "template" {
            New-WorkflowTemplate -TaskDescription $Task
        }
        "validate" {
            Test-ResponseValidation -InputFile $Task
        }
        "workflow" {
            Show-Workflow
        }
        "docs" {
            Show-Documentation
        }
        "help" {
            Show-Help
        }
        default {
            Write-ColorOutput "Unknown action: $Action" "Warning"
            Write-Host ""
            Show-Help
        }
    }
    
} catch {
    Write-ColorOutput "Error: $_" "Error"
    Write-Host ""
    Show-Help
    exit 1
}
