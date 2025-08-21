import { SignedIn, SignedOut, UserButton } from '@clerk/nextjs'
import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen font-sans bg-gray-50 dark:bg-zinc-900 transition-colors">
      {/* Header with authentication */}
      <header className="w-full px-4 py-4">
        <nav className="max-w-3xl mx-auto flex justify-between items-center">
          <h2 className="text-xl font-bold text-blue-700 dark:text-blue-400">
            RAG Knowledge Base
          </h2>
          <div className="flex items-center gap-4">
            <SignedOut>
              <Link 
                href="/sign-in"
                className="text-blue-600 hover:text-blue-700 font-medium"
              >
                Sign In
              </Link>
              <Link 
                href="/sign-up"
                className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-lg transition"
              >
                Sign Up
              </Link>
            </SignedOut>
            <SignedIn>
              <UserButton afterSignOutUrl="/" />
            </SignedIn>
          </div>
        </nav>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-24 flex flex-col items-center justify-center">
        <h1 className="text-4xl font-bold text-blue-700 dark:text-blue-400 mb-4 text-center">
          RAG Knowledge Base
        </h1>
        <p className="text-lg text-gray-700 dark:text-gray-300 mb-8 text-center">
          Unlock the power of Retrieval-Augmented Generation (RAG) for your
          documents, notes, and chats.
          <br />
          Search, chat, and organize your knowledge with AI assistance.
        </p>
        
        {/* Different content based on auth state */}
        <SignedOut>
          <div className="flex flex-col sm:flex-row gap-4">
            <Link
              href="/sign-up"
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg shadow transition text-center"
            >
              Get Started
            </Link>
            <Link
              href="/sign-in"
              className="bg-white dark:bg-zinc-800 border border-blue-600 dark:border-blue-400 text-blue-700 dark:text-blue-400 font-semibold px-6 py-3 rounded-lg shadow transition text-center"
            >
              Sign In
            </Link>
          </div>
        </SignedOut>

        <SignedIn>
          <div className="flex flex-col sm:flex-row gap-4">
            <Link
              href="/chat"
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg shadow transition text-center"
            >
              Start Chatting
            </Link>
            <Link
              href="/profile"
              className="bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-3 rounded-lg shadow transition text-center"
            >
              View Profile Data
            </Link>
            <Link
              href="/dashboard"
              className="bg-white dark:bg-zinc-800 border border-blue-600 dark:border-blue-400 text-blue-700 dark:text-blue-400 font-semibold px-6 py-3 rounded-lg shadow transition text-center"
            >
              Dashboard
            </Link>
          </div>
        </SignedIn>

        <div className="mt-12 text-center text-gray-500 dark:text-gray-400 text-sm">
          <span>✨ Secure. Fast. Powered by AI. ✨</span>
        </div>
      </main>
    </div>
  );
}
