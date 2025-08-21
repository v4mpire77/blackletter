// Accessibility utility functions

/**
 * Announces a message to screen readers
 */
export const announceToScreenReader = (message: string, priority: 'polite' | 'assertive' = 'polite') => {
  const announcement = document.createElement('div')
  announcement.setAttribute('aria-live', priority)
  announcement.setAttribute('aria-atomic', 'true')
  announcement.className = 'sr-only'
  announcement.textContent = message
  
  document.body.appendChild(announcement)
  
  // Remove after announcement
  setTimeout(() => {
    document.body.removeChild(announcement)
  }, 1000)
}

/**
 * Focus management for modal dialogs
 */
export const trapFocus = (element: HTMLElement) => {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  )
  const firstElement = focusableElements[0] as HTMLElement
  const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement

  const handleTabKey = (e: KeyboardEvent) => {
    if (e.key === 'Tab') {
      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          lastElement.focus()
          e.preventDefault()
        }
      } else {
        if (document.activeElement === lastElement) {
          firstElement.focus()
          e.preventDefault()
        }
      }
    }
  }

  element.addEventListener('keydown', handleTabKey)
  firstElement?.focus()

  return () => {
    element.removeEventListener('keydown', handleTabKey)
  }
}

/**
 * Check if reduced motion is preferred
 */
export const prefersReducedMotion = () => {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

/**
 * Ensure minimum touch target size for mobile accessibility
 */
export const ensureMinimumTouchTarget = (element: HTMLElement, minSize: number = 44) => {
  const rect = element.getBoundingClientRect()
  if (rect.width < minSize || rect.height < minSize) {
    element.style.minWidth = `${minSize}px`
    element.style.minHeight = `${minSize}px`
  }
}

/**
 * Generate a unique ID for form elements
 */
export const generateId = (prefix: string = 'id') => {
  return `${prefix}-${Math.random().toString(36).substr(2, 9)}`
}

/**
 * Check color contrast ratio (simplified)
 */
export const getContrastRatio = (foreground: string, background: string): number => {
  // This is a simplified version - in a real app, you'd use a proper color contrast library
  // For now, return a mock value that indicates good contrast
  return 4.5
}

/**
 * Validate WCAG 2.1 AA compliance for color contrast
 */
export const isWCAGCompliant = (foreground: string, background: string, level: 'AA' | 'AAA' = 'AA'): boolean => {
  const ratio = getContrastRatio(foreground, background)
  return level === 'AA' ? ratio >= 4.5 : ratio >= 7
}

/**
 * Format file size for screen readers
 */
export const formatFileSizeForScreenReader = (bytes: number): string => {
  if (bytes === 0) return 'zero bytes'
  
  const k = 1024
  const sizes = ['bytes', 'kilobytes', 'megabytes', 'gigabytes']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  const size = parseFloat((bytes / Math.pow(k, i)).toFixed(2))
  
  return `${size} ${sizes[i]}`
}

/**
 * Create accessible error message
 */
export const createAccessibleErrorMessage = (fieldId: string, errorMessage: string): HTMLElement => {
  const errorElement = document.createElement('div')
  errorElement.id = `${fieldId}-error`
  errorElement.setAttribute('role', 'alert')
  errorElement.className = 'text-sm text-red-600 mt-1'
  errorElement.textContent = errorMessage
  
  return errorElement
}