# AI System Frontend

A Next.js 15 frontend application for interacting with an AI agent system. This frontend provides three main sections: Projects, Collections, and Settings.

## Features

### Projects Section
- **Project Management**: Create, select, and manage projects
- **Chat Interface**: Real-time conversation with AI agents
- **Skills Editor**: YAML template editing with name, description, and content fields
- **File Management**: Drag-and-drop file upload and management
- **Tool Selection**: Configure available AI functionalities for each project

### Collections Section
- **Connect to Collections**: Connect to existing RAG system collections
- **Create Collections**: Create new collections with name and description

### Settings Section
- **Basic Values**: Edit configurable system values
- **Tool Management**: Enable/disable available AI functionalities

## Technology Stack

- **Next.js 15** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Zustand** for state management
- **React Query** for server state management
- **Axios** for HTTP client

## Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables (optional):
```bash
cp .env.example .env.local
# Edit .env.local with your API URL
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3001](http://localhost:3001) in your browser.

## Backend Integration

The frontend is designed to be backend-agnostic. It expects the following API endpoints:

### Projects API
- `POST /api/projects` - Create project
- `GET /api/projects` - List projects
- `PUT /api/projects/:id` - Update project
- `POST /api/projects/:id/messages` - Send chat message
- `GET /api/projects/:id/files` - List project files
- `POST /api/projects/:id/files` - Upload file

### Collections API
- `GET /api/collections` - List available collections
- `POST /api/collections` - Create collection
- `POST /api/collections/:id/connect` - Connect to collection

### Settings API
- `GET /api/settings/available-tools` - Get configured tools
- `PUT /api/settings` - Update settings
- `GET /api/settings` - Get current settings

## Configuration

### Environment Variables
- `NEXT_PUBLIC_API_URL` - Base URL for API calls (default: http://localhost:8000)

## Development

### Project Structure
```
src/
├── app/                    # Next.js App Router pages
├── components/            # React components
│   ├── ui/               # Reusable UI components
│   ├── projects/         # Projects section components
│   ├── collections/      # Collections section components
│   └── settings/         # Settings section components
├── hooks/               # Custom React hooks
├── lib/                 # Utilities and configurations
├── types/               # TypeScript type definitions
```

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Key Implementation Details

### No Mocking Data Policy
The frontend shows loading states and empty states until backend integration. No fake data or simulated functionality is included.

### State Management
- **Local State**: Form inputs, UI states (React useState)
- **Global State**: Projects, chat history, collections (Zustand)
- **Server State**: API responses (React Query)

### Error Handling
- User-friendly error messages
- Loading states for all API calls
- Graceful fallbacks for failed requests

### Styling
- Tailwind CSS for utility-first styling
- Responsive design
- Custom color palette matching requirements
- Smooth transitions and hover states

## License

This project is part of the AI System Interface implementation.