"use client";
import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Menu, X, Trash2, Edit3, ChevronDown, BookOpen, Sparkles, Cpu, MessageSquare, Mic, Image, ArrowLeft } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";
import { dummyAPI, chatAPI, sessionAPI, type ChatSession } from "@/lib/api";
import { useAuth } from "@clerk/nextjs";
import Markdown from "@/components/Markdown";

type Message = {
  id: string;
  content: string;
  sender: "user" | "ai";
  timestamp: Date;
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
    id: "Generative AI",
    name: "Generative AI",
    icon: <Sparkles className="w-5 h-5" />,
    color: "blue",
    units: ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5"]
  },
  {
    id: "Edge AI",
    name: "Edge AI",
    icon: <Cpu className="w-5 h-5" />,
    color: "green",
    units: ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5"]
  },
  {
    id: "Statistical Natural Language Processing",
    name: "Statistical Natural Language Processing",
    icon: <MessageSquare className="w-5 h-5" />,
    color: "purple",
    units: ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5"]
  },
  {
    id: "Speech Processing",
    name: "Speech Processing",
    icon: <Mic className="w-5 h-5" />,
    color: "orange",
    units: ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5"]
  },
  {
    id: "Image Processing and Vision Techniques",
    name: "Image Processing and Vision Techniques",
    icon: <Image className="w-5 h-5" />,
    color: "indigo",
    units: ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5"]
  }
];

export default function AdvancedChatPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { getToken } = useAuth();

  // Get subject and unit from URL params
  const urlSubject = searchParams.get('subject');
  const urlName = searchParams.get('name');
  const urlUnit = searchParams.get('unit');
  
  const currentSubject = subjects.find(s => s.id === urlSubject) || subjects[0];
  
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<number | null>(null);
  const [selectedSubject, setSelectedSubject] = useState<string>(currentSubject.id);
  const [selectedUnit, setSelectedUnit] = useState<string>(urlUnit || currentSubject.units[0]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [loadingSessions, setLoadingSessions] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [editingSessionId, setEditingSessionId] = useState<number | null>(null);
  const [editingTitle, setEditingTitle] = useState("");
  const [unitDropdownOpen, setUnitDropdownOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const currentSession = sessions.find(session => session.id === currentSessionId);
  const activeSubject = subjects.find(s => s.id === selectedSubject) || subjects[0];

  // Convert API messages to frontend Message format
  const convertToMessages = (session: ChatSession): Message[] => {
    if (!session.messages) return [];
    
    const messages: Message[] = [];
    session.messages.forEach((msg, index) => {
      // Add user message
      messages.push({
        id: `user-${session.id}-${index}`,
        content: msg.query,
        sender: "user",
        timestamp: new Date()
      });
      
      // Add AI response
      messages.push({
        id: `ai-${session.id}-${index}`,
        content: msg.response,
        sender: "ai",
        timestamp: new Date()
      });
    });
    
    return messages;
  };

  // Get auth headers
  const getAuthHeaders = async (): Promise<HeadersInit> => {
    const token = await getToken({ template: "user-auth-token-template" });
    return token ? { Authorization: `Bearer ${token}` } : {};
  };

  // Load sessions for current subject and unit
  const loadSessions = async () => {
    if (!selectedSubject || !selectedUnit) return;
    
    setLoadingSessions(true);
    try {
      const headers = await getAuthHeaders();
      const sessionList = await sessionAPI.getAllSessions(selectedSubject, selectedUnit, headers);
      setSessions(sessionList);
      
      // If no current session is selected, select the first one or create a new one
      if (sessionList.length > 0 && !currentSessionId) {
        setCurrentSessionId(sessionList[0].id);
      } else if (sessionList.length === 0) {
        await handleCreateSession();
      }
    } catch (error) {
      console.error("Error loading sessions:", error);
      // If no sessions exist, create one
      await handleCreateSession();
    } finally {
      setLoadingSessions(false);
    }
  };

  // Create a new session
  const handleCreateSession = async () => {
    try {
      const headers = await getAuthHeaders();
      const newSession = await sessionAPI.createSession(
        selectedSubject,
        selectedUnit,
        `${activeSubject.name} - ${selectedUnit}`,
        headers
      );
      
      setSessions(prev => [newSession, ...prev]);
      setCurrentSessionId(newSession.id);
    } catch (error) {
      console.error("Error creating session:", error);
    }
  };

  // Delete a session
  const handleDeleteSession = async (sessionId: number) => {
    if (sessions.length <= 1) return; // Keep at least one session
    
    try {
      const headers = await getAuthHeaders();
      await sessionAPI.deleteSession(sessionId, headers);
      
      setSessions(prev => prev.filter(session => session.id !== sessionId));
      
      if (currentSessionId === sessionId) {
        const remainingSessions = sessions.filter(session => session.id !== sessionId);
        setCurrentSessionId(remainingSessions[0]?.id || null);
      }
    } catch (error) {
      console.error("Error deleting session:", error);
    }
  };

  // Load sessions when subject or unit changes
  useEffect(() => {
    loadSessions();
  }, [selectedSubject, selectedUnit]);

  // Scroll to bottom when messages change
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [currentSession]);

  // Enhanced API call with subject and unit context
  const sendMessageWithContext = async (message: string, subject: string, unit: string): Promise<string> => {
    try {
      const headers = await getAuthHeaders();
      const response = await chatAPI.sendMessage(
        message,
        currentSessionId?.toString(),
        { subject, unit },
        headers
      );
      return response;
    } catch (error) {
      throw error;
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading || !currentSession) return;
    
    const currentMessage = inputMessage;
    setInputMessage("");
    setIsLoading(true);

    try {
      const aiResponse = await sendMessageWithContext(currentMessage, selectedSubject, selectedUnit);
      
      // Reload the current session to get updated messages
      const headers = await getAuthHeaders();
      const updatedSession = await sessionAPI.getSession(currentSessionId!, headers);
      
      // Update sessions with the new data
      setSessions(prev => prev.map(session => 
        session.id === currentSessionId ? updatedSession : session
      ));
      
    } catch (error) {
      console.error("Error calling AI API:", error);
      // You could show an error message to the user here
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubjectChange = async (subjectId: string) => {
    setSelectedSubject(subjectId);
    const newSubject = subjects.find(s => s.id === subjectId);
    if (newSubject) {
      setSelectedUnit(newSubject.units[0]);
      setCurrentSessionId(null);
      setSessions([]);
    }
  };

  const handleUnitChange = async (unit: string) => {
    setSelectedUnit(unit);
    setCurrentSessionId(null);
    setSessions([]);
    setUnitDropdownOpen(false);
  };

  const handleEditSessionTitle = async (sessionId: number, newTitle: string) => {
    // For now, just update locally. You could add an API endpoint to update session title
    setSessions(prev => prev.map(session => 
      session.id === sessionId ? { ...session, title: newTitle } : session
    ));
    setEditingSessionId(null);
    setEditingTitle("");
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatTime = (dateString?: string) => {
    if (!dateString) return "";
    return new Date(dateString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const currentMessages = currentSession ? convertToMessages(currentSession) : [];

  return (
    <div className="flex h-[calc(100vh-65px)] bg-chat">
      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-80' : 'w-0'} transition-all duration-300 overflow-hidden`}>
        <div className="w-80 bg-header border-r border-default flex flex-col h-full">
          {/* Subject Selector */}
          <div className="p-4 border-b border-default">
            <div className="mb-4">
              <label className="block text-sm font-medium text-secondary mb-2">
                Subject
              </label>
              <select
                value={selectedSubject}
                onChange={(e) => handleSubjectChange(e.target.value)}
                className="w-full p-2 border border-default rounded-lg form-input"
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
              <label className="block text-sm font-medium text-secondary mb-2">
                Unit
              </label>
              <div className="relative">
                <button
                  onClick={() => setUnitDropdownOpen(!unitDropdownOpen)}
                  className="w-full p-2 border border-default rounded-lg form-input text-left flex items-center justify-between"
                >
                  <span className="truncate">{selectedUnit}</span>
                  <ChevronDown className={`w-4 h-4 transition-transform ${unitDropdownOpen ? 'rotate-180' : ''}`} />
                </button>
                
                {unitDropdownOpen && (
                  <div className="absolute z-10 w-full mt-1 bg-surface border border-default rounded-lg shadow-lg max-h-60 overflow-y-auto">
                    {activeSubject.units.map((unit, index) => (
                      <button
                        key={index}
                        onClick={() => handleUnitChange(unit)}
                        className="w-full p-2 text-left hover-surface text-primary border-b border-default last:border-b-0"
                      >
                        {unit}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>

            <button
              onClick={handleCreateSession}
              className="w-full flex items-center justify-center space-x-2 btn-primary rounded-lg px-3 py-2 transition-colors"
              disabled={loadingSessions}
            >
              <span>{loadingSessions ? "Loading..." : "+ New Session"}</span>
            </button>
          </div>

          {/* Sessions List */}
          <div className="flex-1 overflow-y-auto">
            <div className="p-2 space-y-1">
              {loadingSessions ? (
                <div className="p-4 text-center text-secondary">
                  <div className="text-sm">Loading sessions...</div>
                </div>
              ) : sessions.length === 0 ? (
                <div className="p-4 text-center text-secondary">
                  <div className="text-sm">No sessions for {activeSubject.name}</div>
                  <div className="text-xs mt-1">Create your first session!</div>
                </div>
              ) : (
                sessions.map((session) => (
                  <div
                    key={session.id}
                    className={`group relative p-3 rounded-lg cursor-pointer transition-colors ${
                      currentSessionId === session.id
                        ? "item-active border"
                        : "hover-surface"
                    }`}
                    onClick={() => setCurrentSessionId(session.id)}
                  >
                    <div className="flex items-center justify-between">
                      {editingSessionId === session.id ? (
                        <input
                          type="text"
                          value={editingTitle}
                          onChange={(e) => setEditingTitle(e.target.value)}
                          onBlur={() => handleEditSessionTitle(session.id, editingTitle)}
                          onKeyPress={(e) => {
                            if (e.key === "Enter") {
                              handleEditSessionTitle(session.id, editingTitle);
                            }
                          }}
                          className="flex-1 text-sm font-medium form-input rounded px-2 py-1"
                          autoFocus
                        />
                      ) : (
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-primary truncate">
                            {session.title || `Session ${session.id}`}
                          </p>
                          <p className="text-xs text-secondary truncate">
                            {session.messages && session.messages.length > 0 
                              ? session.messages[session.messages.length - 1]?.query 
                              : "No messages"}
                          </p>
                          {session.last_updated && (
                            <p className="text-xs text-low">
                              {formatTime(session.last_updated)}
                            </p>
                          )}
                          <p className="text-xs text-brand-weak truncate mt-1">
                            {session.unit_id}
                          </p>
                        </div>
                      )}
                      
                      <div className="opacity-0 group-hover:opacity-100 flex space-x-1">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setEditingSessionId(session.id);
                            setEditingTitle(session.title || `Session ${session.id}`);
                          }}
                          className="p-1 hover-surface rounded transition-colors"
                          title="Edit title"
                        >
                          <Edit3 className="w-3 h-3 text-secondary" />
                        </button>
                        {sessions.length > 1 && (
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDeleteSession(session.id);
                            }}
                            className="p-1 hover-danger rounded transition-colors"
                            title="Delete session"
                          >
                            <Trash2 className="w-3 h-3 text-danger" />
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
        <div className="bg-header border-b border-default p-4">
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover-surface rounded-lg transition-colors text-secondary"
            >
              {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
            <button
              onClick={() => router.push('/chat')}
              className="p-2 hover-surface rounded-lg transition-colors text-secondary"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div className="flex items-center space-x-2">
              {activeSubject.icon}
              <div>
                <h1 className="text-xl font-semibold text-primary">
                  {activeSubject.name}
                </h1>
                <p className="text-sm text-secondary">{selectedUnit}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-chat">
          {currentMessages.length === 0 ? (
            <div className="flex-1 flex items-center justify-center">
              <div className="text-center">
                <Bot className="w-12 h-12 text-secondary mx-auto mb-4" />
                <h3 className="text-lg font-medium text-primary mb-2">
                  Welcome to {activeSubject.name}
                </h3>
                <p className="text-secondary">
                  Ask me anything about {selectedUnit}. I'm here to help you learn!
                </p>
              </div>
            </div>
          ) : (
            currentMessages.map((message) => (
              <div
                key={message.id}
                className={`flex items-start space-x-3 ${
                  message.sender === "user" ? "justify-end" : "justify-start"
                }`}
              > 
                {message.sender === "ai" && (
                  <div className="flex-shrink-0">
                    <Bot className="w-8 h-8 p-1 bg-surface border border-default rounded-full text-secondary" />
                  </div>
                )}
                
                <div
                  className={`px-4 py-2 rounded-lg ${
                    message.sender === "user"
                      ? "bg-accent text-inverse max-w-xs lg:max-w-md"
                      : "bg-surface border border-default max-w-3xl"
                  }`}
                >
                  <Markdown>
                    {message.content}
                  </Markdown>
                  <p
                    className={`text-xs mt-1 ${
                      message.sender === "user"
                        ? "text-brand-weak"
                        : "text-secondary"
                    }`}
                  >
                    {formatTime(new Date().toISOString())}
                  </p>
                </div>

                {message.sender === "user" && (
                  <div className="flex-shrink-0">
                    <User className="w-8 h-8 p-1 bg-accent text-inverse rounded-full" />
                  </div>
                )}
              </div>
            ))
          )}
          
          {isLoading && (
            <div className="flex items-start space-x-3 justify-start">
              <div className="flex-shrink-0">
                <Bot className="w-8 h-8 p-1 bg-surface border border-default rounded-full text-secondary animate-pulse" />
              </div>
              <div className="px-4 py-2 rounded-lg bg-surface border border-default">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-secondary rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-secondary rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-secondary rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-header border-t border-default p-4">
          <div className="flex space-x-3">
            <div className="flex-1">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={`Ask about ${selectedUnit}...`}
                className="w-full form-input rounded-lg resize-none"
                rows={1}
                disabled={isLoading || !currentSession}
              />
            </div>
            <button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading || !currentSession}
              className="btn-primary p-3 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
