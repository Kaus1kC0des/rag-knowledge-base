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
  // Send a message to the AI and get a response with subject/unit context
  sendMessage: async (
    message: string, 
    chatId?: string, 
    context?: { subject?: string; unit?: string }
  ): Promise<string> => {
    const response = await apiCall("/chat/message", {
      method: "POST",
      body: JSON.stringify({ 
        message, 
        chat_id: chatId,
        subject: context?.subject,
        unit: context?.unit,
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

  // Create a new chat with subject/unit context
  createChat: async (
    title?: string, 
    context?: { subject?: string; unit?: string }
  ): Promise<{ id: string; title: string }> => {
    const response = await apiCall("/chat", {
      method: "POST",
      body: JSON.stringify({ 
        title: title || `New Chat ${Date.now()}`,
        subject: context?.subject,
        unit: context?.unit,
        created_at: new Date().toISOString()
      }),
    });

    if (response.success && response.data) {
      return response.data;
    } else {
      throw new Error(response.error || "Failed to create chat");
    }
  },

  // Get all chats for the user, optionally filtered by subject
  getAllChats: async (subject?: string): Promise<any[]> => {
    const url = subject ? `/chats?subject=${encodeURIComponent(subject)}` : "/chats";
    const response = await apiCall(url);
    
    if (response.success && response.data) {
      return response.data.chats || [];
    } else {
      throw new Error(response.error || "Failed to get chats");
    }
  },

  // Get subject-specific study materials
  getStudyMaterials: async (subject: string, unit?: string): Promise<any[]> => {
    const url = unit 
      ? `/study-materials/${encodeURIComponent(subject)}?unit=${encodeURIComponent(unit)}`
      : `/study-materials/${encodeURIComponent(subject)}`;
    
    const response = await apiCall(url);
    
    if (response.success && response.data) {
      return response.data.materials || [];
    } else {
      throw new Error(response.error || "Failed to get study materials");
    }
  },
};

// Enhanced dummy API functions for development/testing
export const dummyAPI = {
  sendMessage: async (message: string, context?: { subject?: string; unit?: string }): Promise<string> => {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 1000 + Math.random() * 2000));
    
    // Enhanced responses based on subject and unit context
    const subject = context?.subject || "";
    const unit = context?.unit || "";
    
    // Subject-specific responses
    const subjectResponses = {
      mathematics: [
        "Great question about mathematics! Let me help you understand this concept step by step.",
        "In mathematics, this topic requires careful attention to detail. Here's how we approach it:",
        "This is a fundamental concept in mathematics. Let me break it down for you:",
        "Mathematics can be challenging, but with the right approach, you'll master this topic.",
      ],
      physics: [
        "Excellent physics question! Let's explore the underlying principles:",
        "In physics, we need to consider the fundamental laws that govern this phenomenon:",
        "This is a fascinating area of physics. Here's what you need to understand:",
        "Physics concepts often build upon each other. Let me explain this systematically:",
      ],
      "computer-science": [
        "Great computer science question! Let's dive into the technical details:",
        "In computer science, this concept is crucial for understanding how systems work:",
        "This is an important topic in computer science. Here's the algorithmic approach:",
        "Computer science problems often have elegant solutions. Let me show you:",
      ],
      engineering: [
        "Excellent engineering question! Let's analyze this from a practical perspective:",
        "In engineering, we need to consider both theoretical and practical aspects:",
        "This engineering concept has real-world applications. Here's how it works:",
        "Engineering solutions require systematic thinking. Let me guide you through this:",
      ],
      "general-studies": [
        "Interesting question in general studies! Let's explore this topic comprehensively:",
        "This area of general studies connects to many other disciplines. Here's the overview:",
        "General studies questions often require interdisciplinary thinking. Let me explain:",
        "This topic in general studies has broader implications. Here's what you should know:",
      ],
    };

    // Unit-specific enhancements
    const unitEnhancements = {
      calculus: "involving derivatives and integrals",
      mechanics: "related to forces and motion",
      algorithms: "focusing on computational efficiency",
      literature: "considering historical and cultural context",
      default: "with comprehensive analysis"
    };

    // Get appropriate responses
    const responses = subjectResponses[subject as keyof typeof subjectResponses] || [
      "That's a great question! Let me provide you with a detailed explanation.",
      "I understand what you're asking about. Here's a comprehensive answer:",
      "This is an important topic. Let me break it down for you:",
      "Excellent question! Here's what you need to know:",
    ];

    // Simple keyword-based responses
    const lowerMessage = message.toLowerCase();
    if (lowerMessage.includes("hello") || lowerMessage.includes("hi")) {
      return `Hello! I'm here to help you with ${subject || 'your studies'}. ${unit ? `We're currently focusing on ${unit}.` : ''} What would you like to learn about?`;
    }
    if (lowerMessage.includes("help")) {
      return `I'm here to assist you with ${subject || 'your studies'}! ${unit ? `For ${unit}, ` : ''}I can help with explanations, problem-solving, examples, and more. What specific topic would you like help with?`;
    }
    if (lowerMessage.includes("explain")) {
      return `I'd be happy to explain that concept${subject ? ` in ${subject}` : ''}! ${unit ? `Since we're working on ${unit}, ` : ''}let me provide a clear, step-by-step explanation that will help you understand this topic thoroughly.`;
    }

    // Random contextual response
    const randomResponse = responses[Math.floor(Math.random() * responses.length)];
    const unitContext = unit ? ` This relates specifically to ${unit}, ` : " ";
    const enhancement = unitEnhancements[unit?.toLowerCase().includes('calculus') ? 'calculus' : 
                                       unit?.toLowerCase().includes('mechanics') ? 'mechanics' :
                                       unit?.toLowerCase().includes('algorithm') ? 'algorithms' :
                                       unit?.toLowerCase().includes('literature') ? 'literature' : 'default'] || 
                        unitEnhancements.default;

    return `${randomResponse}${unitContext}${enhancement}.\n\nYou asked: "${message}"\n\nThis is particularly relevant because it connects to fundamental principles in ${subject || 'this field'} and will help you build a strong foundation for more advanced topics.`;
  },
};
