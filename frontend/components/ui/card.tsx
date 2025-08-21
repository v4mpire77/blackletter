import * as React from 'react';
import { cn } from '@/lib/utils';

// Card Component
export const Card = React.forwardRef<HTMLDivElement, React.HTMLProps<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('shadow-lg rounded-lg', className)} {...props} />
));

// CardHeader Component
export const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLProps<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-4 border-b', className)} {...props} />
));

// CardTitle Component
export const CardTitle = React.forwardRef<HTMLHeadingElement, React.HTMLProps<HTMLHeadingElement>>(({ className, ...props }, ref) => (
  <h2 ref={ref} className={cn('text-lg font-bold', className)} {...props} />
));

// CardDescription Component
export const CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLProps<HTMLParagraphElement>>(({ className, ...props }, ref) => (
  <p ref={ref} className={cn('text-sm text-gray-600', className)} {...props} />
));

// CardContent Component
export const CardContent = React.forwardRef<HTMLDivElement, React.HTMLProps<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-4', className)} {...props} />
));

// CardFooter Component
export const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLProps<HTMLDivElement>>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-4 border-t', className)} {...props} />
));

// Usage Example
/*
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>
    Content goes here.
  </CardContent>
  <CardFooter>
    Footer content.
  </CardFooter>
</Card>
*/
