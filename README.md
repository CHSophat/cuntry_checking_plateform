# AI Frontend Vue

A modern Vue.js 3 application for AI-powered interactions with a clean, scalable project structure.

## 🚀 Features

- **Interactive AI Chat Interface** - Real-time chat with AI
- **Component-Based Architecture** - Reusable Vue components
- **State Management** - Pinia store for global state
- **Vue Router** - Client-side routing
- **Composable Hooks** - Reusable logic composition
- **Service Layer** - Centralized API integration
- **Vite** - Lightning-fast build tool
- **JSON Server** - Mock API with local data

## 📁 Project Structure

```
ai-frontend-vue/
├─ public/                 # Static files (favicon, images)
├─ src/
│  ├─ assets/              # Images, icons, CSS, fonts
│  ├─ components/          # Reusable UI components
│  │   ├─ Button.vue
│  │   ├─ ChatMessage.vue
│  │   └─ Loader.vue
│  ├─ layouts/             # App layouts
│  │   └─ DefaultLayout.vue
│  ├─ pages/               # Page components
│  │   ├─ Home.vue
│  │   ├─ About.vue
│  │   └─ AiTool.vue
│  ├─ router/              # Vue Router setup
│  │   └─ index.js
│  ├─ store/               # Pinia store
│  │   └─ aiStore.js
│  ├─ composables/         # Reusable logic hooks
│  │   └─ useChat.js
│  ├─ services/            # API services
│  │   └─ aiService.js
│  ├─ utils/               # Utilities and helpers
│  │   └─ formatDate.js
│  ├─ App.vue
│  └─ main.js
├─ data/
│  └─ db.json              # Mock database for JSON Server
├─ .env                    # Environment variables
├─ vite.config.js          # Vite configuration
├─ package.json
└─ README.md
```

## 🛠️ Installation

1. Clone or navigate to the project directory:
```bash
cd ai-frontend-vue
```

2. Install dependencies:
```bash
npm install
```

## 🏃 Running the Project

### Development Mode

Start both the Vue dev server and JSON Server:

```bash
# Terminal 1 - Run the Vue development server
npm run dev

# Terminal 2 - Run JSON Server (mock API)
npm run server
```

The application will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## 📚 Available Scripts

- `npm run dev` - Start Vite development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run server` - Start JSON Server with mock data

## 🧩 Component Usage

### Button Component
```vue
<Button 
  label="Click me" 
  variant="primary"
  @click="handleClick"
/>
```

### ChatMessage Component
```vue
<ChatMessage 
  content="Hello!" 
  role="user"
  :timestamp="new Date()"
/>
```

### Loader Component
```vue
<Loader message="Loading..." />
```

## 🎯 Using Composables

```javascript
import { useChat } from '@/composables/useChat';

const { sendMessage, clearChat, messages } = useChat();

await sendMessage('Hello AI!');
```

## 📊 Using Pinia Store

```javascript
import { useAiStore } from '@/store/aiStore';

const aiStore = useAiStore();
aiStore.addMessage('User message', 'user');
```

## 🔌 API Service

The `aiService` provides methods for interacting with the backend:

```javascript
import { aiService } from '@/services/aiService';

// Send a chat message
const response = await aiService.chat('Hello');

// Get Vietnam locations
const locations = await aiService.getVietnamLocations();

// Search locations
const results = await aiService.searchLocations('Hanoi');
```

## 🌍 Environment Variables

Create a `.env` file in the project root:

```
VITE_API_URL=http://localhost:3000
```

## 📦 Dependencies

- **vue** (^3.3.4) - Progressive JavaScript framework
- **vue-router** (^4.2.4) - Official router for Vue.js
- **pinia** (^2.1.4) - State management
- **axios** (^1.5.0) - HTTP client
- **vite** (^4.4.9) - Next generation frontend tooling
- **@vitejs/plugin-vue** (^4.3.4) - Official Vue plugin for Vite
- **json-server** (^0.17.3) - Full fake REST API

## 🎨 Styling

The project uses scoped CSS in Vue components. Global styles can be added in `App.vue`.

### Color Scheme

- Primary: `#007bff` (Blue)
- Secondary: `#6c757d` (Gray)
- Danger: `#dc3545` (Red)
- Background: `#f8f9fa` (Light Gray)

## 🚀 Future Enhancements

- [ ] Add TypeScript support
- [ ] Implement authentication
- [ ] Add unit tests with Vitest
- [ ] Implement E2E tests with Cypress
- [ ] Add dark mode support
- [ ] Implement real AI API integration
- [ ] Add internationalization (i18n)

## 📝 License

MIT License - feel free to use this project for your own purposes.

## 👤 Author

AI Frontend Vue Project

---

**Happy Coding! 🎉**
