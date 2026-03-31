import * as React from "react"
import { cn } from "@/lib/utils"

interface ProgressProps {
  value: number
  max?: number
  className?: string
  indicatorClassName?: string
}

export function Progress({ value, max = 100, className, indicatorClassName }: ProgressProps) {
  return (
    <div
      className={cn(
        "relative h-2 w-full overflow-hidden rounded-full bg-secondary",
        className
      )}
    >
      <div
        className={cn(
          "h-full w-full flex-1 bg-primary transition-all duration-300 ease-out",
          indicatorClassName
        )}
        style={{ transform: `translateX(-${100 - (value / max) * 100}%)` }}
      />
    </div>
  )
}