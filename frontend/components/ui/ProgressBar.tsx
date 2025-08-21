import * as React from "react"
import { cn } from "@/lib/utils"

export interface ProgressBarProps {
  value: number
  max?: number
  className?: string
  variant?: 'default' | 'success' | 'warning' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
  label?: string
  animated?: boolean
}

const variantClasses = {
  default: 'bg-primary-600',
  success: 'bg-risk-low',
  warning: 'bg-risk-medium', 
  danger: 'bg-risk-critical'
}

const sizeClasses = {
  sm: 'h-2',
  md: 'h-3',
  lg: 'h-4'
}

export const ProgressBar = React.forwardRef<HTMLDivElement, ProgressBarProps>(
  ({ 
    value, 
    max = 100, 
    className, 
    variant = 'default',
    size = 'md',
    showLabel = false,
    label,
    animated = false,
    ...props 
  }, ref) => {
    const percentage = Math.min((value / max) * 100, 100)
    
    return (
      <div className={cn("w-full", className)} ref={ref} {...props}>
        {(showLabel || label) && (
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-foreground">
              {label || `${Math.round(percentage)}%`}
            </span>
            {showLabel && (
              <span className="text-sm text-muted-foreground">
                {value}/{max}
              </span>
            )}
          </div>
        )}
        <div 
          className={cn(
            "w-full bg-muted rounded-full overflow-hidden",
            sizeClasses[size]
          )}
          role="progressbar"
          aria-valuenow={value}
          aria-valuemin={0}
          aria-valuemax={max}
          aria-label={label || `Progress: ${percentage}%`}
        >
          <div
            className={cn(
              "h-full transition-all duration-300 ease-out rounded-full",
              variantClasses[variant],
              animated && "animate-pulse-glow"
            )}
            style={{ width: `${percentage}%` }}
          />
        </div>
      </div>
    )
  }
)

ProgressBar.displayName = "ProgressBar"