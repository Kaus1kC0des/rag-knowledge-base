"use client";
import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, ArrowLeft } from "lucide-react";
import { useRouter } from "next/navigation";
import { dummyAPI } from "@/lib/api";

type Message = {
  id: string;
  content: string;
  sender: "user" | "ai";
  timestamp: Date;
};

export default function ChatPage({
  params,
}: {
  params: { slug: string };
}) {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content: "Hello! I'm your AI assistant. How can I help you today?",
      sender: "ai",
      timestamp: new Date(),
    },
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const currentMessage = inputMessage;
    setInputMessage("");
    setIsLoading(true);

    try {
      // Call the dummy API (replace with your actual API when ready)
      const aiResponse = await dummyAPI.sendMessage(currentMessage);
      
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: aiResponse,
        sender: "ai",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error calling AI API:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "Sorry, I encountered an error while processing your request. Please try again.",
        sender: "ai",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] max-w-4xl mx-auto bg-chat">
      {/* Chat Header */}
      <div className="border-b border-default p-4 bg-header">
        <div className="flex items-center space-x-3">
          <button
            onClick={() => router.back()}
            className="p-2 hover-surface rounded-full transition-colors text-secondary"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <h1 className="text-xl font-semibold text-primary">Chat {params.slug}</h1>
            <p className="text-sm text-secondary">AI-powered conversation</p>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-chat">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex items-start space-x-3 ${
              message.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {message.sender === "ai" && (
              <div className="flex-shrink-0 w-8 h-8 bg-accent rounded-full flex items-center justify-center">
                <Bot className="w-5 h-5 text-inverse" />
              </div>
            )}
            
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.sender === "user"
                  ? "bg-accent text-inverse"
                  : "bg-surface text-primary shadow-sm border border-default"
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              <p
                className={`text-xs mt-1 ${
                  message.sender === "user"
                    ? "text-brand-weak"
                    : "text-secondary"
                }`}
              >
                {formatTime(message.timestamp)}
              </p>
            </div>

            {message.sender === "user" && (
              <div className="flex-shrink-0 w-8 h-8 bg-success rounded-full flex items-center justify-center">
                <User className="w-5 h-5 text-inverse" />
              </div>
            )}
          </div>
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-8 h-8 bg-accent rounded-full flex items-center justify-center">
              <Bot className="w-5 h-5 text-inverse" />
            </div>
            <div className="bg-surface text-primary px-4 py-2 rounded-lg shadow-sm border border-default">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-loader-dot rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-loader-dot rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-loader-dot rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-default p-4 bg-header">
        <div className="flex space-x-2">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message here..."
            className="flex-1 resize-none border border-default rounded-lg px-3 py-2 form-input max-h-32"
            rows={1}
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="btn-primary rounded-lg px-4 py-2 transition-colors flex items-center justify-center"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
        <div className="text-xs text-secondary mt-2">
          Press Enter to send, Shift+Enter for new line
        </div>
      </div>
    </div>
  );
}