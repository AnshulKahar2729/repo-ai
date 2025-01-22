"use client";
import { Search, Send } from "lucide-react";
import { useState } from "react";

export default function Home() {
  const [repoUrl, setRepoUrl] = useState("");
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<{ role: string; content: any }[]>(
    []
  );
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Add your API call logic here
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repoUrl, query }),
      });

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        { role: "user", content: query },
        { role: "assistant", content: data.response },
      ]);

      setQuery("");
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-4">
      {/* Repository URL Input */}
      <div className="relative">
        <Search className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
        <input
          type="text"
          placeholder="Enter GitHub repository URL"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border rounded-lg"
        />
      </div>

      {/* Chat Messages */}
      <div className="h-96 border rounded-lg p-4 overflow-y-auto space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`p-3 rounded-lg ${
              message.role === "user"
                ? "bg-blue-100 ml-auto max-w-[80%]"
                : "bg-gray-100 max-w-[80%]"
            }`}
          >
            {message.content}
          </div>
        ))}
      </div>

      {/* Query Input */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          placeholder="Ask about the repository..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 px-4 py-2 border rounded-lg"
        />
        <button
          type="submit"
          disabled={loading || !repoUrl || !query}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg disabled:bg-gray-300 flex items-center gap-2"
        >
          <Send className="h-5 w-5" />
          {loading ? "Processing..." : "Send"}
        </button>
      </form>
    </div>
  );
}
