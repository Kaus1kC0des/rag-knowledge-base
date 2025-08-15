"use client";
import { useState } from "react";


type Chat = {
  id: number;
  title: string;
  lastMessage: string;
  updatedAt: string;
};

export default function HomePage() {
  const [chats, setChats] = useState<Chat[]>([
    {
      id: 1,
      title: "Personal Notes",
      lastMessage: "Remember to buy milk.",
      updatedAt: "2025-08-14 10:30",
    },
    {
      id: 2,
      title: "Work Ideas",
      lastMessage: "Discuss Q3 roadmap.",
      updatedAt: "2025-08-13 16:20",
    },
    {
      id: 3,
      title: "LLM Experiments",
      lastMessage: "Try new prompt for summarization.",
      updatedAt: "2025-08-12 09:10",
    },
  ]);
  const [filter, setFilter] = useState("");
  const [selectedChatId, setSelectedChatId] = useState<number | null>(null);

  const filteredChats = chats.filter(
    (chat) =>
      chat.title.toLowerCase().includes(filter.toLowerCase()) ||
      chat.lastMessage.toLowerCase().includes(filter.toLowerCase())
  );

  const handleCreateChat = () => {
    const newId = chats.length ? chats[chats.length - 1].id + 1 : 1;
    const newChat: Chat = {
      id: newId,
      title: `New Chat ${newId}`,
      lastMessage: "",
      updatedAt: new Date().toISOString().slice(0, 16).replace("T", " "),
    };
    setChats([newChat, ...chats]);
    setSelectedChatId(newId);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-zinc-900 font-sans">
      {/* Top Bar */}

      {/* Filter/Search and Create Chat Button */}
      <div className="max-w-5xl mx-auto px-4 py-6 flex items-center gap-4">
        <input
          type="text"
          className="flex-1 border border-gray-300 dark:border-zinc-700 rounded-lg px-4 py-2 bg-white dark:bg-zinc-800 dark:text-gray-100 shadow-sm"
          placeholder="Search your notes or chats..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
        <button
          className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 shadow transition"
          onClick={handleCreateChat}
          title="Create Chat"
        >
          + Create Chat
        </button>
      </div>
      {/* Chat Cards Grid */}
      <main className="max-w-5xl mx-auto px-4 pb-24">
        {filteredChats.length === 0 ? (
          <div className="text-gray-500 dark:text-gray-400 text-center mt-16">
            No chats found.
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {filteredChats.map((chat) => (
              <div
                key={chat.id}
                className={`bg-white dark:bg-zinc-800 rounded-xl shadow hover:shadow-lg transition cursor-pointer border border-transparent hover:border-blue-400 dark:hover:border-blue-500 p-5 flex flex-col justify-between min-h-[140px] ${
                  selectedChatId === chat.id
                    ? "border-blue-500 dark:border-blue-400"
                    : ""
                }`}
                onClick={() => setSelectedChatId(chat.id)}
              >
                <div>
                  <div className="font-semibold text-lg text-gray-900 dark:text-gray-100 mb-2">
                    {chat.title}
                  </div>
                  <div className="text-gray-600 dark:text-gray-300 text-sm truncate">
                    {chat.lastMessage || "No messages yet."}
                  </div>
                </div>
                <div className="text-gray-400 dark:text-gray-400 text-xs mt-4 text-right">
                  {chat.updatedAt}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
