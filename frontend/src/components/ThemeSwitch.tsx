"use client"

import * as React from "react"
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"

export function ModeToggle() {
  const { resolvedTheme,setTheme } = useTheme()

  return (
    <div>
      <input type="checkbox" id="theme-toggle" className="hidden" />
      <label
        htmlFor="theme-toggle"
        className="cursor-pointer"
        onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")}
      >
        {resolvedTheme === "dark" ? (
          <Sun className="w-6 h-6 text-yellow-500" />
        ) : (
          <Moon className="w-6 h-6 text-gray-800" />
        )}
      </label>
    </div>
  )
}
