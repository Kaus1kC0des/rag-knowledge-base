export default function HomePage() {
  return (
    <div className="min-h-screen font-sans bg-gray-50 dark:bg-zinc-900 transition-colors">
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
        <div className="flex flex-col sm:flex-row gap-4">
          <a
            href="/signup"
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg shadow transition text-center"
          >
            Get Started
          </a>
          <a
            href="/docs"
            className="bg-white dark:bg-zinc-800 border border-blue-600 dark:border-blue-400 text-blue-700 dark:text-blue-400 font-semibold px-6 py-3 rounded-lg shadow transition text-center"
          >
            Learn More
          </a>
        </div>
        <div className="mt-12 text-center text-gray-500 dark:text-gray-400 text-sm">
          <span>✨ Secure. Fast. Powered by AI. ✨</span>
        </div>
      </main>
    </div>
  );
}
