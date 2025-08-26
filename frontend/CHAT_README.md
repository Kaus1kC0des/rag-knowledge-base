# College Study Assistant - AI Chat Application

This is an end-to-end AI chat application built with Next.js, specifically designed for college students to get help with their subjects. The application features subject-based organization with unit-specific context for enhanced learning.

## Features

✨ **Core Features:**
- **Subject-Based Chat System**: 5 predefined subjects (Mathematics, Physics, Computer Science, Engineering, General Studies)
- **Unit-Specific Context**: Each subject has 5 units with focused AI assistance
- **Multiple Chat Sessions**: Create and manage multiple conversations per subject
- **Real-time Messaging**: Instant AI responses with typing indicators
- **Context-Aware AI**: AI responses are tailored to the specific subject and unit
- **Chat History Management**: Save, edit, and organize your study sessions

🎨 **UI Components:**
- **Subject Selection Dashboard**: Visual cards for each subject with icons and descriptions
- **Advanced Chat Interface**: Full-featured chat with sidebar, unit selection, and context display
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Dark Mode Support**: Complete theme support with smooth transitions
- **Interactive Elements**: Hover effects, smooth animations, and intuitive navigation

🔧 **Technical Features:**
- **TypeScript**: Full type safety throughout the application
- **Tailwind CSS**: Modern, responsive styling with consistent theme
- **Clerk Authentication**: User authentication and session management
- **Environment Configuration**: Easy setup for different environments
- **Modular API Layer**: Clean separation between frontend and backend integration

## Subject Organization

### Available Subjects:
1. **📊 Mathematics**: Calculus, Linear Algebra, Statistics
   - Unit 1: Differential Calculus
   - Unit 2: Integral Calculus
   - Unit 3: Linear Algebra
   - Unit 4: Probability
   - Unit 5: Statistics

2. **⚛️ Physics**: Mechanics, Thermodynamics, Electromagnetism
   - Unit 1: Classical Mechanics
   - Unit 2: Thermodynamics
   - Unit 3: Electromagnetism
   - Unit 4: Optics
   - Unit 5: Modern Physics

3. **💻 Computer Science**: Algorithms, Data Structures, Programming
   - Unit 1: Programming Fundamentals
   - Unit 2: Data Structures
   - Unit 3: Algorithms
   - Unit 4: Database Systems
   - Unit 5: Software Engineering

4. **⚡ Engineering**: Circuit Analysis, Control Systems, Signals
   - Unit 1: Circuit Analysis
   - Unit 2: Control Systems
   - Unit 3: Signal Processing
   - Unit 4: Power Systems
   - Unit 5: Communication Systems

5. **📚 General Studies**: Literature, History, Philosophy
   - Unit 1: Literature
   - Unit 2: History
   - Unit 3: Philosophy
   - Unit 4: Economics
   - Unit 5: Political Science

## File Structure

```
frontend/src/
├── app/
│   ├── chat/
│   │   ├── page.tsx                 # Subject selection dashboard
│   │   ├── layout.tsx              # Chat section layout with authentication
│   │   ├── [slug]/
│   │   │   └── page.tsx            # Simple individual chat interface
│   │   └── advanced/
│   │       └── page.tsx            # Advanced chat with subject/unit context
│   └── AppLayout.tsx               # Global app layout with navigation
├── components/
│   ├── ChatSidebar.tsx             # Reusable sidebar component (unused in final)
│   ├── ThemeProviderWrapper.tsx    # Theme management wrapper
│   └── ThemeSwitch.tsx             # Dark/light mode toggle
├── lib/
│   └── api.ts                      # API utilities with subject/unit context support
└── .env.local                      # Environment variables
```

## How It Works

### 1. Subject Selection (`/chat`)
- **Visual Subject Cards**: Click on any of the 5 subject cards to start a study session
- **Recent Study Sessions**: View and continue previous conversations
- **Context Transfer**: Subject and unit information is passed to the chat interface

### 2. Advanced Chat Interface (`/chat/advanced`)
- **Subject Selector**: Change between different subjects while chatting
- **Unit Dropdown**: Select specific units within each subject for focused assistance
- **Context Display**: See current subject and unit in the header and input area
- **Smart Chat Organization**: Chats are filtered by subject in the sidebar
- **Enhanced AI Responses**: AI provides subject and unit-specific assistance

### 3. Context-Aware Messaging
- **Subject Context**: AI knows which subject you're studying
- **Unit Context**: AI provides unit-specific explanations and examples
- **Contextual Responses**: More relevant and targeted assistance based on your current study focus

## API Integration

The application is designed to work with your Python backend. Here's how to integrate:

### 1. Backend API Endpoints

Your backend should implement these endpoints with subject/unit support:

```python
# Expected API endpoints with context
POST /chat/message              # Send message with subject/unit context
GET  /chat/{chat_id}/history   # Get chat history
POST /chat                     # Create new chat with subject/unit
GET  /chats                    # Get all user chats (optionally filter by subject)
GET  /study-materials/{subject} # Get subject-specific materials
PUT  /chat/{chat_id}           # Update chat title
DELETE /chat/{chat_id}         # Delete chat
```

### 2. API Request Format

```typescript
// Example API call with context
const response = await fetch(`${API_BASE_URL}/chat/message`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${userToken}`, // If using auth
  },
  body: JSON.stringify({
    message: userMessage,
    chat_id: currentChatId,
    subject: "mathematics",           // Subject context
    unit: "Unit 1: Differential Calculus",  // Unit context
    timestamp: new Date().toISOString(),
  }),
});
```

### 3. Replace Dummy API

To connect with your backend, update the chat components:

```typescript
// In advanced chat page, replace:
const response = await dummyAPI.sendMessage(message, { subject, unit });

// With:
const response = await chatAPI.sendMessage(message, currentChatId, { subject, unit });
```

## Usage Instructions

### Getting Started

1. **Run the development server**:
   ```bash
   cd frontend
   npm run dev
   ```

2. **Access the application**: Open `http://localhost:3000`

3. **Choose a subject**: Click on one of the 5 subject cards

4. **Start studying**: Ask questions and get AI assistance tailored to your subject and unit

### Features to Test

- ✅ **Subject Selection**: Click different subject cards and see context changes
- ✅ **Unit Switching**: Use the unit dropdown to change focus areas
- ✅ **Contextual Responses**: Notice how AI responses are tailored to subject/unit
- ✅ **Chat Management**: Create, edit, and delete chats per subject
- ✅ **Theme Support**: Toggle between light and dark modes
- ✅ **Responsive Design**: Test on different screen sizes
- ✅ **Navigation**: Move between dashboard and chat interfaces

### Example Usage Flow

1. **Start**: Go to `/chat` and see the subject dashboard
2. **Select Subject**: Click "Mathematics" card
3. **Choose Unit**: Select "Unit 1: Differential Calculus" from dropdown
4. **Ask Questions**: "Can you explain the chain rule?"
5. **Get Contextual Help**: AI provides mathematics-specific, calculus-focused explanations
6. **Switch Context**: Change to "Unit 2: Integral Calculus" for integration help
7. **Manage Chats**: Create new chats, edit titles, organize by subject

## Customization

### Adding New Subjects

To add more subjects, update the `subjects` array in both `/chat/page.tsx` and `/chat/advanced/page.tsx`:

```typescript
const newSubject = {
  id: "chemistry",
  name: "Chemistry",
  description: "Organic, Inorganic, Physical Chemistry",
  icon: <FlaskConical className="w-8 h-8" />,
  color: "red",
  units: [
    "Unit 1: Atomic Structure",
    "Unit 2: Chemical Bonding",
    // ... more units
  ]
};
```

### Styling Customization

The application uses Tailwind CSS with consistent color themes:
- **Blue**: Mathematics
- **Purple**: Physics  
- **Green**: Computer Science
- **Orange**: Engineering
- **Indigo**: General Studies

Each subject has its own color scheme that adapts to both light and dark modes.

## Next Steps

1. **Backend Integration**: Connect to your Python AI backend
2. **Enhanced Context**: Add more detailed unit descriptions and learning objectives
3. **Study Materials**: Integrate with your document storage system
4. **Progress Tracking**: Add learning progress and performance analytics
5. **Collaboration**: Add features for sharing study sessions
6. **Mobile App**: Consider React Native for mobile companion app

## Environment Setup

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000  # Your Python backend URL
NEXT_PUBLIC_APP_NAME=College Study Assistant
NEXT_PUBLIC_APP_VERSION=1.0.0

# Clerk Authentication (optional)
# NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_key
# CLERK_SECRET_KEY=your_secret
```

The application is now fully functional with subject-based organization, unit-specific context, and ready for integration with your Python backend for true AI-powered college study assistance!
