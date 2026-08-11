# ✈️ FlyNAS AI Travel Assistant

An AI-powered travel assistant built with FastAPI, OpenAI, SQLite, and Retrieval-Augmented Generation (RAG).

The assistant can understand user questions, route them to the appropriate service, retrieve structured information from the database, or search the knowledge base when needed.

---

## 🚀 Current Features

- 🤖 AI-powered chat using OpenAI GPT
- ⚡ FastAPI backend
- 🗄️ SQLite database
- ✈️ Flight search
- 🧳 Baggage policy lookup
- 🎫 Booking and cancellation policy lookup
- 💰 Fare detection
- 🏙️ Airport and city detection
- 🧭 Intelligent question routing
- 📚 RAG-based knowledge retrieval
- 🔎 Vector similarity search
- 🛡️ Basic error and edge-case handling
- 📖 Interactive API documentation with Swagger UI

---

## 🧠 How It Works

The assistant uses a routing system to determine how each question should be handled.

```text
User Question
      │
      ▼
   Router
      │
      ├───────────────┐
      │               │
      ▼               ▼
   SQL Routes         RAG
      │               │
      ├── Flights     │
      ├── Baggage     │
      └── Booking     │
      │               │
      ▼               ▼
   SQLite         Vector Store
      │               │
      └───────┬───────┘
              ▼
          AI Service
              │
              ▼
        Final Response

SQL Routes

Structured questions are handled using the SQLite database:

flight_sql
baggage_sql
booking_sql
RAG Route

Questions that require knowledge-base information are handled using:

Vector Store
Similarity Search
Knowledge Base
OpenAI
🛠️ Tech Stack
Python
FastAPI
OpenAI API
SQLite
Pydantic
Python-dotenv
Uvicorn
Vector Search / RAG
📁 Project Structure
flynas-ai-assistant/
│
├── backend/
│   ├── data/
│   ├── database/
│   │   ├── database.py
│   │   └── seed.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── airport_service.py
│   │   ├── baggage_service.py
│   │   ├── booking_service.py
│   │   ├── fare_service.py
│   │   ├── flight_service.py
│   │   ├── router_service.py
│   │   ├── similarity_service.py
│   │   └── vector_store.py
│   │
│   ├── main.py
│   └── prompts.py
│
├── frontend/
├── docs/
├── .gitignore
└── README.md
🔌 API Endpoints
Method	Endpoint	Description
GET	/	Welcome message
GET	/health	Health check
GET	/about	Project information
POST	/chat	Send a question to the AI assistant
💬 Example Questions
Flight Search
What flights are available from Riyadh to Dubai?

The assistant can identify:

Origin airport
Destination airport
Available flights
Departure time
Arrival time
Flight status
Baggage
How much baggage can I take with the Value fare?
Booking Policy
What is the cancellation fee for the Plus fare?
Missing Information
What is the cancellation fee?

The assistant asks the user to specify the fare instead of assuming one.

Unsupported Fare
What is the cancellation fee for the Premium fare?

The assistant informs the user that the fare is not available.

🛡️ Error Handling

The backend handles several edge cases, including:

Missing destination
No flights found
Unsupported fares
Missing fare selection
Questions outside the assistant's scope

Example:

What flights are available from Riyadh?

Response:

What destination would you like to fly to?
🔐 Environment Variables

Create a .env file and add your OpenAI API key:

OPENAI_API_KEY=your_api_key_here

Never commit the .env file to GitHub.

▶️ Running the Backend

Navigate to the backend directory:

cd backend

Activate the virtual environment:

.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Initialize the database:

python database\database.py

Seed the database:

python database\seed.py

Run the FastAPI server:

uvicorn main:app --reload

The API will be available locally at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs
🧪 Testing

The backend has been tested against:

Existing flight routes
Non-existing flight routes
Missing destinations
Supported fares
Unsupported fares
Missing fare information
Baggage questions
Booking policy questions
RAG questions
Out-of-scope questions
📈 Project Status
Backend

~90% complete

Completed:

 FastAPI backend
 OpenAI integration
 SQLite database
 Flight search
 Baggage policies
 Booking policies
 Fare detection
 Airport detection
 Question routing
 RAG
 Vector search
 Error handling
 Edge-case testing

Remaining backend work:

 Final code cleanup
 Requirements file
 Final documentation
 Deployment
Frontend
 Chat interface
 Backend integration
 UI/UX polish
Deployment
 Backend deployment
 Frontend deployment
 Production configuration
🎯 Project Vision

The long-term goal is to build a complete AI-powered travel assistant that can be integrated into FlyNAS digital platforms.

Potential future capabilities include:

Flight booking
Reservation management
Flight status tracking
Check-in assistance
Travel requirements
Personalized recommendations
Multi-language support
Conversation memory
👨‍💻 Author

Developed by Ibrahim AlFayez        