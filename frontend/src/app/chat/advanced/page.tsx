"use client";
import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Menu, X, Trash2, Edit3, ChevronDown, BookOpen, Calculator, Atom, Cpu, Lightbulb, ArrowLeft } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";
import { dummyAPI } from "@/lib/api";

type Message = {
  id: string;
  content: string;
  sender: "user" | "ai";
  timestamp: Date;
};

type Chat = {
  id: string;
  title: string;
  messages: Message[];
  updatedAt: Date;
  subject?: string;
  unit?: string;
};

type Subject = {
  id: string;
  name: string;
  icon: React.ReactNode;
  color: string;
  units: string[];
};

const subjects: Subject[] = [
  {
    id: "mathematics",
    name: "Mathematics",
    icon: <Calculator className="w-5 h-5" />,
    color: "blue",
    units: ["Unit 1: Differential Calculus", "Unit 2: Integral Calculus", "Unit 3: Linear Algebra", "Unit 4: Probability", "Unit 5: Statistics"]
  },
  {
    id: "physics",
    name: "Physics",
    icon: <Atom className="w-5 h-5" />,
    color: "purple",
    units: ["Unit 1: Classical Mechanics", "Unit 2: Thermodynamics", "Unit 3: Electromagnetism", "Unit 4: Optics", "Unit 5: Modern Physics"]
  },
  {
    id: "computer-science",
    name: "Computer Science",
    icon: <Cpu className="w-5 h-5" />,
    color: "green",
    units: ["Unit 1: Programming Fundamentals", "Unit 2: Data Structures", "Unit 3: Algorithms", "Unit 4: Database Systems", "Unit 5: Software Engineering"]
  },
  {
    id: "engineering",
    name: "Engineering",
    icon: <Lightbulb className="w-5 h-5" />,
    color: "orange",
    units: ["Unit 1: Circuit Analysis", "Unit 2: Control Systems", "Unit 3: Signal Processing", "Unit 4: Power Systems", "Unit 5: Communication Systems"]
  },
  {
    id: "general-studies",
    name: "General Studies",
    icon: <BookOpen className="w-5 h-5" />,
    color: "indigo",
    units: ["Unit 1: Literature", "Unit 2: History", "Unit 3: Philosophy", "Unit 4: Economics", "Unit 5: Political Science"]
  }
];

export default function AdvancedChatPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  // Get subject and unit from URL params
  const urlSubject = searchParams.get('subject');
  const urlName = searchParams.get('name');
  const urlUnit = searchParams.get('unit');
  
  const currentSubject = subjects.find(s => s.id === urlSubject) || subjects[0];
  
  const [chats, setChats] = useState<Chat[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string>("");
  const [selectedSubject, setSelectedSubject] = useState<string>(currentSubject.id);
  const [selectedUnit, setSelectedUnit] = useState<string>(urlUnit || currentSubject.units[0]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [editingChatId, setEditingChatId] = useState<string | null>(null);
  const [editingTitle, setEditingTitle] = useState("");
  const [unitDropdownOpen, setUnitDropdownOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize chats for the current subject
  useEffect(() => {
    if (selectedSubject && selectedUnit) {
      const subjectData = subjects.find(s => s.id === selectedSubject);
      if (subjectData) {
        const initialChat: Chat = {
          id: `${selectedSubject}-chat-1`,
          title: `${subjectData.name} - Getting Started`,
          messages: [
            {
              id: `msg-${Date.now()}`,
              content: `Hello! I'm your AI assistant for ${subjectData.name}. I can help you with any questions or topics related to ${selectedUnit}. What would you like to learn about today?`,
              sender: "ai",
              timestamp: new Date(),
            },
          ],
          updatedAt: new Date(),
          subject: selectedSubject,
          unit: selectedUnit,
        };

        setChats([initialChat]);
        setCurrentChatId(initialChat.id);
      }
    }
  }, [selectedSubject, selectedUnit]);

  const currentChat = chats.find(chat => chat.id === currentChatId);
  const activeSubject = subjects.find(s => s.id === selectedSubject) || subjects[0];

  // Filter chats by current subject only
  const subjectChats = chats.filter(chat => chat.subject === selectedSubject);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [currentChat?.messages]);

  // Enhanced API call with subject and unit context
  const sendMessageWithContext = async (message: string, subject: string, unit: string): Promise<string> => {
    try {
      // This is where you'll integrate with your backend
      // For now, using dummy API with enhanced context
      
      // You can replace this with your actual API call:
      // const response = await chatAPI.sendMessage(message, currentChatId, { subject, unit });
      
      const response = await dummyAPI.sendMessage(message, { subject, unit });
      return response;
    } catch (error) {
      throw error;
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading || !currentChat) return;

    const userMessage: Message = {
      id: `msg-${Date.now()}`,
      content: inputMessage,
      sender: "user",
      timestamp: new Date(),
    };

    // Update current chat with user message
    setChats(prev => prev.map(chat => 
      chat.id === currentChatId 
        ? { ...chat, messages: [...chat.messages, userMessage], updatedAt: new Date(), subject: selectedSubject, unit: selectedUnit }
        : chat
    ));

    const currentMessage = inputMessage;
    setInputMessage("");
    setIsLoading(true);

    try {
      const aiResponse = await sendMessageWithContext(currentMessage, selectedSubject, selectedUnit);
      
      const aiMessage: Message = {
        id: `msg-${Date.now() + 1}`,
        content: aiResponse,
        sender: "ai",
        timestamp: new Date(),
      };

      // Update current chat with AI response
      setChats(prev => prev.map(chat => 
        chat.id === currentChatId 
          ? { ...chat, messages: [...chat.messages, aiMessage], updatedAt: new Date() }
          : chat
      ));
    } catch (error) {
      console.error("Error calling AI API:", error);
      const errorMessage: Message = {
        id: `msg-${Date.now() + 1}`,
        content: "Sorry, I encountered an error while processing your request. Please try again.",
        sender: "ai",
        timestamp: new Date(),
      };
      
      setChats(prev => prev.map(chat => 
        chat.id === currentChatId 
          ? { ...chat, messages: [...chat.messages, errorMessage], updatedAt: new Date() }
          : chat
      ));
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateChat = () => {
    const newChatNumber = subjectChats.length + 1;
    const newChat: Chat = {
      id: `${selectedSubject}-chat-${Date.now()}`,
      title: `${activeSubject.name} - Discussion ${newChatNumber}`,
      messages: [
        {
          id: `msg-${Date.now()}`,
          content: `Hello! I'm ready to help you with ${activeSubject.name}. What would you like to explore in ${selectedUnit}?`,
          sender: "ai",
          timestamp: new Date(),
        },
      ],
      updatedAt: new Date(),
      subject: selectedSubject,
      unit: selectedUnit,
    };

    setChats(prev => [newChat, ...prev]);
    setCurrentChatId(newChat.id);
  };

  const handleSubjectChange = (subjectId: string) => {
    setSelectedSubject(subjectId);
    const newSubject = subjects.find(s => s.id === subjectId);
    if (newSubject) {
      setSelectedUnit(newSubject.units[0]);
      
      // Create initial chat for the new subject if none exists
      const existingSubjectChats = chats.filter(chat => chat.subject === subjectId);
      if (existingSubjectChats.length === 0) {
        const initialChat: Chat = {
          id: `${subjectId}-chat-${Date.now()}`,
          title: `${newSubject.name} - Getting Started`,
          messages: [
            {
              id: `msg-${Date.now()}`,
              content: `Hello! I'm your AI assistant for ${newSubject.name}. I can help you with any questions or topics related to ${newSubject.units[0]}. What would you like to learn about today?`,
              sender: "ai",
              timestamp: new Date(),
            },
          ],
          updatedAt: new Date(),
          subject: subjectId,
          unit: newSubject.units[0],
        };
        
        setChats(prev => [initialChat, ...prev]);
        setCurrentChatId(initialChat.id);
      } else {
        // Switch to the most recent chat in this subject
        setCurrentChatId(existingSubjectChats[0].id);
      }
    }
  };

  const handleDeleteChat = (chatId: string) => {
    const subjectSpecificChats = chats.filter(chat => chat.subject === selectedSubject);
    if (subjectSpecificChats.length <= 1) return; // Keep at least one chat per subject

    setChats(prev => prev.filter(chat => chat.id !== chatId));
    
    if (currentChatId === chatId) {
      const remainingSubjectChats = subjectSpecificChats.filter(chat => chat.id !== chatId);
      setCurrentChatId(remainingSubjectChats[0]?.id || "");
    }
  };

  const handleEditChatTitle = (chatId: string, newTitle: string) => {
    setChats(prev => prev.map(chat => 
      chat.id === chatId ? { ...chat, title: newTitle } : chat
    ));
    setEditingChatId(null);
    setEditingTitle("");
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
    <div className="flex h-[calc(100vh-80px)] bg-black">
      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-80' : 'w-0'} transition-all duration-300 overflow-hidden`}>
        <div className="w-80 bg-gray-900 border-r border-gray-800 flex flex-col h-full">
          {/* Subject Selector */}
          <div className="p-4 border-b border-gray-800">
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Subject
              </label>
              <select
                value={selectedSubject}
                onChange={(e) => handleSubjectChange(e.target.value)}
                className="w-full p-2 border border-gray-700 rounded-lg bg-gray-800 text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                {subjects.map((subject) => (
                  <option key={subject.id} value={subject.id}>
                    {subject.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Unit Dropdown */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Unit
              </label>
              <div className="relative">
                <button
                  onClick={() => setUnitDropdownOpen(!unitDropdownOpen)}
                  className="w-full p-2 border border-gray-700 rounded-lg bg-gray-800 text-gray-100 text-left flex items-center justify-between focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <span className="truncate">{selectedUnit}</span>
                  <ChevronDown className={`w-4 h-4 transition-transform ${unitDropdownOpen ? 'rotate-180' : ''}`} />
                </button>
                
                {unitDropdownOpen && (
                  <div className="absolute z-10 w-full mt-1 bg-gray-800 border border-gray-700 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                    {activeSubject.units.map((unit, index) => (
                      <button
                        key={index}
                        onClick={() => {
                          setSelectedUnit(unit);
                          setUnitDropdownOpen(false);
                        }}
                        className="w-full p-2 text-left hover:bg-gray-700 text-gray-100 border-b border-gray-700 last:border-b-0"
                      >
                        {unit}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>

            <button
              onClick={handleCreateChat}
              className="w-full flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-3 py-2 transition-colors"
            >
              <span>+ New Chat</span>
            </button>
          </div>

          {/* Chat List */}
          <div className="flex-1 overflow-y-auto">
            <div className="p-2 space-y-1">
              {subjectChats.length === 0 ? (
                <div className="p-4 text-center text-gray-400">
                  <div className="text-sm">No chats for {activeSubject.name}</div>
                  <div className="text-xs mt-1">Create your first chat!</div>
                </div>
              ) : (
                subjectChats.map((chat) => (
                  <div
                    key={chat.id}
                    className={`group relative p-3 rounded-lg cursor-pointer transition-colors ${
                      currentChatId === chat.id
                        ? "bg-blue-900/30 border border-blue-700"
                        : "hover:bg-gray-800"
                    }`}
                    onClick={() => setCurrentChatId(chat.id)}
                  >
                    <div className="flex items-center justify-between">
                      {editingChatId === chat.id ? (
                        <input
                          type="text"
                          value={editingTitle}
                          onChange={(e) => setEditingTitle(e.target.value)}
                          onBlur={() => handleEditChatTitle(chat.id, editingTitle)}
                          onKeyPress={(e) => {
                            if (e.key === "Enter") {
                              handleEditChatTitle(chat.id, editingTitle);
                            }
                          }}
                          className="flex-1 text-sm font-medium bg-gray-800 border border-blue-600 rounded px-2 py-1 focus:outline-none focus:border-blue-500 text-gray-100"
                          autoFocus
                        />
                      ) : (
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-100 truncate">
                            {chat.title}
                          </p>
                          <p className="text-xs text-gray-400 truncate">
                            {chat.messages[chat.messages.length - 1]?.content || "No messages"}
                          </p>
                          <p className="text-xs text-gray-500">
                            {formatTime(chat.updatedAt)}
                          </p>
                          {chat.unit && (
                            <p className="text-xs text-blue-600 dark:text-blue-400 truncate mt-1">
                              {chat.unit}
                            </p>
                          )}
                        </div>
                      )}
                      
                      <div className="opacity-0 group-hover:opacity-100 flex space-x-1">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setEditingChatId(chat.id);
                            setEditingTitle(chat.title);
                          }}
                          className="p-1 hover:bg-gray-700 rounded transition-colors"
                          title="Edit title"
                        >
                          <Edit3 className="w-3 h-3 text-gray-400" />
                        </button>
                        {subjectChats.length > 1 && (
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDeleteChat(chat.id);
                            }}
                            className="p-1 hover:bg-red-900/20 rounded transition-colors"
                            title="Delete chat"
                          >
                            <Trash2 className="w-3 h-3 text-red-400" />
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="bg-gray-900 border-b border-gray-800 p-4">
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-gray-800 rounded-lg transition-colors text-gray-300"
            >
              {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
            <button
              onClick={() => router.push('/chat')}
              className="p-2 hover:bg-gray-800 rounded-lg transition-colors text-gray-300"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div className="flex items-center space-x-2">
              {activeSubject.icon}
              <div>
                <h1 className="text-xl font-semibold text-gray-100">
                  {activeSubject.name}
                </h1>
                <p className="text-sm text-gray-400">{selectedUnit}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-black">
          {currentChat?.messages.map((message) => (
            <div
              key={message.id}
              className={`flex items-start space-x-3 ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              {message.sender === "ai" && (
                <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                  <Bot className="w-5 h-5 text-white" />
                </div>
              )}
              
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.sender === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-800 text-gray-100 shadow-sm border border-gray-700"
                }`}
              >
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                <p
                  className={`text-xs mt-1 ${
                    message.sender === "user"
                      ? "text-blue-200"
                      : "text-gray-400"
                  }`}
                >
                  {formatTime(message.timestamp)}
                </p>
              </div>

              {message.sender === "user" && (
                <div className="flex-shrink-0 w-8 h-8 bg-green-600 rounded-full flex items-center justify-center">
                  <User className="w-5 h-5 text-white" />
                </div>
              )}
            </div>
          ))}

          {/* Loading indicator */}
          {isLoading && (
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className="bg-gray-800 text-gray-100 px-4 py-2 rounded-lg shadow-sm border border-gray-700">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-gray-900 border-t border-gray-800 p-4">
          <div className="mb-2">
            <div className="flex items-center space-x-2 text-xs text-gray-400">
              <span>📚 {activeSubject.name}</span>
              <span>•</span>
              <span>📖 {selectedUnit}</span>
            </div>
          </div>
          <div className="flex space-x-2">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={`Ask me anything about ${activeSubject.name}...`}
              className="flex-1 resize-none border border-gray-700 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-gray-800 text-white max-h-32"
              rows={1}
              disabled={isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg px-4 py-2 transition-colors flex items-center justify-center"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          <div className="text-xs text-gray-400 mt-2">
            Press Enter to send, Shift+Enter for new line
          </div>
        </div>
      </div>
    </div>
  );
}
