import React from "react";
import { MessageCircle, Plus, Trash2 } from "lucide-react";

interface ChatSidebarProps {
  chats: Array<{
    id: string;
    title: string;
    lastMessage?: string;
    updatedAt: string;
  }>;
  currentChatId?: string;
  onSelectChat: (chatId: string) => void;
  onCreateChat: () => void;
  onDeleteChat?: (chatId: string) => void;
}

export default function ChatSidebar({
  chats,
  currentChatId,
  onSelectChat,
  onCreateChat,
  onDeleteChat,
}: ChatSidebarProps) {
  return (
    <div className="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <button
          onClick={onCreateChat}
          className="w-full flex items-center space-x-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg px-3 py-2 transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>New Chat</span>
        </button>
      </div>

      {/* Chat List */}
      <div className="flex-1 overflow-y-auto">
        {chats.length === 0 ? (
          <div className="p-4 text-center text-gray-500 dark:text-gray-400">
            <MessageCircle className="w-8 h-8 mx-auto mb-2 opacity-50" />
            <p className="text-sm">No chats yet</p>
          </div>
        ) : (
          <div className="space-y-1 p-2">
            {chats.map((chat) => (
              <div
                key={chat.id}
                className={`group relative flex items-center space-x-2 p-3 rounded-lg cursor-pointer transition-colors ${
                  currentChatId === chat.id
                    ? "bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800"
                    : "hover:bg-gray-50 dark:hover:bg-gray-700"
                }`}
                onClick={() => onSelectChat(chat.id)}
              >
                <MessageCircle className="w-4 h-4 text-gray-400" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                    {chat.title}
                  </p>
                  {chat.lastMessage && (
                    <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                      {chat.lastMessage}
                    </p>
                  )}
                  <p className="text-xs text-gray-400 dark:text-gray-500">
                    {new Date(chat.updatedAt).toLocaleDateString()}
                  </p>
                </div>
                {onDeleteChat && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteChat(chat.id);
                    }}
                    className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-100 dark:hover:bg-red-900/20 rounded transition-opacity"
                    title="Delete chat"
                  >
                    <Trash2 className="w-3 h-3 text-red-500" />
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
