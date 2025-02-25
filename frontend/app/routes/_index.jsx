import { useEffect, useRef, useState } from "react";

export default function Index() {
  const [rankings, setRankings] = useState([]);
  const [messages, setMessages] = useState([]);
  const messagesRef = useRef(null);

  const retrieveRecommendation = async () => {
    document.body.style.cursor = "wait";
    const response = await fetch("/api/computers/")
    const data = await response.json();
    const recommendations = data["recommendations"];
    alert("Nuevas recomendaciones generadas")
    setRankings(recommendations);
    document.body.style.cursor = "default";
  }

  useEffect(() => {
    messagesRef.current.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const submitMessage = async (e) => {
    e.preventDefault();
    const target = e.target;
    const input = target.querySelector("[name='message']");
    if (input.value) {
      const value = input.value;
      target.reset();
      setMessages(prev => [...prev, {
        role: "user",
        content: value
      }]);

      const request = await fetch("/api/computers/message/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          "message": value
        })
      });
      const message = await request.json();
      setMessages(prev => [...prev, message]);
    }
  }

  return (
    <div className="flex items-center justify-center h-screen">
      <div className="grid grid-cols-2 space-x-3 p-3">
        <div className="bg-gray-500 p-3 rounded flex flex-col items-center justify-center gap-3">
          <div
          className="p-3 bg-white rounded h-full w-full flex flex-col gap-3 h-[600px] overflow-y-auto">
            {/* messages */}
            {messages.map(message => <div className={`p-3 rounded ${message.role === "assistant"
              ? "ms-8 bg-pink-500/50"
              : "me-8 bg-blue-500/50"}`}>
              <pre className="text-wrap"
              >{message.content}</pre>
            </div>)}
            <div ref={messagesRef}></div>
          </div>
          <form onSubmit={submitMessage} className="flex w-full">
            <input name="message" className="px-3 py-2 rounded-s w-full" type="text" />
            <button className="rounded-e bg-green-700 text-white px-3" type="submit"> Enviar </button>
          </form>
        </div>
        <div className="flex flex-col items-start gap-3">
          <button onClick={retrieveRecommendation}
            className="px-3 py-2 rounded bg-blue-600 text-white">
            Obtener recomendaciones
          </button>
          <ul className="list-style-none space-y-3">
            {rankings?.map(ranking => {
              return <li key={ranking.id}
                className="bg-orange-400 p-3 rounded">
                <strong>{ranking.brand}</strong>
                <p>Precio: {ranking.price} </p>
                <p>Recomendación: <strong>{ranking.rank}</strong></p>
              </li>
            })}
          </ul>
        </div>
      </div>
    </div>
  );
}