# AI Text Generator - Homework 1

## Author
Mariam Khokhiashvili - khokhiashvili.mariam@kiu.edu.ge

## Final Product Screenshot
![App Demo](demo.mp4)

## Features Implemented

### 1. Streaming Text Display
* **Description:** I updated my backend to use the `generate_content()` method with `stream=True` parameter to enable streaming. In the frontend, I implemented a fetch request that reads the response as a Server-Sent Events (SSE) stream. The code processes incoming text chunks in real-time and appends them to the output area character by character, creating a smooth typing effect where the AI's response appears word-by-word instead of all at once.

### 2. Detailed Cost Display
* **Description:** After the stream completes, I parse the `usage_metadata` from the final API response chunk. The backend sends this metadata as a JSON object containing `inputTokens`, `outputTokens`, and `totalTokens`. I then calculate the total cost based on Gemini 2.0 Flash pricing ($0.10 per 1M input tokens and $0.40 per 1M output tokens). The frontend displays this information in a clean grid layout showing Input Token Count, Output Token Count, Total Token Count, and Total Cost with proper formatting.

### 3. Copy to Clipboard Button
* **Description:** I added a "Copy" button next to the AI response header. The button includes an event listener that uses the `navigator.clipboard.writeText()` method to copy the complete AI response text to the user's clipboard. When clicked, the button text and icon change from "Copy" to "Copied!" with a checkmark icon for 2 seconds as visual confirmation, then automatically reverts back to the original state. This provides clear user feedback that the copy operation was successful.

### 4. Personalized Footer
* **Description:** I added a footer section at the bottom of the application using HTML and React. I implemented a JavaScript function inside a `dangerouslySetInnerHTML` script that runs when the DOM loads. This function dynamically generates the current date using `new Date()` and formats it using `toLocaleDateString()`. The footer displays my KIU email address and the dynamically generated current date in the format: "© 2025 khokhiashvili.mariam@kiu.edu.ge - October 8, 2025".

## How to Run This Project

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- A Google Gemini API key

### Backend Setup
1. Navigate to the project directory
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn google-generativeai python-dotenv
   ```
4. Create a `.env` file in the root directory and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
5. Start the backend server:
   ```bash
   uvicorn app:app --reload --port 5000
   ```

### Frontend Setup
1. Install Node.js dependencies:
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
3. Open your browser and navigate to `http://localhost:5173` (or the URL shown in your terminal)


## Notes
- Make sure both frontend and backend servers are running simultaneously
- The backend runs on `http://localhost:5000`
- The frontend runs on `http://localhost:5173` (default Vite port)
- Ensure your Gemini API key has sufficient quota for testing