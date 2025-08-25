// API utility functions for chat functionality

export interface ChatMessage {
  id: string;
  content: string;
  sender: "user" | "ai";
  timestamp: Date;
}

export interface ApiResponse {
  success: boolean;
  data?: any;
  error?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Generic API call function
async function apiCall(endpoint: string, options: RequestInit = {}): Promise<ApiResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    console.error("API call failed:", error);
    return { 
      success: false, 
      error: error instanceof Error ? error.message : "Unknown error occurred" 
    };
  }
}

// Chat-specific API functions
export const chatAPI = {
  // Send a message to the AI and get a response
  sendMessage: async (message: string, chatId?: string): Promise<string> => {
    const response = await apiCall("/chat/message", {
      method: "POST",
      body: JSON.stringify({ 
        message, 
        chat_id: chatId,
        timestamp: new Date().toISOString()
      }),
    });

    if (response.success && response.data) {
      return response.data.response || response.data.message || "No response received";
    } else {
      throw new Error(response.error || "Failed to get AI response");
    }
  },

  // Get chat history
  getChatHistory: async (chatId: string): Promise<ChatMessage[]> => {
    const response = await apiCall(`/chat/${chatId}/history`);
    
    if (response.success && response.data) {
      return response.data.messages || [];
    } else {
      throw new Error(response.error || "Failed to get chat history");
    }
  },

  // Create a new chat
  createChat: async (title?: string): Promise<{ id: string; title: string }> => {
    const response = await apiCall("/chat", {
      method: "POST",
      body: JSON.stringify({ 
        title: title || `New Chat ${Date.now()}`,
        created_at: new Date().toISOString()
      }),
    });

    if (response.success && response.data) {
      return response.data;
    } else {
      throw new Error(response.error || "Failed to create chat");
    }
  },

  // Get all chats for the user
  getAllChats: async (): Promise<any[]> => {
    const response = await apiCall("/chats");
    
    if (response.success && response.data) {
      return response.data.chats || [];
    } else {
      throw new Error(response.error || "Failed to get chats");
    }
  },
};

// Dummy API functions for development/testing
export const dummyAPI = {
  sendMessage: async (message: string): Promise<string> => {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1000 + Math.random() * 2000));
    
    // Dummy responses based on message content
    const responses = [
      "That's a great question! Based on the information available, I can help you understand this better.",
      "I understand your concern. Let me provide you with a comprehensive analysis of the situation.",
      "Interesting point! Here's what I think about that: This approach has several benefits that we should consider.",
      "Based on my knowledge, here are some key insights that might be helpful to you.",
      "That's a complex topic. Let me break it down into simpler terms for better understanding.",
      "Great question! The answer involves several factors that we should examine carefully.",
      "I can definitely help with that. Here's a detailed explanation based on current best practices.",
      "Your question touches on important concepts in AI and machine learning. Here's my perspective...",
      "This is particularly relevant in the context of modern software development practices.",
      "I see you're asking about this topic. Let me provide you with some actionable insights.",
    ];
    
    // Simple keyword-based responses
    const lowerMessage = message.toLowerCase();
    if (lowerMessage.includes("hello") || lowerMessage.includes("hi")) {
      return "Hello! I'm here to help you with any questions you might have. What would you like to know?";
    }
    if (lowerMessage.includes("help")) {
      return "I'm here to assist you! I can help with a wide variety of topics including programming, general knowledge, problem-solving, and more. What specific area would you like help with?";
    }
    if (lowerMessage.includes("code") || lowerMessage.includes("programming")) {
      return "I'd be happy to help with coding! I can assist with various programming languages, debugging, code review, architecture decisions, and best practices. What programming challenge are you working on?";
    }
    
    // Random response
    const randomResponse = responses[Math.floor(Math.random() * responses.length)];
    return `${randomResponse} You asked about: "${message}". This is particularly relevant because it touches on important concepts that can significantly impact your understanding.`;
  },
};
