# AI Chat Application

This is an end-to-end AI chat application built with Next.js, featuring a modern UI with real-time messaging capabilities.

## Features

✨ **Core Features:**
- Real-time chat interface with AI
- Multiple chat sessions
- Chat history management
- Responsive design with dark mode support
- Message timestamps
- Typing indicators
- Chat creation, editing, and deletion

🎨 **UI Components:**
- Modern, clean interface
- Sidebar with chat list
- Message bubbles for user and AI
- Loading animations
- Responsive layout for mobile and desktop

🔧 **Technical Features:**
- TypeScript for type safety
- Tailwind CSS for styling
- Clerk authentication integration
- Environment-based configuration
- Modular API layer

## File Structure

```
frontend/src/
├── app/
│   ├── chat/
│   │   ├── page.tsx                 # Chat list/dashboard
│   │   ├── layout.tsx              # Chat section layout
│   │   ├── [slug]/
│   │   │   └── page.tsx            # Individual chat page
│   │   └── advanced/
│   │       └── page.tsx            # Advanced chat with sidebar
│   └── AppLayout.tsx               # Global app layout
├── components/
│   └── ChatSidebar.tsx             # Reusable sidebar component
├── lib/
│   └── api.ts                      # API utilities and dummy functions
└── .env.local                      # Environment variables
```

## Pages Overview

### 1. Chat Dashboard (`/chat`)
- Overview of all chat sessions
- Search and filter functionality
- Create new chats
- Navigate to individual chats

### 2. Individual Chat (`/chat/[id]`)
- Simple chat interface
- Message history
- Real-time messaging with AI

### 3. Advanced Chat (`/chat/advanced`)
- Full-featured chat interface
- Sidebar with chat management
- Multiple chat sessions
- Chat editing and deletion
- Collapsible sidebar

## API Integration

The application currently uses dummy API responses for development. To integrate with your backend:

### 1. Update Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000  # Your backend URL
```

### 2. Replace Dummy API Calls

In `src/lib/api.ts`, replace the `dummyAPI` usage with real `chatAPI` calls:

```typescript
// In your chat components, change:
import { dummyAPI } from "@/lib/api";
const response = await dummyAPI.sendMessage(message);

// To:
import { chatAPI } from "@/lib/api";
const response = await chatAPI.sendMessage(message, chatId);
```

### 3. Backend API Endpoints

Your backend should implement these endpoints:

```python
# Expected API endpoints
POST /chat/message              # Send message, get AI response
GET  /chat/{chat_id}/history   # Get chat history
POST /chat                     # Create new chat
GET  /chats                    # Get all user chats
PUT  /chat/{chat_id}           # Update chat title
DELETE /chat/{chat_id}         # Delete chat
```

### 4. Example Backend Integration

```typescript
// Example API call structure
const response = await fetch(`${API_BASE_URL}/chat/message`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${userToken}`, // If using auth
  },
  body: JSON.stringify({
    message: userMessage,
    chat_id: currentChatId,
    timestamp: new Date().toISOString(),
  }),
});
```

## Usage Instructions

### Running the Development Server

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:3000`

### Testing the Chat

1. **Navigate to the chat section** - Click on the chat navigation
2. **Try the simple chat** - Click on any existing chat or create a new one
3. **Test advanced features** - Click "🚀 Advanced Chat" for the full experience
4. **Send messages** - Type messages and see AI responses (currently dummy responses)

### Features to Test

- ✅ Send messages and receive AI responses
- ✅ Create new chat sessions
- ✅ Navigate between chats
- ✅ Edit chat titles (in advanced mode)
- ✅ Delete chats (in advanced mode)
- ✅ Responsive design on different screen sizes
- ✅ Dark mode toggle
- ✅ Message timestamps
- ✅ Loading indicators

## Customization

### Styling

The application uses Tailwind CSS. You can customize:
- Colors in the color scheme
- Layout spacing and sizing
- Component styles

### API Responses

Currently using dummy responses. You can:
- Modify response patterns in `src/lib/api.ts`
- Add more sophisticated response logic
- Integrate with your actual AI backend

### Authentication

The app includes Clerk authentication setup. To use:
1. Set up Clerk account
2. Add Clerk keys to environment variables
3. Configure authentication rules

## Next Steps

1. **Connect to Real Backend**: Replace dummy API with your Python backend
2. **Add Authentication**: Complete Clerk setup for user authentication
3. **Enhance Features**: Add file uploads, message reactions, etc.
4. **Performance**: Add message pagination for large chat histories
5. **Real-time**: Implement WebSocket for real-time updates

## Dependencies

Key dependencies used:
- `next` - React framework
- `@clerk/nextjs` - Authentication
- `lucide-react` - Icons
- `tailwindcss` - Styling
- `next-themes` - Dark mode support

## Troubleshooting

### Common Issues

1. **API Connection**: Ensure your backend is running on the correct port
2. **Environment Variables**: Check `.env.local` file is properly configured
3. **CORS Issues**: Configure CORS in your backend to allow frontend requests

### Development Notes

- The application uses client-side rendering for interactive features
- Messages are stored in component state (add persistence as needed)
- Error handling is implemented for API failures
- The UI is responsive and works on mobile devices
