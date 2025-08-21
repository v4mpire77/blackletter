import { useEffect, useCallback } from 'react'

interface KeyboardShortcuts {
  [key: string]: () => void
}

export function useKeyboardShortcuts(shortcuts: KeyboardShortcuts, enabled: boolean = true) {
  const handleKeyPress = useCallback((event: KeyboardEvent) => {
    if (!enabled) return

    // Don't trigger shortcuts when user is typing in input fields
    const target = event.target as HTMLElement
    if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.contentEditable === 'true') {
      return
    }

    // Build the key combination string
    const keys = []
    if (event.ctrlKey || event.metaKey) keys.push('cmd')
    if (event.shiftKey) keys.push('shift')
    if (event.altKey) keys.push('alt')
    keys.push(event.key.toLowerCase())
    
    const combination = keys.join('+')
    
    // Also check for single key shortcuts
    const handler = shortcuts[combination] || shortcuts[event.key.toLowerCase()]
    
    if (handler) {
      event.preventDefault()
      handler()
    }
  }, [shortcuts, enabled])

  useEffect(() => {
    document.addEventListener('keydown', handleKeyPress)
    return () => document.removeEventListener('keydown', handleKeyPress)
  }, [handleKeyPress])
}

// Common keyboard shortcuts for contract analysis
export const useContractKeyboardShortcuts = (callbacks: {
  onUpload?: () => void
  onExport?: () => void
  onToggleTheme?: () => void
  onHelp?: () => void
  onNext?: () => void
  onPrevious?: () => void
}) => {
  const shortcuts = {
    'cmd+u': callbacks.onUpload || (() => {}),
    'cmd+e': callbacks.onExport || (() => {}),
    'cmd+shift+d': callbacks.onToggleTheme || (() => {}),
    'cmd+/': callbacks.onHelp || (() => {}),
    '?': callbacks.onHelp || (() => {}),
    'arrowright': callbacks.onNext || (() => {}),
    'arrowleft': callbacks.onPrevious || (() => {}),
    'j': callbacks.onNext || (() => {}),
    'k': callbacks.onPrevious || (() => {}),
  }

  useKeyboardShortcuts(shortcuts)
}