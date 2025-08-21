import * as React from "react"
import { cn } from "@/lib/utils"

export interface SkeletonLoaderProps {
  className?: string
  variant?: 'text' | 'circular' | 'rectangular' | 'card'
  lines?: number
  height?: string | number
  width?: string | number
  animated?: boolean
}

const SkeletonLoader = React.forwardRef<HTMLDivElement, SkeletonLoaderProps>(
  ({ 
    className, 
    variant = 'rectangular',
    lines = 1,
    height,
    width,
    animated = true,
    ...props 
  }, ref) => {
    const baseClasses = cn(
      "bg-muted rounded",
      animated && "animate-pulse",
      className
    )

    if (variant === 'text') {
      return (
        <div className="space-y-2" ref={ref} {...props}>
          {Array.from({ length: lines }, (_, i) => (
            <div
              key={i}
              className={cn(baseClasses, "h-4")}
              style={{ 
                width: i === lines - 1 && lines > 1 ? '75%' : width || '100%',
                height: height || '1rem'
              }}
            />
          ))}
        </div>
      )
    }

    if (variant === 'circular') {
      return (
        <div
          ref={ref}
          className={cn(baseClasses, "rounded-full")}
          style={{ 
            width: width || '3rem',
            height: height || width || '3rem'
          }}
          {...props}
        />
      )
    }

    if (variant === 'card') {
      return (
        <div 
          ref={ref} 
          className={cn("p-4 space-y-3", className)}
          {...props}
        >
          <div className={cn(baseClasses, "h-4 w-3/4")} />
          <div className={cn(baseClasses, "h-3 w-1/2")} />
          <div className="space-y-2">
            <div className={cn(baseClasses, "h-3")} />
            <div className={cn(baseClasses, "h-3 w-5/6")} />
          </div>
        </div>
      )
    }

    // rectangular variant (default)
    return (
      <div
        ref={ref}
        className={baseClasses}
        style={{ 
          width: width || '100%',
          height: height || '4rem'
        }}
        {...props}
      />
    )
  }
)

SkeletonLoader.displayName = "SkeletonLoader"

export { SkeletonLoader }