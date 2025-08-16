import React from "react";
import {
  SignInButton,
  SignUpButton,
  SignedIn,
  SignedOut,
  UserButton,
} from "@clerk/nextjs";

import { ModeToggle } from "@/components/ThemeSwitch";


export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen font-sans">
      {/* You can add a global header, sidebar, or footer here if needed */}
      <header className="sticky top-0 z-10 border-b flex items-center justify-between px-6 py-4 shadow-sm">
        <h1 className="text-2xl font-bold tracking-tight">
          Notepad LLM
        </h1>
        <div className="flex gap-2">
            {/* Add Dark mode toggle */}
            {/* <ModeToggle /> */}
            <SignedOut>
              <SignInButton />
              <SignUpButton>
                <button className="bg-[#6c47ff] text-ceramic-white rounded-full font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 cursor-pointer">
                  Sign Up
                </button>
              </SignUpButton>
            </SignedOut>
            <SignedIn>
              <UserButton />
            </SignedIn>
          
        </div>
      </header>
      {children}
    </div>
  );
}